from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime

class CourseResponse(BaseModel):
    id: int = Field(
        description="Unique identifier for the course"
    )
    title: str = Field(
        description="Title of the course"
    )
    description: Optional[str] = Field(
        default=None,
        description="Description of the course"
    )
    created_at: datetime = Field(
        description="Timestamp when the course was created"
    )
    
    model_config = ConfigDict(from_attributes=True)