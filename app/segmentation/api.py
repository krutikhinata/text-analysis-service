from fastapi import APIRouter, UploadFile
from fastapi.params import File

from app.parsing.pdf import Parser
from app.segmentation.core.analysis import RegexSegmenter, NLTKSegmenter, SpacySegmenter
from app.segmentation.schemas import TextSegmentation, TextSegmentationStats

router = APIRouter()


@router.post("/pdf/regex", response_model=TextSegmentation)
async def segment_pdf_with_regex(
        file: UploadFile = File(...),
) -> TextSegmentation:

    parser = Parser()
    segmenter = RegexSegmenter()

    pdf_text = await parser.parse(file=file)
    segmentation = segmenter.segment(pdf_text.content)

    stats = TextSegmentationStats(
        symbols=len(pdf_text.content),
        words=len(pdf_text.content.split()),
        sentences=len(segmentation)
    )

    return TextSegmentation(
        file_name=pdf_text.file_name,
        file_extension=pdf_text.file_extension,
        file_size=pdf_text.file_size,
        stats=stats,
        sentences=segmentation
    )


@router.post("/pdf/nltk", response_model=TextSegmentation)
async def segment_pdf_with_nltk(
        file: UploadFile = File(...),
) -> TextSegmentation:

    parser = Parser()
    segmenter = NLTKSegmenter()

    pdf_text = await parser.parse(file=file)
    segmentation = segmenter.segment(pdf_text.content)  # change here

    stats = TextSegmentationStats(
        symbols=len(pdf_text.content),
        words=len(pdf_text.content.split()),
        sentences=len(segmentation)
    )

    return TextSegmentation(
        file_name=pdf_text.file_name,
        file_extension=pdf_text.file_extension,
        file_size=pdf_text.file_size,
        stats=stats,
        sentences=segmentation
    )


@router.post("/pdf/spacy", response_model=TextSegmentation)
async def segment_pdf_with_spacy(
        file: UploadFile = File(...),
) -> TextSegmentation:

    parser = Parser()
    segmenter = SpacySegmenter()

    pdf_text = await parser.parse(file=file)
    segmentation = segmenter.segment(pdf_text.content)  # change here

    stats = TextSegmentationStats(
        symbols=len(pdf_text.content),
        words=len(pdf_text.content.split()),
        sentences=len(segmentation)
    )

    return TextSegmentation(
        file_name=pdf_text.file_name,
        file_extension=pdf_text.file_extension,
        file_size=pdf_text.file_size,
        stats=stats,
        sentences=segmentation
    )
