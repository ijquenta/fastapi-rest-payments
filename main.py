from fastapi import FastAPI
from models import Customer, CustomerCreate, Transaction, Invoice
from db import SessionDep

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

current_id: int = 0

db_customers: list[Customer] = []

@app.post("/customers", response_model=Customer)
async def create_customer(customer: CustomerCreate, session: SessionDep):
    customer_result = Customer.model_validate(customer.model_dump())
    # Asumiendo que sea en la base de datos
    customer_result.id = len(db_customers)
    db_customers.append(customer_result)
    return customer_result

@app.get("/customers", response_model=list[Customer])
async def get_customers():
    return db_customers

@app.post("/transactions")
async def create_transaction(transaction: Transaction):
    return transaction

@app.post("/invoices")
async def create_invoice(invoice: Invoice):
    return invoice