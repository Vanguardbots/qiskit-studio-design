# Copyright contributors to the Qiskit Studio project
# SPDX-License-Identifier: Apache-2.0

import numpy as np
from pymilvus import (
    connections,
    utility,
    FieldSchema,
    CollectionSchema,
    DataType,
    Collection,
)

# --- Connection details ---
HOST = "localhost"
PORT = "19530"
COLLECTION_NAME = "hello_milvus_test"

# --- Collection schema definition ---
# 1. Define fields for our collection
fields = [
    FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=False),
    FieldSchema(name="random_value", dtype=DataType.DOUBLE),
    FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=8)
]

# 2. Create schema
schema = CollectionSchema(fields, "A simple test collection for Milvus")

def run_milvus_test():
    """
    Connects to Milvus, creates a collection, inserts data,
    searches, and then cleans up.
    """
    try:
        # --- 1. Connect to Milvus ---
        print(f"Connecting to Milvus at {HOST}:{PORT}...")
        connections.connect("default", host=HOST, port=PORT)
        print("✅ Connection successful!")

        # --- 2. Check if collection exists and drop it for a clean run ---
        if utility.has_collection(COLLECTION_NAME):
            print(f"Dropping existing collection: {COLLECTION_NAME}")
            utility.drop_collection(COLLECTION_NAME)

        # --- 3. Create collection ---
        print(f"Creating collection: {COLLECTION_NAME}")
        collection = Collection(name=COLLECTION_NAME, schema=schema)
        print("✅ Collection created!")

        # --- 4. Insert data ---
        print("Inserting data...")
        # Generate some random data
        num_entities = 3000
        data = [
            [i for i in range(num_entities)],
            [np.random.random() for _ in range(num_entities)],
            np.random.rand(num_entities, 8).tolist()
        ]
        insert_result = collection.insert(data)
        print(f"✅ Inserted {insert_result.insert_count} entities.")

        # Milvus is eventually consistent, so we need to flush the data
        collection.flush()

        # --- 5. Create an index ---
        print("Creating index...")
        index_params = {
            "metric_type": "L2",
            "index_type": "IVF_FLAT",
            "params": {"nlist": 128},
        }
        collection.create_index(field_name="embedding", index_params=index_params)
        print("✅ Index created!")

        # --- 6. Load collection into memory for searching ---
        print("Loading collection into memory...")
        collection.load()
        print("✅ Collection loaded!")

        # --- 7. Perform a search ---
        print("Performing a vector search...")
        # Generate a random query vector
        query_vector = [np.random.rand(8).tolist()]
        search_params = {
            "metric_type": "L2",
            "params": {"nprobe": 10},
        }
        results = collection.search(
            data=query_vector,
            anns_field="embedding",
            param=search_params,
            limit=3,
            output_fields=["random_value"]
        )
        print("✅ Search complete!")
        print("Search results:")
        for i, hits in enumerate(results):
            print(f"  Query {i+1}:")
            for hit in hits:
                print(f"    - Hit ID: {hit.id}, Distance: {hit.distance:.4f}, Random Value: {hit.entity.get('random_value'):.4f}")

    except Exception as e:
        print(f"❌ An error occurred: {e}")
    finally:
        # --- 8. Clean up ---
        if 'collection' in locals() and utility.has_collection(COLLECTION_NAME):
            print(f"\nCleaning up: Dropping collection '{COLLECTION_NAME}'")
            utility.drop_collection(COLLECTION_NAME)
            print("✅ Cleanup complete.")
        connections.disconnect("default")
        print("Disconnected from Milvus.")

if __name__ == "__main__":
    run_milvus_test()
