from fastapi.testclient import TestClient
from decoding_the_roads.main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200


def test_dashboard():
    response = client.get("/dashboard-index.html")
    assert response.status_code == 200

def test_chart():
    response = client.get("/chart")
    assert response.status_code == 200
