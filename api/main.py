"""
Main module of the application file
"""

import os
from datetime import datetime
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import add_routers
from app.settings.application import get_settings
from app.settings.logger import init_logger
from fastapi.staticfiles import StaticFiles
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import HTMLResponse


settings = get_settings()

init_logger(settings.log_level)


app = FastAPI(
    title="AutoLink",
    description=f"<b>Environment:</b> {settings.environment_name}<br><b>Version:</b> {settings.app_version}<br><b>Release Date:</b> {settings.app_release_date}<br><b>Starting Date:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
    openapi_url="/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
    version=settings.app_version,
)

if settings.environment_name == "local":
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Montar el directorio estático para servir archivos CSS, JS y de imagen
app.mount("/static", StaticFiles(directory="static"), name="static")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, "static")

@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open(os.path.join(TEMPLATE_DIR, "html/landing.html"), "r") as f:
        return HTMLResponse(content=f.read(), status_code=200)

@app.get("/login", response_class=HTMLResponse)
async def get_login():
    with open(os.path.join(TEMPLATE_DIR, "html/login.html"), "r") as f:
        return HTMLResponse(content=f.read(), status_code=200)

@app.get("/create_user", response_class=HTMLResponse)
async def get_login():
    with open(os.path.join(TEMPLATE_DIR, "html/create_agent.html"), "r") as f:
        return HTMLResponse(content=f.read(), status_code=200)

@app.get("/home", response_class=HTMLResponse)
async def get_index():
    with open(os.path.join(TEMPLATE_DIR, "html/index.html"), "r") as f:
        return HTMLResponse(content=f.read(), status_code=200)

@app.get("/queue", response_class=HTMLResponse)
async def get_index():
    with open(os.path.join(TEMPLATE_DIR, "html/dashboard.html"), "r") as f:
        return HTMLResponse(content=f.read(), status_code=200)

@app.get("/create-client", response_class=HTMLResponse)
async def get_index():
    with open(os.path.join(TEMPLATE_DIR, "html/create_client.html"), "r") as f:
        return HTMLResponse(content=f.read(), status_code=200)

@app.get("/interface", response_class=HTMLResponse)
async def get_index():
    with open(os.path.join(TEMPLATE_DIR, "html/interface.html"), "r") as f:
        return HTMLResponse(content=f.read(), status_code=200)

@app.get("/clients", response_class=HTMLResponse)
async def get_index():
    with open(os.path.join(TEMPLATE_DIR, "html/clients.html"), "r") as f:
        return HTMLResponse(content=f.read(), status_code=200)

@app.get("/contact", response_class=HTMLResponse)
async def read_root():
    with open(os.path.join(TEMPLATE_DIR, "html/contact.html"), "r") as f:
        return HTMLResponse(content=f.read(), status_code=200)

@app.get("/about", response_class=HTMLResponse)
async def read_root():
    with open(os.path.join(TEMPLATE_DIR, "html/about.html"), "r") as f:
        return HTMLResponse(content=f.read(), status_code=200)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

add_routers(app)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("API_PORT", "8080")))
