# Copyright contributors to the Qiskit Studio project
# SPDX-License-Identifier: Apache-2.0

import asyncio
import glob
import json
import os
import time
import traceback
from typing import Any, Dict, List, Optional, TypedDict


# Define a custom print function that always flushes output
def print_flush(*args, **kwargs):
    """Print function that always flushes output for real-time logging in Kubernetes."""
    kwargs['flush'] = True
    print(*args, **kwargs)

# Define stats type
class StatsDict(TypedDict):
    total: int
    added: int
    skipped: int
    failed: int
    chunks_added: int
    processing_time: float
    documents: List[Dict[str, Any]]

# External dependencies
import html2text
import httpx
from fastmcp import Client

# -- Configuration --
MCP_SERVER_URL = os.getenv("MCP_SERVER_URL", "http://localhost:8030/mcp/")
LOCAL_DOCS = os.getenv("LOCAL_DOCS", "true")
JSON_ENCODED = os.getenv("JSON_ENCODED", "false")
COLLECTION_NAME = "qiskit_studio_algo"
DOCUMENT_URLS = [
    "https://quantum.cloud.ibm.com/docs/en/tutorials/chsh-inequality",
    "https://quantum.cloud.ibm.com/docs/en/tutorials/combine-error-mitigation-techniques",
    "https://qiskit.github.io/qiskit-addon-sqd/tutorials/02_fermionic_lattice_hamiltonian.html",
    "https://quantum.cloud.ibm.com/docs/en/tutorials/operator-back-propagation",
    "https://quantum.cloud.ibm.com/docs/en/tutorials/quantum-approximate-optimization-algorithm",
    "https://quantum.cloud.ibm.com/docs/en/tutorials/quantum-kernel-training",
    "https://quantum.cloud.ibm.com/docs/en/tutorials/qunova-hivqe"
]
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "custom_local")
CHUNK_STRATEGY = os.getenv("CHUNK_STRATEGY", "Sentence")
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "512"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "24"))

# -- Configuration Options --
REPORT_INFO = os.getenv("REPORT_INFO", "true").lower() == "true"
TEST_QUERY = os.getenv("TEST_QUERY", "true").lower() == "true"
TEST_QUERY_TEXT = os.getenv("TEST_QUERY_TEXT", "quantum circuit")

# -- New Configuration Options --
# Force delete is the default until maestro knowledge reliably allows checking of existence of documents
FORCE_DELETE_COLLECTION = os.getenv("FORCE_DELETE_COLLECTION", "true").lower() == "true"
BATCH_PROCESSING = os.getenv("BATCH_PROCESSING", "false").lower() == "true"
DEBUG_DOCUMENT_CHECK = os.getenv("DEBUG_DOCUMENT_CHECK", "false").lower() == "true"
CLEAR_COLLECTION_CACHE = os.getenv("CLEAR_COLLECTION_CACHE", "false").lower() == "true"


async def main() -> None:
    """Main function to run the document loader."""
    start_time = time.time()
    
    async with Client(MCP_SERVER_URL, timeout=3600) as client:
        print_flush("✅ fastmcp Client initialized successfully.")

        # Check if collection exists and only delete if FORCE_DELETE_COLLECTION is true
        collection_exists = await cleanup_database_if_exists(client, COLLECTION_NAME)
        
        # Only create collection if it doesn't exist
        if not collection_exists:
            await create_vector_db(client, COLLECTION_NAME)
            await create_collection_with_config(
                client,
                COLLECTION_NAME,
                embedding=EMBEDDING_MODEL,
                chunking_config={
                    "strategy": CHUNK_STRATEGY,
                    "parameters": {"chunk_size": CHUNK_SIZE, "overlap": CHUNK_OVERLAP},
                },
            )

            print_flush("\n▶️  Waiting 5 seconds for the database collection to be ready...")
            await asyncio.sleep(5)

        if REPORT_INFO:
            await report_collection_info(client, COLLECTION_NAME, "before")

        # Process documents
        stats = await add_documents_to_db(client, COLLECTION_NAME, DOCUMENT_URLS)

        if REPORT_INFO:
            await report_collection_info(client, COLLECTION_NAME, "after")

        print_flush("▶️  Waiting 5 seconds for the documents to be indexed...")
        await asyncio.sleep(5)

        if TEST_QUERY:
            await perform_test_query(client, COLLECTION_NAME)
        
        # Print summary at the end
        print_summary_table(stats)
            
        total_time = time.time() - start_time
        print_flush(f"\n✅ Total script execution time: {total_time:.2f} seconds")


