import pdftotext
from app.segmentation.core.analysis import NLTKSegmenter
from app.analysis.searchers import NumberSearcher


def test():
    with open('/Users/tatyanakrutikhina/Desktop/2.pdf', 'rb') as file:
        pdf_content = pdftotext.PDF(file)
    content = "\n\n".join(pdf_content)

    test_segmenter = NLTKSegmenter()
    test_segmentation = test_segmenter.segment(text=content)

    searcher = NumberSearcher()
    results = []

    for i in test_segmentation:
        results.append(searcher.identify(string=i.content, metric='°C'))

    with open("test.txt", "w") as txt_file:
        txt_file.write(str(results))

    return results



