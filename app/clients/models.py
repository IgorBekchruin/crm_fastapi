import datetime
from re import M
from typing import List, TYPE_CHECKING

from sqlalchemy import String, Date, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.users.models import User
    from app.orders.models import Order


class Client(Base):
    __tablename__ = 'clients'

    id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)
    price: Mapped[float]
    production: Mapped[str]
    contact: Mapped[str] = mapped_column(String(500))
    last_contact: Mapped[DateTime] = mapped_column(DateTime)

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete="SET NULL"))
    user: Mapped["User"] = relationship(back_populates='client', lazy='joined')

    def __str__(self):
        return self.name