from abc import abstractmethod
from dataclasses import dataclass
from typing import List

import pdftotext
from sqlalchemy import select
from sqlmodel import Session

from app import Document, DocumentIndex
from app import Metric as OntologyMetric
from app.analysis.searchers import MetricRecognised, NumberSearcher
from app.segmentation.core.analysis import RegexSegmenter
from app.segmentation.schemas import Sentence


@dataclass
class TaskStage:
    name: str
    percentage: int

    @abstractmethod
    def run(self, *args, **kwargs):
        ...


class GettingDocument(TaskStage):
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
    def run(self, *args, **kwargs):
        if not args:
            document = kwargs.get("document")  # type: Document
        else:
            document = args[0]  # type: Document

        segmenter = RegexSegmenter()
        pdf_content = pdftotext.PDF(pdf_file=document.file_path)

        segmentation = segmenter.segment("\n\n".join(pdf_content))

        return segmentation


class GetProvision(TaskStage):
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
                            "metrics_recognised": metric_recognised
                        }
                    )

            results[metric.name] = metric_indexing

        return results


class Saving(TaskStage):
    def run(self, *args, **kwargs):
        if not args:
            session = kwargs.get("session")  # type: Session
            document = kwargs.get("document")  # type: Document
            results = kwargs.get("results")  # type: dict
        else:
            session, document, results = args

        for key, value in results.items():
            metrics_recognised = value.get(
                "metrics_recognised"
            )  # type: MetricRecognised

            for metric in metrics_recognised.metrics:
                document_index = DocumentIndex(
                    metric_name=key,
                    sentence_number=value.get("sentence_number"),
                    value=...,
                    document_id=document.uuid
                )

            for metric_range in metrics_recognised.metric_ranges:
                document_index = DocumentIndex(
                    metric_name=key,
                    sentence_number=value.get("sentence_number"),
                    value=...,
                    document_id=document.uuid
                )

                document_index = DocumentIndex(
                    metric_name=key,
                    sentence_number=value.get("sentence_number"),
                    value=...,
                    document_id=document.uuid
                )


class TaskRunner:
    def __init__(self):
        pipeline = [
            GettingDocument(name="Getting document", percentage=10),
            Segmentation(name="Segmentation", percentage=30),
            GetProvision(name="Getting provision", percentage=50),
            Indexing(name="Indexing", percentage=80),
            Saving(name="Saving data", percentage=90)
        ]
