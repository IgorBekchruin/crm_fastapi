from datetime import datetime
from fastapi import APIRouter, Depends, Form, HTTPException, Request, Response, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from app.clients.dao import ClinetDAO

from app.clients.routers import create_client, delete_client, get_all_clients, get_client_by_id, update_client
from app.clients.schemas import ClientSchem, CreateClient, UpdateClient
from app.orders.dao import OrderDAO
from app.orders.routers import create_orders, delete_order, get_all_orders, get_order_by_id, update_order
from app.orders.schemas import OrderSchem, UpdateSchem
from app.users.auth import authenticate_user, get_current_user, pwd_context
from app.users.jwt import create_jwt_token
from app.users.models import User
from app.users.schemas import UserCreate, UserSchem
from app.users.user_dao import UserDAO


router = APIRouter(
    prefix='/pages',
    tags=['Pages']
)

templates = Jinja2Templates(directory='app/templates')


# login page and auth
@router.get('/signin', response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.post('/signin')
async def login_pages(

    username: str = Form(...),
    password: str = Form(...),
):
    user = await UserDAO.find_user(username)  # Получите пользователя из базы данных
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    is_password_correct = pwd_context.verify(password, user.hashed_password)

    if not is_password_correct:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    jwt_token = create_jwt_token({"sub": user.username})
    rr = RedirectResponse('/pages', status_code=303)
    rr.set_cookie(key='access_token', value=f"Bearer {jwt_token}", httponly=True)
    return rr


@router.get("/logout")
def logout_pages(response: Response):
    response = RedirectResponse("/pages/signin", status_code=302)
    response.delete_cookie(key='access_token')
    return response


# router for main page
@router.get('/', response_class=HTMLResponse)
async def get_main_page(
    request: Request,
    current_user: User = Depends(get_current_user)
):
    clients = await ClinetDAO.find_all(10)
    orders = await OrderDAO.find_all(10)
    return templates.TemplateResponse("main.html", {
                                                    "request": request,
                                                    "clients": clients,
                                                    "orders": orders,
                                                    })


# routs for clients
@router.get('/clients', response_class=HTMLResponse)
async def get_clients(
    request: Request,
    current_user: User = Depends(get_current_user)
):
    clients = await ClinetDAO.find_all()
    return templates.TemplateResponse("clients/clients.html", {
                                                    "request": request,
                                                    "clients": clients
                                                    })


@router.get('/clients/{client_id}', response_class=HTMLResponse)
async def get_client_detail(
    request: Request,
    client_id: int
):
    client = await ClinetDAO.find_by_id(client_id)
    return templates.TemplateResponse("clients/clients_detail.html", {
                                                    "request": request,
                                                    "client": client
                                                    })


@router.get('/clients/{client_name}', response_class=HTMLResponse)
async def get_client_detail_by_name(
    request: Request,
    client_name: str
):
    client = await ClinetDAO.find_by_name(client_name)
    return templates.TemplateResponse("clients/clients_detail.html", {
                                                    "request": request,
                                                    "client": client
                                                    })


@router.get("/client_create", response_class=HTMLResponse)
def create_clients_page(
    request: Request,
    current_user: User = Depends(get_current_user)
):
    return templates.TemplateResponse('clients/create_clients.html', {'request': request})


@router.post('/client_create')
async def create_clients(
    request: Request,
    name: str = Form(...),
    price: float = Form(...),
    production: str = Form(...),
    contact: str = Form(...),
    last_contact: datetime = Form(...),
    current_user: User = Depends(get_current_user)

):
    client_data = {
        'name': name,
        'price': price,
        'production': production,
        'contact': contact,
        'last_contact': last_contact,
        'user_id': current_user.id,
        }
    client = CreateClient(**client_data)
    await ClinetDAO.add(client)
    return await get_clients(request)


@router.get("/clients/{client_id}/update", response_class=HTMLResponse)
async def update_clients_page(
    request: Request,
    client_id: int,
    current_user: User = Depends(get_current_user)
):
    client = await ClinetDAO.find_by_id(client_id)
    return templates.TemplateResponse(
        'clients/update_clients.html',
        {
            'request': request,
            'client': client
        }
    )


@router.post("/clients/{client_id}/update")
async def update_clients(
    request: Request,
    client_id: int,
    name: str = Form(...),
    price: float = Form(...),
    production: str = Form(...),
    contact: str = Form(...),
    last_contact: datetime = Form(...),
    current_user: User = Depends(get_current_user)
):
    client_data = {
        'id': client_id,
        'name': name,
        'price': price,
        'production': production,
        'contact': contact,
        'last_contact': last_contact,
        'user_id': current_user.id,
        }
    client = UpdateClient(**client_data)
    await ClinetDAO.update(client_id, client)
    return await get_clients(request)


@router.post('/clients/{client_id}')
async def delete_clients(
    request: Request,
    client_id: int,
    current_user: User = Depends(get_current_user)
):
    await ClinetDAO.delete(client_id)
    return await get_clients(request)


# routs for users
@router.get('/users', response_class=HTMLResponse)
async def get_users(
    request: Request,
    current_user: User = Depends(get_current_user)
):
    users = await UserDAO.find_all()
    return templates.TemplateResponse("users/users.html", {
                                                    "request": request,
                                                    "users": users
                                                    })


@router.get('/users/{user_id}', response_class=HTMLResponse)
async def get_user_detail(
    request: Request,
    current_user: User = Depends(get_current_user)
):
    user_data = await UserDAO.find_by_id(current_user.id)
    return templates.TemplateResponse("clients/clients_detail.html", {
                                                    "request": request,
                                                    "user": user_data
                                                    })


# routs for orders
@router.get('/orders', response_class=HTMLResponse)
async def get_orders(
    request: Request,
    current_user: User = Depends(get_current_user)
):
    orders = await get_all_orders()
    return templates.TemplateResponse("orders/orders.html", {
                                                    "request": request,
                                                    "current_user": current_user,
                                                    "orders": orders
                                                    })


@router.get('/orders/{order_id}', response_class=HTMLResponse)
async def get_order_detail(
    request: Request,
    order_id: int,
    current_user: User = Depends(get_current_user)
):
    order_data = await OrderDAO.find_by_id(order_id)
    return templates.TemplateResponse("orders/orders_detail.html", {
                                                    "request": request,
                                                    "order": order_data
                                                    })


# @router.get('/orders/{user_id}', response_class=HTMLResponse)
# async def get_orders_by_user(
#     request: Request,
#     user_id: int,
#     current_user: User = Depends(get_current_user),
# ):
#     orders = await get_orders_from_user(current_user.id)
#     return templates.TemplateResponse("orders/orders_by_users_id.html", {
#                                                     "request": request,
#                                                     "username": current_user.username,
#                                                     "orders": orders,
#                                                     })


@router.get("/order_create", response_class=HTMLResponse)
def create_orders_page(
    request: Request,
    current_user: User = Depends(get_current_user)
):
    return templates.TemplateResponse('orders/create_orders.html', {'request': request})


@router.post('/order_create')
async def create_order(
    request: Request,
    name: str = Form(...),
    price: float = Form(...),
    amount: int = Form(...),
    client_id: int = Form(...),
    current_user: User = Depends(get_current_user)

):
    order_data = {
        'name': name,
        'price': price,
        'amount': amount,
        'user_id': current_user.id,
        'client_id': client_id
        }
    order = OrderSchem(**order_data)
    await create_orders(order)
    return await get_orders(request)


@router.get("/orders/{order_id}/update", response_class=HTMLResponse)
async def update_order_page(
    request: Request,
    order_id: int,
    current_user: User = Depends(get_current_user)
):
    order = await OrderDAO.find_by_id(order_id)
    return templates.TemplateResponse(
        'orders/update_orders.html',
        {
            'request': request,
            'order': order
        }
    )


# @router.post("/clients/{client_id}/update")
# async def update_clients(
#     request: Request,
#     client_id: int,
#     name: str = Form(...),
#     price: float = Form(...),
#     production: str = Form(...),
#     contact: str = Form(...),
#     last_contact: datetime = Form(...),
#     current_user: User = Depends(get_current_user)
# ):
#     client_data = {
#         'id': client_id,
#         'name': name,
#         'price': price,
#         'production': production,
#         'contact': contact,
#         'last_contact': last_contact,
#         'user_id': current_user.id,
#         }
#     client = UpdateClient(**client_data)
#     await ClinetDAO.update(client_id, client)
#     return await get_clients(request)


@router.post("/orders/{order_id}/update")
async def update_orders(
    request: Request,
    order_id: int,
    name: str = Form(...),
    price: float = Form(...),
    amount: int = Form(...),
    client_id: int = Form(...),
    current_user: User = Depends(get_current_user)
):
    order_data = {
        'id': order_id,
        'name': name,
        'price': price,
        'amount': amount,
        'user_id': current_user.id,
        'client_id': client_id
        }
    order = UpdateSchem(**order_data)
    await OrderDAO.update(order_id, order)
    return await get_orders(request)


@router.post('/orders/{order_id}')
async def delete_orders(
    request: Request,
    order_id: int,
    current_user: User = Depends(get_current_user)
):
    await OrderDAO.delete(order_id)
    return await get_orders(request)

