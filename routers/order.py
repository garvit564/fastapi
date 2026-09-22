from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from database import get_db
from schemas.orders import (
    OrderCreate,
    OrderUpdate,
    OrderPatch
)
from auth.security import get_current_user, get_current_user_id
from services.order_services import order_service


router = APIRouter()


@router.post("/orders")
@get_current_user_id
def create_order(
    request: Request,
    order_data: OrderCreate,
    user_id: int,
    db: Session = Depends(get_db)
):
    try:
        if order_data.user_id != user_id:
            raise HTTPException(
                status_code=403,
                detail="You cannot create an order for another user"
            )

        order_data.user_id = user_id
        return order_service.create_order(db, order_data)

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Failed to create order"
        )


@router.get("/orders/{order_id}")
@get_current_user_id
def get_order(
    request: Request,
    order_id: int,
    user_id: int,
    db: Session = Depends(get_db)
):
    try:
        order = order_service.get_order(db, order_id)

        if order is None:
            raise HTTPException(
                status_code=404,
                detail="Order not found"
            )

        if order.user_id != user_id:
            raise HTTPException(
                status_code=403,
                detail="You cannot access another user's order"
            )

        return order

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Failed to fetch order"
        )


@router.get("/users/{user_id}/orders")
def get_user_orders(user_id: int, current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        if user_id != current_user.id:
            raise HTTPException(
                status_code=403,
                detail="You cannot access another user's orders"
            )

        return order_service.get_user_orders(db, user_id)

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Failed to fetch user orders"
        )


@router.put("/orders/{order_id}")
@get_current_user_id
def update_order(
    request: Request,
    order_id: int,
    order_data: OrderUpdate,
    user_id: int,
    db: Session = Depends(get_db)
):
    try:
        order = order_service.get_order(db, order_id)

        if order is None:
            raise HTTPException(
                status_code=404,
                detail="Order not found"
            )

        if order.user_id != user_id:
            raise HTTPException(
                status_code=403,
                detail="You cannot update another user's order"
            )

        if order_data.user_id != user_id:
            raise HTTPException(
                status_code=403,
                detail="You cannot assign another user to this order"
            )

        return order_service.update_order(db, order_id, order_data)

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Failed to update order"
        )


@router.patch("/orders/{order_id}")
@get_current_user_id
def patch_order(
    request: Request,
    order_id: int,
    order_data: OrderPatch,
    user_id: int,
    db: Session = Depends(get_db)
):
    try:
        order = order_service.get_order(db, order_id)

        if order is None:
            raise HTTPException(
                status_code=404,
                detail="Order not found"
            )

        if order.user_id != user_id:
            raise HTTPException(
                status_code=403,
                detail="You cannot update another user's order"
            )

        if order_data.user_id is not None and order_data.user_id != user_id:
            raise HTTPException(
                status_code=403,
                detail="You cannot assign another user to this order"
            )

        return order_service.patch_order(db, order_id, order_data)

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Failed to update order"
        )


@router.delete("/orders/{order_id}")
@get_current_user_id
def delete_order(
    request: Request,
    order_id: int,
    user_id: int,
    db: Session = Depends(get_db)
):
    try:
        order = order_service.get_order(db, order_id)

        if order is None:
            raise HTTPException(
                status_code=404,
                detail="Order not found"
            )

        if order.user_id != user_id:
            raise HTTPException(
                status_code=403,
                detail="You cannot delete another user's order"
            )

        result = order_service.delete_order(db, order_id)

        if result is None:
            raise HTTPException(
                status_code=404,
                detail="Order not found"
            )

        return {
            "message": "Order deleted successfully"
        }

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Failed to delete order"
        )