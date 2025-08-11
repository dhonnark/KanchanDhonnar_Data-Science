import random

all_words = [
        {"id": 1, "answer": "apple", "clue": "Fruit with which Newton theory started"},
        {"id": 2, "answer": "car", "clue": "Similar word to vehicle"},
        {"id": 3, "answer": "red", "clue": "Color in a rainbow starts with R"},
        {"id": 4, "answer": "blue", "clue": "Color in a rainbow starts with B"},
        {"id": 5, "answer": "rose", "clue": "Red flower with a fragrance"},
        {"id": 6, "answer": "sky", "clue": "Where stars are"},
        {"id": 7, "answer": "bed", "clue": "We sleep on it"},
        {"id": 8, "answer": "cat", "clue": "Pet animal who eats rats"},
        {"id": 9, "answer": "mirror", "clue": "Where we see our reflection"},
        {"id": 10, "answer": "black", "clue": "Color of your hair"},
        {"id": 11, "answer": "water", "clue": "Everyone drinks it daily"},
        {"id": 12, "answer": "green", "clue": "Color in a rainbow starts with G"},
        {"id": 13, "answer": "baby", "clue": "Dearest to a mother"},
        {"id": 14, "answer": "time", "clue": "Related to clock"},
        {"id": 15, "answer": "pen", "clue": "We use it for writing"},
        {"id": 16, "answer": "bird", "clue": "Living thing that flies"},
        {"id": 17, "answer": "ball", "clue": "Round object used to play cricket"},
        {"id": 18, "answer": "panda", "clue": "Popular animal of China"},
]
puzzle_words=random.sample(all_words,6)

puzzle={"grid":puzzle_words}
