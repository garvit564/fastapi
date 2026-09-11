from fastapi import APIRouter, HTTPException

from database import SessionLocal

from schemas.orders import (
    OrderCreate,
    OrderUpdate,
    OrderPatch
)

from services.order_services import order_service


router = APIRouter()


@router.post("/orders")
def create_order(order_data: OrderCreate):

    db = SessionLocal()

    try:
        return order_service.create_order(
            db,
            order_data
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Failed to create order"
        )

    finally:
        db.close()


@router.get("/orders/{order_id}")
def get_order(order_id: int):

    db = SessionLocal()

    try:
        order = order_service.get_order(
            db,
            order_id
        )

        if order is None:
            raise HTTPException(
                status_code=404,
                detail="Order not found"
            )

        return order

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Failed to fetch order"
        )

    finally:
        db.close()


@router.get("/users/{user_id}/orders")
def get_user_orders(user_id: int):

    db = SessionLocal()

    try:
        return order_service.get_user_orders(
            db,
            user_id
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Failed to fetch user orders"
        )

    finally:
        db.close()


@router.put("/orders/{order_id}")
def update_order(
    order_id: int,
    order_data: OrderUpdate
):

    db = SessionLocal()

    try:
        order = order_service.update_order(
            db,
            order_id,
            order_data
        )

        if order is None:
            raise HTTPException(
                status_code=404,
                detail="Order not found"
            )

        return order

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Failed to update order"
        )

    finally:
        db.close()


@router.patch("/orders/{order_id}")
def patch_order(
    order_id: int,
    order_data: OrderPatch
):

    db = SessionLocal()

    try:
        order = order_service.patch_order(
            db,
            order_id,
            order_data
        )

        if order is None:
            raise HTTPException(
                status_code=404,
                detail="Order not found"
            )

        return order

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Failed to update order"
        )

    finally:
        db.close()


@router.delete("/orders/{order_id}")
def delete_order(order_id: int):

    db = SessionLocal()

    try:
        result = order_service.delete_order(
            db,
            order_id
        )

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

    finally:
        db.close()