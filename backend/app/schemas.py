from datetime import date, datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class CategoryBase(BaseModel):
    name: str = Field(..., max_length=64)
    color: str = Field(default="#6366f1", max_length=7)
    monthly_budget: Optional[Decimal] = None


class CategoryCreate(CategoryBase):
    pass


class Category(CategoryBase):
    model_config = ConfigDict(from_attributes=True)
    id: UUID


class ExpenseBase(BaseModel):
    description: str = Field(..., max_length=255)
    amount: Decimal
    spent_on: date
    notes: Optional[str] = None
    category_id: UUID


class ExpenseCreate(ExpenseBase):
    pass


class ExpenseUpdate(BaseModel):
    description: Optional[str] = None
    amount: Optional[Decimal] = None
    spent_on: Optional[date] = None
    notes: Optional[str] = None
    category_id: Optional[UUID] = None


class Expense(ExpenseBase):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    created_at: datetime
    category: Category


class CategorySummary(BaseModel):
    category_id: UUID
    category_name: str
    color: str
    total_spent: Decimal
    monthly_budget: Optional[Decimal] = None


class MonthlySummary(BaseModel):
    month: str
    total_spent: Decimal
    by_category: list[CategorySummary]
