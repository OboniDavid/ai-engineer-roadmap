from fastapi import FastAPI, HTTPException,Query
from pydantic import BaseModel, Field
from typing import List, Optional

app = FastAPI()

class Expense(BaseModel):
    title: str 
    amount: float = Field(..., gt=0, description="The amount of the expense, must be greater than 0")
    category: str

expenses_db = [

    { "id": 1, "title": "Lunch", "amount": 15.0, "category": "Food" },
    { "id": 2, "title": "cloud server", "amount": 20.0, "category": "Infrastructure " },
    { "id": 3, "title": "Notebook", "amount": 3.00, "category": "Supplies" },

]

@app.get("/")
def read_root():
    return {"message": "Welcome to Week 1 day 2: Advanced FastAPI Endpoints!"}

@app.get("/expenses/", response_model=List[dict])
def get_expenses(category: Optional[str] = Query(None, description="Filter expenses by category")):
    if category:
        filtered = [exp for exp in expenses_db if exp["category"].lower() == category.lower()]
        return filtered
    return expenses_db

@app.get("/expenses/{expense_id}", response_model=dict)
def get_expense_by_id(expense_id: int):
    for exp in expenses_db:
        if exp["id"] == expense_id:
            return exp
    raise HTTPException(status_code=404, detail="Expense not found")

@app.post("/expenses/", response_model=dict)
def create_expense(expense: Expense):
    new_id = len(expenses_db) + 1
    new_expense = {"id": new_id, "title": expense.title, "amount": expense.amount, "category": expense.category}
    expenses_db.append(new_expense)
    return new_expense