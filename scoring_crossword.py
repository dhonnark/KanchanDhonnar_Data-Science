def calculate_score(start_time, end_time,constant_time=8):
    elapsed = end_time - start_time
    base_score = 1
    time_bonus = max(0, int(constant_time - elapsed)) 
    return base_score + time_bonus