from fastapi import FastAPI, HTTPException, Depends
from typing import List
import uvicorn

from core.routers import user_router,auth,share_holder_router,attribution_router,company_router,participation_router
from core.routers import share_insuance_router,login,log_router



app = FastAPI(
    title="CAT TABLE API",
    description="cat table management",
    version="1.0.0"
)

# Inclusion du routeur
app.include_router(user_router.router)
app.include_router(share_holder_router.router)
app.include_router(share_insuance_router.router)
app.include_router(attribution_router.router)
app.include_router(participation_router.router)
app.include_router(company_router.router)
app.include_router(login.router)
app.include_router(log_router.router)
app.include_router(auth.router)

# Point de santé de l'API
@app.get("/")
def read_root():
    return {"message": "Bienvenue sur l'API CRUD FastAPI!"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)