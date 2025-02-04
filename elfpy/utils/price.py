"""Utilities for price calculations"""
from __future__ import annotations  # types will be strings by default in 3.11

from fixedpoint import FixedPoint

import elfpy.time as time


### Spot Price and APR ###
def calc_apr_from_spot_price(price: FixedPoint, time_remaining: time.StretchedTime):
    r"""
    Returns the APR (decimal) given the current (positive) base asset price and the remaining pool duration

    Arguments
    ----------
    price : FixedPoint
        Spot price of bonds in terms of base
    time_remaining : StretchedTime
        Time remaining until bond maturity, in years

    Returns
    -------
    FixedPoint
        APR (decimal) calculated from the provided parameters
    """
    if not price.is_finite():
        return price
    assert price > FixedPoint("0.0"), (
        "utils.price.calc_apr_from_spot_price: ERROR: "
        f"Price argument should be greater or equal to zero, not {price}"
    )
    assert time_remaining.normalized_time > FixedPoint("0.0"), (
        "utils.price.calc_apr_from_spot_price: ERROR: "
        f"time_remaining.normalized_time should be greater than zero, not {time_remaining.normalized_time}"
    )
    annualized_time = time_remaining.days / FixedPoint("365.0")
    return (FixedPoint("1.0") - price) / (price * annualized_time)  # r = ((1/p)-1)/t = (1-p)/(pt)


def calc_spot_price_from_apr(apr: FixedPoint, time_remaining: time.StretchedTime) -> FixedPoint:
    r"""Returns the current spot price based on the current APR (decimal) and the remaining pool duration

    Arguments
    ----------
    apr : FixedPoint
        Current fixed APR in decimal units (for example, 5% APR would be 0.05)
    time_remaining : StretchedTime
        Time remaining until bond maturity

    Returns
    -------
    FixedPoint
        Spot price of bonds in terms of base, calculated from the provided parameters
    """
    annualized_time = time_remaining.days / FixedPoint("365.0")
    return FixedPoint("1.0") / (FixedPoint("1.0") + apr * annualized_time)  # price = 1 / (1 + r * t)
