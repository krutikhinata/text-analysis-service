from json import dumps

import pdftotext

from app.analysis.converters import Converter
from app.analysis.searchers import NumberSearcher
from app.segmentation.core.analysis import NLTKSegmenter


def test():
    with open('app/segmentation/tests/data/2.pdf', 'rb') as file:
        pdf_content = pdftotext.PDF(file)
    content = "\n\n".join(pdf_content)

    test_segmenter = NLTKSegmenter()
    test_segmentation = test_segmenter.segment(text=content)

    searcher = NumberSearcher()

    # Input
    # |  Name  |  mapping  |
    # | length |   jsonb   |

    # Output
    # | doc_ref | sentence | tsv_vector |      found     |
    # |    FK   |  varchar |  gin index | array[decimal] |

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

    results = []
    for metric in ["nm"]:
        for sentence_item in test_segmentation:
            sentence, floats = searcher.identify(
                string=sentence_item.content,
                metric=metric
            )

            if floats:
                sentence_repr = " ".join(sentence_item.content.split())

                found = ", ".join([str(i) for i in floats])
                converted = [converter.to_std(i, metric) for i in floats]

                results.append(
                    {
                        "sentence": sentence_repr,
                        "found": found,
                        "converted": converted
                    }
                )

    with open("app/segmentation/tests/data/results.json", "w") as file:
        file.write(dumps(results, indent=2))
