from app.clients.models import Client
from app.dao.base_dao import BaseDAO
from app.users.models import User


class ClinetDAO(BaseDAO):
    model = Client
    child_model = Client.user
    