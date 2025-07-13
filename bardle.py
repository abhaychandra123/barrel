import streamlit as st
import pandas as pd
import random

# --- CONFIG ---
CSV_PATH = 'movie_barcodes_urls.csv'
GAME_TITLE = '🎬 Bardle: Guess the Movie Barcode!'

# --- LOAD DATA ---
@st.cache_data
def load_data():
    df = pd.read_csv(CSV_PATH, header=None, names=['filename', 'url'])
    return df

df = load_data()

# --- HELPER FUNCTIONS ---
def pick_round(df):
    answer_row = df.sample(1).iloc[0]
    answer = answer_row['filename']
    answer_url = answer_row['url']
    options = [answer]
    while len(options) < 4:
        opt = df.sample(1).iloc[0]['filename']
        if opt not in options:
            options.append(opt)
    random.shuffle(options)
    return answer, answer_url, options

def clean_title(filename):
    return filename.replace('.png', '')

# --- SESSION STATE ---
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'streak' not in st.session_state:
    st.session_state.streak = 0
if 'round' not in st.session_state:
    st.session_state.round = 1
if 'answer' not in st.session_state:
    answer, answer_url, options = pick_round(df)
    st.session_state.answer = answer
    st.session_state.answer_url = answer_url
    st.session_state.options = options
if 'selected' not in st.session_state:
    st.session_state.selected = None
if 'show_next' not in st.session_state:
    st.session_state.show_next = False
if 'answered' not in st.session_state:
    st.session_state.answered = False

# --- UI ---
st.markdown(f"<h1 style='text-align:center;'>{GAME_TITLE}</h1>", unsafe_allow_html=True)
st.markdown(f"<div style='text-align:center;font-size:1.2em;'>Round <b>{st.session_state.round}</b> &nbsp;|&nbsp; Score: <b>{st.session_state.score}</b> &nbsp;|&nbsp; Streak: <b>{st.session_state.streak}</b></div>", unsafe_allow_html=True)
st.markdown("<br>")

# --- SHOW IMAGE ---
st.image(st.session_state.answer_url, use_container_width=True, caption='Which movie is this?')
st.markdown("<br>")

# --- GAME LOGIC ---
if st.session_state.selected is None:
    cols = st.columns(2)
    for i, opt in enumerate(st.session_state.options):
        with cols[i % 2]:
            if st.button(clean_title(opt), key=opt, help='Choose this movie', use_container_width=True):
                st.session_state.selected = opt
                st.session_state.show_next = True
                st.session_state.answered = False
                st.rerun()
else:
    # --- FEEDBACK ---
    if not st.session_state.answered:
        if st.session_state.selected == st.session_state.answer:
            st.session_state.score += 1
            st.session_state.streak += 1
            st.session_state.feedback = '✅ **Correct!**'
        else:
            st.session_state.streak = 0
            st.session_state.feedback = f'❌ **Wrong!** The answer was: {clean_title(st.session_state.answer)}'
        st.session_state.answered = True
    st.markdown(f"<div style='text-align:center;font-size:1.5em;'>{st.session_state.feedback}</div>", unsafe_allow_html=True)
    st.markdown("<br>")
    if st.button('Next ▶️', key='next-btn', use_container_width=True):
        answer, answer_url, options = pick_round(df)
        st.session_state.answer = answer
        st.session_state.answer_url = answer_url
        st.session_state.options = options
        st.session_state.round += 1
        st.session_state.selected = None
        st.session_state.show_next = False
        st.session_state.answered = False
        st.rerun()

# --- STYLING ---
st.markdown("""
<style>
    .stButton>button {
        font-size: 1.2em;
        padding: 0.75em 1.5em;
        margin: 0.5em 0.5em;
        border-radius: 8px;
        border: 2px solid #222;
        background: #f7f7f7;
        transition: 0.2s;
        font-weight: bold;
    }
    .stButton>button:hover {
        background: #ffe066;
        color: #222;
        border: 2px solid #ffe066;
        box-shadow: 0 0 8px #ffe06644;
    }
</style>
""", unsafe_allow_html=True)
