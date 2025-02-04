"""Trade related classes and functions"""
from dataclasses import dataclass, field

from fixedpoint import FixedPoint

import elfpy.agents.agent_trade_result as agent_trade_result
import elfpy.markets.hyperdrive.market_action_result as market_action_result
import elfpy.types as types


@types.freezable(frozen=True, no_new_attribs=True)
@dataclass
class TradeBreakdown:
    r"""A granular breakdown of a trade.

    This includes information relating to fees and slippage.

    Attributes
    ----------
    without_fee_or_slippage: FixedPoint
        The amount the user pays without fees or slippage. The units
        are always in terms of bonds or base, depending on input.
    with_fee: FixedPoint
        The fee the user pays. The units are always in terms of bonds or
        base.
    without_fee: FixedPoint
        The amount the user pays with fees and slippage. The units are
        always in terms of bonds or base.
    fee: FixedPoint
        The amount the user pays with slippage and no fees. The units are
        always in terms of bonds or base.
    """

    without_fee_or_slippage: FixedPoint
    with_fee: FixedPoint
    without_fee: FixedPoint
    curve_fee: FixedPoint
    gov_curve_fee: FixedPoint
    #flat_fee: FixedPoint = FixedPoint(0)
    #gov_flat_fee: FixedPoint = FixedPoint(0)
    flat_fee: FixedPoint = field(default_factory=lambda: FixedPoint(0))
    flat_fee: FixedPoint = field(default_factory=lambda: FixedPoint(0))

    @property
    def fee(self) -> FixedPoint:
        """Return the total fee, sum of all four fees."""
        return self.flat_fee + self.gov_flat_fee + self.curve_fee + self.gov_curve_fee

    @property
    def gov_fee(self) -> FixedPoint:
        """Return the total governance fee, sum of flat and curve portions."""
        return self.gov_flat_fee + self.gov_curve_fee


@types.freezable(frozen=True, no_new_attribs=True)
@dataclass
class TradeResult:
    r"""The result of performing a trade.

    This includes granular information about the trade details,
    including the amount of fees collected and the total delta.
    Additionally, breakdowns for the updates that should be applied
    to the user and the market are computed.
    """

    user_result: agent_trade_result.AgentTradeResult
    market_result: market_action_result.MarketActionResult
    breakdown: TradeBreakdown
