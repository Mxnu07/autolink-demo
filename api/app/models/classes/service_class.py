from pydantic import BaseModel
from datetime import timedelta


class ServiceData(BaseModel):
    service_id: int
    service_name: str
    service_description: str
    service_duration: timedelta
    service_price: float
