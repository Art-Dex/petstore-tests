from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum


class OrderStatus(str, Enum):
    placed = "placed"
    approved = "approved"
    delivered = "delivered"


class Order(BaseModel):
    id: Optional[int] = None
    petId: Optional[int] = None
    quantity: Optional[int] = None
    shipDate: Optional[datetime] = None
    status: Optional[OrderStatus] = None
    complete: Optional[bool] = None
