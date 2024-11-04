from pydantic import BaseModel
from datetime import datetime
from uuid import UUID

class AgentData(BaseModel):
    agent_id: UUID
    updated_at: datetime
    first_name: str
    last_name: str
    username: str
    hashed_password: str
    email: str