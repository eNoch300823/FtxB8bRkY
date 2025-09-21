# 代码生成时间: 2025-09-21 09:50:25
import starlette.testclient
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
import pytest

# Define the application
app = Starlette(debug=True)

# Define a simple endpoint
@app.route("/test_endpoint", methods=["GET"])
async def test_endpoint(request):
    try:
        # Perform some operations
        return JSONResponse({"message": "Hello, World!"}, status_code=HTTP_200_OK)
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=HTTP_400_BAD_REQUEST)

# Define the test client
client = starlette.testclient.TestClient(app)

# Define test functions
@pytest.mark.asyncio
async def test_get_test_endpoint():
    response = await client.get("/test_endpoint")
    assert response.status_code == HTTP_200_OK
    assert response.json() == {"message": "Hello, World!"}

@pytest.mark.asyncio
async def test_get_test_endpoint_invalid():
    response = await client.get("/non_existent_endpoint")
    assert response.status_code == HTTP_404_NOT_FOUND

# Run the tests
if __name__ == "__main__