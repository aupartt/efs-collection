"""create_grafana_monitoring_views

Revision ID: 4882f4a1012c
Revises: 01b6400514f8
Create Date: 2025-08-31 00:30:52.292446

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import text
import os


# revision identifiers, used by Alembic.
revision: str = '4882f4a1012c'
down_revision: Union[str, Sequence[str], None] = '01b6400514f8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create monitoring views for Grafana."""
    
    grafana_user = os.getenv('POSTGRES_GRAFANA_USER', 'grafana_reader')
    
    connection = op.get_bind()
    
    # Vue pour les statistiques des tables
    connection.execute(text("""
        CREATE OR REPLACE VIEW grafana_table_stats AS
        SELECT 
            schemaname,
            relname,
            n_tup_ins as inserts,
            n_tup_upd as updates,
            n_tup_del as deletes,
            n_live_tup as live_tuples,
            n_dead_tup as dead_tuples,
            last_vacuum,
            last_autovacuum,
            last_analyze,
            last_autoanalyze
        FROM pg_stat_user_tables;
    """))
    
    # Vue pour les métriques de performance par table
    connection.execute(text("""
        CREATE OR REPLACE VIEW grafana_performance_stats AS
        SELECT 
            schemaname,
            relname,
            seq_scan,
            seq_tup_read,
            idx_scan,
            idx_tup_fetch,
            n_tup_ins + n_tup_upd + n_tup_del as total_modifications
        FROM pg_stat_user_tables;
    """))
    
    # Vue pour l'activité de la base
    connection.execute(text("""
        CREATE OR REPLACE VIEW grafana_database_activity AS
        SELECT 
            datname as database,
            numbackends as connections,
            xact_commit as transactions_committed,
            xact_rollback as transactions_rolled_back,
            blks_read as blocks_read,
            blks_hit as blocks_hit,
            tup_returned as tuples_returned,
            tup_fetched as tuples_fetched,
            tup_inserted as tuples_inserted,
            tup_updated as tuples_updated,
            tup_deleted as tuples_deleted
        FROM pg_stat_database 
        WHERE datname = current_database();
    """))
    
    # Accorder les permissions sur les vues
    connection.execute(text(f"""
        GRANT SELECT ON grafana_table_stats TO {grafana_user};
    """))
    connection.execute(text(f"""
        GRANT SELECT ON grafana_performance_stats TO {grafana_user};
    """))
    connection.execute(text(f"""
        GRANT SELECT ON grafana_database_activity TO {grafana_user};
    """))
    
    # Permissions sur les vues système utiles pour Grafana
    connection.execute(text(f"""
        CREATE VIEW grafana_database_size AS 
            SELECT pg_database_size(current_database()) as size_bytes;
    """))
    connection.execute(text(f"""
        GRANT SELECT ON pg_stat_database TO {grafana_user};
    """))
    connection.execute(text(f"""
        GRANT SELECT ON pg_stat_user_tables TO {grafana_user};
    """))
    connection.execute(text(f"""
        GRANT SELECT ON pg_stat_activity TO {grafana_user};
    """))
    connection.execute(text(f"""
        GRANT SELECT ON grafana_database_size TO {grafana_user};
    """))
    
    print("✅ Vues de monitoring créées pour Grafana")


def downgrade() -> None:
    """Drop monitoring views."""
    
    connection = op.get_bind()
    
    connection.execute(text("""
        DROP VIEW IF EXISTS grafana_table_stats;
    """))
    connection.execute(text("""
        DROP VIEW IF EXISTS grafana_performance_stats;
    """))
    connection.execute(text("""
        DROP VIEW IF EXISTS grafana_database_activity;
    """))
    
    print("🗑️ Vues de monitoring supprimées")