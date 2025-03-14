from fastapi import FastAPI
from models import Customer, CustomerCreate, Transaction, Invoice
from db import SessionDep, create_all_tables
from sqlmodel import select
import uuid
from fastapi import HTTPException, status

app = FastAPI(lifespan=create_all_tables)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/customers", response_model=Customer)
async def create_customer(customer: CustomerCreate, session: SessionDep):
    customer_result = Customer.model_validate(customer.model_dump())
    customer_result.id = uuid.uuid4()
    session.add(customer_result)
    session.commit()
    session.refresh(customer_result)
    return customer_result

@app.get("/customers/{customer_id}", response_model=Customer)
async def read_customer(customer_id: uuid.UUID, session: SessionDep):
    customer_db = session.get(Customer, customer_id)
    if not customer_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    return customer_db

@app.delete("/customers/{customer_id}")
async def delete_customer(customer_id: uuid.UUID, session: SessionDep):
    customer_db = session.get(Customer, customer_id)
    if not customer_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    session.delete(customer_db)
    session.commit()
    return {"detail": "ok"}

@app.get("/customers", response_model=list[Customer])
async def get_customers(session: SessionDep):
    return session.exec(select(Customer)).all()

@app.post("/transactions")
async def create_transaction(transaction: Transaction):
    return transaction

@app.post("/invoices")
async def create_invoice(invoice: Invoice):
    return invoice