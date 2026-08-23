import asyncio
from datetime import datetime, timezone

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.celery_app import celery_app
from app.core.config import settings
from app.repository.ReportRepository import get_monthly_report_data
from app.services.ReportService import generate_monthly_report


async def process_monthly_report():

    engine = create_async_engine(
        settings.DATABASE_URL,
        pool_pre_ping=True,
    )

    Session = async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    try:
        now = datetime.now(timezone.utc)

        first_day_current_month = now.replace(
            day=1,
            hour=0,
            minute=0,
            second=0,
            microsecond=0,
        )

        start_date = first_day_current_month

        async with Session() as session:

            report_data = await get_monthly_report_data(
                session=session,
                start_date=start_date,
                end_date=now,
            )

        report_url, report_bytes = generate_monthly_report(
            report_data=report_data,
            year=now.year,
            month=now.month,
        )

        return report_url

    finally:
        await engine.dispose()


@celery_app.task(
    name="generate_monthly_library_report"
)
def generate_monthly_library_report():

    result = asyncio.run(
        process_monthly_report()
    )

    return result