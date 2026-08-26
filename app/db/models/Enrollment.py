
# ENROLLMENT
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, func

from app.db.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Enrollment(Base):
    __tablename__ = "enrollments"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    member_id: Mapped[int] = mapped_column(
        ForeignKey("members.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    course_id: Mapped[int] = mapped_column(
        ForeignKey("courses.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    enrolled_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    member: Mapped["Member"] = relationship(
        "Member",
        back_populates="enrollments",
    )

    course: Mapped["Course"] = relationship(
        "Course",
        back_populates="enrollments",
    )