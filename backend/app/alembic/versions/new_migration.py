"""fix table names

Revision ID: 8f9d24de1d32
Revises: 7e92b11c133f
Create Date: 2024-xx-xx
"""
from alembic import op

revision = '8f9d24de1d32'
down_revision = '7e92b11c133f'
branch_labels = None
depends_on = None

def upgrade():
    # Drop the foreign key constraints first
    op.drop_constraint(
        'set_menu_cuisine_link_cuisine_id_fkey',
        'set_menu_cuisine_link',
        type_='foreignkey'
    )
    
    # Rename tables
    op.rename_table('cuisines', 'cuisine')
    
    # Recreate the foreign key constraints
    op.create_foreign_key(
        'set_menu_cuisine_link_cuisine_id_fkey',
        'set_menu_cuisine_link',
        'cuisine',
        ['cuisine_id'],
        ['id']
    )

def downgrade():
    # Drop the foreign key constraints first
    op.drop_constraint(
        'set_menu_cuisine_link_cuisine_id_fkey',
        'set_menu_cuisine_link',
        type_='foreignkey'
    )
    
    # Rename tables back
    op.rename_table('cuisine', 'cuisines')
    
    # Recreate the foreign key constraints
    op.create_foreign_key(
        'set_menu_cuisine_link_cuisine_id_fkey',
        'set_menu_cuisine_link',
        'cuisines',
        ['cuisine_id'],
        ['id']
    ) 