async def cleanup_database_if_exists(client: Client, db_name: str) -> bool:
    """
    Check if database exists and clean it up if FORCE_DELETE_COLLECTION is true.
    
    Args:
        client: The MCP client
        db_name: The database name
        
    Returns:
        bool: True if collection exists and was not deleted, False otherwise
    """
    print_flush(f"\n▶️  Checking if database '{db_name}' exists...")
    try:
        # Check if collection exists first
        params = {"input": {'db_name': db_name}}
        collection_info = await client.call_tool('get_collection_info', params)
        
        if FORCE_DELETE_COLLECTION:
            print_flush("🗑️  FORCE_DELETE_COLLECTION is enabled. Deleting existing collection...")
            result = await client.call_tool('cleanup', params)
            print_flush(f"✅ Collection deleted: {result.data}")
            return False
        else:
            print_flush("ℹ️  Collection exists but FORCE_DELETE_COLLECTION is not enabled. Keeping existing collection.")
            return True  # Collection exists and was not deleted
            
    except Exception as e:
        print_flush(f"ℹ️  Collection does not exist or could not be accessed: {e}")
        return False  # Collection doesn't exist


async def create_vector_db(client: Client, db_name: str) -> None:
    """
    Create a vector database.
    
    Args:
        client: The MCP client
        db_name: The database name
    """
    print_flush(f"\n▶️  Creating vector database '{db_name}'...")
    params = {"input": {
        'db_name': db_name,
        'db_type': "milvus",
        'collection_name': db_name
    }}
    result = await client.call_tool('create_vector_database_tool', params)
    print_flush(f"✅ Success! {result.data}")


async def create_collection_with_config(client: Client, db_name: str, embedding: str, chunking_config: Dict[str, Any]) -> None:
    """
    Create a collection with the specified configuration.
    
    Args:
        client: The MCP client
        db_name: The database name
        embedding: The embedding model to use
        chunking_config: The chunking configuration
    """
    print_flush(f"\n📦 Creating collection '{db_name}' with embedding '{embedding}' and chunking {chunking_config}...")
    params = {
        "input": {
            "db_name": db_name,
            "collection_name": db_name,
            "embedding": embedding,
            "chunking_config": chunking_config
        }
    }
    result = await client.call_tool("create_collection", params)
    print_flush(f"   ✓ Collection: {result.data}")


async def document_exists(client: Client, db_name: str, url: str) -> bool:
    """
    Check if a document with the given URL already exists in the collection.
    
    Note: This function currently always returns False as the Maestro Knowledge API
    does not yet support efficient document existence checking.
    See https://github.com/AI4quantum/maestro-knowledge/issues/58
    This check will be implemented once the appropriate APIs are available in maestro knowledge.
    
    Args:
        client: The MCP client
        db_name: The database name
        url: The document URL to check
        
    Returns:
        bool: True if document exists, False otherwise
    """
    # If CLEAR_COLLECTION_CACHE is enabled, we'll always return False
    # This forces the system to re-add documents even if they might exist
    if CLEAR_COLLECTION_CACHE:
        if DEBUG_DOCUMENT_CHECK:
            print_flush("🔍 DEBUG: CLEAR_COLLECTION_CACHE is enabled, skipping existence check")
        print_flush(f"  ✓ Forcing document processing due to CLEAR_COLLECTION_CACHE: {url}")
        return False
    
    # Always return False until proper API support is available
    print_flush(f"  ✓ Document existence check not implemented yet: {url}")
    return False


