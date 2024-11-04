from fastapi import HTTPException
from app.services import postgre_connector
from uuid import UUID
from .classes.vehicle_class import VehicleData

def create_vehicle(vehicle_data):
    conn = postgre_connector.connect_to_database()
    try:
        cur = conn.cursor()
        query = """
            INSERT INTO autolink.vehicles (vehicle_id, client_id, license_plate, make, mileage, model, year)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cur.execute(query, (
            vehicle_data.vehicle_id,
            str(vehicle_data.client_id),
            vehicle_data.license_plate,
            vehicle_data.make,
            vehicle_data.mileage,
            vehicle_data.model,
            vehicle_data.year
        ))
        conn.commit()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cur.close()
        conn.close()

def read_vehicle(vehicle_id):
    conn = postgre_connector.connect_to_database()
    try:
        cur = conn.cursor()
        query = "SELECT * FROM vehicles WHERE vehicle_id = %s"
        cur.execute(query, (vehicle_id,))
        vehicle = cur.fetchone()
        if vehicle is None:
            raise HTTPException(status_code=404, detail="Vehicle not found")
        return VehicleData(
            id=vehicle[0],
            client_id=UUID(vehicle[1]),
            license_plate=vehicle[2],
            make=vehicle[3],
            mileage=vehicle[4],
            model=vehicle[5],
            year=vehicle[6]
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cur.close()
        conn.close()

def update_vehicle(vehicle_id, vehicle_data):
    conn = postgre_connector.connect_to_database()
    try:
        cur = conn.cursor()
        query = """
            UPDATE vehicles
            SET client_id = %s, license_plate = %s, make = %s, mileage = %s, model = %s, year = %s
            WHERE vehicle_id = %s
        """
        cur.execute(query, (
            str(vehicle_data.client_id),
            vehicle_data.license_plate,
            vehicle_data.make,
            vehicle_data.mileage,
            vehicle_data.model,
            vehicle_data.year,
            vehicle_id
        ))
        conn.commit()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cur.close()
        conn.close()

def delete_vehicle(vehicle_id):
    conn = postgre_connector.connect_to_database()
    try:
        cur = conn.cursor()
        query = "DELETE FROM vehicles WHERE vehicle_id = %s"
        cur.execute(query, (vehicle_id,))
        conn.commit()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cur.close()
        conn.close()
