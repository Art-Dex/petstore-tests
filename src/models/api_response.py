from pydantic import BaseModel
from typing import Optional


class ApiResponse(BaseModel):
    code: Optional[int] = None
    type: Optional[str] = None
    message: Optional[str] = None