async def get_document(source: str, is_local: bool = False) -> Optional[Dict[str, str]]:
    """
    Get a single document from a URL or local file.
    
    Args:
        source: The URL or file path
        is_local: Whether the source is a local file
        
    Returns:
        Optional[Dict[str, str]]: The document or None if failed
    """
    try:
        if is_local:
            print_flush(f"  > Reading content from {source}...")
            with open(source, "r") as file:
                file_content = file.read()
                if JSON_ENCODED == "true":
                    file_content = json.loads(file_content)
                print_flush(f"    ✅ Successfully processed {source}")
                return {"url": source, "text": file_content}
        else:
            print_flush(f"  > Fetching content from {source}...")
            async with httpx.AsyncClient() as http_client:
                response = await http_client.get(source, follow_redirects=True, timeout=20.0)
                response.raise_for_status()
                html_content = response.text

            print_flush("    > Converting HTML to Markdown...")
            markdown_content = html2text.html2text(html_content)
            print_flush(f"    ✅ Successfully processed {source}")
            return {"url": source, "text": markdown_content}
    except httpx.HTTPStatusError as e:
        print_flush(f"    ❌ Error fetching {source}: {e}")
    except Exception as e:
        print_flush(f"    ❌ An unexpected error occurred while processing {source}: {e}")
    
    return None


async def get_documents(sources: List[str], is_local: bool = False) -> List[Dict[str, str]]:
    """
    Get multiple documents from URLs or local files.
    
    Args:
        sources: The URLs or file paths
        is_local: Whether the sources are local files
        
    Returns:
        List[Dict[str, str]]: The documents
    """
    if is_local:
        print_flush("\n▶️  Reading documents from local file system...")
        # Use the provided sources or default to glob pattern if empty
        if not sources:
            sources = glob.glob("./documentation/*.md")
    else:
        print_flush("\n▶️  Reading documents from urls...")
    
    documents = []
    for source in sources:
        doc = await get_document(source, is_local)
        if doc:
            documents.append(doc)
    
    return documents


async def process_document(client: Client, db_name: str, doc_url: str, is_local: bool) -> Dict[str, Any]:
    """
    Process a single document and return its status.
    
    Args:
        client: The MCP client
        db_name: The database name
        doc_url: The document URL or filename
        is_local: Whether the document is local
        
    Returns:
        Dict[str, Any]: The processing result
    """
    doc_start_time = time.time()
    result = {
        "url": doc_url,
        "status": "skipped",
        "chunks": 0,
        "time": 0,
        "error": None
    }
    
    try:
        # Check if document exists
        if await document_exists(client, db_name, doc_url):
            print_flush(f"  ⏭️  Document already exists: {doc_url}")
            result["status"] = "skipped"
            return result
            
        # Get document content
        if is_local:
            document = await get_document(doc_url, is_local=True)
        else:
            document = await get_document(doc_url, is_local=False)
            
        if not document:
            result["status"] = "failed"
            result["error"] = "Failed to retrieve document"
            return result
            
        # Add document to database
        params = {"input": {
            'db_name': db_name,
            'documents': [document],
            'embedding': EMBEDDING_MODEL
        }}
        
        write_result = await client.call_tool('write_documents', params)
        
        # Parse result to get chunk count
        try:
            if hasattr(write_result, 'data'):
                payload = json.loads(write_result.data) if isinstance(write_result.data, str) else write_result.data
                write_stats = payload.get("write_stats", {})
                chunks = write_stats.get("chunks", 0)
                result["chunks"] = chunks
                result["status"] = "added"
            elif hasattr(write_result, 'content') and write_result.content:
                # Alternative response format
                result["chunks"] = 1  # Assume at least one chunk
                result["status"] = "added"
            else:
                # If we can't parse the response, just mark as added
                result["status"] = "added"
                result["error"] = "Added but couldn't parse chunk count"
        except (json.JSONDecodeError, AttributeError) as e:
            result["status"] = "added"
            result["error"] = f"Added but couldn't parse chunk count: {e}"
            
    except Exception as e:
        result["status"] = "failed"
        result["error"] = str(e)
        
    result["time"] = time.time() - doc_start_time
    return result


