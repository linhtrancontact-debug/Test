#!/usr/bin/env python3
"""
SMSF Property Loan Calculator

Calculates borrowing capacity, compares SMSF vs personal lending,
and shows which properties from the investment guide are affordable.
"""

import sys
from tabulate import tabulate


# ── Defaults ─────────────────────────────────────────────────────────────────

DEFAULT_SMSF_BALANCE = 250_000
DEFAULT_PERSONAL_CASH = 0

# SMSF loan parameters (typical non-major lender 2025)
SMSF_MAX_LVR = 0.70
SMSF_RATE = 0.072          # 7.2% variable
SMSF_LOAN_TERM_YEARS = 25
SMSF_TAX_RATE = 0.15       # 15% concessional
SMSF_PENSION_CGT = 0.0     # 0% if held to pension phase
SMSF_MIN_CASH_BUFFER = 50_000  # Keep in SMSF for liquidity

# Standard investment loan parameters
STD_MAX_LVR = 0.80
STD_RATE = 0.065            # 6.5% variable
STD_LOAN_TERM_YEARS = 30
STD_TAX_RATE = 0.37         # Marginal rate (assuming ~$120K+ income)
STD_CGT_DISCOUNT = 0.50     # 50% CGT discount after 12 months

# Costs
STAMP_DUTY_RATES_NSW = [
    (17_000, 0.0125),
    (35_000, 0.015),
    (96_000, 0.0175),
    (364_000, 0.035),
    (3_101_000, 0.045),
    (float("inf"), 0.055),
]
STAMP_DUTY_RATES_QLD = [
    (75_000, 0.015),
    (150_000, 0.025),
    (350_000, 0.03),
    (540_000, 0.035),
    (1_000_000, 0.0375),
    (float("inf"), 0.0450),
]

LEGAL_FEES = 3_000
SMSF_BARE_TRUST_SETUP = 2_500
SMSF_ANNUAL_ADMIN = 3_500
BUILDING_PEST = 1_000


def calc_stamp_duty(price: int, state: str = "NSW") -> int:
    """Simplified stamp duty calculation."""
    rates = STAMP_DUTY_RATES_NSW if state == "NSW" else STAMP_DUTY_RATES_QLD
    duty = 0
    prev_threshold = 0
    for threshold, rate in rates:
        taxable = min(price, threshold) - prev_threshold
        if taxable <= 0:
            break
        duty += taxable * rate
        prev_threshold = threshold
    return int(duty)


def monthly_repayment(principal: float, annual_rate: float, years: int) -> float:
    """Calculate monthly P&I repayment."""
    r = annual_rate / 12
    n = years * 12
    if r == 0:
        return principal / n
    return principal * (r * (1 + r) ** n) / ((1 + r) ** n - 1)


def fmt(amount) -> str:
    if isinstance(amount, float):
        amount = int(amount)
    if abs(amount) >= 1_000_000:
        return f"${amount / 1_000_000:.2f}M"
    return f"${amount:,.0f}"


