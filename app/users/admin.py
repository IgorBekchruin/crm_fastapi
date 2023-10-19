from sqladmin import ModelView

from app.users.models import Role, User


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.username, User.role_id]


class RoleAdmin(ModelView, model=Role):
    column_list = [Role.id, User.username]

