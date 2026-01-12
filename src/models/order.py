from pydantic import BaseModel, RootModel
from typing import Optional
from datetime import datetime
from enum import Enum
from typing import Dict


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


class InventoryResponse(RootModel[Dict[str, int]]):
    pass
