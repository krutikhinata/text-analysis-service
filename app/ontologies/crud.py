from uuid import UUID

from fastapi import HTTPException
from fastapi import status as http_status
from sqlalchemy import delete, select, update
from sqlmodel.ext.asyncio.session import AsyncSession

from app import Metric
from app.ontologies.models import MetricCreate, MetricPatch


class MetricsCRUD:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, data: MetricCreate) -> Metric:
        values = data.dict()
        metric = Metric(**values)

        self.session.add(metric)
        await self.session.commit()
        await self.session.refresh(metric)

        return metric

    async def get(self, metric_id: str | UUID) -> Metric:
        # SELECT * FROM ont_metrics WHERE uuid == :metric_id;
        statement = select(
            Metric
        ).where(
            Metric.uuid == metric_id
        )
        results = await self.session.execute(statement=statement)
        metric = results.scalar_one_or_none()

        if metric is None:
            raise HTTPException(
                status_code=http_status.HTTP_404_NOT_FOUND,
                detail="The metric hasn't been found!"
            )

        return metric

    async def patch(self, metric_id: str | UUID, data: MetricPatch) -> Metric:
        values = data.dict(exclude_unset=True)
        statement = update(
            Metric
        ).where(
            Metric.uuid == metric_id
        ).values(values)
        await self.session.execute(statement=statement)
        await self.session.commit()

        return await self.get(metric_id=metric_id)

    async def delete(self, metric_id: str | UUID) -> bool:
        statement = delete(
            Metric
        ).where(
            Metric.uuid == metric_id
        )

        await self.session.execute(statement=statement)
        await self.session.commit()

        return True
