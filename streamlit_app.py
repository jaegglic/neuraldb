import os

from dotenv import load_dotenv
import streamlit as st

from src.gpt import OpenAISummarizer
from src.ndb import ThirdAI

load_dotenv()

# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title='ThirdAI',
                   page_icon=":bomb:",
                   layout='wide')

filenames = [
    'data/raw/2020-Scrum-Guide-US.pdf',
    'data/raw/Swissmedic_GB_2021_Layout_Englisch_ES_web.pdf',
]

if 'thirdai' not in st.session_state:
    thirdai_api_key = os.getenv('THIRDAI_KEY')
    thirdai = ThirdAI(api_key=thirdai_api_key)
    thirdai.insert(filenames=filenames)
    st.session_state['thirdai'] = thirdai

if 'summarizer' not in st.session_state:
    openai_model = os.getenv('OPENAI_CHAT_MODEL')
    openai_api_key = os.getenv('OPENAI_API_KEY')
    summarizer = OpenAISummarizer(model=openai_model, api_key=openai_api_key)
    st.session_state['summarizer'] = summarizer

# Text input
text_input = st.text_input("Ask something...")

# Text output
if text_input:
    thirdai = st.session_state['thirdai']
    results = thirdai.search(query=text_input, top_k=3)

    st.markdown('---')
    for res in results:
        st.write(f'Score: {res.score:.3f} | Source: {res.source}')
        st.write(res.text)
        st.markdown('---')

    if st.button('Summarize'):
        context = [res.text for res in results]
        summarizer = st.session_state['summarizer']
        answer = summarizer.apply(human_text=text_input, context=context)

        st.write(answer)


