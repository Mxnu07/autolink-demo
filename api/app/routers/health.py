from fastapi import APIRouter
from app.services import postgre_connector as pg_conn
from app.settings.logger import get_logger

logger = get_logger()
router = APIRouter()


@router.get("/")
def health():
    conn = pg_conn.connect_to_database()
    db_status = False

    if conn:
        db_status = True
    return {"API": "ok",
            "db_status": "ok" if db_status else "error"}
