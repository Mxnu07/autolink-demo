from fastapi import HTTPException
from app.services import postgre_connector
from .classes.client_class import ClientResponse
from typing import List, Dict
import psycopg2

def create_client(client_data):
    conn = postgre_connector.connect_to_database()
    try:
        cur = conn.cursor()
        query = "INSERT INTO autolink.clients (client_id, first_name, last_name, email, phone) VALUES (%s, %s, %s, %s, %s)"
        cur.execute(query, (
            str(client_data.client_id),
            client_data.first_name,
            client_data.last_name,
            client_data.email,
            client_data.phone,
        ))
        conn.commit()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cur.close()
        conn.close()


def read_client(client_id=None, first_name=None, last_name=None, email=None, phone=None):
    # Create a list to store conditions for WHERE clause
    conditions = []
    params = []

    # Check each parameter and add condition to the list if not None
    if client_id:
        conditions.append("id = %s")
        params.append(str(client_id))
    if first_name:
        conditions.append("first_name = %s")
        params.append(first_name)
    if last_name:
        conditions.append("last_name = %s")
        params.append(last_name)
    if email:
        conditions.append("email = %s")
        params.append(email)
    if phone:
        conditions.append("phone = %s")
        params.append(phone)

    # Join conditions with 'AND' and create the WHERE clause
    where_clause = " AND ".join(conditions)

    # Connect to the database
    conn = postgre_connector.connect_to_database()
    try:
        cur = conn.cursor()
        query = "SELECT first_name, last_name, email, phone FROM autolink.clients"
        if where_clause:
            query += " WHERE " + where_clause
        cur.execute(query, tuple(params))
        clients = cur.fetchall()
        if not clients:
            raise HTTPException(status_code=404, detail="Clients not found")
        return [ClientResponse(
            first_name=client[0],
            last_name=client[1],
            email=client[2],
            phone=client[3],
        ) for client in clients]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cur.close()
        conn.close()


def update_client(client_id, client_data):
    conn = postgre_connector.connect_to_database()
    try:
        cur = conn.cursor()
        query = "UPDATE autolink.clients SET first_name = %s, last_name = %s, email = %s, phone = %s WHERE client_id = %s"
        cur.execute(query, (
            client_data.first_name,
            client_data.last_name,
            client_data.email,
            client_data.phone,
            str(client_id)
        ))
        conn.commit()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cur.close()
        conn.close()


def delete_client(client_id):
    conn = postgre_connector.connect_to_database()
    try:
        cur = conn.cursor()
        query = "DELETE FROM autolink.clients WHERE client_id = %s"
        cur.execute(query, (str(client_id),))
        conn.commit()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cur.close()
        conn.close()




def get_clients_data() -> List[Dict[str, str]]:
    conn = postgre_connector.connect_to_database()
    cur = postgre_connector.create_cursor(conn)
    data = []
    if conn is not None and cur is not None:
        try:
            query = '''
            SELECT clients.first_name, vehicles.license_plate, appointments.appt_time
            FROM clients
            JOIN vehicles ON clients.id = vehicles.client_id
            JOIN appointments ON clients.id = appointments.client_id
            '''
            cur.execute(query)
            rows = cur.fetchall()
            data = [{"first_name": row[0], "license_plate": row[1], "date": row[2]} for row in rows]
        except (Exception, psycopg2.Error) as error:
            print("Error retrieving data :", error)
        finally:
            postgre_connector.close_connection(conn)
    return data

