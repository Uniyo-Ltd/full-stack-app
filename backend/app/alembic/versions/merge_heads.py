"""merge heads

Revision ID: 9f3d24de1d33
Revises: 7e92b11c133f
Create Date: 2024-xx-xx
"""
from alembic import op

# revision identifiers, used by Alembic
revision = '9f3d24de1d33'
down_revision = '7e92b11c133f'  # Only reference the initial migration
branch_labels = None
depends_on = None

def upgrade():
    # Create indexes for set_menu table
    op.create_index('idx_price_per_person', 'set_menu', ['price_per_person'])
    op.create_index('idx_dietary', 'set_menu', ['is_vegan', 'is_vegetarian', 'is_halal'])
    op.create_index('idx_name', 'set_menu', ['name'])
    op.create_index('idx_created_at', 'set_menu', ['created_at'])

def downgrade():
    # Drop indexes in reverse order
    op.drop_index('idx_created_at', table_name='set_menu')
    op.drop_index('idx_name', table_name='set_menu')
    op.drop_index('idx_dietary', table_name='set_menu')
    op.drop_index('idx_price_per_person', table_name='set_menu') 