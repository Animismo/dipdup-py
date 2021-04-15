import demo_hic_et_nunc.models as models
from demo_hic_et_nunc.types.hen_minter.parameter.swap import Swap
from dipdup.models import HandlerContext, OperationContext


async def on_swap(
    ctx: HandlerContext,
    swap: OperationContext[Swap],
) -> None:
    holder, _ = await models.Holder.get_or_create(address=swap.data.sender_address)
    swap_model = models.Swap(
        id=int(swap.storage.swap_id) - 1,  # type: ignore
        creator=holder,
        price=swap.parameter.xtz_per_objkt,
        amount=swap.parameter.objkt_amount,
        amount_left=swap.parameter.objkt_amount,
        status=models.SwapStatus.ACTIVE,
        level=swap.data.level,
        timestamp=swap.data.timestamp,
    )
    await swap_model.save()