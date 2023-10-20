from typing import List

import openai
import nltk
import pandas as pd


class TextEntityGenerator:

    @staticmethod
    def apply(text: str) -> List[str]:
        return nltk.sent_tokenize(text=text)


class OpenAIEmbedder:

    def __init__(self, model: str, api_key: str):
        self._model = model
        self._api_key = api_key

    def apply(self, text_entities: List[str]) -> pd.DataFrame:
        data = openai.Embedding.create(input=text_entities, model=self._model)['data']
        return pd.DataFrame([d['embedding'] for d in data])
