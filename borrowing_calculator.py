#!/usr/bin/env python3
"""
Personal vs SMSF Borrowing Comparison Calculator.

Compares what a couple can afford buying personally vs through SMSF,
given their combined income and super balance.
"""

import sys
from tabulate import tabulate


# ── Inputs ───────────────────────────────────────────────────────────────────

INCOME_1 = 135_000
INCOME_2 = 160_000
COMBINED_INCOME = INCOME_1 + INCOME_2  # $295K
SUPER_BALANCE = 250_000
PERSONAL_CASH = 0

# Super contributions (employer 11.5% of gross salary)
SUPER_GUARANTEE_RATE = 0.115
ANNUAL_SUPER_CONTRIB_1 = int(INCOME_1 * SUPER_GUARANTEE_RATE)  # ~$15,525
ANNUAL_SUPER_CONTRIB_2 = int(INCOME_2 * SUPER_GUARANTEE_RATE)  # ~$18,400
TOTAL_ANNUAL_SUPER = ANNUAL_SUPER_CONTRIB_1 + ANNUAL_SUPER_CONTRIB_2

# ── Personal Loan Parameters ────────────────────────────────────────────────

PERSONAL_RATE = 0.0639          # Current avg investment rate
PERSONAL_BUFFER_RATE = 0.03     # Banks assess at rate + 3%
PERSONAL_TERM = 30
PERSONAL_LVR = 0.80
PERSONAL_DTI_CAP = 6.0          # Debt-to-income ratio cap
MARGINAL_TAX_RATE = 0.37        # $135K earner
MARGINAL_TAX_RATE_2 = 0.37      # $160K earner
CGT_DISCOUNT = 0.50             # 50% after 12 months

# ── SMSF Loan Parameters ────────────────────────────────────────────────────

SMSF_RATE = 0.072
SMSF_TERM = 25
SMSF_LVR = 0.70
SMSF_TAX_RATE = 0.15
SMSF_PENSION_CGT = 0.0
SMSF_CASH_BUFFER = 50_000
SMSF_ANNUAL_ADMIN = 3_500
SMSF_BARE_TRUST = 2_500

# ── Common Costs ─────────────────────────────────────────────────────────────

LEGAL_FEES = 3_000
BUILDING_PEST = 1_000


def monthly_repayment(principal: float, annual_rate: float, years: int) -> float:
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


def calc_stamp_duty(price: int, state: str = "NSW") -> int:
    """Simplified stamp duty."""
    rates_nsw = [
        (17_000, 0.0125), (35_000, 0.015), (96_000, 0.0175),
        (364_000, 0.035), (3_101_000, 0.045), (float("inf"), 0.055),
    ]
    rates_qld = [
        (75_000, 0.015), (150_000, 0.025), (350_000, 0.03),
        (540_000, 0.035), (1_000_000, 0.0375), (float("inf"), 0.045),
    ]
    rates = rates_nsw if state in ("NSW", "VIC", "WA", "SA") else rates_qld
    duty = 0
    prev = 0
    for threshold, rate in rates:
        taxable = min(price, threshold) - prev
        if taxable <= 0:
            break
        duty += taxable * rate
        prev = threshold
    return int(duty)


def personal_borrowing_capacity():
    """Calculate max borrowing using bank serviceability rules."""
    # Method 1: DTI ratio
    max_loan_dti = int(COMBINED_INCOME * PERSONAL_DTI_CAP)

    # Method 2: Serviceability (30% of gross income at assessment rate)
    assessment_rate = PERSONAL_RATE + PERSONAL_BUFFER_RATE
    max_annual_repayment = COMBINED_INCOME * 0.30
    max_monthly = max_annual_repayment / 12
    # Reverse calc from monthly repayment to principal
    r = assessment_rate / 12
    n = PERSONAL_TERM * 12
    max_loan_service = int(max_monthly * ((1 + r) ** n - 1) / (r * (1 + r) ** n))

    return min(max_loan_dti, max_loan_service)


