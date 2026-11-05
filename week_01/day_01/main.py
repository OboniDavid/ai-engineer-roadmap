from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

class Expense(BaseModel):
    title: str
    amount: float
    category: str

expenses_db = []

@app.get("/")
def read_root():
    return {"message": "Welcome to your AI Engineer Expense Tracker API!"}

@app.post("/expenses/", response_model=Expense)
def create_expense(expense: Expense):
    expenses_db.append(expense)
    return expense

@app.get("/expenses/", response_model=List[Expense])
def get_expenses():
    return expenses_db