from datetime import date
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import extract, func
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db

router = APIRouter(prefix="/api/expenses", tags=["expenses"])


@router.get("", response_model=list[schemas.Expense])
def list_expenses(
    month: int | None = Query(None, ge=1, le=12),
    year: int | None = Query(None, ge=2000, le=2100),
    category_id: UUID | None = None,
    db: Session = Depends(get_db),
):
    q = db.query(models.Expense)
    if month:
        q = q.filter(extract("month", models.Expense.spent_on) == month)
    if year:
        q = q.filter(extract("year", models.Expense.spent_on) == year)
    if category_id:
        q = q.filter(models.Expense.category_id == category_id)
    return q.order_by(models.Expense.spent_on.desc()).all()


@router.post("", response_model=schemas.Expense, status_code=201)
def create_expense(payload: schemas.ExpenseCreate, db: Session = Depends(get_db)):
    category = db.query(models.Category).get(payload.category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    expense = models.Expense(**payload.model_dump())
    db.add(expense)
    db.commit()
    db.refresh(expense)
    return expense


@router.patch("/{expense_id}", response_model=schemas.Expense)
def update_expense(expense_id: UUID, payload: schemas.ExpenseUpdate, db: Session = Depends(get_db)):
    expense = db.query(models.Expense).get(expense_id)
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(expense, field, value)
    db.commit()
    db.refresh(expense)
    return expense


@router.delete("/{expense_id}", status_code=204)
def delete_expense(expense_id: UUID, db: Session = Depends(get_db)):
    expense = db.query(models.Expense).get(expense_id)
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    db.delete(expense)
    db.commit()


@router.get("/summary/monthly", response_model=schemas.MonthlySummary)
def monthly_summary(
    month: int = Query(..., ge=1, le=12),
    year: int = Query(..., ge=2000, le=2100),
    db: Session = Depends(get_db),
):
    rows = (
        db.query(
            models.Category.id,
            models.Category.name,
            models.Category.color,
            models.Category.monthly_budget,
            func.coalesce(func.sum(models.Expense.amount), 0).label("total"),
        )
        .outerjoin(
            models.Expense,
            (models.Expense.category_id == models.Category.id)
            & (extract("month", models.Expense.spent_on) == month)
            & (extract("year", models.Expense.spent_on) == year),
        )
        .group_by(models.Category.id)
        .order_by(models.Category.name)
        .all()
    )

    by_category = [
        schemas.CategorySummary(
            category_id=r.id,
            category_name=r.name,
            color=r.color,
            total_spent=r.total,
            monthly_budget=r.monthly_budget,
        )
        for r in rows
    ]
    total_spent = sum((c.total_spent for c in by_category), start=0)

    return schemas.MonthlySummary(
        month=f"{year}-{month:02d}",
        total_spent=total_spent,
        by_category=by_category,
    )
