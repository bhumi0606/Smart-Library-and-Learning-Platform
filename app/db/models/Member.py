

# MEMBER
from datetime import datetime

from sqlalchemy import DateTime, String, func, Enum

from app.db.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.enums.RoleEnums import Role

class Member(Base):
    __tablename__ = "members"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True,
    )

    password: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    role: Mapped[Role] = mapped_column(
        Enum(
            Role,
            name="role",
            values_callable=lambda enum_class: [
                member.value for member in enum_class
            ],
        ),
        default=Role.MEMBER,
        nullable=False
    )

    loans: Mapped[list["Loan"]] = relationship(
        "Loan",
        back_populates="member",
    )

    enrollments: Mapped[list["Enrollment"]] = relationship(
        "Enrollment",
        back_populates="member",
    )