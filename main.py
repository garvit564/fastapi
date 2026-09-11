from fastapi import FastAPI

from database import engine, Base

from models.user import User
from models.orders import Order

from routers.user import router as user_router
from routers.order import router as order_router
from routers.report import router as report_router


app = FastAPI()

# Base.metadata.create_all(bind=engine)

app.include_router(user_router)
app.include_router(order_router)
app.include_router(report_router)


@app.get("/")
def home():
    return {
        "message": "Order Report API is running"
    }