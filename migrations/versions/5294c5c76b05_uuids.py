"""uuids

Revision ID: 5294c5c76b05
Revises: 41dcf35b6fad
Create Date: 2024-05-12 22:28:01.176104

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '5294c5c76b05'
down_revision: Union[str, None] = '41dcf35b6fad'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('uuid', sqlmodel.sql.sqltypes.GUID(), server_default=sa.text('gen_random_uuid()'), nullable=False))
    op.create_index(op.f('ix_users_uuid'), 'users', ['uuid'], unique=True)

    # Then handle posts and comments
    op.add_column('posts', sa.Column('uuid', sqlmodel.sql.sqltypes.GUID(), server_default=sa.text('gen_random_uuid()'), nullable=False))
    op.add_column('posts', sa.Column('author_uuid', sqlmodel.sql.sqltypes.GUID(), nullable=False))
    op.create_foreign_key(None, 'posts', 'users', ['author_uuid'], ['uuid'])
    op.create_index(op.f('ix_posts_uuid'), 'posts', ['uuid'], unique=True)

    op.add_column('comments', sa.Column('uuid', sqlmodel.sql.sqltypes.GUID(), server_default=sa.text('gen_random_uuid()'), nullable=False))
    op.add_column('comments', sa.Column('author_uuid', sqlmodel.sql.sqltypes.GUID(), nullable=False))
    op.add_column('comments', sa.Column('post_uuid', sqlmodel.sql.sqltypes.GUID(), nullable=False))
    op.create_foreign_key(None, 'comments', 'users', ['author_uuid'], ['uuid'])
    op.create_foreign_key(None, 'comments', 'posts', ['post_uuid'], ['uuid'])
    op.create_index(op.f('ix_comments_uuid'), 'comments', ['uuid'], unique=True)

    op.drop_constraint('fk_comments_post_id_posts', 'comments', type_='foreignkey')
    op.drop_constraint('fk_comments_author_id_users', 'comments', type_='foreignkey')
    op.drop_column('comments', 'post_id')
    op.drop_column('comments', 'author_id')
    op.drop_column('comments', 'id')
    op.drop_constraint('fk_posts_author_id_users', 'posts', type_='foreignkey')
    op.drop_column('posts', 'author_id')
    op.drop_column('posts', 'id')
    op.drop_column('users', 'id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False))
    op.drop_index(op.f('ix_users_uuid'), table_name='users')
    op.drop_column('users', 'uuid')
    op.add_column('posts', sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False))
    op.add_column('posts', sa.Column('author_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'posts', type_='foreignkey')
    op.create_foreign_key('fk_posts_author_id_users', 'posts', 'users', ['author_id'], ['id'])
    op.drop_index(op.f('ix_posts_uuid'), table_name='posts')
    op.drop_column('posts', 'author_uuid')
    op.drop_column('posts', 'uuid')
    op.add_column('comments', sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False))
    op.add_column('comments', sa.Column('author_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.add_column('comments', sa.Column('post_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'comments', type_='foreignkey')
    op.drop_constraint(None, 'comments', type_='foreignkey')
    op.create_foreign_key('fk_comments_author_id_users', 'comments', 'users', ['author_id'], ['id'])
    op.create_foreign_key('fk_comments_post_id_posts', 'comments', 'posts', ['post_id'], ['id'])
    op.drop_index(op.f('ix_comments_uuid'), table_name='comments')
    op.drop_column('comments', 'post_uuid')
    op.drop_column('comments', 'author_uuid')
    op.drop_column('comments', 'uuid')
    # ### end Alembic commands ###