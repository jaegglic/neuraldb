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


class OpenAISummarizer:

    _task = "I want you to act like a most rational person that only give answers for which he has strong evidence. " \
            "Therefore, I don't want you to give me any information that is not contained in the provided context. " \
            "Please just summarize the context with respect to the asked question in simple words. If there is no " \
            "related information in the context please inform me accordingly. Keep the simplification in the " \
            "original language of the context that is provided."

    def __init__(self, model: str, api_key: str):
        self._model = model
        self._api_key = api_key

    def _get_messages(self, human_text: str, context: List[str]) -> List[dict]:
        cntxt = '\n\n'.join(context)
        messages = [
            {"role": "system", "content": self._task},
            {"role": "system", "content": f'Context: {cntxt}'},
        ]

        # Add final message
        msg = f'Briefly summarize the above context with respect to the following message: "{human_text}". ' \
              f'Write your summary in the same language as the given message.'
        messages.append({'role': 'user', 'content': msg})
        return messages

    def apply(self, human_text: str, context: List[str]) -> str:
        messages = self._get_messages(human_text=human_text, context=context)
        response = openai.ChatCompletion.create(
            model=self._model,
            messages=messages,
            api_key=self._api_key,
        )
        return response["choices"][0]["message"]["content"]
