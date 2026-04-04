from sqlalchemy import event
from sqlalchemy.orm import Session, with_loader_criteria

from app.models.mixins import BaseFieldsMixin, TenantMixin


@event.listens_for(Session, "before_flush")
def auto_fill_tenant_id(session, flush_context, instances):
    tenant_id = session.info.get("tenant_id")
    if tenant_id is None:
        return

    for obj in session.new:
        if isinstance(obj, TenantMixin):
            if getattr(obj, "tenant_id", None) is None:
                obj.tenant_id = tenant_id


@event.listens_for(Session, "do_orm_execute")
def add_global_filters(execute_state):
    if not execute_state.is_select:
        return

    # 全局总开关
    if execute_state.execution_options.get("skip_global_filters", False):
        return

    stmt = execute_state.statement
    tenant_id = execute_state.session.info.get("tenant_id")
    execution_options = execute_state.execution_options

    # 1. 租户过滤 (由 skip_tenant_filter 控制)
    if tenant_id is not None and not execution_options.get("skip_tenant_filter", False):
        stmt = stmt.options(
            with_loader_criteria(
                TenantMixin,
                lambda cls: cls.tenant_id == tenant_id,
                include_aliases=True,
            )
        )

    # 2. 软删除过滤 (由 include_deleted 控制)
    if not execution_options.get("include_deleted", False):
        stmt = stmt.options(
            with_loader_criteria(
                BaseFieldsMixin,
                lambda cls: cls.is_deleted.is_(False),
                include_aliases=True,
            )
        )

    execute_state.statement = stmt