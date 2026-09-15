from fastapi import FastAPI
import os
from dotenv import load_dotenv
from database import engine, Base
from starlette.middleware.sessions import SessionMiddleware
from models.user import User
from models.orders import Order

from routers.user import router as user_router
from routers.order import router as order_router
from routers.report import router as report_router

load_dotenv()
app = FastAPI()

app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("SESSION_SECRET_KEY"),
    max_age=60 * 60 * 24 * 7
)

# Base.metadata.create_all(bind=engine)

app.include_router(user_router)
app.include_router(order_router)
app.include_router(report_router)


@app.get("/")
def home():
    return {
        "message": "Order Report API is running"
    }