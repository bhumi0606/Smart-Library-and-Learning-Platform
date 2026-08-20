from pydantic import BaseModel, Field
from typing import Optional

class UpdateEnrollment(BaseModel):
    member_id: Optional[int] = Field(
        default=None,
        description="The ID of the member enrolling in the course"
    )
    course_id: Optional[int] = Field(
        default=None,
        description="The ID of the course the member is enrolling in"
    )