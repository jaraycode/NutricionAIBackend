from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.app.Config.db import conn
from src.app.core.users.Routes import router as user
from src.app.core.auth.Routes import router as login
from src.app.core.food.Routes import router as food
from src.app.core.config.Routes import router as config
import uvicorn, os

def init_app() -> FastAPI:
    @asynccontextmanager
    async def lifespan(app:FastAPI):
        await conn.connect()
        yield
        await conn.disconnect()
    app = FastAPI(title="NutricionBackend", description="Backend side of the application that looks for your health", version="0.0.1", lifespan=lifespan)
    app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

    @app.get("/")
    def home() -> str:
        return "Nutricion Backend"

    for router in [user, login, food, config]:
        app.include_router(router)

    return app

app = init_app()


if __name__ == "__main__":
    uvicorn.run(app="main:app", host=os.getenv("APP_HOST"), port=int(os.getenv("APP_PORT")), reload=True)