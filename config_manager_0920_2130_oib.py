# 代码生成时间: 2025-09-20 21:30:00
# config_manager.py
# This module provides a simple configuration manager for a Starlette application.

from starlette.config import Config
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.applications import Starlette
from starlette.exceptions import HTTPException
import os
import json

class ConfigManager:
    """Manages the application configuration."""
    def __init__(self, config_file='config.json'):
        self.config = self.load_config(config_file)

    def load_config(self, config_file):
        """Loads configuration from a JSON file."""
        try:
            with open(config_file, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            raise HTTPException(status_code=500, detail="Configuration file not found.")
        except json.JSONDecodeError:
            raise HTTPException(status_code=500, detail="Invalid JSON format in configuration file.")

    def get_config(self):
        """Returns the loaded configuration."""
        return self.config

    def update_config(self, new_config):
        """Updates configuration with new values and writes them to the file."""
        try:
            with open(self.config_file, 'w') as file:
                json.dump(new_config, file, indent=4)
            self.config = new_config
        except Exception as e:
            raise HTTPException(status_code=500, detail="Failed to update configuration: " + str(e))

# Example usage of the ConfigManager
if __name__ == '__main__':
    # Create an instance of ConfigManager with a specified config file
    config_manager = ConfigManager()

    # Create a Starlette application
    app = Starlette()

    # Define a route to get the current configuration
    app.add_route('/get-config', lambda request: JSONResponse(config_manager.get_config()))

    # Define a route to update the configuration
    @app.route('/update-config', methods=['POST'])
    async def update_config_endpoint(request):
        try:
            new_config = await request.json()
            config_manager.update_config(new_config)
            return JSONResponse({'status': 'success', 'message': 'Configuration updated.'})
        except HTTPException as e:
            return JSONResponse({'status': 'error', 'message': str(e.detail)}, status_code=e.status_code)

    # Run the application
    if os.environ.get('ENVIRONMENT') == 'development':
        import uvicorn
        uvicorn.run(app, host='0.0.0.0', port=8000)