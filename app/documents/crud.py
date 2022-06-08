from uuid import UUID

from fastapi import HTTPException
from fastapi import status as http_status
from sqlalchemy import delete, select, update
from sqlmodel.ext.asyncio.session import AsyncSession

from app import Document
from app.documents.models import DocumentCreate, DocumentPatch


class DocumentsCRUD:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, data: DocumentCreate) -> Document:
        values = data.dict()
        doc = Document(**values)

        self.session.add(doc)
        await self.session.commit()
        await self.session.refresh(doc)

        return doc

    async def get(self, doc_id: str | UUID) -> Document:
        statement = select(
            Document
        ).where(
            Document.uuid == doc_id
        )
        results = await self.session.execute(statement=statement)
        doc = results.scalar_one_or_none()

        if doc is None:
            raise HTTPException(
                status_code=http_status.HTTP_404_NOT_FOUND,
                detail="The document hasn't been found!"
            )

        return doc

    async def patch(self, doc_id: str | UUID, data: DocumentPatch) -> Document:
        values = data.dict(exclude_unset=True)
        statement = update(
            Document
        ).where(
            Document.uuid == doc_id
        ).values(values)
        await self.session.execute(statement=statement)
        await self.session.commit()

        return await self.get(doc_id=doc_id)

    async def delete(self, doc_id: str | UUID) -> bool:
        statement = delete(
            Document
        ).where(
            Document.uuid == doc_id
        )

        await self.session.execute(statement=statement)
        await self.session.commit()

        return True
