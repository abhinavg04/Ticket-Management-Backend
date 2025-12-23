from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.user import router as user_router
from api.ticket import router as ticket_router
from api.dashboard import router as dashboard_router
from core.config import settings

app = FastAPI()
app.include_router(user_router)
app.include_router(ticket_router)
app.include_router(dashboard_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
async def root():
    return {'hello':"world"}