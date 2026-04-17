"""drop multi tenant

Revision ID: 9a6b3f5e2d11
Revises: ecf0b671791d
Create Date: 2026-04-17 16:20:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "9a6b3f5e2d11"
down_revision: Union[str, Sequence[str], None] = "ecf0b671791d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("ALTER TABLE user_tokens DROP COLUMN IF EXISTS tenant_id CASCADE")
    op.execute("ALTER TABLE employees DROP COLUMN IF EXISTS tenant_id CASCADE")
    op.execute("ALTER TABLE merchants DROP COLUMN IF EXISTS tenant_id CASCADE")
    op.execute("ALTER TABLE room_orders DROP COLUMN IF EXISTS tenant_id CASCADE")
    op.execute("ALTER TABLE rooms DROP COLUMN IF EXISTS tenant_id CASCADE")
    op.execute("ALTER TABLE shops DROP COLUMN IF EXISTS tenant_id CASCADE")
    op.execute("DROP TABLE IF EXISTS user_tenants CASCADE")
    op.execute("DROP TABLE IF EXISTS tenants CASCADE")


def downgrade() -> None:
    """Downgrade schema."""
    op.create_table(
        "tenants",
        sa.Column("id", sa.BigInteger(), sa.Identity(always=False), nullable=False, comment="主键ID"),
        sa.Column("tenant_name", sa.String(length=255), server_default="", nullable=False, comment="租户名称"),
        sa.Column("code", sa.String(length=128), server_default="", nullable=False, comment="租户唯一标识"),
        sa.Column("is_deleted", sa.Boolean(), server_default="false", nullable=False, comment="是否删除"),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True, comment="删除时间（软删时记录）"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False, comment="创建时间"),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False, comment="更新时间"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "user_tenants",
        sa.Column("id", sa.BigInteger(), sa.Identity(always=False), nullable=False, comment="主键ID"),
        sa.Column("tenant_id", sa.BigInteger(), nullable=False, comment="租户ID"),
        sa.Column("user_id", sa.BigInteger(), nullable=False, comment="用户ID"),
        sa.Column("is_deleted", sa.Boolean(), server_default="false", nullable=False, comment="是否删除"),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True, comment="删除时间（软删时记录）"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False, comment="创建时间"),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False, comment="更新时间"),
        sa.ForeignKeyConstraint(["tenant_id"], ["tenants.id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="RESTRICT"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.add_column("user_tokens", sa.Column("tenant_id", sa.BigInteger(), nullable=False, comment="租户ID"))
    op.create_foreign_key(None, "user_tokens", "tenants", ["tenant_id"], ["id"], ondelete="RESTRICT")
    op.add_column("employees", sa.Column("tenant_id", sa.BigInteger(), nullable=False, comment="租户ID"))
    op.create_foreign_key(None, "employees", "tenants", ["tenant_id"], ["id"], ondelete="RESTRICT")
    op.add_column("merchants", sa.Column("tenant_id", sa.BigInteger(), nullable=False, comment="租户ID"))
    op.create_foreign_key(None, "merchants", "tenants", ["tenant_id"], ["id"], ondelete="RESTRICT")
    op.add_column("room_orders", sa.Column("tenant_id", sa.BigInteger(), nullable=False, comment="租户ID"))
    op.create_foreign_key(None, "room_orders", "tenants", ["tenant_id"], ["id"], ondelete="RESTRICT")
    op.add_column("rooms", sa.Column("tenant_id", sa.BigInteger(), nullable=False, comment="租户ID"))
    op.create_foreign_key(None, "rooms", "tenants", ["tenant_id"], ["id"], ondelete="RESTRICT")
    op.add_column("shops", sa.Column("tenant_id", sa.BigInteger(), nullable=False, comment="租户ID"))
    op.create_foreign_key(None, "shops", "tenants", ["tenant_id"], ["id"], ondelete="RESTRICT")
