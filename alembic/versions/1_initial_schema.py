# Nome do arquivo: alembic/versions/1_initial_schema.py

"""Criação da base de dados inicial

Revision ID: 0001
Revises:
Create Date: 2025-09-16 11:27:00.123456

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = '0001'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(), nullable=True),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('hashed_password', sa.String(), nullable=False),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_name'), 'users', ['name'], unique=False)

    op.create_table('categories',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(), nullable=False),
                    sa.Column('user_id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_index(op.f('ix_categories_name'), 'categories', ['name'], unique=False)

    op.create_table('transactions',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('user_id', sa.Integer(), nullable=True),
                    sa.Column('trans_type', sa.Enum('INCOME', 'EXPENSE', name='transactiontype'), nullable=True),
                    sa.Column('amount', sa.Float(), nullable=False),
                    sa.Column('description', sa.String(), nullable=True),
                    sa.Column('date', sa.DateTime(timezone=False), nullable=True),
                    sa.Column('category_id', sa.Integer(), nullable=True),
                    sa.ForeignKeyConstraint(['category_id'], ['categories.id'], ),
                    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_index(op.f('ix_transactions_description'), 'transactions', ['description'], unique=False)

    op.create_table('recurring_transactions',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('user_id', sa.Integer(), nullable=False),
                    sa.Column('category_id', sa.Integer(), nullable=True),
                    sa.Column('description', sa.String(), nullable=False),
                    sa.Column('amount', sa.Float(), nullable=False),
                    sa.Column('trans_type', sa.Enum('INCOME', 'EXPENSE', name='transactiontype'), nullable=False),
                    sa.Column('frequency', sa.Enum('DAILY', 'WEEKLY', 'MONTHLY', name='frequencyenum'), nullable=False),
                    sa.Column('day_of_month', sa.Integer(), nullable=True),
                    sa.Column('day_of_week', sa.Integer(), nullable=True),
                    sa.Column('start_date', sa.Date(), nullable=False),
                    sa.Column('end_date', sa.Date(), nullable=True),
                    sa.ForeignKeyConstraint(['category_id'], ['categories.id'], ),
                    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_index(op.f('ix_recurring_transactions_description'), 'recurring_transactions', ['description'],
                    unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_recurring_transactions_description'), table_name='recurring_transactions')
    op.drop_table('recurring_transactions')

    op.drop_index(op.f('ix_transactions_description'), table_name='transactions')
    op.drop_table('transactions')

    op.drop_index(op.f('ix_categories_name'), table_name='categories')
    op.drop_table('categories')

    op.drop_index(op.f('ix_users_name'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')