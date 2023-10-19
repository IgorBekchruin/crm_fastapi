from pydantic import BaseModel, ConfigDict


class OrderSchem(BaseModel):
    name: str
    price: float
    amount: int
    user_id: int
    client_id: int

    model_config = ConfigDict(
        from_attributes=True,
        arbitrary_types_allowed=True)


class UpdateSchem(OrderSchem):
    id: int
