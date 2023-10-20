import streamlit as st

from src.ndb import ThirdAI

# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title='ThirdAI',
                   page_icon=":bomb:",
                   layout='wide')

filenames = [
    'data/raw/2020-Scrum-Guide-US.pdf',
    'data/raw/Swissmedic_GB_2021_Layout_Englisch_ES_web.pdf',
]

if 'thirdai' not in st.session_state:
    thirdai = ThirdAI()
    thirdai.insert(filenames=filenames)
    st.session_state['thirdai'] = thirdai

# Text input
text_input = st.text_input("Enter some text")

# Text output
if text_input:
    thirdai = st.session_state['thirdai']
    results = thirdai.search(query=text_input, top_k=3)
    st.markdown('---')
    for res in results:
        st.write(f'Score: {res.score}')
        st.write(f'Source: {res.source}')
        st.write(res.text)
        st.markdown('---')
