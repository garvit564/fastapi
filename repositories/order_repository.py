from sqlalchemy.orm import Session

from models.orders import Order


class OrderRepository:

    def create_order(self, db: Session, order_data):
        order = Order(
            user_id=order_data.user_id,
            product=order_data.product,
            amount=order_data.amount,
            description=order_data.description,
            status=order_data.status
        )

        db.add(order)
        db.commit()
        db.refresh(order)

        return order

    def get_order_by_id(self, db: Session, order_id: int):
        return (
            db.query(Order)
            .filter(Order.id == order_id)
            .first()
        )

    def get_user_orders(self, db: Session, user_id: int):
        return (
            db.query(Order)
            .filter(Order.user_id == user_id)
            .all()
        )

    def update_order(self, db: Session, order, order_data):
        order.user_id = order_data.user_id
        order.product = order_data.product
        order.amount = order_data.amount
        order.description = order_data.description
        order.status = order_data.status

        db.commit()
        db.refresh(order)

        return order

    def patch_order(self, db: Session, order, order_data):

        if order_data.user_id is not None:
            order.user_id = order_data.user_id

        if order_data.product is not None:
            order.product = order_data.product

        if order_data.amount is not None:
            order.amount = order_data.amount

        if order_data.description is not None:
             order.discription = order_data.description    

        if order_data.status is not None:
            order.status = order_data.status

        db.commit()
        db.refresh(order)

        return order

    def delete_order(self, db: Session, order):
        db.delete(order)
        db.commit()


order_repository = OrderRepository()