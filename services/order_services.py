from sqlalchemy.orm import Session

from repositories.order_repository import order_repository


class OrderService:

    def create_order(self, db: Session, order_data):
        return order_repository.create_order(
            db,
            order_data
        )

    def get_order(self, db: Session, order_id: int):
        return order_repository.get_order_by_id(
            db,
            order_id
        )

    def get_user_orders(self, db: Session, user_id: int):
        return order_repository.get_user_orders(
            db,
            user_id
        )

    def update_order(
        self,
        db: Session,
        order_id: int,
        order_data
    ):
        order = order_repository.get_order_by_id(
            db,
            order_id
        )

        if order is None:
            return None

        return order_repository.update_order(
            db,
            order,
            order_data
        )

    def patch_order(
        self,
        db: Session,
        order_id: int,
        order_data
    ):
        order = order_repository.get_order_by_id(
            db,
            order_id
        )

        if order is None:
            return None

        return order_repository.patch_order(
            db,
            order,
            order_data
        )

    def delete_order(
        self,
        db: Session,
        order_id: int
    ):
        order = order_repository.get_order_by_id(
            db,
            order_id
        )

        if order is None:
            return None

        order_repository.delete_order(
            db,
            order
        )

        return True


order_service = OrderService()