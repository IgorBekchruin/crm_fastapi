from typing import List, TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.clients.models import Client
    from app.orders.models import Order


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    username: Mapped[str] = mapped_column(String(100), unique=True)
    hashed_password: Mapped[str] = mapped_column(String(1024), nullable=False)

    client: Mapped[List['Client']] = relationship(back_populates='user', lazy='joined')
    order: Mapped[List['Order']] = relationship(back_populates='user', lazy='joined')

    role_id: Mapped[int] = mapped_column(ForeignKey('roles.id', ondelete="SET NULL"), nullable=True)
    role: Mapped['Role'] = relationship(backref='roles')

    def __str__(self):
        return self.name


class Role(Base):
    __tablename__ = 'roles'

    id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    name: Mapped[str] = mapped_column(nullable=False)

    def __str__(self):
        return self.name
