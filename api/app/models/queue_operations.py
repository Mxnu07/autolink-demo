from fastapi import HTTPException
from pydantic import BaseModel


class QueueItem(BaseModel):
    name: str
    model: str
    license_plate: str
    service: str = ""
    start_time: float = 0.0
    duration: int = 0
    status: str = "Pending"  # Add status field

queue = []
ongoing_services = []
completed_services_count = 0  # To keep track of the number of completed services


def get_queue():
    return {"queue": queue, "ongoingServices": ongoing_services}


def add_to_queue(item: QueueItem):
    queue.append(item.model_dump())
    return {"message": "Client added to queue"}


def start_service(item: QueueItem):
    item_dict = item.model_dump()
    if item_dict in queue:
        ongoing_services.append(item_dict)
        queue.remove(item_dict)
        return {"message": "Service started"}
    raise HTTPException(status_code=404, detail="Client not found in queue")


def update_service(item: QueueItem):
    for service in ongoing_services:
        if service['name'] == item.name and service['license_plate'] == item.license_plate:
            service.update(item.model_dump())
            return {"message": "Service updated"}
    raise HTTPException(status_code=404, detail="Service not found")


def delete_from_queue(name: str):
    global queue, ongoing_services, completed_services_count
    queue = [item for item in queue if item['name'] != name]
    ongoing_services = [item for item in ongoing_services if item['name'] != name]
    completed_services_count += 1
    return {"message": f"Client {name} removed from queue"}


def get_stats():
    return {"queue_count": len(queue), "visits_count": completed_services_count}


def reset_visits_count():
    global completed_services_count
    completed_services_count = 0
    return {"message": "Visits count reset to 0"}

