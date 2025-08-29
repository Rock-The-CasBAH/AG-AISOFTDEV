from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Text, Date, CheckConstraint
from sqlalchemy.orm import declarative_base, sessionmaker, Session, relationship
# from sqlalchemy.orm import relationship, declarative_base
from pydantic import BaseModel
from pathlib import Path
from typing import List, Optional
from sqlalchemy.exc import SQLAlchemyError
# from models import Base

# models.py

# Create a base class for declarative models
Base = declarative_base()

class User(Base):
    """
    SQLAlchemy model for the 'users' table.
    
    Attributes:
        id (int): Primary key, auto-incremented.
        name (str): Full name of the user, cannot be empty.
        email (str): Unique email address of the user, used for login and notifications.
        role (str): Role of the user within the system, with constraints on possible values.
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    role = Column(String, nullable=False)
    # single-element tuple requires a trailing comma so SQLAlchemy accepts it as a tuple
    __table_args__ = (
                  CheckConstraint("role IN ('New Hire', 'HR Manager', 'Department Manager')"),)

    # Establish a one-to-many relationship with onboarding_tasks
    onboarding_tasks = relationship('OnboardingTask', back_populates='user', cascade='all, delete-orphan')

# --- Pydantic Models ---
class UserBase(BaseModel):
    email: str
    name: str
    role: str

class UserCreate(UserBase):
    pass

class UserSchema(UserBase):
    id: int
    class Config:
        orm_mode = True

class OnboardingTask(Base):
    """
    SQLAlchemy model for the 'onboarding_tasks' table.
    
    Attributes:
        id (int): Primary key, auto-incremented.
        title (str): Title of the onboarding task, cannot be empty.
        description (str): Detailed explanation of the task.
        due_date (str): Due date for task completion, in 'YYYY-MM-DD' format.
        status (str): Current status of the task, defaults to 'Pending'.
        user_id (int): Foreign key linking to the user, cannot be empty.
    """
    __tablename__ = 'onboarding_tasks'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    due_date = Column(String)
    status = Column(String, nullable=False, default='Pending')
    # single-element tuple requires a trailing comma so SQLAlchemy accepts it as a tuple
    __table_args__ = (
                    CheckConstraint("status IN ('Pending', 'Completed')"),)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    # Establish a many-to-one relationship with users
    user = relationship('User', back_populates='onboarding_tasks')

# SQLite connection string and engine creation with connection arguments to handle threading
# Prefer the seeded DB under the repository's `artifacts/` directory. Fall back to the
# repository-root `onboarding.db` for backward compatibility.
project_root = Path(__file__).resolve().parents[1]
db_path = project_root / "artifacts" / "onboarding.db"
if not db_path.exists():
    # fallback to repo root onboarding.db
    db_path = project_root / "onboarding.db"
DATABASE_URL = f"sqlite:///{db_path.as_posix()}"
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# SessionLocal class to create database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

app = FastAPI()

def get_db():
    """
    Dependency for getting a database session in FastAPI.
    Ensures that each request gets its own session and closes it after.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create all tables in the database if they do not exist
try:
    Base.metadata.create_all(bind=engine)
except SQLAlchemyError as e:
    print(f"Error creating database tables: {e}")
    
