import logging

from fastapi import APIRouter, UploadFile
from fastapi.params import File
from starlette.background import BackgroundTasks

from app.celery_app.app import celery_app
from app.celery_app.schemas import TaskCreated
from app.parsing.pdf import Parser
from app.segmentation.core.analysis import (NLTKSegmenter, RegexSegmenter,
                                            SpacySegmenter)
from app.segmentation.schemas import TextSegmentation, TextSegmentationStats

router = APIRouter()

log = logging.getLogger(__name__)


def background_on_message(task):
    log.info(task.get(propagate=False))


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


@router.post("/pdf/regex/task", response_model=TaskCreated)
async def segment_pdf_with_regex_as_task(
        background_tasks: BackgroundTasks,
        file: UploadFile = File(...),
) -> TaskCreated:
    parser = Parser()
    pdf_text = await parser.parse(file=file)

    task = celery_app.send_task(
        "segment_pdf_with_regex",
        args=(pdf_text.dict(),)
    )
    background_tasks.add_task(background_on_message, task)

    return TaskCreated(task_id=task.id)


@router.post("/pdf/nltk", response_model=TextSegmentation)
async def segment_pdf_with_nltk(
        file: UploadFile = File(...),
) -> TextSegmentation:

    parser = Parser()
    segmenter = NLTKSegmenter()

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


@router.post("/pdf/spacy", response_model=TextSegmentation)
async def segment_pdf_with_spacy(
        file: UploadFile = File(...),
) -> TextSegmentation:

    parser = Parser()
    segmenter = SpacySegmenter()

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
