from fastapi import FastAPI
from models import Transaction, Invoice
from db import create_all_tables
from .routers import customers

app = FastAPI(lifespan=create_all_tables)
app.include_router(customers.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}



@app.post("/transactions")
async def create_transaction(transaction: Transaction):
    return transaction

@app.post("/invoices")
async def create_invoice(invoice: Invoice):
    return invoice