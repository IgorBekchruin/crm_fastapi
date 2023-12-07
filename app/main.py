from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from sqladmin import Admin

from app.clients.admin import ClientAdmin
from app.clients.routers import router as client_router
from app.config import settings
from app.database import engine
from app.orders.admin import OrderAdmin
from app.orders.routers import router as order_router
from app.pages.router import router as pages_router
from app.users.admin import RoleAdmin, UserAdmin
from app.users.auth import router as auth_router

app = FastAPI(title="CRM App")

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(auth_router)
app.include_router(client_router)
app.include_router(order_router)
app.include_router(pages_router)

admin = Admin(app, engine)

admin.add_view(UserAdmin)
admin.add_view(RoleAdmin)
admin.add_view(OrderAdmin)
admin.add_view(ClientAdmin)

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers",
                   "Access-Control-Allow-Origin", "Authorization"],
)



@app.on_event("startup")
async def startup():
    redis = aioredis.from_url(f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}")
    FastAPICache.init(RedisBackend(redis), prefix="cache")
