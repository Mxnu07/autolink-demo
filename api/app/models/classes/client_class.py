from datetime import date, datetime
from pydantic import BaseModel
from typing import Optional
from uuid import UUID


class ClientData(BaseModel):
    client_id: UUID
    first_name: str
    last_name: str
    email: str
    phone: str

class ClientResponse(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone: str

class ClientInfo(BaseModel):
    first_name: str
    model: str
    license_plate: str
    client_id: Optional[str] = None
