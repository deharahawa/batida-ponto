"""empty message

Revision ID: ea61fb6a1676
Revises: 
Create Date: 2020-07-27 18:14:58.702127

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ea61fb6a1676'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nome_completo', sa.String(length=255), nullable=True),
    sa.Column('cpf', sa.String(length=11), nullable=True),
    sa.Column('email', sa.String(length=255), nullable=True),
    sa.Column('data_cadastro', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('ponto',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('data_batida', sa.DateTime(), nullable=True),
    sa.Column('tipo_batida', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('ponto')
    op.drop_table('user')
    # ### end Alembic commands ###
