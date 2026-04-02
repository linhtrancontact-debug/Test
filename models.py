"""Data models for the property investment analysis system."""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class PropertyType(Enum):
    HOUSE = "house"
    UNIT = "unit"
    TOWNHOUSE = "townhouse"


class MarketCyclePhase(Enum):
    BOTTOM = "bottom"
    EARLY_RECOVERY = "early_recovery"
    RISING = "rising"
    PEAK = "peak"
    DECLINING = "declining"


class State(Enum):
    NSW = "NSW"
    VIC = "VIC"
    QLD = "QLD"
    SA = "SA"
    WA = "WA"
    TAS = "TAS"
    ACT = "ACT"
    NT = "NT"


@dataclass
class SuburbMetrics:
    """Quantitative metrics for scoring a suburb's investment potential."""

    # Demand-side
    population_growth_pct: float  # Annual population growth %
    employment_growth_pct: float  # Annual employment growth %
    income_growth_pct: float  # Annual household income growth %
    vacancy_rate_pct: float  # Rental vacancy rate %
    days_on_market: int  # Median days on market
    auction_clearance_rate_pct: Optional[float] = None  # Where applicable
    online_search_interest: float = 0.0  # Relative demand score 0-100

    # Supply-side
    stock_on_market: float = 0.0  # Listings per 1000 dwellings
    building_approvals_trend: float = 0.0  # YoY change in approvals (-ve = constrained)
    vendor_discount_pct: float = 0.0  # Avg discount from list to sale price

    # Infrastructure
    infrastructure_score: float = 0.0  # 0-100 score for planned infrastructure
    private_investment_score: float = 0.0  # 0-100 score for private development

    # Market cycle
    price_cagr_10yr: float = 0.0  # 10-year compound annual growth rate
    price_cagr_5yr: float = 0.0  # 5-year compound annual growth rate
    rent_growth_annual_pct: float = 0.0  # Annual rent growth %
    gross_yield_pct: float = 0.0  # Gross rental yield %

    # Demographics
    owner_occupier_ratio_pct: float = 0.0  # % owner-occupiers
    seifa_score: int = 0  # Socio-economic index (1-10 decile)


@dataclass
class Suburb:
    """Represents an Australian suburb with investment analysis data."""

    name: str
    state: State
    postcode: str
    lga: str  # Local Government Area
    median_house_price: int
    median_unit_price: int
    metrics: SuburbMetrics
    market_phase: MarketCyclePhase
    property_types_available: list[PropertyType] = field(
        default_factory=lambda: [PropertyType.HOUSE, PropertyType.UNIT]
    )

    # Computed scores (populated by scoring engine)
    demand_score: float = 0.0
    supply_score: float = 0.0
    infrastructure_score: float = 0.0
    market_timing_score: float = 0.0
    demographics_score: float = 0.0
    overall_score: float = 0.0
    capital_growth_rating: str = ""  # e.g. "HIGH", "MEDIUM", "LOW"


@dataclass
class SearchCriteria:
    """User's property search filters."""

    budget_min: int = 0
    budget_max: int = 1_000_000
    property_types: list[PropertyType] = field(
        default_factory=lambda: [PropertyType.HOUSE]
    )
    states: list[State] = field(default_factory=list)  # Empty = all states
    min_yield_pct: float = 0.0
    priority: str = "capital_growth"  # "capital_growth", "yield", "balanced"
    min_overall_score: float = 0.0
