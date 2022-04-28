from io import BytesIO

import pdftotext
from fastapi import HTTPException, UploadFile
from fastapi import status as http_status

from app.parsing.schemas import ParsedText


class Parser:
    valid_size_mb = 30

    async def parse(self, file: UploadFile) -> ParsedText:
        extension = file.filename.split(".")[-1].lower()
        file_size = sum([len(chunk) for chunk in file.file]) / 1024 / 1024

        if file_size > self.valid_size_mb:
            raise HTTPException(
                status_code=http_status.HTTP_406_NOT_ACCEPTABLE,
                detail="PDF file size is too large."
            )

        file.file.seek(0, 0)
        pdf = pdftotext.PDF(pdf_file=BytesIO(await file.read()))

        return ParsedText(
            file_name=file.filename,
            file_extension=extension,
            file_size=file_size,
            content="\n\n".join(pdf)
        )
