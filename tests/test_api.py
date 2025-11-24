from fastapi.testclient import TestClient
from src.api import app

client = TestClient(app)

def test_predict_endpoint():
    payload = {
        "MedInc": 3.5,
        "AveRooms": 6.0,
        "AveOccup": 2.5
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    assert "predicted_house_price" in response.json()
    assert isinstance(response.json()["predicted_house_price"], float)
