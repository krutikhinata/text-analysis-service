from pydantic import BaseModel


class ParsedText(BaseModel):
    file_name: str
    file_extension: str
    file_size: int

    content: str