def smsf_max_purchase():
    """Max SMSF purchase price given balance."""
    available = SUPER_BALANCE - SMSF_CASH_BUFFER
    max_price = 0
    for price in range(300_000, 1_500_001, 10_000):
        deposit = int(price * (1 - SMSF_LVR))
        sd = calc_stamp_duty(price, "NSW")
        total = deposit + sd + LEGAL_FEES + SMSF_BARE_TRUST + BUILDING_PEST
        if total <= available:
            max_price = price
        else:
            break
    return max_price


def main():
    print(f"\n{'='*78}")
    print(f"  PERSONAL vs SMSF BORROWING COMPARISON")
    print(f"{'='*78}")

    print(f"\n  YOUR HOUSEHOLD")
    print(f"    Your Income:           {fmt(INCOME_1)}/year (excl. super)")
    print(f"    Wes's Income:          {fmt(INCOME_2)}/year (excl. super)")
    print(f"    Combined Income:       {fmt(COMBINED_INCOME)}/year")
    print(f"    SMSF Balance:          {fmt(SUPER_BALANCE)}")
    print(f"    Cash Savings:          $0")
    print(f"    Annual Super In:       {fmt(TOTAL_ANNUAL_SUPER)}/yr ({fmt(ANNUAL_SUPER_CONTRIB_1)} + {fmt(ANNUAL_SUPER_CONTRIB_2)})")

    # ── Personal Borrowing ───────────────────────────────────────────────
    max_loan = personal_borrowing_capacity()
    max_price_80 = int(max_loan / PERSONAL_LVR)

    # But they have $0 cash for deposit...
    # Option A: Save for deposit
    deposit_needed_900k = int(900_000 * 0.20) + calc_stamp_duty(900_000) + LEGAL_FEES + BUILDING_PEST
    deposit_needed_800k = int(800_000 * 0.20) + calc_stamp_duty(800_000) + LEGAL_FEES + BUILDING_PEST
    monthly_savings = int(COMBINED_INCOME * 0.25 / 12)  # Assume 25% savings rate
    months_to_800k = deposit_needed_800k // monthly_savings
    months_to_900k = deposit_needed_900k // monthly_savings

    print(f"\n{'─'*78}")
    print(f"  OPTION 1: BUY PERSONALLY (Standard Home Loan)")
    print(f"{'─'*78}")
    print(f"\n  BORROWING CAPACITY")
    print(f"    Max Loan (DTI 6x):     {fmt(int(COMBINED_INCOME * PERSONAL_DTI_CAP))}")
    print(f"    Max Loan (Serv. test): {fmt(max_loan)}")
    print(f"    Effective Max Loan:    {fmt(max_loan)}")
    print(f"    Max Purchase (80% LVR):{fmt(max_price_80)}")
    print(f"    Interest Rate:         {PERSONAL_RATE * 100:.2f}%")
    print(f"    Term:                  {PERSONAL_TERM} years")

    print(f"\n  THE PROBLEM: You have $0 cash for a deposit")
    print(f"    Deposit + costs for $800K property: {fmt(deposit_needed_800k)}")
    print(f"    Deposit + costs for $900K property: {fmt(deposit_needed_900k)}")

    print(f"\n  HOW LONG TO SAVE? (assuming 25% savings rate = {fmt(monthly_savings)}/month)")
    print(f"    For $800K property: ~{months_to_800k} months ({months_to_800k // 12} yrs {months_to_800k % 12} mo)")
    print(f"    For $900K property: ~{months_to_900k} months ({months_to_900k // 12} yrs {months_to_900k % 12} mo)")

    # ── Option B: Family Guarantee ───────────────────────────────────────
    print(f"\n  SHORTCUT: Family Guarantee / Guarantor Loan")
    print(f"    If a family member can guarantee using their property:")
    print(f"    → You could buy with $0 deposit, NO LMI, up to {fmt(max_price_80)}")
    print(f"    → You only need stamp duty + legal costs:")

    for price in [800_000, 900_000, 1_000_000]:
        sd = calc_stamp_duty(price, "NSW")
        costs = sd + LEGAL_FEES + BUILDING_PEST
        loan = int(price * PERSONAL_LVR)
        mthly = monthly_repayment(loan, PERSONAL_RATE, PERSONAL_TERM)
        print(f"       {fmt(price)} property: {fmt(costs)} costs, {fmt(int(mthly))}/mo repayment")

    # ── SMSF Option ──────────────────────────────────────────────────────
    smsf_max = smsf_max_purchase()
    smsf_loan = int(smsf_max * SMSF_LVR)
    smsf_monthly = monthly_repayment(smsf_loan, SMSF_RATE, SMSF_TERM)
    smsf_annual_repay = smsf_monthly * 12

    print(f"\n{'─'*78}")
    print(f"  OPTION 2: BUY THROUGH SMSF")
    print(f"{'─'*78}")
    print(f"\n  SMSF CAPACITY")
    print(f"    SMSF Balance:          {fmt(SUPER_BALANCE)}")
    print(f"    Less Cash Buffer:      -{fmt(SMSF_CASH_BUFFER)}")
    print(f"    Available:             {fmt(SUPER_BALANCE - SMSF_CASH_BUFFER)}")
    print(f"    Max Purchase (70% LVR):{fmt(smsf_max)}")
    print(f"    Loan Amount:           {fmt(smsf_loan)}")
    print(f"    Monthly Repayment:     {fmt(int(smsf_monthly))}")
    print(f"    Interest Rate:         {SMSF_RATE * 100:.1f}% (higher than personal)")

    print(f"\n  SMSF CASHFLOW CHECK")
    print(f"    Annual Super Contributions:  {fmt(TOTAL_ANNUAL_SUPER)}")
    print(f"    Annual Loan Repayments:      {fmt(int(smsf_annual_repay))}")
    print(f"    Estimated Annual Rent (5%):  {fmt(int(smsf_max * 0.05))}")
    print(f"    SMSF Admin Costs:            {fmt(SMSF_ANNUAL_ADMIN)}")
    print(f"    Property Costs (est):        {fmt(int(smsf_max * 0.012))}")
    total_in = TOTAL_ANNUAL_SUPER + int(smsf_max * 0.05)
    total_out = int(smsf_annual_repay) + SMSF_ANNUAL_ADMIN + int(smsf_max * 0.012)
    net = total_in - total_out
    print(f"    ─────────────────────────────────")
    print(f"    Total In (contrib + rent):   {fmt(total_in)}")
    print(f"    Total Out (loan + costs):    {fmt(total_out)}")
    label = "SURPLUS" if net >= 0 else "SHORTFALL"
    print(f"    NET ANNUAL:                  {fmt(net)} ({label})")

    # ── Side-by-side comparison ──────────────────────────────────────────
    print(f"\n{'─'*78}")
    print(f"  SIDE-BY-SIDE COMPARISON")
    print(f"{'─'*78}\n")

    comparison = [
        ["Max Purchase Price", fmt(max_price_80) + " *", fmt(smsf_max)],
        ["LVR", "80%", "70%"],
        ["Interest Rate", f"{PERSONAL_RATE*100:.2f}%", f"{SMSF_RATE*100:.1f}%"],
        ["Loan Term", f"{PERSONAL_TERM} years", f"{SMSF_TERM} years"],
        ["Deposit Required", "20% + costs", "30% + costs (from super)"],
        ["Cash Needed Today", fmt(deposit_needed_800k) + " (for $800K)", "$0 personal cash"],
        ["Tax on Rental Income", f"{MARGINAL_TAX_RATE*100:.0f}% marginal", f"{SMSF_TAX_RATE*100:.0f}% flat"],
        ["CGT on Sale", f"{MARGINAL_TAX_RATE*100:.0f}% (with 50% discount)", "0% (pension phase)"],
        ["Renovation Allowed", "Yes, unlimited", "No (repairs only)"],
        ["Can You Live In It", "Yes (if owner-occ)", "No — must rent to strangers"],
        ["Negative Gearing", "Offsets personal income", "Trapped inside SMSF"],
        ["Your Budget Range", "$800K-$1M (need deposit)", "Max $570K"],
    ]
    print(tabulate(comparison, headers=["", "PERSONAL LOAN", "SMSF LOAN"], tablefmt="simple_outline"))

    # ── 10-year wealth comparison ────────────────────────────────────────
    print(f"\n{'─'*78}")
    print(f"  10-YEAR WEALTH COMPARISON (@ 7% annual growth)")
    print(f"{'─'*78}\n")

    growth = 0.07
    scenarios = [
        ("Personal: $900K property", 900_000, PERSONAL_RATE, PERSONAL_TERM, PERSONAL_LVR, "personal"),
        ("Personal: $800K property", 800_000, PERSONAL_RATE, PERSONAL_TERM, PERSONAL_LVR, "personal"),
        ("SMSF: $560K (Ellenbrook)", 560_000, SMSF_RATE, SMSF_TERM, SMSF_LVR, "smsf"),
        ("SMSF: $450K (Munno Para)", 450_000, SMSF_RATE, SMSF_TERM, SMSF_LVR, "smsf"),
    ]

    rows = []
    for label, price, rate, term, lvr, mode in scenarios:
        future_val = int(price * (1 + growth) ** 10)
        equity_gain = future_val - price
        loan = int(price * lvr)
        deposit = int(price * (1 - lvr))

        if mode == "personal":
            # CGT: 50% discount, then marginal rate
            cgt = int(equity_gain * 0.5 * MARGINAL_TAX_RATE)
            net_gain = equity_gain - cgt
        else:
            # SMSF pension phase = 0% CGT
            cgt = 0
            net_gain = equity_gain

        rows.append([
            label, fmt(price), fmt(future_val), fmt(equity_gain),
            fmt(cgt), fmt(net_gain),
        ])

    print(tabulate(rows, headers=[
        "Scenario", "Buy Price", "Value @10yr", "Gross Gain", "CGT", "Net Gain"
    ], tablefmt="simple_outline"))

    # ── Verdict ──────────────────────────────────────────────────────────
    print(f"\n{'='*78}")
    print(f"  VERDICT & RECOMMENDED STRATEGY")
    print(f"{'='*78}")
    print(f"""
  With {fmt(COMBINED_INCOME)}/yr combined income, you have STRONG borrowing
  capacity ({fmt(max_loan)} loan). The problem is the $0 deposit.

  OPTION A: SAVE & BUY PERSONALLY (RECOMMENDED if you can wait)
  ─────────────────────────────────────────────────────────────
    • Save {fmt(monthly_savings)}/month (25% of income)
    • In {months_to_800k // 12} years {months_to_800k % 12} months → buy $800K-$1M in Oran Park/Leppington
    • Lower interest rate ({PERSONAL_RATE*100:.2f}% vs {SMSF_RATE*100:.1f}%)
    • Can negatively gear against your {fmt(COMBINED_INCOME)} income
    • More suburbs in range, stronger capital growth suburbs

  OPTION B: FAMILY GUARANTEE (BEST if available)
  ─────────────────────────────────────────────────────────────
    • If parents/family can guarantee → buy NOW with $0 deposit
    • Only need ~{fmt(calc_stamp_duty(900_000) + LEGAL_FEES + BUILDING_PEST)} for stamp duty + costs on a $900K property
    • Could potentially borrow this or save in ~{(calc_stamp_duty(900_000) + LEGAL_FEES + BUILDING_PEST) // monthly_savings} months
    • Access the $800K-$1M high-growth suburbs immediately

  OPTION C: BUY VIA SMSF NOW (if you can't wait)
  ─────────────────────────────────────────────────────────────
    • Max $570K — limited to WA/SA suburbs
    • Higher rate, lower growth suburbs, negative cashflow
    • But: 0% CGT in pension phase is a big long-term advantage
    • Your {fmt(TOTAL_ANNUAL_SUPER)}/yr super contributions help cover shortfall
    • Best SMSF pick: Ellenbrook WA ($560K) or Munno Para West SA ($450K)

  OPTION D: HYBRID — SMSF NOW + SAVE FOR PERSONAL LATER
  ─────────────────────────────────────────────────────────────
    • Buy a $450K property in SMSF now (preserves cash buffer)
    • Simultaneously save for a personal deposit
    • In 2-3 years, buy an $800K-$1M property personally
    • End up with TWO investment properties
""")

    print("  ⚠  DISCLAIMER: This is illustrative analysis, NOT financial advice.")
    print("     Consult a licensed financial adviser, mortgage broker, and SMSF")
    print("     accountant before making any investment decisions.\n")


if __name__ == "__main__":
    main()
