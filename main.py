from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from fastapi import FastAPI
from core.app.Config.db import conn
import uvicorn

def init_app() -> FastAPI:
    @asynccontextmanager
    async def lifespan(app:FastAPI):
        print("Server started")
        await conn.connect()
        yield
        print("Shutdown server")
        await conn.disconnect()
    app = FastAPI(title="NutricionBackend", description="Backend side of the application that looks for your health", version="0.0.1", lifespan=lifespan)
    app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

    @app.get("/")
    def home() -> str:
        return "Nutricion Backend"

    return app

app = init_app()


if __name__ == "__main__":
    uvicorn.run(app="main:app", host="0.0.0.0", port=8888, reload=True)