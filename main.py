from fastapi import FastAPI

from pydantic import BaseModel

class Customer(BaseModel):
    name: str
    description: str | None
    email: str
    age: int

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/customers")
async def create_customer(customer: Customer):
    return customer