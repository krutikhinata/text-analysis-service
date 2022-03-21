from abc import ABC
from re import MULTILINE, compile
from typing import List

from nltk import sent_tokenize
from spacy import load

from app.segmentation.schemas import Sentence


class Segmenter(ABC):
    @staticmethod
    def _assemble_sentences(raw_sentences: List[str]) -> List[Sentence]:
        sentences = []
        for i, raw_sentence in enumerate(raw_sentences, 1):
            sentence = Sentence(
                number=i,
                content=raw_sentence,
                symbols=len(raw_sentence),
                words=len(raw_sentence.split())
            )

            sentences.append(sentence)

        return sentences

    def segment(self, text: str) -> List[Sentence]:
        ...


class RegexSegmenter(Segmenter):
    def segment(self, text: str) -> List[Sentence]:
        pattern = compile(r'([A-Z][^.!?]*[.!?])', MULTILINE)
        raw_sentences = pattern.findall(text)

        return self._assemble_sentences(raw_sentences=raw_sentences)


class NLTKSegmenter(Segmenter):
    def segment(self, text: str) -> List[Sentence]:
        raw_sentences = sent_tokenize(text)

        return self._assemble_sentences(raw_sentences=raw_sentences)


class SpacySegmenter(Segmenter):
    model = load('en_core_web_sm')

    def segment(self, text: str) -> List[Sentence]:
        document = self.model(text)
        raw_sentences = [s.text for s in document.sents]

        return self._assemble_sentences(raw_sentences=raw_sentences)
