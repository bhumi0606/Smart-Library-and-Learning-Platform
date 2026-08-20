from pydantic import BaseModel, Field
from typing import Optional

class UpdateCourse(BaseModel):
    title: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=255,
        description="Title of the course"
    )
    description: Optional[str] = Field(
        default=None,
        max_length=255,
        description="Description of the course"
    )
