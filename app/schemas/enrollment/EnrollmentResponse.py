from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime

class EnrollmentResponse(BaseModel):
    id: int = Field(
        description="The unique identifier of the enrollment"
    )
    member_id: int = Field(
        description="The ID of the enrolled member"
    )
    course_id: int = Field(
        description="The ID of the enrolled course"
    )
    enrolled_at: datetime = Field(
        description="Timestamp when the enrollment was created"
    )
    
    model_config = ConfigDict(from_attributes=True)