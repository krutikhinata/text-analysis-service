from abc import abstractmethod
from dataclasses import dataclass
from typing import List

import pdftotext
from sqlalchemy import select
from sqlmodel import Session

from app import Document, DocumentIndex
from app import Metric as OntologyMetric
from app.analysis.converters import Converter
from app.analysis.searchers import MetricRecognised, NumberSearcher
from app.celery_app.app import update_task_run
from app.core.db import get_sync_session
from app.segmentation.core.analysis import SpacySegmenter
from app.segmentation.schemas import Sentence


@dataclass
class TaskStage:
    name: str
    percentage: int

    @abstractmethod
    def run(self, *args, **kwargs):
        ...


class GettingDocument(TaskStage):
    @update_task_run
    def run(self, *args, **kwargs):
        if not args:
            session = kwargs.get("session")  # type: Session
            document_id = kwargs.get("document_id")
        else:
            session, document_id = args

        statement = select(
            Document
        ).where(
            Document.uuid == document_id
        )
        result = session.execute(statement=statement)
        document = result.scalar_one()

        return document


class Segmentation(TaskStage):
    @update_task_run
    def run(self, *args, **kwargs):
        if not args:
            document = kwargs.get("document")  # type: Document
        else:
            document = args[0]  # type: Document

        segmenter = SpacySegmenter()
        with open(document.file_path, "rb") as file:
            pdf_content = pdftotext.PDF(pdf_file=file)

        segmentation = segmenter.segment("\n\n".join(pdf_content))

        return segmentation


class GetProvision(TaskStage):
    @update_task_run
    def run(self, *args, **kwargs):
        if not args:
            session = kwargs.get("session")  # type: Session
        else:
            session = args[0]

        statement = select(OntologyMetric)
        results = session.execute(statement=statement)
        metrics = results.scalars().all()  # type: List[OntologyMetric]

        return metrics


class Indexing(TaskStage):
    @update_task_run
    def run(self, *args, **kwargs):
        if not args:
            segmentation = kwargs.get("segmentation")  # type: List[Sentence]
            metrics = kwargs.get("metrics")  # type: List[OntologyMetric]
        else:
            segmentation, metrics = args

        searcher = NumberSearcher()

        results = {}
        for metric in metrics:
            metric_indexing = []
            for sentence in segmentation:
                for k in metric.mapping.keys():
                    metric_recognised = searcher.identify(
                        string=sentence.content,
                        metric=k
                    )

                    metric_indexing.append(
                        {
                            "sentence_number": sentence.number,
                            "metrics_recognised": metric_recognised,
                            "mapping": metric.mapping
                        }
                    )

            results[metric.name] = metric_indexing

        return results


class Saving(TaskStage):
    @update_task_run
    def run(self, *args, **kwargs):
        if not args:
            session = kwargs.get("session")  # type: Session
            document = kwargs.get("document")  # type: Document
            results = kwargs.get("results")  # type: dict
        else:
            session, document, results = args

        for key, value in results.items():
            for metric_indexing in value:
                metrics_recognised = metric_indexing.get(
                    "metrics_recognised"
                )  # type: MetricRecognised

                converter = Converter(mapping=metric_indexing.get("mapping"))

                for metric in metrics_recognised.metrics:

                    document_index = DocumentIndex(
                        metric_name=key,
                        sentence_number=metric_indexing.get("sentence_number"),
                        value=converter.to_std(
                            value=metric.value,
                            metric=metric.unit
                        ),
                        document_id=document.uuid
                    )
                    session.add(document_index)

                for metric_range in metrics_recognised.metric_ranges:
                    document_index = DocumentIndex(
                        metric_name=key,
                        sentence_number=metric_indexing.get("sentence_number"),
                        value=converter.to_std(
                            value=metric_range.to.value,
                            metric=metric_range.to.unit
                        ),
                        document_id=document.uuid
                    )
                    session.add(document_index)

                    document_index = DocumentIndex(
                        metric_name=key,
                        sentence_number=metric_indexing.get("sentence_number"),
                        value=converter.to_std(
                            value=metric_range.from_.value,
                            metric=metric_range.from_.unit
                        ),
                        document_id=document.uuid
                    )
                    session.add(document_index)

        session.commit()


class TaskRunner:
    def __init__(self):
        self.session = get_sync_session()

    def run(self, document_id: str):
        first_stage = GettingDocument(name="Getting document", percentage=10)
        document = first_stage.run(
            session=self.session,
            document_id=document_id
        )

        second_stage = Segmentation(name="Segmentation", percentage=30)
        segmentation = second_stage.run(document=document)

        third_stage = GetProvision(name="Getting provision", percentage=50)
        metrics = third_stage.run(session=self.session)

        fourth_stage = Indexing(name="Indexing", percentage=80)
        results = fourth_stage.run(segmentation=segmentation, metrics=metrics)

        fifth_stage = Saving(name="Saving data", percentage=90)
        fifth_stage.run(
            session=self.session,
            document=document,
            results=results
        )

        return {
            "status": True,
            "message": "The processing has been completed with success!"
        }