def analyse_smsf(smsf_balance: int, target_prices: list[dict]):
    """Analyse what the user can afford via SMSF."""

    available_deposit = smsf_balance - SMSF_MIN_CASH_BUFFER
    if available_deposit <= 0:
        print(f"\n  Your SMSF balance ({fmt(smsf_balance)}) is too low.")
        print(f"  After keeping {fmt(SMSF_MIN_CASH_BUFFER)} liquidity buffer, nothing remains for a deposit.")
        return

    print(f"\n{'='*74}")
    print(f"  SMSF PROPERTY AFFORDABILITY CALCULATOR")
    print(f"{'='*74}")
    print(f"\n  YOUR SITUATION")
    print(f"    SMSF Balance:          {fmt(smsf_balance)}")
    print(f"    Cash Outside Super:    $0")
    print(f"    Liquidity Buffer:      {fmt(SMSF_MIN_CASH_BUFFER)} (kept in SMSF for admin/insurance)")
    print(f"    Available for Purchase:{fmt(available_deposit)}")

    # Max purchase price
    # available = deposit + stamp_duty + legal + bare_trust + building
    # deposit = price * (1 - LVR)
    # So: available = price * 0.30 + stamp_duty(price) + legal + bare_trust + building
    # Solve iteratively
    max_price = 0
    for price in range(400_000, 1_200_001, 10_000):
        state = "NSW"  # Default, recalc per property later
        sd = calc_stamp_duty(price, state)
        deposit = int(price * (1 - SMSF_MAX_LVR))
        total_upfront = deposit + sd + LEGAL_FEES + SMSF_BARE_TRUST_SETUP + BUILDING_PEST
        if total_upfront <= available_deposit:
            max_price = price
        else:
            break

    print(f"\n  SMSF BORROWING CAPACITY (70% LVR)")
    print(f"    Max Purchase Price:    {fmt(max_price)}")
    print(f"    Max Loan Amount:       {fmt(int(max_price * SMSF_MAX_LVR))}")
    print(f"    Interest Rate:         {SMSF_RATE * 100:.1f}%")
    print(f"    Loan Term:             {SMSF_LOAN_TERM_YEARS} years")

    loan = int(max_price * SMSF_MAX_LVR)
    monthly = monthly_repayment(loan, SMSF_RATE, SMSF_LOAN_TERM_YEARS)
    print(f"    Monthly Repayment:     {fmt(int(monthly))}/month")
    print(f"    Annual Repayment:      {fmt(int(monthly * 12))}/year")

    # ── Breakdown per target property ────────────────────────────────────
    print(f"\n{'─'*74}")
    print(f"  CAN YOU AFFORD THE TOP 5 SUBURBS?")
    print(f"{'─'*74}\n")

    rows = []
    for p in target_prices:
        name = p["name"]
        price = p["price"]
        state = p["state"]
        yield_pct = p["yield"]

        sd = calc_stamp_duty(price, state)
        deposit = int(price * (1 - SMSF_MAX_LVR))
        total_upfront = deposit + sd + LEGAL_FEES + SMSF_BARE_TRUST_SETUP + BUILDING_PEST
        shortfall = max(0, total_upfront - available_deposit)
        affordable = "YES" if shortfall == 0 else f"NO (-{fmt(shortfall)})"

        loan_amt = int(price * SMSF_MAX_LVR)
        mthly = monthly_repayment(loan_amt, SMSF_RATE, SMSF_LOAN_TERM_YEARS)
        annual_repay = mthly * 12

        weekly_rent = price * (yield_pct / 100) / 52
        annual_rent = weekly_rent * 52
        annual_costs = SMSF_ANNUAL_ADMIN + (annual_rent * 0.08) + (price * 0.004)  # mgmt + council/water/insurance
        net_income = annual_rent - annual_repay - annual_costs
        tax_on_income = max(0, (annual_rent - annual_costs) * SMSF_TAX_RATE) if annual_rent > annual_costs else 0

        rows.append([
            name,
            state,
            fmt(price),
            fmt(deposit),
            fmt(sd),
            fmt(total_upfront),
            affordable,
        ])

    headers = ["Suburb", "State", "Price", "Deposit(30%)", "Stamp Duty", "Total Upfront", "Affordable?"]
    print(tabulate(rows, headers=headers, tablefmt="simple_outline"))

    # ── Detailed breakdown for affordable properties ─────────────────────
    print(f"\n{'─'*74}")
    print(f"  DETAILED CASHFLOW — AFFORDABLE PROPERTIES")
    print(f"{'─'*74}")

    for p in target_prices:
        price = p["price"]
        state = p["state"]
        yield_pct = p["yield"]

        sd = calc_stamp_duty(price, state)
        deposit = int(price * (1 - SMSF_MAX_LVR))
        total_upfront = deposit + sd + LEGAL_FEES + SMSF_BARE_TRUST_SETUP + BUILDING_PEST

        if total_upfront > available_deposit:
            continue

        loan_amt = int(price * SMSF_MAX_LVR)
        mthly = monthly_repayment(loan_amt, SMSF_RATE, SMSF_LOAN_TERM_YEARS)
        annual_repay = mthly * 12

        annual_rent = price * (yield_pct / 100)
        weekly_rent = annual_rent / 52
        mgmt_fee = annual_rent * 0.08
        council_water_ins = price * 0.004
        annual_costs = SMSF_ANNUAL_ADMIN + mgmt_fee + council_water_ins
        taxable_income = annual_rent - (loan_amt * SMSF_RATE) - annual_costs  # Interest deductible
        tax = max(0, taxable_income * SMSF_TAX_RATE)
        net_cashflow = annual_rent - annual_repay - annual_costs - tax
        remaining_smsf = available_deposit - total_upfront + SMSF_MIN_CASH_BUFFER

        print(f"\n  {p['name']}, {state} — {fmt(price)}")
        print(f"  {'─'*40}")
        print(f"    Deposit (30%):         {fmt(deposit)}")
        print(f"    Stamp Duty:            {fmt(sd)}")
        print(f"    Legal + Bare Trust:     {fmt(LEGAL_FEES + SMSF_BARE_TRUST_SETUP)}")
        print(f"    Building & Pest:       {fmt(BUILDING_PEST)}")
        print(f"    TOTAL UPFRONT:         {fmt(total_upfront)}")
        print(f"    Remaining in SMSF:     {fmt(remaining_smsf)}")
        print()
        print(f"    Loan Amount:           {fmt(loan_amt)} @ {SMSF_RATE*100:.1f}%")
        print(f"    Monthly Repayment:     {fmt(int(mthly))}")
        print(f"    Annual Repayment:      {fmt(int(annual_repay))}")
        print()
        print(f"    INCOME")
        print(f"      Weekly Rent:         {fmt(int(weekly_rent))}/wk")
        print(f"      Annual Rent:         {fmt(int(annual_rent))}")
        print(f"    EXPENSES")
        print(f"      Loan Repayments:     {fmt(int(annual_repay))}")
        print(f"      SMSF Admin:          {fmt(SMSF_ANNUAL_ADMIN)}")
        print(f"      Property Mgmt (8%):  {fmt(int(mgmt_fee))}")
        print(f"      Council/Water/Ins:   {fmt(int(council_water_ins))}")
        print(f"      Tax (15%):           {fmt(int(tax))}")
        print(f"    ────────────────────────────────────")
        cashflow_label = "SURPLUS" if net_cashflow >= 0 else "SHORTFALL"
        print(f"    NET ANNUAL CASHFLOW:   {fmt(int(net_cashflow))} ({cashflow_label})")
        print(f"    NET MONTHLY CASHFLOW:  {fmt(int(net_cashflow / 12))}/month")

        if net_cashflow < 0:
            print(f"\n    ⚠  This property is NEGATIVELY GEARED by {fmt(int(abs(net_cashflow)))}/yr")
            print(f"       Your SMSF needs other income (contributions, dividends) to cover")
            print(f"       the {fmt(int(abs(net_cashflow / 12)))}/month shortfall.")
            years_buffer = remaining_smsf / abs(net_cashflow) if net_cashflow < 0 else 999
            print(f"       SMSF cash buffer covers ~{years_buffer:.1f} years of shortfall.")

    # ── 10-year projection ───────────────────────────────────────────────
    print(f"\n{'─'*74}")
    print(f"  10-YEAR CAPITAL GROWTH PROJECTION")
    print(f"{'─'*74}\n")

    growth_rates = [0.05, 0.07, 0.09]  # Conservative, moderate, strong
    proj_rows = []
    for p in target_prices:
        price = p["price"]
        deposit = int(price * (1 - SMSF_MAX_LVR))
        sd = calc_stamp_duty(price, p["state"])
        total_upfront = deposit + sd + LEGAL_FEES + SMSF_BARE_TRUST_SETUP + BUILDING_PEST
        if total_upfront > available_deposit:
            continue

        vals = []
        for rate in growth_rates:
            future_val = int(price * (1 + rate) ** 10)
            equity_gain = future_val - price
            total_invested = total_upfront
            roi = (equity_gain / total_invested) * 100
            vals.extend([fmt(future_val), fmt(equity_gain), f"{roi:.0f}%"])

        proj_rows.append([p["name"], fmt(price)] + vals)

    if proj_rows:
        proj_headers = [
            "Suburb", "Buy Price",
            "Val@5%", "Gain@5%", "ROI@5%",
            "Val@7%", "Gain@7%", "ROI@7%",
            "Val@9%", "Gain@9%", "ROI@9%",
        ]
        print(tabulate(proj_rows, headers=proj_headers, tablefmt="simple_outline"))
        print()
        print("  Note: ROI = equity gain / total upfront cost. SMSF pension phase = 0% CGT.")
        print("  At marginal tax rate outside super, you'd lose ~23.5% of gains to CGT.")

    # ── Verdict ──────────────────────────────────────────────────────────
    print(f"\n{'='*74}")
    print(f"  VERDICT FOR YOUR SITUATION ($250K SMSF, $0 CASH)")
    print(f"{'='*74}")
    print(f"""
    Max affordable price (SMSF, 70% LVR):  {fmt(max_price)}

    AFFORDABLE from top 5:
""")
    for p in target_prices:
        sd = calc_stamp_duty(p["price"], p["state"])
        deposit = int(p["price"] * (1 - SMSF_MAX_LVR))
        total = deposit + sd + LEGAL_FEES + SMSF_BARE_TRUST_SETUP + BUILDING_PEST
        if total <= available_deposit:
            print(f"      ✓  {p['name']} ({p['state']}) — {fmt(p['price'])}")
        else:
            print(f"      ✗  {p['name']} ({p['state']}) — {fmt(p['price'])} (need extra {fmt(total - available_deposit)})")

    print(f"""
    RECOMMENDATION:
      With $250K in super and no outside cash, your best option is to
      target the MOST AFFORDABLE suburb with the highest growth potential.

      Look at properties UNDER {fmt(max_price)} in the top-ranked suburbs.
      The lower the purchase price, the more cash buffer you retain in
      your SMSF for loan repayments and holding costs.

    IMPORTANT NEXT STEPS:
      1. Confirm your SMSF trust deed allows property investment (LRBA)
      2. Appoint an SMSF-specialist accountant to review compliance
      3. Get pre-approval from an SMSF mortgage broker
      4. Ensure your employer contributions + rent cover loan repayments
      5. Consider: is your super balance growing fast enough to support this?
    """)


def main():
    smsf_balance = DEFAULT_SMSF_BALANCE
    if len(sys.argv) > 1:
        smsf_balance = int(sys.argv[1])

    target_prices = [
        {"name": "Oran Park", "price": 960_000, "state": "NSW", "yield": 3.7},
        {"name": "Leppington", "price": 880_000, "state": "NSW", "yield": 3.9},
        {"name": "Gledswood Hills", "price": 980_000, "state": "NSW", "yield": 3.6},
        {"name": "Coomera", "price": 820_000, "state": "QLD", "yield": 4.1},
        {"name": "Box Hill (NSW)", "price": 990_000, "state": "NSW", "yield": 3.5},
    ]

    analyse_smsf(smsf_balance, target_prices)

    print("  ⚠  DISCLAIMER: This calculator uses estimates and general assumptions.")
    print("     Rates, fees, stamp duty, and lending criteria change frequently.")
    print("     This is NOT financial advice. Consult a licensed financial adviser,")
    print("     SMSF accountant, and mortgage broker before making any decisions.\n")


if __name__ == "__main__":
    main()
