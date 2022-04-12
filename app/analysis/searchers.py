from abc import ABC
from typing import Optional


class Searcher(ABC):
    def identify(self, string: str, **kwargs):
        ...


class NumberSearcher(Searcher):
    def identify(self, string: str, **kwargs):
        pattern_variable = kwargs.get("pattern_variable")

        # pattern for ,
        # 1,000 -> 1000

        return
