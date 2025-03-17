from pydantic import BaseModel
from sqlmodel import SQLModel, Field, Relationship
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
    transactions: list["Transaction"] = Relationship(back_populates="customer")

class TransactionBase(SQLModel):
    ammount: int
    description: str

class Transaction(TransactionBase, table=True):
    id: uuid.UUID | None = Field(default_factory=uuid.uuid4, primary_key=True)
    customer_id: uuid.UUID = Field(default=None, foreign_key="customer.id")
    customer: Customer = Relationship(back_populates="transactions")

class TransactionCreate(TransactionBase):
    customer_id: uuid.UUID = Field(default=None, foreign_key="customer.id")
class Invoice(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    customer: Customer
    transactions: list[Transaction]
    total: int

    @property
    def amount_total(self):
        return sum(transaction.amount for transaction in self.transactions)