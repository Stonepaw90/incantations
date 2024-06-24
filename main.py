from helper_functions import *


st.set_page_config(page_title = "Incantations",
                   page_icon=":male_mage:",
                   layout="wide",
                   #initial_sidebar_state="collapsed",
                   menu_items={"about":"Created by :mage: Abraham Holleran and the Nigros :male_mage: :female_mage:."})

def calculate_scrabble_score(word):
    #Calculate the Scrabble score for a given word.
    score = 0
    for letter in word.upper():
        if letter in scrabble_scores:
            score += scrabble_scores[letter]
    return score

def start_timer(duration):
    #con = st.container()
    while duration:
        mins, secs = divmod(duration, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        st.toast(f"⏳ Time Remaining: {timer}")
        time.sleep(1)
        duration -= 1
        #con.empty()


def intro():
    st.markdown(f"<span style = 'font_size: 24px;'><h1>:male_mage: Inc{title_blue('a')}nt{title_blue('a')}t{title_blue('io')}ns</h1></span>", unsafe_allow_html = True)

    cols = st.columns([10,12])
    with cols[1]:
        write_text(
          f"Banned letter: <span style='font-size: 60px; color: #3A96DD;'>{str.upper(st.session_state.BANK.banned)}</span>",
          header_size=1)
    with cols[0]:
        write_text(f"Score: <span style='font-size: 60px; color: #3A96DD;'>{st.session_state.SCORE}</span>", header_size=1)

def submit():
    st.session_state.spell = st.session_state.spell_widget
    st.session_state.spell_widget = ''

def cast_spell():
    st.text_input(":sparkles: Cast your spell, or enter two letter to exchange them.", key = "spell_widget", on_change=submit, value='')
    input_word = st.session_state.spell
    if len(input_word) == 0:
        pass
    elif not st.session_state.BANK.check_spell(input_word):
        st.write(f"The spell fizzles out :face_with_spiral_eyes:. You need to only use letters from your tile bank, {st.session_state.BANK.asList()}.")

    elif len(input_word) == 1:
        st.warning("Your spell must be at least three letters long.")

    elif (len(input_word) == 2) and (len(set(input_word)) == 2): #"dad" and "aa" do not work but "ad" does
        st.session_state.BANK = st.session_state.BANK.exchange(input_word)
        st.session_state.spell = ''
        time.sleep(2)

        st.rerun()

    elif input_word in WORD_BANK:
        word_score = calculate_scrabble_score(input_word)
        st.session_state.SCORE += word_score
        emoji = random.choice(["comet", "sparkler", "firewords", "stars", "star2", "boom", "fire"])
        st.markdown(
            f":sparkles: You cast {blue_bold(input_word.upper() + '!')} :{emoji}: Your score increases by {word_score}.",
            unsafe_allow_html=True)
        st.session_state.BANK = st.session_state.BANK.exchange(input_word)
        st.session_state.spell = ''
        time.sleep(2)
        st.rerun()

    else:
        st.warning("That's not a word.")

    return input_word

    #what_letters_lose = set(st.text_input(":heavy_exclamation_mark: Panic! Trade two letters for new ones."))

def trade():
    with st.form("Tradein2"):
        what_letters_lose = st.multiselect(
            ":arrows_clockwise: Select two letters to trade-in for new ones.",
            st.session_state.BANK.asList(),
            default=[],
            max_selections=2
        )
        if st.form_submit_button("Submit"):
            if len(set(what_letters_lose)) == 2:
                st.session_state.BANK = st.session_state.BANK.exchange(what_letters_lose)
            elif len(what_letters_lose) != 0:
                st.warning("Select two tiles to trade in.")


def main():
    initialize_whole_session_state()

    intro()
    st.header("Your letters are:")
    st.session_state.BANK.display_11()
    input = cast_spell()

if __name__ == '__main__':
    main()