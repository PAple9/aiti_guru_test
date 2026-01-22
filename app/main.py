from contextlib import asynccontextmanager
from fastapi import FastAPI
import uvicorn
from app.database import create_tables, engine
from app.order_router import router as order_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    yield
    await engine.dispose()


app = FastAPI(lifespan=lifespan)
app.include_router(order_router)


@app.get("/")
async def root():
    return {"message": "Order Service работает"}


if __name__ == "__main__":
    uvicorn.run(app="main:app", host="localhost", port=8000, reload=True)
