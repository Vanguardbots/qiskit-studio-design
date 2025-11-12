# Copyright contributors to the Qiskit Studio project
# SPDX-License-Identifier: Apache-2.0

from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
import uvicorn
import socket
import argparse
import subprocess
import sys
import asyncio
import io
import logging
import contextlib
import json
from json.decoder import JSONDecodeError
import re

# Global variable to control execution mode
LOCAL_MODE = True

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI()


# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add exception handler for JSON decode errors
@app.exception_handler(JSONDecodeError)
async def json_decode_exception_handler(request: Request, exc: JSONDecodeError):
    return JSONResponse(
        status_code=400,
        content={"detail": "Invalid JSON format in request body"},
    )


def replace_ibm_quantum_config(code: str, ibm_config: dict = None) -> str:
    """Replace IBM Quantum Config section based on execution mode and IBM config."""

    # If IBM config is provided, use IBM Quantum Runtime Service
    if ibm_config and ibm_config.get("token"):
        token = ibm_config["token"]
        channel = ibm_config.get("channel", "ibm_quantum")
        instance = ibm_config.get("instance")
        region = ibm_config.get("region")

        logger.info(f"IBM config provided. Injecting token: {token[:10]}...")
        logger.info(
            f"Channel: {channel}, Instance: {'yes' if instance else 'no'}, Region: {region or 'none'}"
        )

        # Pattern to match AerSimulator config (if switching from local to cloud)
        aer_pattern = r"from qiskit_aer import AerSimulator\n\nbackend = AerSimulator\(\)\nprint\(\"Using local simulator\.\.\.\"\)"

        # Pattern to match IBM Quantum imports and backend setup (without token)
        ibm_pattern_no_token = r"from qiskit_ibm_runtime import QiskitRuntimeService\n\nservice = QiskitRuntimeService\(\)\nbackend = service\.least_busy\(operational=True, simulator=False\)"

        # Pattern to match IBM Quantum imports and backend setup (with existing token)
        ibm_pattern_with_token = r"from qiskit_ibm_runtime import QiskitRuntimeService\n\nservice = QiskitRuntimeService\(token='[^']+'\)\nbackend = service\.least_busy\(operational=True, simulator=False\)"

        # Build service initialization parameters
        service_params = [f'channel="{channel}"', f'token="{token}"']

        if instance:
            service_params.append(f'instance="{instance}"')

        if region:
            service_params.append(f'region="{region}"')

        service_params_str = ",\n    ".join(service_params)

        # Replacement text with IBM Quantum Runtime Service and full config
        replacement = f"""from qiskit_ibm_runtime import QiskitRuntimeService

# Initialize IBM Quantum Runtime Service with provided configuration
service = QiskitRuntimeService(
    {service_params_str}
)
backend = service.least_busy(operational=True, simulator=False)
print(f"Using IBM Quantum backend: {{backend.name}}")"""

        # Replace AerSimulator with IBM Quantum if found
        if re.search(aer_pattern, code, re.DOTALL):
            logger.info("Found AerSimulator config, replacing with IBM Quantum config.")
            return re.sub(aer_pattern, replacement, code, flags=re.DOTALL)

        # Replace existing IBM Quantum config (without token) to include token
        if re.search(ibm_pattern_no_token, code, re.DOTALL):
            logger.info("Found IBM Quantum config without token, injecting token.")
            return re.sub(ibm_pattern_no_token, replacement, code, flags=re.DOTALL)

        # Replace existing IBM Quantum config (with token) to update token
        if re.search(ibm_pattern_with_token, code, re.DOTALL):
            logger.info("Found IBM Quantum config with existing token, updating it.")
            return re.sub(ibm_pattern_with_token, replacement, code, flags=re.DOTALL)

        # If no exact patterns found, try to find and inject token into existing QiskitRuntimeService calls
        if "QiskitRuntimeService()" in code:
            logger.info("Found generic 'QiskitRuntimeService()', injecting parameters.")
            modified_code = code.replace(
                "QiskitRuntimeService()",
                f"QiskitRuntimeService(\n    {service_params_str}\n)",
            )
            return modified_code

        logger.info(
            "No specific IBM Quantum pattern matched for token injection. Returning original code."
        )
        return code

    # Only replace with local simulator if LOCAL_MODE is True and no token provided
    if not LOCAL_MODE:
        logger.info(
            "Cloud mode is active and no token provided. No code replacement will be performed."
        )
        return code

    logger.info(
        "No token provided and local mode is active. Attempting to replace IBM Quantum config with local simulator."
    )

    # Replacement text with local simulator
    replacement = """from qiskit_aer import AerSimulator

backend = AerSimulator()
print("Using local simulator...")"""

    # Find the IBM Quantum Config section
    ibm_config_pattern = r"## STEP 0 : IBM Quantum Config"
    if re.search(ibm_config_pattern, code):
        logger.info("Found IBM Quantum Config section header.")

        # Split the code into sections based on "## STEP" markers
        sections = re.split(r"(## STEP \d+.*?\n)", code)

        # If we have at least 3 elements (before STEP 0, STEP 0 marker, STEP 0 content)
        if len(sections) >= 3:
            # Replace the content of STEP 0 with our simulator code
            for i in range(1, len(sections), 2):
                if "STEP 0" in sections[i] and "IBM Quantum Config" in sections[i]:
                    # Replace the content (which is in the next section)
                    sections[i+1] = "\n" + replacement + "\n\n"
                    break

            # Join the sections back together
            modified_code = "".join(sections)

            # Remove all IBM Runtime specific options
            logger.info("Removing any remaining IBM Runtime options from code.")
            modified_code = re.sub(r".*?\.options\..*?\n", "", modified_code)

            return modified_code

    # If we didn't find a structured IBM Quantum Config section, try the old patterns
    ibm_patterns = [
        r"from qiskit_ibm_runtime import QiskitRuntimeService\n\nservice = QiskitRuntimeService\(token='[^']+'\)\nbackend = service\.least_busy\(operational=True, simulator=False\)\nprint\(f\"Using IBM Quantum backend: {[^}]+}\"\)",
        r"from qiskit_ibm_runtime import QiskitRuntimeService\n\nservice = QiskitRuntimeService\(\)\nbackend = service\.least_busy\(operational=True, simulator=False\)",
    ]

    # Try each pattern
    for i, pattern in enumerate(ibm_patterns):
        if re.search(pattern, code, re.DOTALL):
            logger.info(
                f"Matched IBM Quantum pattern #{i + 1}. Replacing with local simulator."
            )
            modified_code = re.sub(pattern, replacement, code, flags=re.DOTALL)
            # Remove all IBM Runtime specific options
            logger.info("Removing any remaining IBM Runtime options from code.")
            modified_code = re.sub(r".*?\.options\..*?\n", "", modified_code)
            return modified_code

    logger.info(
        "No IBM Quantum patterns matched for local simulator replacement. Returning original code."
    )
    return code


