from collections.abc import Sequence
from uuid import UUID

from sqlmodel import Session, select

from ..models.plan import Plan
from ..schemas.plan import PlanCreate


def get_plans(plan_id: UUID, session: Session) -> Sequence[Plan]:
    statement = select(Plan).where(Plan.user_id == plan_id)

    return session.exec(statement).all()


def write_plan(user_id: UUID, plan_data: PlanCreate, session: Session) -> Plan:
    plan_dict = plan_data.model_dump()  # Convert PlanCreate to a dictionary
    plan_dict["user_id"] = user_id
    plan = Plan(**plan_dict)
    session.add(plan)
    session.commit()
    session.refresh(plan)
    return plan


def delete_plan(user_id: UUID, plan_id: UUID, session: Session) -> None:
    plan = session.get(Plan, plan_id)
    if not plan or plan.user_id != user_id:
        raise ValueError("Plan not found or access denied")
    session.delete(plan)
    session.commit()
