import os

from dotenv import load_dotenv
import pandas as pd

from src.scraping import TikaExtractor
from src.gpt import TextEntityGenerator, OpenAIEmbedder

load_dotenv()

if __name__ == '__main__':
    filename = 'data/raw/2020-Scrum-Guide-US.pdf'
    tika_url = os.getenv('TIKA_URL')
    openai_engine = os.getenv('OPENAI_ENGINE')
    openai_model = os.getenv('OPENAI_MODEL')
    openai_api_key = os.getenv('OPENAI_API_KEY')

    text = TikaExtractor(url=tika_url).apply(filename=filename)
    text_entities = TextEntityGenerator().apply(text=text)
    embeddings = OpenAIEmbedder(model=openai_model, api_key=openai_api_key).apply(text_entities=text_entities)
    df = pd.DataFrame.fro
