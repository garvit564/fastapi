from fastapi import FastAPI,Request
import os
from dotenv import load_dotenv
from database import engine, Base
from starlette.middleware.sessions import SessionMiddleware
from models.user import User
from models.orders import Order
import logging
import time

from routers.user import router as user_router
from routers.order import router as order_router
from routers.report import router as report_router

load_dotenv()
app = FastAPI()


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)

@app.middleware("http")
async def logging_middleware(request: Request, call_next):

    start_time = time.perf_counter()

    logger.info(
        "Request started | %s %s",
        request.method,
        request.url.path
    )

    response = await call_next(request)

    process_time = time.perf_counter() - start_time

    logger.info(
        "Request completed | status=%s | time=%.3fs",
        response.status_code,
        process_time
    )

    return response



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