from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.documents.crud import DocumentsCRUD


async def get_documents_crud(
        session: AsyncSession = Depends(get_async_session)
) -> DocumentsCRUD:
    return DocumentsCRUD(session=session)
