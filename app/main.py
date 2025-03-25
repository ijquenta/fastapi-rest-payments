from fastapi import FastAPI
from models import Transaction, Invoice
from db import create_all_tables
from .routers import customers, transactions, plans

app = FastAPI(lifespan=create_all_tables)
app.include_router(customers.router)
app.include_router(transactions.router)
app.include_router(plans.router)

@app.get("/")
async def root():
    return {"message": "Api Rest payments"}

@app.post("/invoices")
async def create_invoice(invoice: Invoice):
    return invoice