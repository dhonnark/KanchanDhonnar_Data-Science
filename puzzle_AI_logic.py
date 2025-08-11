import openai
import time
import random
import textwrap


def ai_solving(puzzle, solved_ids):

    unsolved=[]
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
        
        return f"(Mock AI) I solved '{word}' and I'm {game_state}!"
   
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=50,
        temperature=0.8
    )
    return response.choices[0].message.content.strip()
