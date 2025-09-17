# 代码生成时间: 2025-09-17 10:30:51
import starlette.responses
from starlette.requests import Request
from starlette.exceptions import HTTPException as StarletteHTTPException


class ApiResponseFormatter:
    """
    A utility class to format API responses in a standardized way.
    """

    def __init__(self):
        """
        Initialize the ApiResponseFormatter instance.
        """
        pass

    def format_response(self, data, status_code):
        """
        Formats the response data into a standardized structure.
        
        Args:
            data (any): The data to be included in the response.
            status_code (int): The HTTP status code for the response.
        
        Returns:
            starlette.responses.Response: A JSON response object.
        """
        return starlette.responses.JSONResponse(
            {
                "status": "success",
                "data": data,
                "message": "Request was successful"
            },
            status_code=status_code
        )

    def format_error_response(self, exc, status_code):
        """
        Formats error responses into a standardized structure.
        
        Args:
            exc (Exception): The exception that occurred.
            status_code (int): The HTTP status code for the response.
        
        Returns:
            starlette.responses.Response: A JSON response object.
        """
        if isinstance(exc, StarletteHTTPException):
            return starlette.responses.JSONResponse(
                {
                    "status": "error",
                    "error": exc.detail,
                    "message": f"An error occurred: {exc.detail}"
                },
                status_code=exc.status_code
            )
        else:
            return starlette.responses.JSONResponse(
                {
                    "status": "error",
                    "error": "Internal Server Error",
                    "message": "An unexpected error occurred"
                },
                status_code=status_code
            )

# Example usage in a Starlette route
async def example_route(request: Request):
    try:
        # Simulate some logic that could fail
        # result = some_logic()
        # if result is None:
        #     raise ValueError("Invalid input")
        
        # For demonstration purposes, we'll just return a success response
        response_formatter = ApiResponseFormatter()
        return response_formatter.format_response({"key": "value"}, 200)
    except Exception as e:
        response_formatter = ApiResponseFormatter()
        return response_formatter.format_error_response(e, 500)
