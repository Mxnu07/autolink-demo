from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.models.client_operations import create_client
from app.models.vehicle_operations import create_vehicle
from app.models.classes.client_class import ClientData
from app.models.classes.vehicle_class import VehicleData
from app.models.queue_operations import QueueItem, queue

router = APIRouter()

class ClientAndVehicleData(BaseModel):
    client_data: ClientData
    vehicle_data: VehicleData

@router.post("/create-client")
async def create_client_and_vehicle(data: ClientAndVehicleData):
    try:
        create_client(data.client_data)
        create_vehicle(data.vehicle_data)
        # Add the new client to the queue
        queue_item = QueueItem(
            name=data.client_data.first_name,
            model=data.vehicle_data.model,
            license_plate=data.vehicle_data.license_plate
        )
        queue.append(queue_item.model_dump())  # Add directly to the queue
        return {"message": "Client and vehicle created successfully",
                "client_id": data.client_data.client_id,
                "vehicle_id": data.vehicle_data.vehicle_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

