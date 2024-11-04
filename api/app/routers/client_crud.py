from app.models.client_operations import create_client, read_client, update_client, delete_client, get_clients_data
from fastapi import APIRouter, HTTPException
from uuid import UUID
from typing import List, Dict
from app.services.postgre_connector import connect_to_database
from app.models.classes.client_class import ClientInfo, ClientData, ClientResponse


router = APIRouter()

@router.post("/")
async def create_client_endpoint(client_data: ClientData) -> dict:
    create_client(client_data)
    return {"message": "Client created successfully"}

@router.get("/")
async def read_client_endpoint(client_id: UUID = None, first_name: str = None, last_name: str = None, email: str = None, phone: str = None) -> List[ClientResponse]:
    return read_client(client_id=client_id, first_name=first_name, last_name=last_name, email=email, phone=phone)

@router.put("/{client_id}")
async def update_clients_endpoint(client_id: UUID = None, first_name: str = None, last_name: str = None, email: str = None, phone: str = None, client_data: ClientData = None) -> dict:
    # Ensure that the client ID provided in the path matches the client ID in the request body
    if client_id != client_data.client_id:
        raise HTTPException(status_code=400, detail="Client ID in path does not match client ID in request body")
    # Update the client
    update_client(client_id, client_data)
    return {"message": "Client updated successfully"}

@router.delete("/{client_id}")
async def delete_client_endpoint(client_id: UUID = None, first_name: str = None, last_name: str = None, email: str = None, phone: str = None, client_data: ClientData = None) -> dict:
    delete_client(client_id)
    return {"message": "Client deleted successfully"}

@router.get("/dashboard-data")
async def get_dashboard_data_endpoint() -> List[Dict[str, str]]:
    data = get_clients_data()
    if data:
        return data
    else:
        raise HTTPException(status_code=500, detail="Error retrieving data")

@router.get("/clients", response_model=List[ClientInfo])
async def get_clients():
    conn = connect_to_database()
    try:
        cur = conn.cursor()
        query = """
            SELECT c.first_name, v.model, v.license_plate, c.client_id
            FROM autolink.clients AS c
            JOIN autolink.vehicles AS v ON c.client_id = v.client_id
            """
        cur.execute(query)
        rows = cur.fetchall()
        clients = [
            ClientInfo(first_name=row[0], model=row[1], license_plate=row[2])
            for row in rows
        ]
        return clients
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cur.close()
        conn.close()