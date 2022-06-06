from typing import Optional

from sqlmodel import Field, SQLModel

from app.core.models import TimestampModel, UUIDModel

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

    hash_value: str = Field(
            max_length=56,
            nullable=False,
            index=True
        )


class DocumentRead(DocumentBase):
    ...


class DocumentCreate(DocumentBase):
    ...


class DocumentPatch(DocumentBase):
    name: Optional[str] = Field(max_length=127)
    link: Optional[str] = Field(max_length=2047)
