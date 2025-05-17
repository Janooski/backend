from collections.abc import Sequence
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlmodel import Session

from ..database import get_session
from ..middlewares.auth_middleware import auth_dependency
from ..schemas.plan import PlanCreate, PlanRead
from ..services import plan_service

router = APIRouter()


@router.get("/plans", dependencies=[Depends(auth_dependency)])
async def get_plans(
    request: Request, session: Annotated[Session, Depends(get_session)]
) -> dict[str, Sequence[PlanRead]]:
    try:
        plans = plan_service.get_plans(request.state.user.id, session)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to delete plan. Please report to page-admin") from e
    return {"plans": plans}


@router.post("/plans", dependencies=[Depends(auth_dependency)], status_code=201)
async def create_plan(
    request: Request, plan_data: PlanCreate, session: Annotated[Session, Depends(get_session)]
) -> PlanRead:
    try:
        created_plan = plan_service.write_plan(request.state.user.id, plan_data, session)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to create plan. Please report to page-admin") from e
    return created_plan


@router.delete("/plans/{plan_id}", dependencies=[Depends(auth_dependency)], status_code=204)
async def delete_plan(request: Request, plan_id: UUID, session: Annotated[Session, Depends(get_session)]) -> None:
    try:
        plan_service.delete_plan(request.state.user.id, plan_id, session)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to delete plan. Please report to page-admin") from e
