import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_home():
    response = client.get("/")

    assert response.status_code == 200


def test_get_products():
    response = client.get("/produits")

    assert response.status_code == 200


def test_create_product():
    product_data = {
        "nom": "Clavier",
        "description": "Clavier mécanique",
        "prix": 99.99,
        "quantite_stock": 10
    }

    response = client.post("/produits", json=product_data)

    print("\nCREATE RESPONSE :", response.json())

    assert response.status_code in [200, 201]


def test_get_product_by_id():
    response = client.get("/produits/1")

    print("\nGET PRODUCT RESPONSE :", response.json())

    assert response.status_code in [200, 404]

def test_update_product():
    updated_data = {
        "nom": "Clavier Gamer",
        "description": "Clavier RGB performant",
        "prix": 120.0,
        "quantite_stock": 5
    }

    response = client.put("/produits/1", json=updated_data)

    print("\nUPDATE RESPONSE :", response.json())

    assert response.status_code in [200, 404]

def test_delete_product():
    response = client.delete("/produits/1")

    print("\nDELETE RESPONSE :", response.json())

    assert response.status_code in [200, 404]