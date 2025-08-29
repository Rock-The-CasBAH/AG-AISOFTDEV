from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Text, Date, CheckConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
# from sqlalchemy.orm import relationship, declarative_base
from pydantic import BaseModel
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
    __table_args__ = (
                  CheckConstraint("role IN ('New Hire', 'HR Manager', 'Department Manager')"))

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
    __table_args__ = (
                    CheckConstraint("status IN ('Pending', 'Completed')"))
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    # Establish a many-to-one relationship with users
    user = relationship('User', back_populates='onboarding_tasks')

# SQLite connection string and engine creation with connection arguments to handle threading
DATABASE_URL = "sqlite:///./onboarding.db"
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
    users = db.query(User).offset(skip).limit(limit).all()
    return users

@app.get("/users/{user_id}", response_model=UserSchema)
def read_user(user_id: int, db: Session = Depends(get_db)):
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