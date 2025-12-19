from typing import List, Optional
from pydantic import BaseModel, RootModel
from enum import Enum


class PetStatus(str, Enum):
    available = "available"
    pending = "pending"
    sold = "sold"


class Category(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None


class Tag(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None


class Pet(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    category: Optional[Category] = None
    photoUrls: List[str]
    tags: Optional[List[Tag]] = None
    status: Optional[PetStatus] = None


class PetsList(RootModel[List[Pet]]):
    pass


class FieldPetStatus(BaseModel):
    code: int = 400
    message: str

    @classmethod
    def from_invalid_status(cls, status: str):
        return cls(
            message=(
                f"Input error: query parameter `status value `{status}` is not in the allowable "
                f"values `[available, pending, sold]`"
            )
        )
