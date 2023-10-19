from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from sqladmin import Admin
from app.clients.admin import ClientAdmin
from app.orders.admin import OrderAdmin
from app.users.admin import RoleAdmin, UserAdmin
from app.clients.routers import router as client_router
from app.orders.routers import router as order_router
from app.pages.router import router as pages_router
from app.users.auth import router as auth_router
from app.database import engine

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache

from redis import asyncio as aioredis


app = FastAPI(
    title="CRM App"
)

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


@app.on_event("startup")
async def startup():
    redis = aioredis.from_url("redis://localhost:6379")
    FastAPICache.init(RedisBackend(redis), prefix="cache")