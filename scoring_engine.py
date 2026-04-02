"""
Suburb Scoring Engine — inspired by InvestorKit's methodology.

Scores suburbs across 5 dimensions using weighted metrics:
1. Demand (30%) — population growth, employment, vacancy, days on market
2. Supply Constraints (25%) — low stock, limited building approvals, vendor discounts
3. Infrastructure (15%) — government & private investment catalysts
4. Market Timing (20%) — cycle phase, price momentum, rent growth
5. Demographics (10%) — owner-occupier ratio, socioeconomic index

Each dimension produces a 0-100 score. The overall score is a weighted average.
"""

from models import Suburb, MarketCyclePhase


# ── Weights ──────────────────────────────────────────────────────────────────

DIMENSION_WEIGHTS = {
    "demand": 0.30,
    "supply": 0.25,
    "infrastructure": 0.15,
    "market_timing": 0.20,
    "demographics": 0.10,
}

# ── Helper ───────────────────────────────────────────────────────────────────

def _clamp(value: float, lo: float = 0.0, hi: float = 100.0) -> float:
    return max(lo, min(hi, value))


def _linear_scale(value: float, worst: float, best: float) -> float:
    """Scale a value linearly to 0-100 where worst→0 and best→100."""
    if best == worst:
        return 50.0
    raw = (value - worst) / (best - worst) * 100
    return _clamp(raw)


def _inverse_scale(value: float, best: float, worst: float) -> float:
    """Scale where lower value is better (e.g. vacancy rate, days on market)."""
    return _linear_scale(value, worst, best)


# ── Dimension Scorers ────────────────────────────────────────────────────────

def score_demand(suburb: Suburb) -> float:
    m = suburb.metrics
    pop = _linear_scale(m.population_growth_pct, 0.0, 3.0)
    emp = _linear_scale(m.employment_growth_pct, -1.0, 4.0)
    inc = _linear_scale(m.income_growth_pct, 0.0, 5.0)
    vac = _inverse_scale(m.vacancy_rate_pct, 0.5, 5.0)
    dom = _inverse_scale(m.days_on_market, 15, 120)
    search = _linear_scale(m.online_search_interest, 0, 100)

    weights = [0.20, 0.15, 0.10, 0.25, 0.20, 0.10]
    scores = [pop, emp, inc, vac, dom, search]
    return _clamp(sum(w * s for w, s in zip(weights, scores)))


def score_supply(suburb: Suburb) -> float:
    m = suburb.metrics
    # Low stock on market is good (supply constrained)
    stock = _inverse_scale(m.stock_on_market, 5, 40)
    # Negative building approvals trend = less future supply = good for prices
    approvals = _inverse_scale(m.building_approvals_trend, -20, 30)
    # Low vendor discount = strong market
    discount = _inverse_scale(m.vendor_discount_pct, 0, 10)

    weights = [0.40, 0.35, 0.25]
    scores = [stock, approvals, discount]
    return _clamp(sum(w * s for w, s in zip(weights, scores)))


def score_infrastructure(suburb: Suburb) -> float:
    m = suburb.metrics
    infra = _linear_scale(m.infrastructure_score, 0, 100)
    private = _linear_scale(m.private_investment_score, 0, 100)
    return _clamp(0.60 * infra + 0.40 * private)


def score_market_timing(suburb: Suburb) -> float:
    m = suburb.metrics

    # Cycle phase scoring — early recovery is the sweet spot
    phase_scores = {
        MarketCyclePhase.BOTTOM: 60,
        MarketCyclePhase.EARLY_RECOVERY: 95,
        MarketCyclePhase.RISING: 70,
        MarketCyclePhase.PEAK: 20,
        MarketCyclePhase.DECLINING: 10,
    }
    phase = phase_scores.get(suburb.market_phase, 50)

    cagr5 = _linear_scale(m.price_cagr_5yr, 0, 10)
    rent_g = _linear_scale(m.rent_growth_annual_pct, 0, 8)
    yld = _linear_scale(m.gross_yield_pct, 2, 6)

    weights = [0.35, 0.25, 0.25, 0.15]
    scores = [phase, cagr5, rent_g, yld]
    return _clamp(sum(w * s for w, s in zip(weights, scores)))


def score_demographics(suburb: Suburb) -> float:
    m = suburb.metrics
    owner = _linear_scale(m.owner_occupier_ratio_pct, 30, 80)
    seifa = _linear_scale(m.seifa_score, 1, 10)
    return _clamp(0.55 * owner + 0.45 * seifa)


# ── Main Scoring ─────────────────────────────────────────────────────────────

def score_suburb(suburb: Suburb) -> Suburb:
    """Score a suburb across all dimensions and compute overall rating."""
    suburb.demand_score = round(score_demand(suburb), 1)
    suburb.supply_score = round(score_supply(suburb), 1)
    suburb.infrastructure_score = round(score_infrastructure(suburb), 1)
    suburb.market_timing_score = round(score_market_timing(suburb), 1)
    suburb.demographics_score = round(score_demographics(suburb), 1)

    suburb.overall_score = round(
        DIMENSION_WEIGHTS["demand"] * suburb.demand_score
        + DIMENSION_WEIGHTS["supply"] * suburb.supply_score
        + DIMENSION_WEIGHTS["infrastructure"] * suburb.infrastructure_score
        + DIMENSION_WEIGHTS["market_timing"] * suburb.market_timing_score
        + DIMENSION_WEIGHTS["demographics"] * suburb.demographics_score,
        1,
    )

    if suburb.overall_score >= 75:
        suburb.capital_growth_rating = "HIGH"
    elif suburb.overall_score >= 55:
        suburb.capital_growth_rating = "MEDIUM"
    else:
        suburb.capital_growth_rating = "LOW"

    return suburb


def score_all(suburbs: list[Suburb]) -> list[Suburb]:
    """Score and rank all suburbs, returning them sorted by overall score."""
    scored = [score_suburb(s) for s in suburbs]
    scored.sort(key=lambda s: s.overall_score, reverse=True)
    return scored
