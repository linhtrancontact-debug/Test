"""
Property Search & Filtering Engine.

Filters suburbs by user criteria (budget, state, property type, yield)
and returns ranked results optimised for the user's priority
(capital growth, yield, or balanced).
"""

from models import Suburb, SearchCriteria, PropertyType
from scoring_engine import score_all


def _median_price(suburb: Suburb, prop_types: list[PropertyType]) -> int:
    """Return the relevant median price based on desired property types."""
    prices = []
    if PropertyType.HOUSE in prop_types or PropertyType.TOWNHOUSE in prop_types:
        prices.append(suburb.median_house_price)
    if PropertyType.UNIT in prop_types:
        prices.append(suburb.median_unit_price)
    return min(prices) if prices else suburb.median_house_price


def filter_suburbs(
    suburbs: list[Suburb], criteria: SearchCriteria
) -> list[Suburb]:
    """Apply all search filters and return matching suburbs."""
    results = []
    for s in suburbs:
        # Budget filter
        price = _median_price(s, criteria.property_types)
        if price < criteria.budget_min or price > criteria.budget_max:
            continue

        # State filter
        if criteria.states and s.state not in criteria.states:
            continue

        # Property type filter
        if not any(pt in s.property_types_available for pt in criteria.property_types):
            continue

        # Yield filter
        if criteria.min_yield_pct and s.metrics.gross_yield_pct < criteria.min_yield_pct:
            continue

        # Minimum score filter
        if criteria.min_overall_score and s.overall_score < criteria.min_overall_score:
            continue

        results.append(s)
    return results


def search(
    suburbs: list[Suburb], criteria: SearchCriteria
) -> list[Suburb]:
    """
    Full search pipeline:
    1. Score all suburbs
    2. Filter by criteria
    3. Re-sort based on user's priority
    """
    scored = score_all(suburbs)
    filtered = filter_suburbs(scored, criteria)

    if criteria.priority == "capital_growth":
        # Weight towards market timing + demand
        filtered.sort(
            key=lambda s: s.market_timing_score * 0.4
            + s.demand_score * 0.3
            + s.supply_score * 0.2
            + s.overall_score * 0.1,
            reverse=True,
        )
    elif criteria.priority == "yield":
        filtered.sort(key=lambda s: s.metrics.gross_yield_pct, reverse=True)
    # "balanced" keeps the default overall_score sort

    return filtered
