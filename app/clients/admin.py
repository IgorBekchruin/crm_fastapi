from sqladmin import ModelView

from app.clients.models import Client


class ClientAdmin(ModelView, model=Client):
    column_list = [
        Client.id,
        Client.name,
        Client.price,
        Client.production,
        Client.contact,
        Client.last_contact,
        Client.user_id
        ]

