from fastapi.testclient import TestClient
 # Import your FastAPI app
from decoding_the_roads.main import app
client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200

def test_chart():
    response = client.get("/chart")
    assert response.status_code == 200
