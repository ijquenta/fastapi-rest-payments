from fastapi import APIRouter, status, HTTPException
import uuid

from sqlmodel import select

from models import Customer, CustomerCreate, CustomerUpdate, Plan, CustomerPlan
from db import SessionDep

router = APIRouter(tags=['customers'])

@router.post("/customers", response_model=Customer)
async def create_customer(customer: CustomerCreate, session: SessionDep):
    customer_result = Customer.model_validate(customer.model_dump())
    customer_result.id = uuid.uuid4()
    session.add(customer_result)
    session.commit()
    session.refresh(customer_result)
    return customer_result

@router.get("/customers/{customer_id}", response_model=Customer)
async def read_customer(customer_id: uuid.UUID, session: SessionDep):
    customer_db = session.get(Customer, customer_id)
    if not customer_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    return customer_db

@router.patch("/customers/{customer_id}", response_model=Customer, status_code=status.HTTP_201_CREATED)
async def update_customer(customer_id: uuid.UUID, customer_data: CustomerUpdate , session: SessionDep):
    customer_db = session.get(Customer, customer_id)
    if not customer_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    customer_data_dict = customer_data.model_dump(exclude_unset=True)
    customer_db.sqlmodel_update(customer_data_dict)
    session.add(customer_db)
    session.commit()
    session.refresh(customer_db)
    return customer_db

@router.delete("/customers/{customer_id}")
async def delete_customer(customer_id: uuid.UUID, session: SessionDep):
    customer_db = session.get(Customer, customer_id)
    if not customer_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    session.delete(customer_db)
    session.commit()
    return {"detail": "ok"}

@router.get("/customers", response_model=list[Customer])
async def get_customers(session: SessionDep):
    return session.exec(select(Customer)).all()

@router.get("/customers/{customer_id}/plans/{plan_id}")
async def subscribe_customer_to_plan(customer_id: uuid.UUID, plan_id: uuid.UUID, session: SessionDep):
    customer_db = session.get(Customer, customer_id)
    plan_db = session.get(Plan, plan_id)

    if not customer_db or not plan_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The customer or plan doesn't exist"
        )

    customer_plan_db = CustomerPlan(plan_id=plan_db.id, customer_id=customer_db.id)
    session.add(customer_plan_db)
    session.commit()
    session.refresh(customer_plan_db)
    return customer_plan_db

@router.get("/customers/{customer_id}/plans")
async def subscribe_customer_to_plan(customer_id: uuid.UUID, session: SessionDep):
    customer_db = session.get(Customer, customer_id)

    if not customer_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
        )

    return customer_db.plans