import streamlit as st
import time
from Crossword_DATA import puzzle
from puzzle_AI_logic import ai_solving, ai_comment1
from scoring_crossword import calculate_score

st.set_page_config(page_title="Crossword Battle Arena", layout="centered")
st.title("Welcome to the Crossword Game!")

# --- Session State Setup ---
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

# --- Show Clues ---
st.header("Clues")
for word in puzzle["grid"]:
    st.markdown(word['clue'])

# --- Handle Player Answer ---
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

    st.session_state.user_input = ""
    st.session_state.run_ai_turn = True

st.text_input("Type your answer and press Enter", key="user_input", on_change=handle_answer)

if "last_feedback" in st.session_state:
    kind, msg = st.session_state.last_feedback
    if kind == "success":
        st.success(msg)
    else:
        st.error(msg)
    del st.session_state.last_feedback

# --- AI Turn ---
if st.session_state.get("run_ai_turn") and len(st.session_state.solved_words) < len(puzzle["grid"]):
    st.session_state.run_ai_turn = False
    ai_start_time = time.time()

    st.info("Thinking...")
    word_id, answer = ai_solving(puzzle, st.session_state.solved_words.keys())
    ai_end_time = time.time()

    if word_id:
        st.session_state.solved_words[word_id] = "ai"

        ai_points = calculate_score(ai_start_time, ai_end_time)
        st.session_state.ai_score += ai_points

        game_state = "winning" if st.session_state.ai_score > st.session_state.player_score else "losing"
        comment = ai_comment1(answer, game_state)
        st.session_state.chat_log.append(("ai", comment))

    st.rerun()

# --- Display Crossword Grid ---
size = puzzle["grid_size"]
display_grid = []
for _ in range(size):
    row_list = []
    for _ in range(size):
        row_list.append("")
    display_grid.append(row_list)

# Fill solved words
for word in puzzle["grid"]:
    if word["id"] in st.session_state.solved_words:
        row, col = word["row"], word["col"]
        dr, dc = (0, 1) if word["direction"] == "across" else (1, 0)
        for j, letter in enumerate(word["answer"].upper()):
            display_grid[row + dr * j][col + dc * j] = letter

# Render grid
for row_list in display_grid:
    row_display = []
    for cell in row_list:
        row_display.append(cell if cell else "⬜")
    st.write(" ".join(row_display))

# --- Scores ---
st.subheader("Scores")
st.write(f"You: {st.session_state.player_score}")
st.write(f"AI: {st.session_state.ai_score}")

# --- AI Commentary ---
st.subheader("AI Commentary")
for sender, msg in st.session_state.chat_log[::-1]:
    st.markdown(f"**{sender.upper()}**: {msg}")

# --- End Game ---
if len(st.session_state.solved_words) == len(puzzle["grid"]):
    st.success("Puzzle Completed!")
    winner = "You" if st.session_state.player_score > st.session_state.ai_score else "AI"
    st.balloons()
    st.markdown(f"Winner: {winner}")
    st.stop()
