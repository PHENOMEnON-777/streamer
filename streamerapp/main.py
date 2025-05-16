from fastapi import FastAPI
from . import models
from .database import async_engine
from .routes import user,authentication,stationservice
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with async_engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)
    yield
    await async_engine.dispose()
app = FastAPI(lifespan=lifespan)    

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development only, restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router)
app.include_router(authentication.router)
app.include_router(stationservice.router)

