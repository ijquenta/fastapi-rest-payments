from fastapi import FastAPI
from models import Customer, CustomerCreate, Transaction, Invoice
from db import SessionDep, create_all_tables
from sqlmodel import select
import uuid

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

@app.get("/customers", response_model=list[Customer])
async def get_customers(session: SessionDep):
    return session.exec(select(Customer)).all()

@app.post("/transactions")
async def create_transaction(transaction: Transaction):
    return transaction

@app.post("/invoices")
async def create_invoice(invoice: Invoice):
    return invoice