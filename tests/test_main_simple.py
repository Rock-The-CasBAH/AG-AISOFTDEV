# tests/test_main_simple.py
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from main import app, get_db
from models import Base, User

# Configure test database
TEST_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override get_db dependency
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# Test client
client = TestClient(app)

@pytest.fixture(scope="function")
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_create_user(test_db):
    """Test user creation endpoint"""
    user_data = {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "role": "New Hire"
    }
    
    response = client.post("/users/", json=user_data)
    
    assert response.status_code == 200
    assert response.json()["email"] == user_data["email"]
    assert response.json()["name"] == user_data["name"]
    assert response.json()["role"] == user_data["role"]
    assert "id" in response.json()

def test_get_users(test_db):
    """Test users retrieval endpoint"""
    # First create test users
    users_data = [
        {"name": "User One", "email": "user1@example.com", "role": "New Hire"},
        {"name": "User Two", "email": "user2@example.com", "role": "HR Manager"}
    ]
    
    for user_data in users_data:
        client.post("/users/", json=user_data)
    
    # Test retrieving all users
    response = client.get("/users/")
    
    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[0]["email"] == users_data[0]["email"]
    assert response.json()[1]["email"] == users_data[1]["email"]

def test_get_users_pagination(test_db):
    """Test users endpoint with pagination"""
    # Create multiple users
    for i in range(5):
        user_data = {
            "name": f"User {i}",
            "email": f"user{i}@example.com",
            "role": "New Hire"
        }
        client.post("/users/", json=user_data)
    
    # Test skip and limit parameters
    response = client.get("/users/?skip=2&limit=2")
    
    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[0]["name"] == "User 2"
    assert response.json()[1]["name"] == "User 3"