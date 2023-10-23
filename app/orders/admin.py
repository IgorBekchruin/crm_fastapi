from sqladmin import ModelView

from app.orders.models import Order


class OrderAdmin(ModelView, model=Order):
    column_list = [
        Order.id,
        Order.name,
        Order.price,
        Order.amount,
        Order.user_id,
        Order.client_id,
    ]