def execute_python_code(code: str, ibm_config: dict = None) -> str:
    """Execute Python code and capture stdout/stderr."""
    logger.info("Beginning code execution process.")
    # Replace IBM Quantum Config section automatically
    code = replace_ibm_quantum_config(code, ibm_config)
    logger.info("Code transformation complete. Preparing execution environment.")

    stdout_capture = io.StringIO()
    stderr_capture = io.StringIO()

    try:
        # Create execution namespace with common imports
        exec_globals = {
            "__builtins__": __builtins__,
        }

        with (
            contextlib.redirect_stdout(stdout_capture),
            contextlib.redirect_stderr(stderr_capture),
        ):
            logger.info("Executing user-provided code via exec().")
            exec(code, exec_globals)
            logger.info("Finished executing user-provided code.")

        stdout_output = stdout_capture.getvalue()
        stderr_output = stderr_capture.getvalue()

        output = ""
        if stdout_output:
            output += stdout_output
        if stderr_output:
            output += stderr_output

        logger.info("Successfully captured output from code execution.")
        return output if output else "Code executed successfully (no output)"

    except Exception as e:
        logger.error("An exception occurred during user code execution.", exc_info=True)
        # Also capture any stderr that might have been produced before the exception
        stderr_output = stderr_capture.getvalue()
        return f"Error executing code: {str(e)}\n{stderr_output}"


@app.post("/run")
async def run_program(request: Request):
    logger.info("Received /run request from %s.", request.client.host)
    data = await request.json()
    code = data["input_value"]

    ibm_token = data.get("ibm_token")  # Optional IBM Quantum token
    channel = data.get("channel", "ibm_quantum")  # Default to ibm_quantum
    instance = data.get("instance")  # Optional instance CRN
    region = data.get("region")  # Optional region

    # Create IBM config object
    ibm_config = (
        {"token": ibm_token, "channel": channel, "instance": instance, "region": region}
        if ibm_token
        else None
    )

    if ibm_config:
        logger.info("Request includes IBM Quantum configuration.")
    else:
        logger.info(
            "Request does not include IBM Quantum configuration; will use local simulator if agent is in local mode."
        )
    logger.info("Dispatching code execution to a background thread.")

    try:
        # Execute the blocking Python code in a separate thread to avoid freezing the event loop.
        # This prevents timeouts from upstream components like load balancers.
        # A 30-minute timeout is also applied to the execution itself.
        loop = asyncio.get_running_loop()
        timeout_seconds = 30 * 60  # 30 minutes

        output = await asyncio.wait_for(
            loop.run_in_executor(None, execute_python_code, code, ibm_config),
            timeout=timeout_seconds,
        )
        logger.info("Background execution task completed successfully.")
    except asyncio.TimeoutError:
        output = (
            f"Error: Code execution timed out after {timeout_seconds / 60:.0f} minutes."
        )
        logger.warning("Background execution task timed out.")

    logger.info("Sending response for /run request from %s.", request.client.host)
    # Fix for escaped newlines in chemistry simulation output
    # Replace any double escaped newlines with actual newlines
    if output and isinstance(output, str):
        output = output.replace('\\\\n', '\n')
    return JSONResponse({"output": output})


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run the FastAPI app with a custom port."
    )
    parser.add_argument(
        "--port", type=int, default=8000, help="Port to run the server on"
    )
    parser.add_argument(
        "--local",
        action="store_true",
        default=False,
        help="Enable local mode (replace IBM Quantum with AerSimulator)",
    )
    parser.add_argument(
        "--cloud",
        action="store_true",
        default=False,
        help="Enable cloud mode (use QiskitRuntimeService)",
    )
    args = parser.parse_args()

    # Set execution mode based on arguments
    if args.cloud:
        LOCAL_MODE = False
        logger.info("Starting in CLOUD mode - using QiskitRuntimeService")
    else:
        # Default behavior
        LOCAL_MODE = True
        logger.info("Starting in LOCAL mode (default) - replacing with AerSimulator")

    uvicorn.run(app, host="0.0.0.0", port=args.port)