# --- API Endpoints ---
@app.post("/users/", response_model=UserSchema)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Creates a new user in the database.
    
    This endpoint accepts user information and creates a new user record in the
    database after validating that the email address is not already registered.
    It's typically used during the onboarding process to register new employees
    or users in the system.
    
    Args:
        user (UserCreate): A Pydantic model containing the user data to create.
            Required fields:
            - email (str): Unique email address for the user
            - name (str): Full name of the user
            - role (str): User's role in the organization
        db (Session): Database session provided by FastAPI dependency injection.
            Automatically managed by the get_db dependency.
    
    Returns:
        UserSchema: A Pydantic model representing the created user with all fields:
            - id (int): Auto-generated unique identifier
            - email (str): The user's email address
            - name (str): The user's full name
            - role (str): The user's role
    
    Raises:
        HTTPException: 
            - 400 Bad Request: If a user with the provided email already exists.
              Returns {"detail": "Email already registered"}
    
    Notes:
        - Email addresses must be unique across all users
        - The user ID is auto-generated by the database
        - The created user is immediately committed to the database
        - Uses SQLAlchemy ORM for database operations
        - The response model ensures only specified fields are returned
    
    Example:
        >>> # POST /users/
        >>> # Request body:
        >>> {
        ...     "email": "john.doe@example.com",
        ...     "name": "John Doe",
        ...     "role": "Software Engineer"
        ... }
        >>> # Response (201 Created):
        >>> {
        ...     "id": 1,
        ...     "email": "john.doe@example.com",
        ...     "name": "John Doe",
        ...     "role": "Software Engineer"
        ... }
    
    Dependencies:
        - User: SQLAlchemy model for the users table
        - get_db: Dependency function providing database session
    """
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    db_user = User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/users/", response_model=List[UserSchema])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieves a paginated list of all users from the database.
    
    This endpoint returns a list of users with support for pagination through
    skip and limit parameters. It's useful for displaying user lists in admin
    interfaces or for bulk user management operations.
    
    Args:
        skip (int, optional): Number of records to skip from the beginning.
            Used for pagination. Defaults to 0 (start from first record).
            Must be >= 0.
        limit (int, optional): Maximum number of records to return.
            Used to control page size. Defaults to 100. Maximum is 100
            to prevent excessive data transfer.
        db (Session): Database session provided by FastAPI dependency injection.
            Automatically managed by the get_db dependency.
    
    Returns:
        List[UserSchema]: A list of user objects, each containing:
            - id (int): Unique user identifier
            - email (str): User's email address
            - name (str): User's full name
            - role (str): User's role in the organization
            
            Returns empty list if no users exist or if skip exceeds total count.
    
    Raises:
        None: This endpoint doesn't raise HTTP exceptions but may encounter
            database errors which are handled by FastAPI's error handlers.
    
    Notes:
        - Results are not sorted by default (database order)
        - Pagination is zero-based (skip=0 returns first record)
        - The limit parameter prevents loading too many records at once
        - Useful for implementing paginated user lists in frontend
        - Consider adding sorting parameters for production use
    
    Example:
        >>> # GET /users/?skip=0&limit=10
        >>> # Response (200 OK):
        >>> [
        ...     {
        ...         "id": 1,
        ...         "email": "john.doe@example.com",
        ...         "name": "John Doe",
        ...         "role": "Software Engineer"
        ...     },
        ...     {
        ...         "id": 2,
        ...         "email": "jane.smith@example.com",
        ...         "name": "Jane Smith",
        ...         "role": "Product Manager"
        ...     }
        ... ]
    
    Dependencies:
        - User: SQLAlchemy model for the users table
        - get_db: Dependency function providing database session
    """
    users = db.query(User).offset(skip).limit(limit).all()
    return users

@app.get("/users/{user_id}", response_model=UserSchema)
def read_user(user_id: int, db: Session = Depends(get_db)):
    """
    Retrieves a single user by their ID.
    
    This endpoint fetches detailed information about a specific user identified
    by their unique ID. It's commonly used for viewing user profiles, editing
    user information, or retrieving user details for other operations.
    
    Args:
        user_id (int): The unique identifier of the user to retrieve.
            Must be a positive integer corresponding to an existing user.
        db (Session): Database session provided by FastAPI dependency injection.
            Automatically managed by the get_db dependency.
    
    Returns:
        UserSchema: A Pydantic model representing the requested user with fields:
            - id (int): The user's unique identifier (same as requested)
            - email (str): The user's email address
            - name (str): The user's full name
            - role (str): The user's role in the organization
    
    Raises:
        HTTPException:
            - 404 Not Found: If no user exists with the provided ID.
              Returns {"detail": "User not found"}
            - 422 Unprocessable Entity: If user_id is not a valid integer
              (handled automatically by FastAPI)
    
    Notes:
        - The user_id is extracted from the URL path
        - Only returns the user if they exist in the database
        - Does not include related data (like tasks) in the response
        - Consider adding authentication/authorization in production
        - The response model ensures consistent field formatting
    
    Example:
        >>> # GET /users/1
        >>> # Response (200 OK):
        >>> {
        ...     "id": 1,
        ...     "email": "john.doe@example.com",
        ...     "name": "John Doe",
        ...     "role": "Software Engineer"
        ... }
        
        >>> # GET /users/999 (non-existent user)
        >>> # Response (404 Not Found):
        >>> {
        ...     "detail": "User not found"
        ... }
    
    Dependencies:
        - User: SQLAlchemy model for the users table
        - get_db: Dependency function providing database session
    """
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# Convenience wrapper so `uvicorn main:app` works from the project root.
# It imports the FastAPI app instance from the inner `app/main.py` module.
# When run directly this will start uvicorn (useful for local debugging)
if __name__ == "__main__":
    import uvicorn
    import importlib

    # Uvicorn's auto-reload requires the application to be importable by
    # module path (e.g. "app.main:app"). When running `python app/main.py`,
    # the interpreter's sys.path[0] is set to the `app/` directory and the
    # top-level package `app` is not importable which causes a
    # ModuleNotFoundError inside the reloader subprocess. We try to import
    # the package first and only enable reload when possible. Otherwise we
    # start the server without reload to avoid the error.
    try:
        importlib.import_module("app")
        uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
    except Exception:
        # Fallback: start without reload (safe when launching as a script)
        print("Note: 'app' package not importable — starting server without reload.")
        uvicorn.run(app, host="127.0.0.1", port=8000, reload=False)