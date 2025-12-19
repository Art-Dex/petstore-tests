from pydantic import BaseModel
from typing import Optional


class User(BaseModel):
    id: Optional[int] = None
    username: Optional[str]
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    phone: Optional[str] = None
    userStatus: Optional[int] = None
