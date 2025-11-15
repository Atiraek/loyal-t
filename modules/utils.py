import re

def valid_email(e):
    return re.match(r"[^@]+@[^@]+\.[^@]+", e)
