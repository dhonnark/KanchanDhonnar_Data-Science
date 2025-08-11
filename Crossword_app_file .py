import streamlit as st
import time
from Crossword_DATA import puzzle
from puzzle_AI_logic import ai_solving, ai_comment1
from scoring_crossword import calculate_score

st.set_page_config(page_title="Crossword Battle Arena", layout="centered")
st.title("Welcome to the Crossword Game!")

if "solved_words" not in st.session_state:
    st.session_state.solved_words = {}
    st.session_state.player_score = 0
    st.session_state.ai_score = 0
    st.session_state.chat_log = []
    st.session_state.start_time = time.time()  

st.header("Clues")
for word in puzzle["grid"]:
    st.markdown(word['clue'])

st.subheader("Your Turn")
user_answer = st.text_input("Type your answer and press Enter").strip().lower()

if user_answer:
    player_correct = False
    for word in puzzle["grid"]:
        if word["id"] not in st.session_state.solved_words and word["answer"].lower() == user_answer:
            st.session_state.solved_words[word["id"]] = "player"

            end_time = time.time()
            score = calculate_score(st.session_state.start_time, end_time)
            st.session_state.player_score += score
            st.session_state.start_time = end_time  # reset for next round

            st.success(f"Correct! You scored {score} points for '{user_answer}'")
            st.session_state.chat_log.append(("player", f"I got '{user_answer}'! (+{score} points)"))

            player_correct = True
            break

    if not player_correct:
        st.error("Incorrect or already solved!")

    st.session_state.run_ai_turn = True
    st.experimental_rerun()


if st.session_state.get("run_ai_turn") and len(st.session_state.solved_words) < len(puzzle["grid"]):
    st.session_state.run_ai_turn = False  # Reset flag
    ai_start_time = time.time()

    st.info("Thinking...")
    word_id, answer = ai_solving(puzzle, st.session_state.solved_words.keys())
    ai_end_time = time.time()

    if word_id:
        
        st.session_state.solved_words[word_id] = "ai"

        ai_points = calculate_score(ai_start_time, ai_end_time)
        st.session_state.ai_score += ai_points

        if st.session_state.ai_score > st.session_state.player_score:
            game_state = "winning"
        else:
            game_state = "losing"

        comment = ai_comment1(answer, game_state)
        st.session_state.chat_log.append(("ai", comment))

    st.experimental_rerun()


st.subheader("Scores")
st.write(f"You: {st.session_state.player_score}")
st.write(f"AI: {st.session_state.ai_score}")


st.subheader("AI Commentary")
for sender, msg in st.session_state.chat_log[::-1]:
    st.markdown(f"**{sender.upper()}**: {msg}")


if len(st.session_state.solved_words) == len(puzzle["grid"]):
    st.success("Puzzle Completed!")
    if st.session_state.player_score > st.session_state.ai_score:
        winner = "You"
    else:
        winner = "AI"
    st.balloons()
    st.markdown(f"Winner: {winner}")
    st.stop()
