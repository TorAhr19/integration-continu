import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.main import app
from app.database import get_db, Base

SQLALCHEMY_TEST_URL = "sqlite://"

test_engine = create_engine(
    SQLALCHEMY_TEST_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

Base.metadata.create_all(bind=test_engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
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
