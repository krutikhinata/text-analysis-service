from typing import Optional

import sqlalchemy as sa
from pydantic import BaseModel
from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import Field, SQLModel

from app.core.models import TimestampModel, UUIDModel
from app.ontologies.examples import (ex_metric_create, ex_metric_patch,
                                     ex_metric_read)

prefix = "ont"


class MetricBase(SQLModel):
    name: str = Field(
        max_length=127,
        nullable=False,
        sa_column_kwargs={
            "unique": True
        }
    )

    mapping: dict = Field(
        sa_column=sa.Column(
            "mapping",
            JSONB,
            nullable=False,
            default={}
        )
    )


class Metric(
    TimestampModel,
    MetricBase,
    UUIDModel,
    table=True
):
    __tablename__ = f"{prefix}_metrics"

    class Config:
        schema_extra = {"example": ex_metric_read}


class MetricCreate(MetricBase):
    class Config:
        schema_extra = {"example": ex_metric_create}


class MetricPatch(BaseModel):
    name: Optional[str] = Field(max_length=127)
    mapping: Optional[dict]

    class Config:
        schema_extra = {"example": ex_metric_patch}
