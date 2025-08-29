from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr, validator
from typing import List, Optional
from fastapi.middleware.cors import CORSMiddleware

# Initialize FastAPI application
app = FastAPI()

# Allow all CORS origins for demonstration purposes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for input validation and data representation
class UserBase(BaseModel):
    name: str
    email: EmailStr
    role: str

    @validator('role')
    def validate_role(cls, v):
        valid_roles = ['New Hire', 'HR Manager', 'Department Manager']
        if v not in valid_roles:
            raise ValueError(f'Role must be one of {valid_roles}')
        return v

class UserCreate(UserBase):
    pass

class UserRead(UserBase):
    id: int

# In-memory "database" of users
fake_db: List[UserRead] = [
    UserRead(id=1, name='John Doe', email='john.doe@example.com', role='New Hire'),
    UserRead(id=2, name='Jane Smith', email='jane.smith@example.com', role='HR Manager')
]

# Utility function to find a user by email
def get_user_by_email(email: str) -> Optional[UserRead]:
    return next((user for user in fake_db if user.email == email), None)

# Utility function to find a user by ID
def get_user_by_id(user_id: int) -> Optional[UserRead]:
    return next((user for user in fake_db if user.id == user_id), None)

# CRUD Endpoints
@app.post("/users", response_model=UserRead, status_code=201)
def create_user(user: UserCreate):
    """Create a new user and add to the in-memory database."""
    if get_user_by_email(user.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    
    new_id = max(user.id for user in fake_db) + 1 if fake_db else 1
    new_user = UserRead(id=new_id, **user.dict())
    fake_db.append(new_user)
    return new_user

@app.get("/users", response_model=List[UserRead])
def read_users(role: Optional[str] = None):
    """Retrieve all users or filter by role."""
    if role:
        return [user for user in fake_db if user.role == role]
    return fake_db

@app.get("/users/{user_id}", response_model=UserRead)
def read_user(user_id: int):
    """Retrieve a user by their ID."""
    user = get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.put("/users/{user_id}", response_model=UserRead)
def update_user(user_id: int, user: UserCreate):
    """Update an existing user's information."""
    stored_user = get_user_by_id(user_id)
    if not stored_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user.email != stored_user.email and get_user_by_email(user.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    
    updated_user = stored_user.copy(update=user.dict())
    fake_db[fake_db.index(stored_user)] = updated_user
    return updated_user

@app.delete("/users/{user_id}", status_code=204)
def delete_user(user_id: int):
    """Delete a user by their ID."""
    user = get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    fake_db.remove(user)

# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)