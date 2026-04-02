#!/usr/bin/env python3
"""
Property Investment Analysis Tool
Inspired by InvestorKit's data-driven methodology.

Scores Australian suburbs across 5 dimensions (Demand, Supply, Infrastructure,
Market Timing, Demographics) and ranks them for capital growth potential.
"""

import argparse
import sys
from tabulate import tabulate

from models import SearchCriteria, PropertyType, State, MarketCyclePhase
from dataset import get_suburbs
from search_engine import search


def format_currency(amount: int) -> str:
    if amount >= 1_000_000:
        return f"${amount / 1_000_000:.2f}M"
    return f"${amount / 1_000:,.0f}K"


def print_summary(suburbs, criteria):
    """Print a high-level results table."""
    if not suburbs:
        print("\n  No suburbs matched your criteria. Try widening your budget or filters.\n")
        return

    print(f"\n{'='*90}")
    print(f"  PROPERTY INVESTMENT ANALYSIS — Top Suburbs for Capital Growth")
    print(f"  Budget: {format_currency(criteria.budget_min)} – {format_currency(criteria.budget_max)}")
    print(f"  Priority: {criteria.priority.replace('_', ' ').title()}")
    print(f"  Results: {len(suburbs)} suburbs matched")
    print(f"{'='*90}\n")

    headers = [
        "Rank", "Suburb", "State", "Median Price",
        "Demand", "Supply", "Infra", "Timing", "Demo",
        "OVERALL", "Rating", "Yield", "Phase"
    ]

    rows = []
    for i, s in enumerate(suburbs, 1):
        price = s.median_house_price if PropertyType.HOUSE in criteria.property_types else s.median_unit_price
        rows.append([
            i,
            s.name,
            s.state.value,
            format_currency(price),
            f"{s.demand_score:.0f}",
            f"{s.supply_score:.0f}",
            f"{s.infrastructure_score:.0f}",
            f"{s.market_timing_score:.0f}",
            f"{s.demographics_score:.0f}",
            f"{s.overall_score:.0f}",
            s.capital_growth_rating,
            f"{s.metrics.gross_yield_pct:.1f}%",
            s.market_phase.value.replace("_", " ").title(),
        ])

    print(tabulate(rows, headers=headers, tablefmt="simple_outline"))


def print_detailed(suburb, rank):
    """Print a detailed suburb report card."""
    s = suburb
    m = s.metrics

    print(f"\n{'─'*70}")
    print(f"  #{rank}  {s.name}, {s.state.value} {s.postcode}  |  LGA: {s.lga}")
    print(f"{'─'*70}")
    print(f"  Median House Price:  {format_currency(s.median_house_price):<12}  Market Phase: {s.market_phase.value.replace('_',' ').title()}")
    if s.median_unit_price:
        print(f"  Median Unit Price:   {format_currency(s.median_unit_price)}")
    print(f"  Capital Growth Rating: {s.capital_growth_rating}")
    print()

    # Scores bar chart
    dims = [
        ("Demand",         s.demand_score),
        ("Supply",         s.supply_score),
        ("Infrastructure", s.infrastructure_score),
        ("Market Timing",  s.market_timing_score),
        ("Demographics",   s.demographics_score),
    ]
    print("  SCORES")
    for label, score in dims:
        bar = "█" * int(score / 2) + "░" * (50 - int(score / 2))
        print(f"    {label:<16} {bar} {score:.0f}/100")
    bar = "█" * int(s.overall_score / 2) + "░" * (50 - int(s.overall_score / 2))
    print(f"    {'OVERALL':<16} {bar} {s.overall_score:.0f}/100")

    print()
    print("  KEY METRICS")
    print(f"    Population Growth:   {m.population_growth_pct:.1f}%    Vacancy Rate:    {m.vacancy_rate_pct:.1f}%")
    print(f"    Employment Growth:   {m.employment_growth_pct:.1f}%    Days on Market:  {m.days_on_market}d")
    print(f"    Income Growth:       {m.income_growth_pct:.1f}%    Vendor Discount: {m.vendor_discount_pct:.1f}%")
    print(f"    5yr CAGR:            {m.price_cagr_5yr:.1f}%    Gross Yield:     {m.gross_yield_pct:.1f}%")
    print(f"    Rent Growth:         {m.rent_growth_annual_pct:.1f}%    Owner-Occ Ratio: {m.owner_occupier_ratio_pct:.0f}%")
    print(f"    Stock on Market:     {m.stock_on_market:.0f}/1000   SEIFA Decile:    {m.seifa_score}/10")
    print()

    # Why this suburb
    reasons = []
    if s.market_phase == MarketCyclePhase.EARLY_RECOVERY:
        reasons.append("Early recovery phase — ideal entry point before prices surge")
    if m.vacancy_rate_pct < 1.5:
        reasons.append(f"Very tight rental market ({m.vacancy_rate_pct}% vacancy)")
    if m.population_growth_pct > 2.5:
        reasons.append(f"Strong population growth ({m.population_growth_pct}%)")
    if m.infrastructure_score > 75:
        reasons.append(f"Major infrastructure investment (score {m.infrastructure_score}/100)")
    if m.price_cagr_5yr > 8:
        reasons.append(f"Strong recent price growth ({m.price_cagr_5yr}% 5yr CAGR)")
    if m.rent_growth_annual_pct > 6:
        reasons.append(f"Accelerating rents ({m.rent_growth_annual_pct}% annual growth)")
    if m.stock_on_market < 12:
        reasons.append(f"Supply constrained (only {m.stock_on_market}/1000 listings)")

    if reasons:
        print("  WHY THIS SUBURB?")
        for r in reasons:
            print(f"    + {r}")
    print()


