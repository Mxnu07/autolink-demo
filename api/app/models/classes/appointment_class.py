from pydantic import BaseModel
from datetime import datetime, date
from uuid import UUID

class AppointmentData(BaseModel):
    appointment_id: int
    client_id: UUID
    vehicle_id: UUID
    appointment_time: datetime