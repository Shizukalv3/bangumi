import re

def get_genre(input_str):
    genre_match=re.search(r'\/.*?\/(.*)', input_str)
    if genre_match:
        genre = genre_match.group(1)
        return genre
    else:
        pass
