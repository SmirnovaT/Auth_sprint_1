"""create-table

Revision ID: 9a71074344e9
Revises: 
Create Date: 2024-06-02 08:28:49.646464

"""
import uuid
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column

# revision identifiers, used by Alembic.
revision: str = '9a71074344e9'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('roles',
    sa.Column('id', sa.UUID(), nullable=False, comment='Идентификатор роли'),
    sa.Column('name', sa.String(length=255), nullable=True, comment='Название роли'),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True, comment='Дата создания записи'),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True, comment='Дата обновления записи'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id'),
    comment='Роли пользователей'
    )

    s_roles_table = table('roles', column('id', sa.UUID()),
                          column('name', sa.String(length=255)))
    op.bulk_insert(s_roles_table,
                   [{"id": uuid.uuid4(), "name": "admin"},
                    {"id": uuid.uuid4(), "name": "general"},
                    {"id": uuid.uuid4(), "name": "subscriber"},],)

    op.create_table('users',
    sa.Column('id', sa.UUID(), nullable=False, comment='Идентификатор пользователя'),
    sa.Column('login', sa.String(length=255), nullable=False, comment='Логин пользователя'),
    sa.Column('email', sa.String(length=255), nullable=False, comment='Электронный адрес пользователя'),
    sa.Column('password', sa.String(length=255), nullable=False, comment='Пароль пользователя'),
    sa.Column('first_name', sa.String(length=50), nullable=True, comment='Имя пользователя'),
    sa.Column('last_name', sa.String(length=50), nullable=True, comment='Фамилия пользователя'),
    sa.Column('role_id', sa.UUID(), nullable=True, comment='Идентификатор роли пользователя'),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True, comment='Дата создания записи'),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True, comment='Дата обновления записи'),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ondelete='RESTRICT'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('login'),
    comment='Пользователи'
    )
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=True)
    op.create_table('authentication_histories',
    sa.Column('id', sa.UUID(), nullable=False, comment='Идентификатор аутентификации'),
    sa.Column('success', sa.Boolean(), nullable=False, comment='Флаг, указывающий, был ли вход успешным (True) или нет (False)'),
    sa.Column('user_agent', sa.String(), nullable=True, comment='Информация о браузере и операционной системе пользователя'),
    sa.Column('user_id', sa.UUID(), nullable=False, comment='Идентификатор пользователя, связанного с этой записью о входе'),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True, comment='Дата создания записи'),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True, comment='Дата обновления записи'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    comment='История аутентификации пользователей'
    )
    op.create_index(op.f('ix_authentication_histories_id'), 'authentication_histories', ['id'], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_authentication_histories_id'), table_name='authentication_histories')
    op.drop_table('authentication_histories')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_table('users')
    op.drop_table('roles')

    # ### end Alembic commands ###