import re
from abc import ABC
from dataclasses import dataclass
from decimal import Decimal
from typing import List


@dataclass
class Metric:
    unit: str
    value: Decimal

    def __hash__(self):
        return hash(f'{self.unit}{self.value}')

    def __eq__(self, other):
        return self.unit == other.unit and self.value == other.value


@dataclass
class MetricRange:
    from_: Metric
    to: Metric

    def __hash__(self):
        return hash(f'{self.from_.unit}{self.to.unit}/'
                    f'{self.from_.value}{self.to.value}')

    def __eq__(self, other):
        return self.from_.unit == other.from_.unit and \
               self.to.unit == other.to.unit and \
               self.from_.value == other.from_.value and \
               self.to.value == other.to.value


@dataclass
class MetricRecognised:
    metrics: List[Metric]
    metric_ranges: List[MetricRange]


class Searcher(ABC):
    def identify(self, string: str, metric: str):
        ...


class NumberSearcher(Searcher):

    @staticmethod
    def _general(
            string: str,
            pattern_variable: str
    ) -> List:

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
            metric = Metric(
                unit=pattern_variable,
                value=Decimal(matched_value)
            )
            buffer.append(metric)

        return buffer

    @staticmethod
    def _ranges(
            string: str,
            pattern_variable: str
    ) -> List:
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
            MetricRange(
                from_=Metric(pattern_variable, Decimal(range_boundary1)),
                to=Metric(pattern_variable, Decimal(range_boundary2))
            )
            buffer.append(MetricRange)

        return buffer

    # 1) (100 ± 10) -> range(90 - 110)?
    # [-+]?(?:\d+(?:[\.\, \d] *)?)±(?:\d+(?:[\.\, \d] *)?)(?=m)

    # 2) ±100 -> [-100.0, 100.0]
    # ±(?:\d+(?:[\.\, \d] *)?)(?=m)
    # this one captures the second part of 1)

    @staticmethod
    def _error_range(
            string: str,
            pattern_variable: str
    ) -> List[MetricRange]:
        pattern = rf'[-+]?(?:\d+(?:[\.\, \d] *)?)±(?:\d+(?:[\.\, \d] *)?)' \
                  rf'(?={pattern_variable})'
        matched_values = re.findall(pattern, string, re.IGNORECASE)
        buffer = []

        for matched_value in matched_values:
            values = matched_value.split('±')
            median, diff = Decimal(values[0]), Decimal(values[1])
            from_ = median - diff
            to = median + diff
            MetricRange(
                from_=Metric(pattern_variable, Decimal(from_)),
                to=Metric(pattern_variable, Decimal(to))
            )
            buffer.append(MetricRange)

        return buffer

    @staticmethod
    def _positive_negative(
            string: str,
            pattern_variable: str
    ) -> List[Metric]:
        pattern = rf'±(?:\d+(?:[\.\, \d] *)?)(?={pattern_variable})'
        matched_values = re.findall(pattern, string, re.IGNORECASE)
        buffer = []

        for matched_value in matched_values:
            string = string.replace(
                f'{matched_value}{pattern_variable}',
                ' [cropped] '
            )
            value = Decimal(matched_value.replace('±', ''))
            metric = Metric(
                unit=pattern_variable,
                value=value
            )
            buffer.append(metric)
            metric = Metric(
                unit=pattern_variable,
                value=-value
            )
            buffer.append(metric)

        return buffer

    @staticmethod
    def _exponential(
            string: str,
            pattern_variable: str
    ) -> List[Metric]:
        pattern = rf'[-+]?(?:\d+(?:[\.\,\d]*)?|\.\d+)[eE]' \
                  rf'(?:[-+]?\d+)?(?={pattern_variable})'
        matched_values = re.findall(pattern, string, re.IGNORECASE)

        buffer = []
        for matched_value in matched_values:
            string = string.replace(
                f'{matched_value}{pattern_variable}',
                ' [cropped] '
            )
            metric = Metric(
                unit=pattern_variable,
                value=Decimal(matched_value.replace(',', '.'))
            )
            buffer.append(metric)

        return buffer

    @staticmethod
    def _scientific_notation(
            string: str,
            pattern_variable: str
    ) -> List[Metric]:
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
                        degree = Decimal(factor_with_degree[2:])
                        factor2 = 10
                    else:
                        continue

                string = string.replace(
                    f'{matched_value}{pattern_variable}',
                    ' [cropped] '
                )
                matched_value = factor1 * (factor2 ** degree)
                metric = Metric(
                    unit=pattern_variable,
                    value=Decimal(matched_value)
                )
                buffer.append(metric)

        return buffer

    def identify(self, string: str, metric: str) -> List[Metric, MetricRange]:
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
        metrics = exponential + general + scientific + pos_neg
        metric_ranges = error_range + ranges
        results = []
        return results[metrics + metric_ranges]
