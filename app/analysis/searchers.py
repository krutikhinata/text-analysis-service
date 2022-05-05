import re
from abc import ABC
from typing import List, Tuple


class Searcher(ABC):
    def identify(self, string: str, metric: str):
        ...


class NumberSearcher(Searcher):

    @staticmethod
    def _ranges(
            string: str,
            pattern_variable: str
    ) -> Tuple[str, List[float]]:
        pattern = rf'[-+]?(?:\d+(?:[\.\,\d]*)?)-' \
                  rf'(?:\d+(?:[\.\,\d]*)?)\s?(?={pattern_variable})'
        matched_values = re.findall(pattern, string, re.IGNORECASE)
        buffer = []

        for matched_value in matched_values:
            string = string.replace(
                f'{matched_value}{pattern_variable}',
                ' [cropped] '
            )
            matched_value = matched_value.replace(',', '.')
            occurrences = matched_value.count('.')
            if occurrences > 2:
                matched_value = matched_value.replace('.', '')
            values = matched_value.split('-')
            range_boundary1, range_boundary2 = values[0], values[1]
            buffer.extend((float(range_boundary1), float(range_boundary2)))

        return string, buffer

    # 1) (100 ± 10) -> range(90 - 110)?
    # [-+]?(?:\d+(?:[\.\, \d] *)?)±(?:\d+(?:[\.\, \d] *)?)(?=m)

    # 2) ±100 -> [-100.0, 100.0]
    # ±(?:\d+(?:[\.\, \d] *)?)(?=m)
    # this one captures the second part of 1)

    @staticmethod
    def _error_range(
            string: str,
            pattern_variable: str
    ) -> Tuple[str, List[float]]:
        pattern = rf'[-+]?(?:\d+(?:[\.\, \d] *)?)±(?:\d+(?:[\.\, \d] *)?)' \
                  rf'(?={pattern_variable})'
        matched_values = re.findall(pattern, string, re.IGNORECASE)
        buffer = []

        for matched_value in matched_values:
            values = matched_value.split('±')
            median, diff = float(values[0]), float(values[1])
            first = median - diff
            second = median + diff
            buffer.extend((first, second))

        return string, buffer

    @staticmethod
    def _positive_negative(
            string: str,
            pattern_variable: str
    ) -> Tuple[str, List[float]]:
        pattern = rf'±(?:\d+(?:[\.\, \d] *)?)(?={pattern_variable})'
        matched_values = re.findall(pattern, string, re.IGNORECASE)
        buffer = []

        for matched_value in matched_values:
            string = string.replace(
                f'{matched_value}{pattern_variable}',
                ' [cropped] '
            )
            buffer.append(float(matched_value.replace('±', '')))
            buffer.append(float((matched_value.replace('±', '')) * (-1)))

        return string, buffer

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
        string = string.replace(', ', '[, ]')
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
        string, ranges = self._ranges(string, pattern_variable=metric)
        string, error_range = self._error_range(
            string,
            pattern_variable=metric
        )
        string, pos_neg = self._positive_negative(
            string,
            pattern_variable=metric
        )
        values = exponential + general + scientific + error_range + pos_neg + ranges
        return string, values
