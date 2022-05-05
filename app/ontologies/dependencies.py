from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.ontologies.crud import MetricsCRUD


async def get_metrics_crud(
        session: AsyncSession = Depends(get_async_session)
) -> MetricsCRUD:
    return MetricsCRUD(session=session)
