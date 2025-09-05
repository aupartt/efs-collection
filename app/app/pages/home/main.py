import streamlit as st

from .panels import collect_types_count, hist_next_collections, map_locations, table_locations
from .services import get_locations_data


def display_page():
    try:
        data = get_locations_data()

        st.title("Futures collectes mobiles (EFS) en Bretagne.")

        # Row 1: Global locations details and filter
        c1, c2 = st.columns([4, 2])
        with c1:
            table_locations(data)
        with c2:
            hist_next_collections(data)

        # Filter 1 on collections
        df = data.copy()
        if len(st.session_state["selected_locations"]) > 0:
            df = df.iloc[st.session_state.selected_locations]

        # Row 2: Global locations visulization
        c1, c2 = st.columns([1, 9], gap=None)
        with c1:
            collect_types_count(df, height=500)
        st.text(st.session_state.selected_locations)
        with c2:
            map_locations(data)

    except Exception as e:
        print(f"Something went wrong: {e}")
        raise e
