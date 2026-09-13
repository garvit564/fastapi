from fastapi import APIRouter, HTTPException,Depends

from database import SessionLocal

from schemas.orders import (
    OrderCreate,
    OrderUpdate,
    OrderPatch
)
from auth.security import get_current_user
from services.order_services import order_service


router = APIRouter()


@router.post("/orders")
def create_order(order_data: OrderCreate,current_user = Depends(get_current_user)):

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
def get_order(order_id: int,current_user = Depends(get_current_user)):

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

        if order.user_id != current_user.id:
            raise HTTPException(
                status_code=403,
                detail= "you cannot access another's order"
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
def get_user_orders(user_id: int,current_user = Depends(get_current_user)):

    db = SessionLocal()

    try:
        if user_id != current_user.id:
            raise HTTPException(
                status_code=403,
                detail="you can not acsess other's order"
            )

        return order_service.get_user_orders(
            db,
            user_id
        )

    except HTTPException:
        raise

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
    order_data: OrderUpdate,
    current_user = Depends(get_current_user)
):

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

        if order.user_id != current_user.id:
            raise HTTPException(
                status_code=403,
                detail="you cannot update other's order"
            )

        updated_order = order_service.update_order(db,order_id,order_data)

        return updated_order

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
    order_data: OrderPatch,
    current_user = Depends(get_current_user)
):

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
        if order.user_id != current_user.id:
            raise HTTPException(
                status_code=403,
                detail="you cannot update another's order"
            )

        updated_order = order_service.patch_order(db,order_id,order_data)


        return updated_order

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
def delete_order(order_id: int,current_user = Depends(get_current_user)):

    db = SessionLocal()

    try:
        order = order_service.get_order(db,order_id)

        if order is None:
            raise HTTPException(
                status_code=404,
                detail="order not found"
            )

        if order.user_id != current_user.id:
            raise HTTPException(
                status_code=403,
                detail="you cannot delete another'ss order"
            )
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