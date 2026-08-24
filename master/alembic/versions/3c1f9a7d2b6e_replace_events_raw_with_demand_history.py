"""replace events_raw with demand_history

Revision ID: 3c1f9a7d2b6e
Revises: 7a905cbd5c44
Create Date: 2026-08-24 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '3c1f9a7d2b6e'
down_revision: Union[str, Sequence[str], None] = '7a905cbd5c44'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('demand_history',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('idpk', sa.String(), nullable=False),
    sa.Column('type', sa.String(), nullable=False),
    sa.Column('city', sa.String(), nullable=False),
    sa.Column('demand', sa.Float(), nullable=False),
    sa.Column('unit', sa.String(), nullable=False),
    sa.Column('valid_until', sa.DateTime(timezone=True), nullable=False),
    sa.Column('meta_content', sa.Text(), nullable=True),
    sa.Column('received_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_demand_history_idpk'), 'demand_history', ['idpk'], unique=False)
    op.create_index(op.f('ix_demand_history_received_at'), 'demand_history', ['received_at'], unique=False)

    op.drop_table('events_raw')


def downgrade() -> None:
    """Downgrade schema."""
    op.create_table('events_raw',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('payload', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
    sa.Column('received_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )

    op.drop_index(op.f('ix_demand_history_received_at'), table_name='demand_history')
    op.drop_index(op.f('ix_demand_history_idpk'), table_name='demand_history')
    op.drop_table('demand_history')
