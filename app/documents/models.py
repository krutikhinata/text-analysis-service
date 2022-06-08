from typing import Optional
from uuid import UUID

from pydantic import BaseModel, condecimal
from sqlmodel import Field, SQLModel

from app.core.models import TimestampModel, UUIDModel
from app.core.utils import form_body_model

prefix = "doc"


class DocumentBase(SQLModel):
    name: str = Field(
        max_length=127,
        nullable=False
    )

    link: str = Field(
        max_length=2047,
        nullable=False,
        sa_column_kwargs={
            "unique": True
        }
    )


class Document(
    TimestampModel,
    UUIDModel,
    DocumentBase,
    table=True
):
    __tablename__ = f"{prefix}_documents"

    file_path: str = Field(nullable=False)

    hash_value: str = Field(
        max_length=56,
        nullable=False,
        index=True
    )


class DocumentRead(DocumentBase):
    ...


@form_body_model
class DocumentCreate(BaseModel):
    name: str = Field(max_length=127, nullable=False)
    link: str = Field(max_length=2047, nullable=False)


class DocumentPatch(DocumentBase):
    name: Optional[str] = Field(max_length=127)
    link: Optional[str] = Field(max_length=2047)


class DocumentIndexBase(SQLModel):
    metric_name: str = Field(max_length=127, nullable=False)
    sentence_number: int = Field(nullable=False)
    value: condecimal() = Field(nullable=False)


class DocumentIndex(
    TimestampModel,
    DocumentIndexBase,
    UUIDModel,
    table=True
):
    __tablename__ = f"{prefix}_documents_index"

    document_id: UUID = Field(
        foreign_key="doc_documents.uuid",
        nullable=False
    )
