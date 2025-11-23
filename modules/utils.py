import re
from modules import config

def valid_email(e):
    return re.match(r"[^@]+@[^@]+\.[^@]+", e)


def style_achieved_streak(row, reward_threshold):
    # This function is applied to EACH ROW (axis=1) of the DataFrame
    
    # Check if the streak is achieved
    # Convert both to string for consistent comparison, as done previously
    is_achieved = str(row["Streak"]).startswith(str(reward_threshold))
    
    # Define the styling
    if is_achieved:
        # Returns a list of strings: ['background-color: yellow'] for every cell in the row
        return ['background-color: ' + config.STREAK_HIGHLIGHT] * len(row) 
    else:
        # Returns an empty string for every cell (no styling)
        return [''] * len(row)
