"""create tables and indexes

Revision ID: 7e92b11c133f
Revises: 
Create Date: 2024-xx-xx

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
import uuid

# revision identifiers, used by Alembic
revision = '7e92b11c133f'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Create user table with UUID
    op.create_table(
        'user',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('hashed_password', sa.String(), nullable=False),
        sa.Column('full_name', sa.String(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('is_superuser', sa.Boolean(), nullable=False)
    )
    op.create_index('idx_user_email', 'user', ['email'], unique=True)

    # Create cuisine table (singular)
    op.create_table(
        'cuisine',  # Changed from 'cuisines'
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('slug', sa.String(), nullable=False)  # Added missing slug column
    )
    op.create_index('idx_cuisine_slug', 'cuisine', ['slug'])

    # Create set_menu table (singular)
    op.create_table(
        'set_menu',  # Changed from 'set_menus'
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('display_text', sa.Integer(), nullable=False),
        sa.Column('image', sa.String(), nullable=False),
        sa.Column('thumbnail', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('status', sa.Integer(), nullable=False),
        sa.Column('price_per_person', sa.Float(), nullable=False),
        sa.Column('min_spend', sa.Float(), nullable=False),
        sa.Column('is_vegan', sa.Boolean(), nullable=False),
        sa.Column('is_vegetarian', sa.Boolean(), nullable=False),
        sa.Column('is_halal', sa.Boolean(), nullable=False),
        sa.Column('is_kosher', sa.Boolean(), nullable=False),
        sa.Column('is_seated', sa.Boolean(), nullable=False),
        sa.Column('is_standing', sa.Boolean(), nullable=True),
        sa.Column('is_canape', sa.Boolean(), nullable=False),
        sa.Column('is_mixed_dietary', sa.Boolean(), nullable=False),
        sa.Column('is_meal_prep', sa.Boolean(), nullable=False),
        sa.Column('available', sa.Boolean(), nullable=False),
        sa.Column('number_of_orders', sa.Integer(), nullable=False)
    )

    # Create link table
    op.create_table(
        'set_menu_cuisine_link',
        sa.Column('set_menu_id', sa.Integer(), nullable=False),
        sa.Column('cuisine_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['cuisine_id'], ['cuisine.id']),  # Changed from cuisines.id
        sa.ForeignKeyConstraint(['set_menu_id'], ['set_menu.id']),  # Changed from set_menus.id
        sa.PrimaryKeyConstraint('set_menu_id', 'cuisine_id')
    )

    # Just one index for status queries
    op.create_index('idx_status', 'set_menu', ['status'])

def downgrade():
    # Drop indexes first
    op.drop_index('idx_status', table_name='set_menu')
    op.drop_index('idx_user_email', table_name='user')
    op.drop_index('idx_cuisine_slug', table_name='cuisine')
    
    # Drop link table first (because it has foreign keys)
    op.drop_table('set_menu_cuisine_link')
    
    # Now we can safely drop the main tables
    op.drop_table('set_menu')
    op.drop_table('cuisine')
    op.drop_table('user')
