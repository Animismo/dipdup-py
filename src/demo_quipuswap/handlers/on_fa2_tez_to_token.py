from decimal import Decimal

import demo_quipuswap.models as models
from demo_quipuswap.types.fa2_token.parameter.transfer import Transfer
from demo_quipuswap.types.quipu_fa2.parameter.tez_to_token_payment import TezToTokenPayment
from dipdup.models import HandlerContext, OperationContext


async def on_fa2_tez_to_token(
    ctx: HandlerContext,
    tez_to_token_payment: OperationContext[TezToTokenPayment],
    transfer: OperationContext[Transfer],
) -> None:
    if ctx.template_values is None:
        raise Exception('This index must be templated')

    decimals = int(ctx.template_values['decimals'])
    trader, _ = await models.Trader.get_or_create(address=transfer.parameter.__root__[0].from_)
    instrument, _ = await models.Instrument.get_or_create(symbol=ctx.template_values['symbol'])

    min_token_quantity = Decimal(tez_to_token_payment.parameter.min_out) / (10 ** decimals)
    token_quantity = Decimal(transfer.parameter.__root__[0].txs[0].amount) / (10 ** decimals)
    tez_quantity = Decimal(tez_to_token_payment.data.amount) / (10 ** 6)
    trade = models.Trade(
        instrument=instrument,
        trader=trader,
        side=models.TradeSide.BUY,
        quantity=token_quantity,
        price=token_quantity / tez_quantity,
        slippage=((min_token_quantity / token_quantity) - 1) * 100,
        level=transfer.data.level,
        timestamp=transfer.data.timestamp,
    )
    await trade.save()