import pandas as pd
import pydeck as pdk
import streamlit as st


def collect_types_count(data: pd.DataFrame, height: int = 500):
    for t, c in zip(st.session_state.collect_types.values(), st.columns(3)):
        count = data.loc[data[f"give_{t['en']}"], "n_collections"].sum()
        st.metric(t["fr"].capitalize(), count, height=int(height / 3), width="stretch", delta_color="normal")


def table_locations(data: pd.DataFrame) -> list[int]:
    df = data[["taux_remplissage", "city", "post_code", "start_date", "end_date"]].copy()
    data.drop(columns=["latitude", "longitude", "give_blood", "give_plasma", "give_platelet"])

    df.taux_remplissage = df.taux_remplissage / 100
    column_config = {
        "taux_remplissage": st.column_config.NumberColumn("Taux de Remplissage", format="percent", width="small"),
        "city": st.column_config.TextColumn("Ville", width="medium"),
        "post_code": st.column_config.TextColumn("CP", width="small"),
        "start_date": st.column_config.DatetimeColumn("Débute le", format="DD/MM/YYYY", width="small"),
        "end_date": st.column_config.DatetimeColumn("Fini le", format="DD/MM/YYYY", width="small"),
        "n_collections": st.column_config.NumberColumn("Nombre de collectes", format="accounting", width="small"),
        "id": st.column_config.NumberColumn(
            "Lieux ID",
            width="small",
        ),
        "collection_id": st.column_config.NumberColumn("Collecte ID", width="small"),
    }

    selected = st.dataframe(
        df, width="stretch", on_select="rerun", selection_mode="multi-row", column_config=column_config
    )
    st.session_state["selected_locations"] = selected.selection.rows


def _create_layer(data: pd.DataFrame, collect_type: str):
    df = data[data[f"give_{collect_type}"]].to_dict("records")
    return pdk.Layer(
        type="IconLayer",
        data=df,
        get_icon="icon_data",
        get_size=20,
        get_position=["longitude", "latitude"],
        get_color=[255, 0, 0, 255],  # red
        get_radius=100,
        elevation_scale=10,
        elevation_range=[200, 1000],
        pickable=True,
        extruded=True,
        coverage=1,
        auto_highlight=True,
    )


def map_locations(data: pd.DataFrame):
    df = data.copy()

    base_lat = 48.17
    base_lng = -2.9
    zoom = 7.3
    pitch = 0

    selected_locations = st.session_state.selected_locations
    if len(selected_locations) > 0:
        df = df.iloc[selected_locations]
        # base_lat = df.latitude.mean()
        # base_lng = df.longitude.mean()

    if len(st.session_state.selected_locations) == 1:
        base_lat = df.latitude.mean()
        base_lng = df.longitude.mean()
        zoom = 13
        pitch = 0

    icon_data = {
        "url": "https://upload.wikimedia.org/wikipedia/commons/f/fb/Blood_drop_plain.svg",
        "width": 150,
        "height": 150,
        "anchorY": 150,
    }
    df["icon_data"] = None
    df.icon_data = df.icon_data.apply(lambda x: icon_data)
    df.start_date = df.start_date.dt.strftime("%d/%m/%Y")
    df.end_date = df.end_date.apply(lambda x: x.strftime("%d/%m/%Y"))

    layers = [_create_layer(df, collect_type) for collect_type in ["blood", "plasma", "platelet"]]

    # View state
    view_state = pdk.ViewState(latitude=base_lat, longitude=base_lng, zoom=zoom, pitch=pitch)

    # Deck with tooltip
    deck = pdk.Deck(
        layers=layers,
        initial_view_state=view_state,
        tooltip={"text": "{full_address}\nÉvénements: {n_collections}\nDu {start_date} au {end_date}"},
        map_style="road",
    )

    return st.pydeck_chart(deck)


def hist_next_collections(data: pd.DataFrame):
    from datetime import datetime

    df = data[["start_date", "n_collections"]]
    df["semaine"] = ((df.start_date - datetime.now()).dt.days + 1) // 7
    df = df.groupby("semaine").aggregate({"semaine": "mean", "n_collections": "count"})

    df = df.rename(columns={"n_collections": "Collectes", "semaine": "Semaine"})
    st.subheader("Nombre de collectes pour les prochaines semaines")
    st.bar_chart(df, x="Semaine", y="Collectes")
