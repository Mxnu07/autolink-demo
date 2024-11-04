from app.routers.client_crud import router as client_router
from app.routers.user_crud import router as user_router
from app.routers.health import router as health_router
from app.routers.queue import router as queue_router
from app.routers.create_client_vehicle import router as create_client_vehicle_router
from app.routers.auth import router as auth_router



def add_routers(app):
    app.include_router(health_router, prefix="/health", tags=["Health"])
    app.include_router(client_router, prefix="/client", tags=["Clients"])
    app.include_router(user_router, prefix="/user", tags=["Users"])
    app.include_router(queue_router, prefix="/queue", tags=["Queue"])
    app.include_router(create_client_vehicle_router, prefix="/create", tags=["Create"])
    app.include_router(auth_router, prefix="/auth", tags=["Auth"])