async def add_documents_to_db(client: Client, db_name: str, doc_urls: List[str]) -> "StatsDict":
    """
    Add documents to the database, checking for existence and tracking progress.
    
    Args:
        client: The MCP client
        db_name: The database name
        doc_urls: The document URLs to process
        
    Returns:
        Dict[str, Any]: The processing statistics
    """
    print_flush(f"\n▶️  Processing documents for '{db_name}'...")
    
    # Initialize tracking variables
    start_time = time.time()
    is_local = LOCAL_DOCS == "true"
    
    # Step 1: Get all document sources
    if is_local:
        # For local docs, get the list of files
        sources = glob.glob("./documentation/*.md")
        print_flush(f"  Found {len(sources)} local documents")
    else:
        # For remote URLs, use the provided list
        sources = doc_urls
        print_flush(f"  Processing {len(sources)} remote URLs")
    
    # Initialize stats
    stats: StatsDict = {
        "total": len(sources),
        "added": 0,
        "skipped": 0,
        "failed": 0,
        "chunks_added": 0,
        "processing_time": 0.0,
        "documents": []  # Track individual document results
    }
    
    # Step 2: Process documents based on mode
    if BATCH_PROCESSING:
        print_flush("🔄 Using batch processing mode")
        documents_to_add = []
        
        # Process each source (file or URL)
        for source in sources:
            # Check if document exists
            if await document_exists(client, db_name, source):
                print_flush(f"  ⏭️  Document already exists: {source}")
                stats["skipped"] += 1
                continue
            
            # Get document content
            document = await get_document(source, is_local=is_local)
            if document:
                documents_to_add.append(document)
                print_flush(f"  ✅ Document prepared for batch: {source}")
            else:
                stats["failed"] += 1
                print_flush(f"  ❌ Failed to process document: {source}")
        
        # Write documents in batch if any
        if documents_to_add:
            print_flush(f"\n▶️  Writing {len(documents_to_add)} documents to the database...")
            params = {"input": {
                'db_name': db_name,
                'documents': documents_to_add,
                'embedding': EMBEDDING_MODEL
            }}
            
            result = await client.call_tool('write_documents', params)
            
            try:
                if hasattr(result, 'data'):
                    payload = json.loads(result.data) if isinstance(result.data, str) else result.data
                    write_stats = payload.get("write_stats", {})
                    total_chunks = write_stats.get("chunks", 0)
                    stats["chunks_added"] = total_chunks
                    stats["added"] = len(documents_to_add)
                    print_flush(f"✅ Batch complete! {total_chunks} chunks were added to the database.")
                    
                    # Calculate average chunks per document
                    avg_chunks = total_chunks // len(documents_to_add) if len(documents_to_add) > 0 else 0
                    
                    # Add document details to tracking
                    for doc in documents_to_add:
                        doc_url = doc.get("url", "unknown")
                        stats["documents"].append({
                            "url": doc_url,
                            "status": "added",
                            "chunks": avg_chunks,
                            "time": None,
                            "error": None
                        })
                else:
                    stats["added"] = len(documents_to_add)
                    print_flush("✅ Batch complete, but couldn't parse chunk count from response")
                    
                    # Add document details with unknown chunk count
                    for doc in documents_to_add:
                        doc_url = doc.get("url", "unknown")
                        stats["documents"].append({
                            "url": doc_url,
                            "status": "added",
                            "chunks": 0,
                            "time": None,
                            "error": None
                        })
            except (json.JSONDecodeError, AttributeError) as e:
                stats["added"] = len(documents_to_add)
                print_flush(f"✅ Batch complete, but couldn't parse chunk count: {e}")
                
                # Add document details with unknown chunk count
                for doc in documents_to_add:
                    doc_url = doc.get("url", "unknown")
                    stats["documents"].append({
                        "url": doc_url,
                        "status": "added",
                        "chunks": 0,
                        "time": None,
                        "error": f"Couldn't parse chunk count: {e}"
                    })
    else:
        print_flush("🔄 Processing documents individually")
        
        # Process each source (file or URL)
        for source in sources:
            print_flush(f"\n  ▶️  Processing document: {source}")
            
            # Process document
            result = await process_document(client, db_name, source, is_local)
            
            # Track document result
            stats["documents"].append(result)
            
            if result["status"] == "added":
                stats["added"] += 1
                stats["chunks_added"] += result["chunks"]
                print_flush(f"  ✅ Added document: {source} ({result['chunks']} chunks, {result['time']:.2f}s)")
            elif result["status"] == "skipped":
                stats["skipped"] += 1
                print_flush(f"  ⏭️  Skipped document: {source} (already exists)")
            else:
                stats["failed"] += 1
                print_flush(f"  ❌ Failed to process document: {source} - {result['error']}")
    
    stats["processing_time"] = time.time() - start_time
    return stats


