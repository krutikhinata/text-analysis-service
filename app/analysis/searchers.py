from abc import ABC
from typing import List, Tuple
import re


class Searcher(ABC):
    def identify(self, string: str, metric: str):
        ...


class NumberSearcher(Searcher):
    @staticmethod
    def _exponential(
            string: str,
            pattern_variable: str
    ) -> Tuple[str, List[float]]:
        pattern = rf'[-+]?(?:\d+(?:[\.\,\d]*)?|\.\d+)[eE]' \
                  rf'(?:[-+]?\d+)?(?={pattern_variable})'
        matched_values = re.findall(pattern, string, re.IGNORECASE)

        buffer = []
        for matched_value in matched_values:
            string = string.replace(
                f'{matched_value}{pattern_variable}',
                ' [cropped] '
            )
            buffer.append(float(matched_value.replace(',', '.')))

        return string, buffer

    @staticmethod
    def _scientific_notation(
            string: str,
            pattern_variable: str
    ) -> Tuple[str, List[float]]:
        pattern = rf'[-+]?(?:\d+(?:[\.\,\d]*)?|\.\d+)[*×]\d*\^?\d+' \
                  rf'(?={pattern_variable})'
        matched_values = re.findall(pattern, string, re.IGNORECASE)
        buffer = []

        for matched_value in matched_values:
            if '*' in matched_value or '×' in matched_value:
                values = matched_value.split('*')
                if len(values) != 2:
                    values = matched_value.split('×')
                factor1, factor_with_degree = float(values[0]), values[1]
                if '^' in factor_with_degree:
                    factor_with_degree = factor_with_degree.split('^')
                    factor2, degree = (
                        int(factor_with_degree[0]),
                        int(factor_with_degree[1])
                    )
                else:
                    if factor_with_degree.startswith('10'):
                        degree = float(factor_with_degree[2:])
                        factor2 = 10
                    else:
                        continue

                string = string.replace(
                    f'{matched_value}{pattern_variable}',
                    ' [cropped] '
                )
                matched_value = factor1 * (factor2 ** degree)
                buffer.append(matched_value)

        return string, buffer

    @staticmethod
    def _general(
            string: str,
            pattern_variable: str
    ) -> Tuple[str, List[float]]:

        pattern = rf'[-+]?(?:\d+(?:[\.\,\d]*)?)(?={pattern_variable})'
        matched_values = re.findall(pattern, string, re.IGNORECASE)
        buffer = []

        for matched_value in matched_values:
            string = string.replace(
                f'{matched_value}{pattern_variable}',
                ' [cropped] '
            )
            matched_value = matched_value.replace(',', '.')
            occurrences = matched_value.count('.')
            if occurrences > 1:
                matched_value = matched_value.replace('.', '')
            buffer.append(float(matched_value))

        return string, buffer

    def identify(self, string: str, metric: str) -> Tuple[str, List[float]]:
        string = ''.join(string.split())
        string, exponential = self._exponential(
            string,
            pattern_variable=metric
        )
        string, scientific = self._scientific_notation(
            string,
            pattern_variable=metric
        )
        string, general = self._general(string, pattern_variable=metric)
        values = exponential + general + scientific
        return string, values

