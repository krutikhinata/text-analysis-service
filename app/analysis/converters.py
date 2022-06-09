from decimal import Decimal
from typing import Dict


class Converter:
    def __init__(self, mapping: Dict[str, Decimal]):
        self.mapping = mapping

    def _calculate(
            self,
            value: Decimal,
            metric: str,
            operator: str
    ) -> Decimal:
        coefficient = self.mapping[metric]
        value = eval(f"{value} {operator} {coefficient}")

        return value

    def to_std(self, value: Decimal, metric: str) -> Decimal:
        return self._calculate(value=value, metric=metric, operator=" / ")

    def from_std(self, value: Decimal, metric: str) -> Decimal:
        return self._calculate(value=value, metric=metric, operator=" * ")
