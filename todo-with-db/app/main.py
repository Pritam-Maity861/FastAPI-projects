from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from app.db.database import create_tables,engine
from app.api.todo import todoRouter
from app.api.user import userRouter
import time


@asynccontextmanager
async def lifespan(app:FastAPI):
    # await create_tables()

    yield

    await engine.dispose()


app=FastAPI(
    title="Todo with db connection",
    lifespan=lifespan
)




@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()

    response = await call_next(request)

    process_time = time.perf_counter() - start_time

    print(process_time)

    response.headers["X-Process-Time"] = f"{process_time:.4f}"

    return response



@app.get("/root")
async def root():
    return {
        "message":"This is root path"
    }

app.include_router(prefix="/api/v1",router=todoRouter)
app.include_router(prefix="/api/v1",router=userRouter)