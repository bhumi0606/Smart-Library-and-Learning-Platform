from pydantic import BaseModel, Field

class CreateEnrollment(BaseModel):
    member_id: int = Field(
        description="The ID of the member enrolling in the course"
    )
    course_id: int = Field(
        description="The ID of the course the member is enrolling in"
    )