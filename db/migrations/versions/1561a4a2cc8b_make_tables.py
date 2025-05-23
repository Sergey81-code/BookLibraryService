"""Make tables

Revision ID: 1561a4a2cc8b
Revises: 
Create Date: 2025-05-03 13:39:28.927411

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1561a4a2cc8b'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('authors',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('birthday', sa.Date(), nullable=True),
    sa.Column('deathday', sa.Date(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('books',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('url', sa.String(), nullable=True),
    sa.Column('year', sa.Integer(), nullable=False),
    sa.Column('totalAmount', sa.Integer(), nullable=False),
    sa.Column('borrowedAmount', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('book_authors',
    sa.Column('author_id', sa.UUID(), nullable=False),
    sa.Column('book_id', sa.UUID(), nullable=False),
    sa.ForeignKeyConstraint(['author_id'], ['authors.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['book_id'], ['books.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('author_id', 'book_id')
    )
    op.create_table('book_copies',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('book_id', sa.UUID(), nullable=False),
    sa.Column('status', sa.Enum('AVAILABLE', 'BORROWED', 'RESERVED', name='book_statuses_enum'), nullable=False),
    sa.Column('condition', sa.Enum('NEW', 'USED', 'DAMAGED', name='book_conditions_enum'), nullable=False),
    sa.Column('user_id', sa.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['book_id'], ['books.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ondelete='SET NULL', use_alter=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('book_copies')
    op.drop_table('book_authors')
    op.drop_table('books')
    op.drop_table('authors')
    # ### end Alembic commands ###
