from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.db.database import create_tables,engine
from app.api.todo import todoRouter



@asynccontextmanager
async def lifespan(app:FastAPI):
    await create_tables()

    yield

    await engine.dispose()


app=FastAPI(
    title="Todo with db connection",
    lifespan=lifespan
)


@app.get("/root")
async def root():
    return {
        "message":"This is root path"
    }

app.include_router(prefix="/api/v1",router=todoRouter)