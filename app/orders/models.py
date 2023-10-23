from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.clients.models import Client
    from app.users.models import User


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)
    price: Mapped[float]
    amount: Mapped[int]

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"))
    user: Mapped["User"] = relationship(back_populates="order", lazy="joined")

    client_id: Mapped[int] = mapped_column(ForeignKey("clients.id", ondelete="CASCADE"))
    client: Mapped["Client"] = relationship(backref="orders", lazy="joined")

    def __str__(self):
        return self.name
