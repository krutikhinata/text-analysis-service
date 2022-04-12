from typing import Dict


class Converter:
    def __init__(self, mapping: Dict[str, float]):
        self.mapping = mapping

    def _calculate(self, value: float, metric: str, operator: str) -> float:
        coefficient = self.mapping[metric]
        value = eval(f"{value} {operator} {coefficient}")

        return value

    def to_std(self, value: float, metric: str) -> float:
        return self._calculate(value=value, metric=metric, operator=" / ")

    def from_std(self, value: float, metric: str) -> float:
        return self._calculate(value=value, metric=metric, operator=" * ")
