from typing import List

from pydantic import BaseModel


class Sentence(BaseModel):
    number: int
    content: str
    symbols: int
    words: int


class TextSegmentationStats(BaseModel):
    symbols: int
    words: int
    sentences: int


class TextSegmentation(BaseModel):
    file_name: str
    file_extension: str
    file_size: int

    stats: TextSegmentationStats
    sentences: List[Sentence]
