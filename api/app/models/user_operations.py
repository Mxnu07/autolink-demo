#!/usr/bin/env python3
from psycopg2 import sql
from passlib.context import CryptContext
from typing import Optional
from app.services.postgre_connector import connect_to_database, close_connection, create_cursor
from fastapi import HTTPException
from datetime import datetime, timedelta
from jose import jwt
from app.models.auth_operaations import SECRET_KEY, ALGORITHM

# Contexto de hash de contraseña
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Función para obtener el hash de una contraseña
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# Función para verificar una contraseña
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# Función para crear un usuario
def create_user(username: str, email: str, password: str) -> Optional[int]:
    conn = connect_to_database()
    try:
        cur = conn.cursor()
        hashed_password = get_password_hash(password)
        insert_user_query = '''
<<<<<<< HEAD
<<<<<<< HEAD
        INSERT INTO autolink.users (users_id, username, email, hashed_password)
        VALUES (%s, %s, %s, %s);
=======
        INSERT INTO users (username, email, hashed_password)
        VALUES (%s, %s, %s) RETURNING id;
>>>>>>> main
=======
        INSERT INTO autolink.users (users_id, username, email, hashed_password)
        VALUES (%s, %s, %s, %s);
>>>>>>> main
        '''
        cur.execute(insert_user_query, (username, email, hashed_password))
        conn.commit()
        user_id = cur.fetchone()[0]
        return user_id
    except Exception as e:
        print("Error al crear usuario:", e)
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        if cur:
            cur.close()
        if conn:
            close_connection(conn)

def verify_user(username: str, password: str) -> Optional[dict]:
    conn = connect_to_database()
    try:
        cur = create_cursor(conn)
        select_user_query = sql.SQL('''
        SELECT id, username, email, hashed_password, role FROM users WHERE username = %s;
        ''')
        cur.execute(select_user_query, (username,))
        user = cur.fetchone()
        if user and verify_password(password, user[3]):
            return {"id": user[0], "username": user[1], "email": user[2], "role": user[4]}
        return None
    except Exception as e:
        print("Error verifying user:", e)
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        if cur:
            cur.close()
        if conn:
            close_connection(conn)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt