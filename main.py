from fastapi import FastAPI, HTTPException, Depends
from typing import List
import uvicorn


app = FastAPI(
    title="CAT TABLE API",
    description="cat table management",
    version="1.0.0"
)

# Point de santé de l'API
@app.get("/")
def read_root():
    return {"message": "Bienvenue sur l'API CRUD FastAPI!"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)