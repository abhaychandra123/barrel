import streamlit as st
import os
import random
from PIL import Image

# --- CONFIG ---
BARCODE_DIR = 'movie_barcodes'
GAME_TITLE = '🎬 Bardle: Guess the Movie Barcode!'

# --- HELPER FUNCTIONS ---
def get_movie_files():
    files = [f for f in os.listdir(BARCODE_DIR) if f.endswith('.png')]
    return files

def pick_round(files):
    answer = random.choice(files)
    options = [answer]
    while len(options) < 4:
        opt = random.choice(files)
        if opt not in options:
            options.append(opt)
    random.shuffle(options)
    return answer, options

def clean_title(filename):
    return os.path.splitext(filename)[0]

# --- SESSION STATE ---
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'streak' not in st.session_state:
    st.session_state.streak = 0
if 'round' not in st.session_state:
    st.session_state.round = 0
if 'answer' not in st.session_state or 'options' not in st.session_state:
    files = get_movie_files()
    answer, options = pick_round(files)
    st.session_state.answer = answer
    st.session_state.options = options
    # st.session_state.round += 1
if 'selected' not in st.session_state:
    st.session_state.selected = None
if 'show_next' not in st.session_state:
    st.session_state.show_next = False
if 'answered' not in st.session_state:
    st.session_state.answered = False

# --- UI STYLING ---
st.set_page_config(page_title=GAME_TITLE, page_icon='🎬', layout='centered')
st.markdown("""
    <style>
    .bardle-btn {
        display: block;
        width: 100%;
        padding: 1em;
        margin: 0.5em 0;
        font-size: 1.2em;
        font-weight: bold;
        border-radius: 10px;
        border: 2px solid #4B8BBE;
        background: #f5f6fa;
        color: #222;
        transition: 0.2s;
        cursor: pointer;
    }
    .bardle-btn:hover {
        background: #4B8BBE;
        color: #fff;
        border: 2px solid #222;
    }
    .bardle-center { text-align: center; }
    </style>
""", unsafe_allow_html=True)

st.markdown(f"<h1 class='bardle-center' style='color:#4B8BBE; font-size:3em;'>{GAME_TITLE}</h1>", unsafe_allow_html=True)
st.markdown("<p class='bardle-center' style='color:#FFFFFF; font-size:1.2em;'>Can you guess the movie from its barcode? One guess per round. Try to keep your streak going! 🔥</p>", unsafe_allow_html=True)

# --- GAME LOGIC ---
files = get_movie_files()
image_path = os.path.join(BARCODE_DIR, st.session_state.answer)
image = Image.open(image_path)
st.image(image, use_container_width=True, caption='Which movie is this?')

# --- OPTIONS ---
if st.session_state.selected is None:
    for opt in st.session_state.options:
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
        else:
            st.session_state.streak = 0
        st.session_state.answered = True
    if st.session_state.selected == st.session_state.answer:
        st.success(f"✅ Correct! It's '{clean_title(st.session_state.selected)}'!")
    else:
        st.error(f"❌ Oops! That was '{clean_title(st.session_state.selected)}'. The correct answer was '{clean_title(st.session_state.answer)}'.")
    st.markdown(f"<h3 class='bardle-center'>Score: {st.session_state.score} | Streak: {st.session_state.streak}</h3>", unsafe_allow_html=True)
    if st.session_state.show_next:
        if st.button('Next ▶️', key='next-btn', use_container_width=True):
            answer, options = pick_round(files)
            st.session_state.answer = answer
            st.session_state.options = options
            st.session_state.selected = None
            st.session_state.show_next = False
            st.session_state.answered = False
            st.rerun()

if st.session_state.selected is None:
    st.markdown(f"<h3 class='bardle-center' style='color:#888;'>Score: {st.session_state.score} | Streak: {st.session_state.streak}</h3>", unsafe_allow_html=True)

# --- FOOTER ---
st.markdown("<hr style='margin-top:2em;'/>", unsafe_allow_html=True)
