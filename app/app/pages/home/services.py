import pandas as pd
import streamlit as st
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.database import tables, with_session


@st.cache_data
@with_session
def get_locations_data(session: Session) -> pd.DataFrame:
    # Subquery next collection event (for each locations)
    cg_subquery = (
        select(
            tables.collection_groups.c.id,
            tables.collection_groups.c.location_id,
            tables.collection_groups.c.start_date,
            tables.collection_groups.c.end_date,
            func.row_number()
            .over(
                partition_by=tables.collection_groups.c.location_id,
                order_by=tables.collection_groups.c.start_date,
            )
            .label("row_number"),
            func.count().over(partition_by=tables.collection_groups.c.location_id).label("n_collections"),
        ).where(tables.collection_groups.c.end_date >= func.now())
    ).subquery()

    next_cg = select(cg_subquery).where(cg_subquery.c.row_number == 1).subquery()

    # Subquery last snapshot (for each NEXT collection groups)
    snap_subquery = (
        select(
            tables.collection_group_snapshots,
            func.row_number()
            .over(
                partition_by=tables.collection_group_snapshots.c.collection_group_id,
                order_by=tables.collection_group_snapshots.c.created_at.desc(),
            )
            .label("row_number"),
        ).join(next_cg, next_cg.c.id == tables.collection_group_snapshots.c.collection_group_id)
    ).subquery()
    latest_snap = select(snap_subquery).where(snap_subquery.c.row_number == 1).subquery()

    # Query the locations details with the next collections and the last taken snapshot
    query = (
        select(
            tables.locations.c.id,
            tables.locations.c.full_address,
            tables.locations.c.city,
            tables.locations.c.post_code,
            tables.locations.c.latitude,
            tables.locations.c.longitude,
            tables.locations.c.give_blood,
            tables.locations.c.give_plasma,
            tables.locations.c.give_platelet,
            next_cg.c.id.label("collection_id"),
            next_cg.c.start_date,
            next_cg.c.end_date,
            next_cg.c.n_collections,
            latest_snap.c.taux_remplissage,
        )
        .join(tables.locations, tables.locations.c.id == next_cg.c.location_id)
        .outerjoin(latest_snap, latest_snap.c.collection_group_id == next_cg.c.id)
        .where(next_cg.c.end_date >= func.current_date(), func.extract("day", next_cg.c.start_date - func.now()) <= 60)
    )

    query = query.order_by(next_cg.c.start_date)
    query = query.limit(st.session_state["limit"])

    result = session.execute(query).all()
    return pd.DataFrame(result)
