from abc import ABC
from typing import Optional
import re


class Searcher(ABC):
    def identify(self, string: str, **kwargs):
        ...


class NumberSearcher(Searcher):
    def _scientific_notion(self, string: str, pattern_variable: str):
        # numbers only with "E" or "e"
        pattern = rf'[-+]?(?:\d+(?:[\.\,\d]*)?|\.\d+)[eE]' \
                  rf'(?:[-+]?\d+)?(?={pattern_variable})'
        matched_values = re.findall(pattern, string, re.IGNORECASE)
        if matched_values:
            for matched_value in matched_values:
                if ',' in matched_value:
                    matched_value = matched_value.replace(',', '.')
                matched_value = float(matched_value)
            return matched_value

    def _millions(self, string: str, pattern_variable: str):
        pattern = rf'[-+]?(?:\d+(?:[\.\,\d]*)?)(?={pattern_variable})'
        # if more than 1 comma or dot then remove
        # if 1 comma replace with dot
        matched_values = re.findall(pattern, string, re.IGNORECASE)
        if matched_values:
            for matched_value in matched_values:
                if ',' in matched_value:
                    matched_value = matched_value.replace(',', '.')
                    occurrences = matched_value.count('.')
                    if occurrences > 1:
                        matched_value = matched_value.replace('.', '')
            return float(matched_value)

    def _multiplication(self, string: str, pattern_variable: str):
        # multiply by 10
        pattern = rf'[-+]?(?:\d+(?:[\.\,\d]*)?|\.\d+)[*×]\d*\^?\d+' \
                  rf'(?={pattern_variable})'
        matched_values = re.findall(pattern, string, re.IGNORECASE)
        if matched_values:
            for matched_value in matched_values:
                if '*' in matched_value:
                    values = matched_value.split('*')
                    factor1, factor_with_degree = float(values[0]), values[1]
                    if '^' in factor_with_degree:
                        factor_with_degree = factor_with_degree.split('^')
                        factor2, degree = int(factor_with_degree[0]), \
                        int(factor_with_degree[1])
                    else:
                        # there is a trouble
                        degree = re.search(r'?<=(10\d+)', factor_with_degree)
                        factor2 = re.search(rf'?={degree}')
                    matched_value = factor1 * (factor2**degree)

            return matched_value

    # logarithm
    # range


    # def identify(self, string: str, **kwargs) -> str:
    #     pattern_variable = kwargs.get("pattern_variable")
    #     pattern = rf'[-+]?(?:\d+(?:[\.\,\d]*)?|\.\d+)' \
    #               rf'(?:[eE][-+]?\d+)?(?={pattern_variab-le})'
    #     match = re.search(
    #         pattern=pattern,
    #         string=string,
    #         flags=re.IGNORECASE
    #     )
    #     if match:
    #         matched_value = float(match.group().replace(",", ""))
    #
    #     return str()
