from fastapi import APIRouter, HTTPException

from tasks.report_task import generate_order_report


router = APIRouter()


@router.post("/orders/{order_id}/report")
def generate_report(order_id: int):

    try:

        task = generate_order_report.delay(order_id)

        return {
            "message": "Report generation started",
            "task_id": task.id
        }

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Failed to start report generation"
        )