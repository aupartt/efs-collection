"""create_grafana_user

Revision ID: 01b6400514f8
Revises: a8c4c6d8cc51
Create Date: 2025-08-31 00:07:05.266305

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import text
import os


# revision identifiers, used by Alembic.
revision: str = '01b6400514f8'
down_revision: Union[str, Sequence[str], None] = 'a8c4c6d8cc51'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create Grafana read-only user with appropriate permissions."""
    
    # Récupération des variables d'environnement
    grafana_user = os.getenv('POSTGRES_GRAFANA_USER', 'grafana_reader')
    grafana_password = os.getenv('POSTGRES_GRAFANA_PASSWORD', 'grafana_password')
    database_name = os.getenv('POSTGRES_DB', 'mydb')
    
    # Obtenir la connexion
    connection = op.get_bind()
    
    # 1. Créer l'utilisateur s'il n'existe pas
    connection.execute(text(f"""
        DO $$
        BEGIN
            IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = '{grafana_user}') THEN
                CREATE USER {grafana_user} WITH PASSWORD '{grafana_password}';
                RAISE NOTICE 'Utilisateur % créé', '{grafana_user}';
            ELSE
                RAISE NOTICE 'Utilisateur % existe déjà', '{grafana_user}';
            END IF;
        END
        $$;
    """))
    
    # 2. Accorder les permissions de base
    connection.execute(text(f"""
        GRANT CONNECT ON DATABASE {database_name} TO {grafana_user};
    """))
    
    # 3. Permissions sur le schéma public
    connection.execute(text(f"""
        GRANT USAGE ON SCHEMA public TO {grafana_user};
    """))
    
    # 4. Permissions de lecture sur toutes les tables existantes
    connection.execute(text(f"""
        GRANT SELECT ON ALL TABLES IN SCHEMA public TO {grafana_user};
    """))
    
    # 5. Permissions automatiques sur les futures tables
    connection.execute(text(f"""
        ALTER DEFAULT PRIVILEGES IN SCHEMA public 
            GRANT SELECT ON TABLES TO {grafana_user};
    """))
    
    # 6. Permissions sur les séquences (pour les dashboards qui utilisent les IDs)
    connection.execute(text(f"""
        GRANT SELECT ON ALL SEQUENCES IN SCHEMA public TO {grafana_user};
    """))
    connection.execute(text(f"""
        ALTER DEFAULT PRIVILEGES IN SCHEMA public 
            GRANT SELECT ON SEQUENCES TO {grafana_user};
    """))
    
    # 7. Si vous avez d'autres schémas, ajoutez-les ici
    # connection.execute(text(f"""
    #     GRANT USAGE ON SCHEMA monitoring TO {grafana_user};
    #     GRANT SELECT ON ALL TABLES IN SCHEMA monitoring TO {grafana_user};
    #     ALTER DEFAULT PRIVILEGES IN SCHEMA monitoring 
    #         GRANT SELECT ON TABLES TO {grafana_user};
    # """))
    
    print(f"✅ Utilisateur Grafana '{grafana_user}' créé avec permissions read-only")


def downgrade() -> None:
    """Remove Grafana user."""
    
    grafana_user = os.getenv('POSTGRES_GRAFANA_USER', 'grafana_reader')
    
    # Obtenir la connexion
    connection = op.get_bind()
    
    # Révoquer toutes les permissions avant de supprimer l'utilisateur
    connection.execute(text(f"""
        DO $$
        BEGIN
            IF EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = '{grafana_user}') THEN
                -- Révoquer les permissions
                REVOKE ALL ON ALL TABLES IN SCHEMA public FROM {grafana_user};
                REVOKE ALL ON ALL SEQUENCES IN SCHEMA public FROM {grafana_user};
                REVOKE USAGE ON SCHEMA public FROM {grafana_user};
                
                -- Supprimer l'utilisateur
                DROP USER {grafana_user};
                RAISE NOTICE 'Utilisateur % supprimé', '{grafana_user}';
            ELSE
                RAISE NOTICE 'Utilisateur % n''existe pas', '{grafana_user}';
            END IF;
        END
        $$;
    """))
    
    print(f"🗑️ Utilisateur Grafana '{grafana_user}' supprimé")