async def report_collection_info(client: Client, db_name: str, stage: str) -> None:
    """
    Report information about the collection.
    
    Args:
        client: The MCP client
        db_name: The database name
        stage: The stage of processing (before/after)
    """
    print_flush(f"\n▶️  Reporting collection info ({stage})...")
    try:
        params = {"input": {'db_name': db_name}}
        result = await client.call_tool('get_collection_info', params)
        
        # Format the collection info for better readability
        if hasattr(result, 'data'):
            if isinstance(result.data, str):
                try:
                    # Try to parse and format the JSON data
                    formatted_data = pretty_print_json(result.data)
                    print_flush(f"✅ Collection info:\n{formatted_data}")
                except Exception:
                    # Fallback to original data if formatting fails
                    print_flush(f"✅ Collection info: {result.data}")
            else:
                # If data is not a string, use pretty_print_json directly
                formatted_data = pretty_print_json(result.data)
                print_flush(f"✅ Collection info:\n{formatted_data}")
        else:
            print_flush(f"✅ Collection info: {result}")
    except Exception as e:
        print_flush(f"⚠️  Could not get collection info: {e}")


def pretty_print_json(data: Any) -> str:
    """
    Format JSON data for better readability.
    
    Args:
        data: The data to format (string or object)
        
    Returns:
        str: Formatted JSON string
    """
    try:
        # If data is a string, try to parse it as JSON
        if isinstance(data, str):
            try:
                parsed_data = json.loads(data)
                return json.dumps(parsed_data, indent=2)
            except json.JSONDecodeError:
                # If it's not valid JSON, return the original string
                return data
        
        # If data is already a dict or list, format it
        elif isinstance(data, (dict, list)):
            return json.dumps(data, indent=2)
        
        # For other types, convert to string and return
        return str(data)
    except Exception:
        # If any error occurs, return the original data as string
        return str(data)


