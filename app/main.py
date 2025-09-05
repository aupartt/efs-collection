import streamlit as st

from app.core.settings import settings
from app.pages.home import display_page


def init():
    st.set_page_config(page_title="Home", page_icon="🌍", layout="wide")
    if len(st.session_state.keys()) == 0:
        st.session_state.update(settings.ST_SESSION_STATE)


def main():
    try:
        init()
        display_page()
    except Exception as e:
        print(f"ERROR: {e}")
        raise e


if __name__ == "__main__":
    main()