def main():
    parser = argparse.ArgumentParser(
        description="Property Investment Analysis Tool — find high capital growth suburbs",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --budget-min 800000 --budget-max 1000000
  python main.py --budget-max 700000 --states QLD SA WA --detailed
  python main.py --priority yield --min-yield 4.5
        """,
    )
    parser.add_argument("--budget-min", type=int, default=0, help="Minimum budget (default: 0)")
    parser.add_argument("--budget-max", type=int, default=1_000_000, help="Maximum budget (default: 1,000,000)")
    parser.add_argument("--states", nargs="+", choices=[s.value for s in State], help="Filter by state(s)")
    parser.add_argument("--property-type", choices=["house", "unit", "townhouse"], default="house")
    parser.add_argument("--priority", choices=["capital_growth", "yield", "balanced"], default="capital_growth")
    parser.add_argument("--min-yield", type=float, default=0, help="Minimum gross yield %%")
    parser.add_argument("--min-score", type=float, default=0, help="Minimum overall score (0-100)")
    parser.add_argument("--detailed", action="store_true", help="Show detailed suburb report cards")
    parser.add_argument("--top", type=int, default=10, help="Number of results to show")

    args = parser.parse_args()

    criteria = SearchCriteria(
        budget_min=args.budget_min,
        budget_max=args.budget_max,
        property_types=[PropertyType(args.property_type)],
        states=[State(s) for s in args.states] if args.states else [],
        min_yield_pct=args.min_yield,
        priority=args.priority,
        min_overall_score=args.min_score,
    )

    suburbs = get_suburbs()
    results = search(suburbs, criteria)
    top_results = results[: args.top]

    print_summary(top_results, criteria)

    if args.detailed and top_results:
        print(f"\n{'='*70}")
        print(f"  DETAILED SUBURB REPORT CARDS")
        print(f"{'='*70}")
        for i, s in enumerate(top_results, 1):
            print_detailed(s, i)

    if not args.detailed and top_results:
        print("  Tip: Use --detailed for full suburb report cards\n")

    # Disclaimer
    print("  ⚠  DISCLAIMER: This tool uses sample data for illustration only.")
    print("     Always consult a qualified buyer's agent and do your own research.")
    print("     Past performance does not guarantee future capital growth.\n")


if __name__ == "__main__":
    main()
