import os
import re

from tika import parser


class TikaExtractor:
    """Text extractors for pdfs using tika."""

    def __init__(self, url: str):
        self._tika_url = url

    @staticmethod
    def _clean_text(text: str) -> str:
        return re.sub(r'\n\s*', '\n', text)

    def apply(self, filename: str) -> str:
        """Extracting the text from pdfs."""
        parsed = parser.from_file(filename=filename)
        text = parsed['content']
        return self._clean_text(text=text)


if __name__ == '__main__':
    filename = 'data/raw/2020-Scrum-Guide-US.pdf'
    url = os.getenv('TIKA_URL')

    text = TikaExtractor(url=url).apply(filename=filename)
    print(text)
