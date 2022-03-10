from abc import ABC
from re import MULTILINE, compile
from typing import List

import nltk
from nltk import sent_tokenize
from spacy.lang.en import English

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
        nltk.download('punkt')
        raw_sentences = sent_tokenize(text)

        return self._assemble_sentences(raw_sentences=raw_sentences)


class SpacySegmenter(Segmenter):
    nlp = English()
    sbd = nlp.add_pipe('sentencizer')
    nlp.add_pipe(sbd)

    def segment(self, text: str) -> List[Sentence]:
        doc = self.nlp(text)
        raw_sentences = []
        for sent in doc.sents:
            raw_sentences.append(sent.text)

        return self._assemble_sentences(raw_sentences=raw_sentences)