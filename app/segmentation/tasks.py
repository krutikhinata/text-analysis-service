from app.celery_app.app import celery_app
from app.segmentation.core.analysis import RegexSegmenter
from app.segmentation.schemas import TextSegmentationStats, TextSegmentation


@celery_app.task(name="segment_pdf_with_regex", acks_late=True)
def segment_pdf_with_regex(pdf_text_obj: dict):
    segmenter = RegexSegmenter()
    segmentation = segmenter.segment(pdf_text_obj["content"])

    stats = TextSegmentationStats(
        symbols=len(pdf_text_obj["content"]),
        words=len(pdf_text_obj["content"].split()),
        sentences=len(segmentation)
    )

    data = TextSegmentation(
        file_name=pdf_text_obj["file_name"],
        file_extension=pdf_text_obj["file_extension"],
        file_size=pdf_text_obj["file_size"],
        stats=stats,
        sentences=segmentation
    )

    return data.dict()
