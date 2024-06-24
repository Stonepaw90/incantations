import random
import string
import streamlit as st
import time

def get_dictionary():
  word_file = open("words_alpha.txt")
  words = word_file.readlines()
  word_file.close()
  #no_duplicates = [i[:-1] for i in words if len(set(i[:-1])) == word_len & len(i[:-1]) == word_len]
  no_duplicates = [i[:-1] for i in words]
  return no_duplicates

def blue_bold(text):
    return f"<span style='font-size: 24px; color: #3A96DD;'><b>{text}</b></span>"

def title_blue(text):
    return f"<span style='font-size: 38px; color: #3A96DD;'><b>{text}</b></span>"



def write_text(text, font_size = 24,
               header_size = None,
               alignment = "left",
               text_color = "black",
               font_family = "Source Sans Pro"):#"sans-serif"):
    if header_size is None:
        tag = "span"
        size_text = f"font-size: {font_size}px; "
    else:
        tag = f"h{header_size}"
        size_text = ""
    st.markdown(f"<{tag} style='"
                    f"{size_text}"
                    f"text-align: {alignment}; "
                    f"font-family: {font_family}; "
                    f"color: {text_color};'"
                f">{text}</{tag}>",
                unsafe_allow_html=True)



ALPHABET = set(string.ascii_lowercase)
# Dictionary of Scrabble letter values
scrabble_scores = {
    'A': 1, 'B': 3, 'C': 3, 'D': 2, 'E': 1, 'F': 4, 'G': 2,
    'H': 4, 'I': 1, 'J': 8, 'K': 5, 'L': 1, 'M': 3, 'N': 1,
    'O': 1, 'P': 3, 'Q': 10, 'R': 1, 'S': 1, 'T': 1, 'U': 1,
    'V': 4, 'W': 4, 'X': 8, 'Y': 4, 'Z': 10
}
WORD_BANK = get_dictionary()


class Tiles:
    def __init__(self, tiles = None):
        self.banned = random.choice(list(ALPHABET))
        self.newA = ALPHABET.difference(self.banned)
        if tiles is None:
            self.Tiles = set(random.sample(list(self.newA), 11))
        else:
            self.Tiles = set(tiles)

    def __add__(self, other):
        #self.Tiles = self.Tiles.union(set(other))
        return Tiles(self.Tiles.union(set(other)))

    def __sub__(self, other):
        #self.Tiles = self.Tiles.difference(set(other))
        return Tiles(self.Tiles.difference(set(other)))

    def draw(self, k):
        legal_draw = self.newA.difference(self.Tiles)
        return random.sample(list(legal_draw), k = k)

    def exchange(self, old_letters):
        new_letters = self.draw( k = len(set(old_letters)))
        st.subheader("You draw the new letters:")
        self.display(new_letters)
        return (self - old_letters) + new_letters

    def asList(self):
        return sorted(self.Tiles)

    def __str__(self):
        return f"Tiles: {sorted(self.Tiles)}\n" \
               f"Banned: {self.banned}\n"
        #return sorted(self.Tiles)

    def display_11(self):
        self.display(letters = sorted(self.Tiles))

    def display(self, letters):
        cols = st.columns(3)
        for i in range(min(11, len(letters))):
            upper_letter = str.upper(letters[i])
            if upper_letter in ["A", "E", "I", "O", "U"]:
                upper_letter = blue_bold(upper_letter)
            with cols[i%3]:
                write_text(upper_letter)

    def check_spell(self, spell):
        return all([let in self.Tiles for let in spell])
        #letter_good = [spell.count(i) <= self.Tiles.count(i) for i in self.Tiles]



def init_session_state(dict_name, dict_val):
    if dict_name not in st.session_state:
        st.session_state[dict_name] = dict_val

def initialize_whole_session_state():
    init_session_state("timer", 60)
    init_session_state("BANK", Tiles())
    init_session_state("SCORE", 0)
    init_session_state("spell", '')
    init_session_state("spell_widget", '')
