
import time
import random
import requests
import streamlit as st

HF_API_KEY = st.secrets["HF_API_KEY"]
API_URL = "https://api-inference.huggingface.co/models/gpt2"
HEADERS = {"Authorization": f"Bearer {HF_API_KEY}"}

def ai_solving(puzzle, solved_ids):
    unsolved = []
    for w_id in puzzle["grid"]:
        if w_id["id"] not in solved_ids:
            unsolved.append(w_id)
    if not unsolved:
        return None, None
    chosen = random.choice(unsolved)
    time.sleep(random.randint(3, 8))
    return chosen["id"], chosen["answer"]

client = None

def ai_comment1(word, game_state):
    prompt = f"""
    You are a playful AI opponent in a crossword game.
    You just solved the word '{word}'.
    You are currently {game_state} the game.
    Respond in ONE short, witty sentence.
    """

    if client is None:
        # Call Hugging Face API instead of OpenAI
        payload = {"inputs": prompt}
        response = requests.post(API_URL, headers=HEADERS, json=payload)
        result = response.json()
        if isinstance(result, list) and len(result) > 0:
            return result[0]["generated_text"].strip()
        return f"(Mock AI) I solved '{word}' and I'm {game_state}!"
   
    # Keeping your original structure for compatibility
    return f"(Mock AI) I solved '{word}' and I'm {game_state}!"

