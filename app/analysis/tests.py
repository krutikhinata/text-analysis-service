import re
from app.analysis.converters import Converter


def test_length_index():
    mapping = {
        "µm": 1e+6,
        "nm": 1e+9,
        "mm": 1000,
        "cm": 100,
        "dm": 10,
        "m": 1,
        "km": .001
    }

    converter = Converter(mapping=mapping)

    string = "The diameter of the pipe is 1.5km."

    for metric in mapping.keys():
        pattern = rf'[-+]?(?:\d+(?:[\.\,\d]*)?|\.\d+)' \
                  rf'(?:[eE][-+]?\d+)?(?={metric})'
        match = re.search(
            pattern=pattern,
            string=string,
            flags=re.IGNORECASE
        )

        if match:
            matched_value = float(match.group())
            value = converter.to_std(
                value=matched_value,
                metric=metric
            )

            print(
                f"Identified: {matched_value} {metric}\n"
                f"\tTransformed to: {value} m"
            )
