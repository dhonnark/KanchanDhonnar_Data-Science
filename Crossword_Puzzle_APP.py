import streamlit as st
import time
from Crossword_DATA import puzzle
from puzzle_AI_logic import ai_solving, ai_comment1
from scoring_crossword import calculate_score

st.set_page_config(page_title="Crossword Battle Arena", layout="centered")
st.title("Welcome to the Crossword Game!")

# Initialize session state variables
if "solved_words" not in st.session_state:
    st.session_state.solved_words = {}
    st.session_state.player_score = 0
    st.session_state.ai_score = 0
    st.session_state.chat_log = []
    st.session_state.start_time = time.time()
if "user_input" not in st.session_state:
    st.session_state.user_input = ""
if "run_ai_turn" not in st.session_state:
    st.session_state.run_ai_turn = False

st.header("Clues")
for word in puzzle["grid"]:
    st.markdown(word['clue'])

st.subheader("Your Turn")

# --- FIXED: Use callback to handle answer and clear input safely ---
def handle_answer():
    user_answer = st.session_state.user_input.strip().lower()
    if not user_answer:
        return
    player_correct = False
    for word in puzzle["grid"]:
        if word["id"] not in st.session_state.solved_words and word["answer"].lower() == user_answer:
            st.session_state.solved_words[word["id"]] = "player"

            end_time = time.time()
            score = calculate_score(st.session_state.start_time, end_time)
            st.session_state.player_score += score
            st.session_state.start_time = end_time  # reset for next round

            st.session_state.chat_log.append(("player", f"I got '{user_answer}'! (+{score} points)"))
            st.session_state.last_feedback = ("success", f"Correct! You scored {score} points for '{user_answer}'")

            player_correct = True
            break

    if not player_correct:
        st.session_state.last_feedback = ("error", "Incorrect or already solved!")

    # Clear input and trigger AI turn
    st.session_state.user_input = ""
    st.session_state.run_ai_turn = True

# Text input with callback
st.text_input("Type your answer and press Enter", key="user_input", on_change=handle_answer)

# Show one-time feedback if present
if "last_feedback" in st.session_state:
    kind, msg = st.session_state.last_feedback
    if kind == "success":
        st.success(msg)
    else:
        st.error(msg)
    del st.session_state.last_feedback

# --- AI turn logic ---
if st.session_state.get("run_ai_turn") and len(st.session_state.solved_words) < len(puzzle["grid"]):
    st.session_state.run_ai_turn = False  # Reset flag
    ai_start_time = time.time()

    st.info("Thinking...")
    word_id, answer = ai_solving(puzzle, st.session_state.solved_words.keys())
    ai_end_time = time.time()

    if word_id:
        st.session_state.solved_word
