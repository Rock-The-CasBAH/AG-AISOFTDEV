# Convenience wrapper so `uvicorn main:app` works from the project root.
# It imports the FastAPI app instance from the inner `app/main.py` module.

from app.main import app

# When run directly this will start uvicorn (useful for local debugging)
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
