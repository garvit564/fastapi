from celery import Celery

celery_app = Celery(
    "order_report",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/1",
    include=["tasks.report_task"]
)