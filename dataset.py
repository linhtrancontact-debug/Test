"""
Sample Australian suburb dataset with realistic metrics.

This is illustrative data inspired by publicly available market trends.
In production, this would be sourced from CoreLogic, ABS, SQM Research, etc.
"""

from models import (
    Suburb, SuburbMetrics, PropertyType, MarketCyclePhase, State
)


def get_suburbs() -> list[Suburb]:
    return [
        # ── NSW ──────────────────────────────────────────────────────────
        Suburb(
            name="Marsden Park", state=State.NSW, postcode="2765",
            lga="Blacktown", median_house_price=920_000, median_unit_price=0,
            market_phase=MarketCyclePhase.RISING,
            property_types_available=[PropertyType.HOUSE],
            metrics=SuburbMetrics(
                population_growth_pct=2.8, employment_growth_pct=3.1,
                income_growth_pct=3.5, vacancy_rate_pct=1.2, days_on_market=22,
                online_search_interest=82, stock_on_market=12,
                building_approvals_trend=5, vendor_discount_pct=2.1,
                infrastructure_score=85, private_investment_score=70,
                price_cagr_10yr=7.2, price_cagr_5yr=8.1,
                rent_growth_annual_pct=6.5, gross_yield_pct=3.8,
                owner_occupier_ratio_pct=78, seifa_score=7,
            ),
        ),
        Suburb(
            name="Schofields", state=State.NSW, postcode="2762",
            lga="Blacktown", median_house_price=950_000, median_unit_price=580_000,
            market_phase=MarketCyclePhase.RISING,
            metrics=SuburbMetrics(
                population_growth_pct=2.5, employment_growth_pct=2.8,
                income_growth_pct=3.2, vacancy_rate_pct=1.4, days_on_market=25,
                online_search_interest=75, stock_on_market=14,
                building_approvals_trend=8, vendor_discount_pct=2.5,
                infrastructure_score=80, private_investment_score=65,
                price_cagr_10yr=6.8, price_cagr_5yr=7.5,
                rent_growth_annual_pct=5.8, gross_yield_pct=3.6,
                owner_occupier_ratio_pct=75, seifa_score=7,
            ),
        ),
        Suburb(
            name="Leppington", state=State.NSW, postcode="2179",
            lga="Camden", median_house_price=880_000, median_unit_price=0,
            market_phase=MarketCyclePhase.EARLY_RECOVERY,
            property_types_available=[PropertyType.HOUSE],
            metrics=SuburbMetrics(
                population_growth_pct=3.0, employment_growth_pct=3.5,
                income_growth_pct=3.0, vacancy_rate_pct=1.0, days_on_market=18,
                online_search_interest=88, stock_on_market=9,
                building_approvals_trend=-5, vendor_discount_pct=1.5,
                infrastructure_score=90, private_investment_score=80,
                price_cagr_10yr=7.8, price_cagr_5yr=9.2,
                rent_growth_annual_pct=7.0, gross_yield_pct=3.9,
                owner_occupier_ratio_pct=82, seifa_score=7,
            ),
        ),
        Suburb(
            name="Box Hill (NSW)", state=State.NSW, postcode="2765",
            lga="The Hills", median_house_price=990_000, median_unit_price=0,
            market_phase=MarketCyclePhase.EARLY_RECOVERY,
            property_types_available=[PropertyType.HOUSE],
            metrics=SuburbMetrics(
                population_growth_pct=2.6, employment_growth_pct=2.9,
                income_growth_pct=3.8, vacancy_rate_pct=1.1, days_on_market=20,
                online_search_interest=70, stock_on_market=10,
                building_approvals_trend=-3, vendor_discount_pct=1.8,
                infrastructure_score=75, private_investment_score=72,
                price_cagr_10yr=7.0, price_cagr_5yr=8.5,
                rent_growth_annual_pct=6.2, gross_yield_pct=3.5,
                owner_occupier_ratio_pct=80, seifa_score=8,
            ),
        ),

        # ── QLD ──────────────────────────────────────────────────────────
        Suburb(
            name="Ripley", state=State.QLD, postcode="4306",
            lga="Ipswich", median_house_price=620_000, median_unit_price=0,
            market_phase=MarketCyclePhase.EARLY_RECOVERY,
            property_types_available=[PropertyType.HOUSE],
            metrics=SuburbMetrics(
                population_growth_pct=3.5, employment_growth_pct=3.8,
                income_growth_pct=3.0, vacancy_rate_pct=0.8, days_on_market=16,
                online_search_interest=90, stock_on_market=8,
                building_approvals_trend=-2, vendor_discount_pct=1.0,
                infrastructure_score=88, private_investment_score=75,
                price_cagr_10yr=6.5, price_cagr_5yr=9.8,
                rent_growth_annual_pct=7.5, gross_yield_pct=4.5,
                owner_occupier_ratio_pct=85, seifa_score=6,
            ),
        ),
        Suburb(
            name="Park Ridge", state=State.QLD, postcode="4125",
            lga="Logan", median_house_price=680_000, median_unit_price=0,
            market_phase=MarketCyclePhase.EARLY_RECOVERY,
            property_types_available=[PropertyType.HOUSE],
            metrics=SuburbMetrics(
                population_growth_pct=3.2, employment_growth_pct=3.0,
                income_growth_pct=2.8, vacancy_rate_pct=0.9, days_on_market=17,
                online_search_interest=85, stock_on_market=9,
                building_approvals_trend=0, vendor_discount_pct=1.2,
                infrastructure_score=82, private_investment_score=70,
                price_cagr_10yr=6.2, price_cagr_5yr=9.0,
                rent_growth_annual_pct=7.0, gross_yield_pct=4.8,
                owner_occupier_ratio_pct=80, seifa_score=5,
            ),
        ),
        Suburb(
            name="Springfield Lakes", state=State.QLD, postcode="4300",
            lga="Ipswich", median_house_price=750_000, median_unit_price=450_000,
            market_phase=MarketCyclePhase.RISING,
            metrics=SuburbMetrics(
                population_growth_pct=2.8, employment_growth_pct=3.2,
                income_growth_pct=3.5, vacancy_rate_pct=1.0, days_on_market=19,
                online_search_interest=80, stock_on_market=11,
                building_approvals_trend=3, vendor_discount_pct=1.8,
                infrastructure_score=85, private_investment_score=78,
                price_cagr_10yr=6.8, price_cagr_5yr=8.8,
                rent_growth_annual_pct=6.5, gross_yield_pct=4.2,
                owner_occupier_ratio_pct=76, seifa_score=7,
            ),
        ),
        Suburb(
            name="Caboolture South", state=State.QLD, postcode="4510",
            lga="Moreton Bay", median_house_price=620_000, median_unit_price=380_000,
            market_phase=MarketCyclePhase.EARLY_RECOVERY,
            metrics=SuburbMetrics(
                population_growth_pct=2.5, employment_growth_pct=2.2,
                income_growth_pct=2.5, vacancy_rate_pct=1.3, days_on_market=24,
                online_search_interest=65, stock_on_market=15,
                building_approvals_trend=2, vendor_discount_pct=2.8,
                infrastructure_score=70, private_investment_score=55,
                price_cagr_10yr=5.5, price_cagr_5yr=7.5,
                rent_growth_annual_pct=5.5, gross_yield_pct=4.6,
                owner_occupier_ratio_pct=68, seifa_score=4,
            ),
        ),

        # ── VIC ──────────────────────────────────────────────────────────
        Suburb(
            name="Tarneit", state=State.VIC, postcode="3029",
            lga="Wyndham", median_house_price=650_000, median_unit_price=420_000,
            market_phase=MarketCyclePhase.BOTTOM,
            metrics=SuburbMetrics(
                population_growth_pct=3.0, employment_growth_pct=2.5,
                income_growth_pct=2.8, vacancy_rate_pct=1.8, days_on_market=32,
                online_search_interest=60, stock_on_market=18,
                building_approvals_trend=5, vendor_discount_pct=3.5,
                infrastructure_score=70, private_investment_score=60,
                price_cagr_10yr=5.0, price_cagr_5yr=4.5,
                rent_growth_annual_pct=5.0, gross_yield_pct=4.0,
                owner_occupier_ratio_pct=72, seifa_score=5,
            ),
        ),
        Suburb(
            name="Craigieburn", state=State.VIC, postcode="3064",
            lga="Hume", median_house_price=680_000, median_unit_price=430_000,
            market_phase=MarketCyclePhase.BOTTOM,
            metrics=SuburbMetrics(
                population_growth_pct=2.2, employment_growth_pct=2.0,
                income_growth_pct=2.5, vacancy_rate_pct=2.0, days_on_market=35,
                online_search_interest=55, stock_on_market=20,
                building_approvals_trend=8, vendor_discount_pct=4.0,
                infrastructure_score=65, private_investment_score=55,
                price_cagr_10yr=4.8, price_cagr_5yr=4.0,
                rent_growth_annual_pct=4.5, gross_yield_pct=3.8,
                owner_occupier_ratio_pct=70, seifa_score=5,
            ),
        ),
        Suburb(
            name="Truganina", state=State.VIC, postcode="3029",
            lga="Wyndham", median_house_price=640_000, median_unit_price=0,
            market_phase=MarketCyclePhase.EARLY_RECOVERY,
            property_types_available=[PropertyType.HOUSE],
            metrics=SuburbMetrics(
                population_growth_pct=3.2, employment_growth_pct=3.0,
                income_growth_pct=3.0, vacancy_rate_pct=1.5, days_on_market=28,
                online_search_interest=68, stock_on_market=14,
                building_approvals_trend=2, vendor_discount_pct=2.5,
                infrastructure_score=72, private_investment_score=65,
                price_cagr_10yr=5.5, price_cagr_5yr=5.8,
                rent_growth_annual_pct=5.5, gross_yield_pct=4.2,
                owner_occupier_ratio_pct=75, seifa_score=5,
            ),
        ),

        # ── SA ───────────────────────────────────────────────────────────
        Suburb(
            name="Munno Para West", state=State.SA, postcode="5115",
            lga="Playford", median_house_price=450_000, median_unit_price=0,
            market_phase=MarketCyclePhase.RISING,
            property_types_available=[PropertyType.HOUSE],
            metrics=SuburbMetrics(
                population_growth_pct=2.0, employment_growth_pct=2.5,
                income_growth_pct=2.2, vacancy_rate_pct=0.6, days_on_market=14,
                online_search_interest=72, stock_on_market=7,
                building_approvals_trend=-5, vendor_discount_pct=0.8,
                infrastructure_score=65, private_investment_score=50,
                price_cagr_10yr=5.0, price_cagr_5yr=10.5,
                rent_growth_annual_pct=8.0, gross_yield_pct=5.5,
                owner_occupier_ratio_pct=65, seifa_score=3,
            ),
        ),
        Suburb(
            name="Mount Barker", state=State.SA, postcode="5251",
            lga="Mount Barker", median_house_price=580_000, median_unit_price=380_000,
            market_phase=MarketCyclePhase.EARLY_RECOVERY,
            metrics=SuburbMetrics(
                population_growth_pct=2.8, employment_growth_pct=2.5,
                income_growth_pct=3.0, vacancy_rate_pct=0.7, days_on_market=16,
                online_search_interest=78, stock_on_market=10,
                building_approvals_trend=-3, vendor_discount_pct=1.2,
                infrastructure_score=75, private_investment_score=60,
                price_cagr_10yr=5.8, price_cagr_5yr=9.5,
                rent_growth_annual_pct=7.5, gross_yield_pct=4.8,
                owner_occupier_ratio_pct=78, seifa_score=6,
            ),
        ),

        # ── WA ───────────────────────────────────────────────────────────
        Suburb(
            name="Baldivis", state=State.WA, postcode="6171",
            lga="Rockingham", median_house_price=580_000, median_unit_price=0,
            market_phase=MarketCyclePhase.EARLY_RECOVERY,
            property_types_available=[PropertyType.HOUSE],
            metrics=SuburbMetrics(
                population_growth_pct=2.5, employment_growth_pct=3.0,
                income_growth_pct=3.2, vacancy_rate_pct=0.5, days_on_market=12,
                online_search_interest=85, stock_on_market=6,
                building_approvals_trend=-8, vendor_discount_pct=0.5,
                infrastructure_score=70, private_investment_score=60,
                price_cagr_10yr=4.5, price_cagr_5yr=11.0,
                rent_growth_annual_pct=9.0, gross_yield_pct=5.2,
                owner_occupier_ratio_pct=82, seifa_score=6,
            ),
        ),
        Suburb(
            name="Ellenbrook", state=State.WA, postcode="6069",
            lga="Swan", median_house_price=560_000, median_unit_price=380_000,
            market_phase=MarketCyclePhase.RISING,
            metrics=SuburbMetrics(
                population_growth_pct=2.2, employment_growth_pct=2.8,
                income_growth_pct=3.0, vacancy_rate_pct=0.6, days_on_market=14,
                online_search_interest=80, stock_on_market=8,
                building_approvals_trend=-5, vendor_discount_pct=0.8,
                infrastructure_score=78, private_investment_score=65,
                price_cagr_10yr=4.2, price_cagr_5yr=10.2,
                rent_growth_annual_pct=8.5, gross_yield_pct=5.0,
                owner_occupier_ratio_pct=80, seifa_score=6,
            ),
        ),

        # ── More NSW (higher price points) ───────────────────────────────
        Suburb(
            name="Oran Park", state=State.NSW, postcode="2570",
            lga="Camden", median_house_price=960_000, median_unit_price=0,
            market_phase=MarketCyclePhase.EARLY_RECOVERY,
            property_types_available=[PropertyType.HOUSE],
            metrics=SuburbMetrics(
                population_growth_pct=3.2, employment_growth_pct=3.5,
                income_growth_pct=3.6, vacancy_rate_pct=0.9, days_on_market=17,
                online_search_interest=92, stock_on_market=8,
                building_approvals_trend=-4, vendor_discount_pct=1.3,
                infrastructure_score=88, private_investment_score=82,
                price_cagr_10yr=8.0, price_cagr_5yr=9.5,
                rent_growth_annual_pct=7.2, gross_yield_pct=3.7,
                owner_occupier_ratio_pct=85, seifa_score=8,
            ),
        ),
        Suburb(
            name="Gledswood Hills", state=State.NSW, postcode="2557",
            lga="Camden", median_house_price=980_000, median_unit_price=0,
            market_phase=MarketCyclePhase.EARLY_RECOVERY,
            property_types_available=[PropertyType.HOUSE],
            metrics=SuburbMetrics(
                population_growth_pct=2.9, employment_growth_pct=3.2,
                income_growth_pct=4.0, vacancy_rate_pct=0.8, days_on_market=19,
                online_search_interest=78, stock_on_market=9,
                building_approvals_trend=-6, vendor_discount_pct=1.5,
                infrastructure_score=82, private_investment_score=75,
                price_cagr_10yr=7.5, price_cagr_5yr=9.0,
                rent_growth_annual_pct=6.8, gross_yield_pct=3.6,
                owner_occupier_ratio_pct=88, seifa_score=8,
            ),
        ),

        # ── More QLD (Brisbane metro) ────────────────────────────────────
        Suburb(
            name="Redbank Plains", state=State.QLD, postcode="4301",
            lga="Ipswich", median_house_price=600_000, median_unit_price=0,
            market_phase=MarketCyclePhase.RISING,
            property_types_available=[PropertyType.HOUSE],
            metrics=SuburbMetrics(
                population_growth_pct=2.8, employment_growth_pct=2.5,
                income_growth_pct=2.5, vacancy_rate_pct=1.0, days_on_market=18,
                online_search_interest=75, stock_on_market=11,
                building_approvals_trend=0, vendor_discount_pct=1.5,
                infrastructure_score=72, private_investment_score=60,
                price_cagr_10yr=5.8, price_cagr_5yr=8.5,
                rent_growth_annual_pct=6.5, gross_yield_pct=4.8,
                owner_occupier_ratio_pct=72, seifa_score=4,
            ),
        ),
        Suburb(
            name="Coomera", state=State.QLD, postcode="4209",
            lga="Gold Coast", median_house_price=820_000, median_unit_price=520_000,
            market_phase=MarketCyclePhase.EARLY_RECOVERY,
            metrics=SuburbMetrics(
                population_growth_pct=3.0, employment_growth_pct=3.5,
                income_growth_pct=3.2, vacancy_rate_pct=1.1, days_on_market=20,
                online_search_interest=85, stock_on_market=10,
                building_approvals_trend=-2, vendor_discount_pct=1.8,
                infrastructure_score=85, private_investment_score=80,
                price_cagr_10yr=6.5, price_cagr_5yr=9.0,
                rent_growth_annual_pct=6.8, gross_yield_pct=4.1,
                owner_occupier_ratio_pct=76, seifa_score=6,
            ),
        ),
    ]
