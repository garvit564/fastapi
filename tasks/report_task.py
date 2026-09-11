from celery_app import celery_app

from database import SessionLocal

from repositories.order_repository import order_repository
from repositories.user_repository import UserRepository


@celery_app.task
def generate_order_report(order_id):

    db = SessionLocal()

    try:

        order = order_repository.get_order_by_id(
            db,
            order_id
        )

        if order is None:
            return {
                "message": "Order not found"
            }

        user_repository = UserRepository()

        user = user_repository.get_user_by_id(
            db,
            order.user_id
        )

        return {
            "order_id": order.id,

            "user": {
                "id": user.id,
                "name": user.name,
                "email": user.email
            },

            "order": {
                "product": order.product,
                "amount": order.amount,
                "status": order.status
            }
        }

    finally:
        db.close()