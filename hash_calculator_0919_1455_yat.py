# 代码生成时间: 2025-09-19 14:55:26
# hash_calculator.py
# A simple hash calculator tool using the Starlette framework.

from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
import hashlib
import json

# Define the hash calculation function
def calculate_hash(data: str, algorithm: str = 'sha256') -> str:
    """Calculate the hash value of the given data using the specified algorithm.

    Args:
        data (str): The data to be hashed.
        algorithm (str): The hashing algorithm to use (default is 'sha256').

    Returns:
        str: The calculated hash value.
    """
    try:
        hash_obj = getattr(hashlib, algorithm)()
        hash_obj.update(data.encode('utf-8'))
        return hash_obj.hexdigest()
    except AttributeError:
        raise ValueError(f"Unsupported algorithm: {algorithm}")

# Define the endpoint for calculating hash
async def calculate_hash_endpoint(request):
    """Endpoint to handle hash calculation requests.

    Args:
        request: The incoming request.

    Returns:
        JSONResponse: A JSON response containing the calculated hash or error message.
    """
    data = await request.json()
    if 'data' not in data:
        return JSONResponse(
            content={"error": "Missing 'data' key in request body"},
            status_code=HTTP_400_BAD_REQUEST
        )

    data_value = data['data']
    algorithm = data.get('algorithm', 'sha256')

    try:
        hash_value = calculate_hash(data_value, algorithm)
        return JSONResponse(
            content={"hash": hash_value},
            status_code=HTTP_200_OK
        )
    except ValueError as e:
        return JSONResponse(
            content={"error": str(e)},
            status_code=HTTP_400_BAD_REQUEST
        )

# Create the Starlette application with the hash calculation endpoint
app = Starlette(
    routes=[
        Route('/calculate-hash', calculate_hash_endpoint, methods=['POST']),
    ],
)

# Documentation for the endpoint
@app.documentation
def app_documentation():
    return {
        "/calculate-hash": {
            "post": {
                "summary": "Calculate the hash of a given data",
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "data": {
                                        "type": "string",
                                        "description": "The data to be hashed",
                                    },
                                    "algorithm": {
                                        "type": "string",
                                        "description": "The hashing algorithm to use (default is 'sha256')",
                                    },
                                },
                            },
                        },
                    },
                },
                "responses": {
                    "200": {
                        "description": "Hash calculation successful",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "hash": {
                                            "type": "string",
                                            "description": "The calculated hash value",
                                        },
                                    },
                                },
                            },
                        },
                        "400": {
                            "description": "Invalid request",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "error": {
                                                "type": "string",
                                                "description": "Error message",
                                            },
                                        },
                                    },
                                },
                            },
                        },
                },
            },
        },
    }
