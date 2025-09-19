# 代码生成时间: 2025-09-19 22:44:15
import json
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route, Mount
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.status import HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR
import os
from typing import Any, Dict

# Custom Exception
class ConfigException(Exception):
    """Custom exception for configuration related errors."""
    pass


# Config Manager Class
class ConfigManager:
    """Class to manage configurations from a JSON file."""
    def __init__(self, config_file: str):
        """Initialize the configuration manager with a JSON file."""
        self.config_file = config_file
        self.config_data = self.load_config()

    def load_config(self) -> Dict[str, Any]:
        """Load configuration data from a JSON file."""
        try:
            with open(self.config_file, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            raise ConfigException(f"Configuration file '{self.config_file}' not found.")
        except json.JSONDecodeError:
            raise ConfigException(f"Failed to parse configuration file '{self.config_file}' as JSON.")

    def get_config(self, key: str) -> Any:  # type: ignore
        """Retrieve a configuration value by key."""
        try:
            return self.config_data[key]
        except KeyError:
            raise ConfigException(f"Configuration key '{key}' not found.")

    def update_config(self, key: str, value: Any) -> None:
        """Update a configuration value by key."""
        self.config_data[key] = value
        self.save_config()

    def save_config(self) -> None:
        """Save the current configuration data back to the JSON file."""
        with open(self.config_file, 'w') as file:
            json.dump(self.config_data, file, indent=4)


# API Endpoint for Config Management
async def get_config_endpoint(request):  # type: ignore
    config_key = request.query_params.get('key')
    if not config_key:
        return JSONResponse({'error': 'Missing key parameter'}, status_code=HTTP_400_BAD_REQUEST)
    try:
        config_value = config_manager.get_config(config_key)
        return JSONResponse({'key': config_key, 'value': config_value})
    except ConfigException as e:
        return JSONResponse({'error': str(e)}, status_code=HTTP_500_INTERNAL_SERVER_ERROR)

async def update_config_endpoint(request):  # type: ignore
    json_body = await request.json()
    config_key = json_body.get('key')
    config_value = json_body.get('value')
    if not config_key or not config_value:
        return JSONResponse({'error': 'Missing key or value parameter'}, status_code=HTTP_400_BAD_REQUEST)
    try:
        config_manager.update_config(config_key, config_value)
        return JSONResponse({'key': config_key, 'value': config_value})
    except ConfigException as e:
        return JSONResponse({'error': str(e)}, status_code=HTTP_500_INTERNAL_SERVER_ERROR)


# Starlette Application Setup
routes = [  # type: ignore
    Route('/config', endpoint=get_config_endpoint, methods=['GET']),
    Route('/config', endpoint=update_config_endpoint, methods=['POST']),
]

app = Starlette(debug=True, routes=routes)

# Ensure ConfigManager instance is created with a valid JSON file path
config_manager = ConfigManager('config.json')