def print_summary_table(stats: "StatsDict") -> None:
    """
    Print a summary table of document processing results.
    
    Args:
        stats: The processing statistics
    """
    print_flush("\n" + "="*50)
    print_flush("📊 DOCUMENT PROCESSING SUMMARY")
    print_flush("="*50)
    print_flush(f"Total documents processed: {stats['total']}")
    print_flush(f"Documents added:           {stats['added']}")
    print_flush(f"Documents skipped:         {stats['skipped']} (already existed)")
    print_flush(f"Documents failed:          {stats['failed']}")
    print_flush(f"Total chunks added:        {stats['chunks_added']}")
    print_flush(f"Total processing time:     {stats['processing_time']:.2f} seconds")
    print_flush("="*50)
    
    # Print detailed document results if available
    if stats.get("documents"):
        print_flush("\nDETAILED DOCUMENT RESULTS:")
        print_flush("-"*50)
        print_flush(f"{'URL':<30} | {'Status':<10} | {'Chunks':<6} | {'Time (s)':<8} | {'Error'}")
        print_flush("-"*50)
        for doc in stats["documents"]:
            url = doc.get("url", "unknown")
            # Truncate URL if too long
            if len(url) > 27:
                url = url[:24] + "..."
            status = doc.get("status", "unknown")
            chunks = doc.get("chunks", 0)
            time_s = f"{doc.get('time', 0):.2f}" if doc.get("time") is not None else "N/A"
            error = doc.get("error", "")
            print_flush(f"{url:<30} | {status:<10} | {chunks:<6} | {time_s:<8} | {error}")
        print_flush("-"*50)


async def perform_test_query(client: Client, db_name: str) -> None:
    """
    Perform a test query on the collection.
    
    Args:
        client: The MCP client
        db_name: The database name
    """
    print_flush("\n▶️  Performing test query...")
    try:
        params = {"input": {
            'db_name': db_name,
            'query': TEST_QUERY_TEXT,
            'limit': 1
        }}
        result = await client.call_tool('search', params)
        
        if hasattr(result, 'content') and result.content and len(result.content) > 0:
            # Try to format the content for better readability
            try:
                # If content is a list of objects with a text attribute
                if hasattr(result.content[0], 'text'):
                    # Try to parse the text field if it's a JSON string
                    text = result.content[0].text
                    try:
                        # Check if the text is a JSON string
                        if text.startswith('[{') and text.endswith('}]'):
                            parsed_text = json.loads(text)
                            # Extract the actual text from the parsed JSON
                            if isinstance(parsed_text, list) and len(parsed_text) > 0:
                                actual_text = parsed_text[0].get('text', '')
                                # Create a clean result object
                                result_obj = {
                                    "text": actual_text,
                                    "url": parsed_text[0].get('url', 'N/A'),
                                    "metadata": parsed_text[0].get('metadata', {})
                                }
                                formatted_result = pretty_print_json(result_obj)
                                print_flush(f"✅ Test query result for '{TEST_QUERY_TEXT}':\n{formatted_result}")
                                return
                    except json.JSONDecodeError:
                        pass  # Not a JSON string, continue with normal formatting
                    
                    # If not a JSON string or parsing failed, use the original approach
                    result_obj = {
                        "text": text,
                        "url": getattr(result.content[0], 'url', 'N/A'),
                        "metadata": getattr(result.content[0], 'metadata', {})
                    }
                    formatted_result = pretty_print_json(result_obj)
                    print_flush(f"✅ Test query result for '{TEST_QUERY_TEXT}':\n{formatted_result}")
                else:
                    # Format the raw content
                    formatted_content = pretty_print_json(result.content)
                    print_flush(f"✅ Test query result for '{TEST_QUERY_TEXT}':\n{formatted_content}")
            except Exception as e:
                # Fallback to original output if formatting fails
                print_flush(f"✅ Test query result: {result.content[0].text}")
                if DEBUG_DOCUMENT_CHECK:
                    print_flush(f"⚠️ Error formatting test query result: {e}")
        elif hasattr(result, 'data') and result.data:
            # Try to format the data
            formatted_data = pretty_print_json(result.data)
            print_flush(f"✅ Test query result for '{TEST_QUERY_TEXT}':\n{formatted_data}")
        else:
            print_flush("⚠️ Test query returned no results")
    except Exception as e:
        print_flush(f"⚠️  Test query failed: {e}")
        print_flush(f"Error details: {traceback.format_exc()}")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print_flush(f"\n❌ An unexpected error occurred: {e}")
        print_flush(f"Error details: {traceback.format_exc()}")

# Made with Bob
