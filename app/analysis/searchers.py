from abc import ABC
from typing import Optional
import re


class Searcher(ABC):
    def identify(self, string: str, **kwargs):
        ...


class NumberSearcher(Searcher):
    def identify(self, string: str, **kwargs):
        for _ in kwargs:
            pattern_variable = kwargs.get("pattern_variable")
            pattern = rf'[-+]?(?:\d+(?:[\.\,\d]*)?|\.\d+)(?:[eE][-+]?\d+)?(?={pattern_variable})'
            match = re.search(pattern=pattern,
                              string=string,
                              flags=re.IGNORECASE
                              )
            if match:
                matched_value = float(match.group().replace(",", ""))

            return matched_value
