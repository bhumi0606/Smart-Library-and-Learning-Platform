from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ReservationResponse(BaseModel):

    id: int

    member_id: int

    book_id: int

    reserved_at: datetime

    expires_at: datetime | None

    status: str

    model_config = ConfigDict(
        from_attributes=True,
    )