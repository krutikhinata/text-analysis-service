from fastapi import APIRouter, Depends, File, UploadFile
from fastapi import status as http_status

from app.core.models import StatusMessage
from app.documents.crud import DocumentsCRUD
from app.documents.dependencies import get_documents_crud
from app.documents.models import (Document, DocumentCreate, DocumentPatch,
                                  DocumentRead)

router = APIRouter()


@router.post(
    "",
    response_model=Document,
    status_code=http_status.HTTP_201_CREATED
)
async def create_document(
        data: DocumentCreate = Depends(DocumentCreate.as_form),
        file: UploadFile = File(...),
        documents: DocumentsCRUD = Depends(get_documents_crud)
):
    document = await documents.create(data=data, file=file)
    return document


@router.get(
    "/{doc_id}",
    response_model=DocumentRead,
    status_code=http_status.HTTP_200_OK
)
async def get_document(
        doc_id: str,
        documents: DocumentsCRUD = Depends(get_documents_crud)
):
    doc = await documents.get(
        doc_id=doc_id
    )

    return doc


@router.patch(
    "/{doc_id}",
    response_model=DocumentRead,
    status_code=http_status.HTTP_200_OK
)
async def patch_document(
        doc_id: str,
        data: DocumentPatch,
        documents: DocumentsCRUD = Depends(get_documents_crud)
):
    doc = await documents.patch(
        doc_id=doc_id,
        data=data
    )

    return doc


@router.delete(
    "/{doc_id}",
    response_model=StatusMessage,
    status_code=http_status.HTTP_200_OK
)
async def delete_document(
        doc_id: str,
        documents: DocumentsCRUD = Depends(get_documents_crud)
):
    status = await documents.delete(
        doc_id=doc_id
    )

    return {"status": status, "message": "The document has been deleted!"}
