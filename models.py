from pydantic import BaseModel
from sqlmodel import SQLModel, Field
import uuid

class CustomerBase(SQLModel):
    name: str = Field(default=None)
    description: str | None = Field(default=None)
    email: str = Field(default=None)
    age: int = Field(default=None)

class CustomerCreate(CustomerBase):
    pass

class CustomerUpdate(CustomerBase):
    pass

class Customer(CustomerBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)


class Transaction(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    ammount: int
    description: str


class Invoice(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    customer: Customer
    transactions: list[Transaction]
    total: int

    @property
    def amount_total(self):
        return sum(transaction.amount for transaction in self.transactions)