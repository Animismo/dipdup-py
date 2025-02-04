from demo_domains.handlers.on_storage_diff import on_storage_diff
from demo_domains.types.name_registry.parameter.admin_update import AdminUpdateParameter
from demo_domains.types.name_registry.storage import NameRegistryStorage
from dipdup.context import HandlerContext
from dipdup.models import Transaction


async def on_admin_update(
    ctx: HandlerContext,
    admin_update: Transaction[AdminUpdateParameter, NameRegistryStorage],
) -> None:
    storage = admin_update.storage
    await on_storage_diff(ctx, storage)
