import logging
from collections.abc import Sequence
from uuid import UUID

from sqlmodel import Session, select

from ..models.plan import Plan
from ..schemas.plan import PlanCreate, PlanRead, PlanBookmark

def get_plans(user_id: UUID, session: Session) -> Sequence[PlanRead]:
    statement = select(Plan).where(Plan.user_id == user_id)

    plans = session.exec(statement).all()
    return [PlanRead.model_validate(plan) for plan in plans]


def write_plan(user_id: UUID, plan_data: PlanCreate, session: Session) -> PlanRead:
    plan_dict = plan_data.model_dump()  # Convert PlanCreate to a dictionary
    plan_dict["user_id"] = user_id
    created_plan = Plan(**plan_dict)
    session.add(created_plan)
    session.commit()
    session.refresh(created_plan)
    return PlanRead.model_validate(created_plan)


def delete_plan(user_id: UUID, plan_id: UUID, session: Session) -> None:
    plan = session.get(Plan, plan_id)
    if not plan or plan.user_id != user_id:
        error_msg = "Plan not found or access denied"
        raise ValueError(error_msg)
    session.delete(plan)
    session.commit()

def bookmark_plan(user_id: UUID, plan_id: UUID, session: Session) -> PlanBookmark:
    plan = session.get(Plan, plan_id)
    if not plan or plan.user_id != user_id:
        error_msg = "Plan not found or access denied"
        raise ValueError(error_msg)

    plan.bookmark = not plan.bookmark
    session.add(plan)
    session.commit()
    session.refresh(plan)
    return PlanBookmark.model_validate(plan)

