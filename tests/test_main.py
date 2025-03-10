from fastapi.testclient import TestClient
from decoding_the_roads.main import app  # Import FastAPI app

# Create a test client
client = TestClient(app)

def test_server_running():
    """Check if the FastAPI server is running by pinging the root URL."""
    response = client.get("/")
    assert response.status_code == 200  # Ensure the server responds successfully
