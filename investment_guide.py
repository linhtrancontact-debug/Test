"""
Detailed Investment Guide for Top 5 Suburbs ($800K-$1M Budget).

Provides suburb profiles, infrastructure catalysts, what to look for,
and investment thesis for each recommended suburb.
"""


SUBURB_GUIDES = {
    "Oran Park": {
        "rank": 1,
        "score": 87,
        "state": "NSW",
        "postcode": "2570",
        "lga": "Camden",
        "median_house_price": "$960K",
        "budget_entry": "$850K-$1M (4-bed house, 300-450sqm lot)",
        "market_phase": "Early Recovery",
        "profile": (
            "Master-planned community in Camden LGA, south-west Sydney. "
            "One of the fastest-growing suburbs in NSW with a rapidly "
            "maturing town centre, new schools, and strong family demographics."
        ),
        "infrastructure_catalysts": [
            "Western Sydney International Airport (opening ~2026) — 15-20km away, "
            "will bring tens of thousands of jobs to the region",
            "Sydney Metro Western Sydney Airport line — Oran Park station planned "
            "in future extensions, providing direct rail connectivity",
            "Western Sydney Aerotropolis — planned city precinct bringing aerospace, "
            "defence, and advanced manufacturing jobs",
            "The Northern Road upgrades — improved connectivity to M5/M7 motorways",
            "Oran Park Town Centre — growing retail/commercial hub with supermarkets, "
            "medical, restaurants, and community facilities",
            "Multiple new schools (Oran Park Anglican College, Oran Park Public School)",
        ],
        "what_to_look_for": [
            "4-bed, 2-bath houses on 350-450sqm blocks — these appeal to "
            "owner-occupiers (broader resale market)",
            "Properties close to the town centre or future metro station alignment",
            "Established builds (1-5 years old) rather than off-the-plan — "
            "avoids developer premium",
            "Streets with mature landscaping and established neighbours",
        ],
        "investment_thesis": (
            "Oran Park scores highest because it sits at the intersection of "
            "THREE mega-infrastructure projects: the Western Sydney Airport, "
            "the Aerotropolis employment hub, and the future Metro extension. "
            "The suburb is in early recovery phase with 9.5% 5-year CAGR, "
            "sub-1% vacancy rate, and only 17 days on market. The combination "
            "of constrained supply (8 listings per 1000 dwellings), strong "
            "population growth (3.2%), and massive incoming infrastructure "
            "creates a compelling case for above-average capital growth over "
            "the next 5-10 years. High owner-occupier ratio (85%) provides "
            "a strong price floor."
        ),
        "risks": [
            "New supply from ongoing development could moderate price growth",
            "Airport construction delays may push catalysts further out",
            "Distance from Sydney CBD limits appeal for some buyers",
        ],
    },
    "Leppington": {
        "rank": 2,
        "score": 86,
        "state": "NSW",
        "postcode": "2179",
        "lga": "Camden",
        "median_house_price": "$880K",
        "budget_entry": "$800K-$950K (4-bed house, 300-400sqm lot)",
        "market_phase": "Early Recovery",
        "profile": (
            "Fast-growing suburb in Camden LGA, south-west Sydney. Home to "
            "the Willowdale and Emerald Hills estates. Already has a train "
            "station (opened 2015), giving it an edge over nearby suburbs."
        ),
        "infrastructure_catalysts": [
            "Leppington Train Station (operational since 2015) — direct CBD access "
            "via South West Rail Link",
            "Western Sydney Airport — very close proximity to Badgerys Creek site",
            "Sydney Metro Western Sydney Airport line — stations planned in the "
            "broader south-west corridor",
            "Western Sydney Aerotropolis — within the direct employment catchment",
            "Camden Valley Way and Bringelly Road upgrades",
            "Willowdale Shopping Centre and growing retail precincts",
            "Multiple new schools serving the growing population",
        ],
        "what_to_look_for": [
            "Properties within walking distance of Leppington Station — "
            "rail access is a proven value driver",
            "4-bed houses in Willowdale or Emerald Hills estates",
            "Blocks over 350sqm with north-facing backyards",
            "Established homes (avoid off-the-plan developer premiums)",
        ],
        "investment_thesis": (
            "Leppington's key advantage is its EXISTING train station plus "
            "proximity to the upcoming airport. It's one of the few suburbs "
            "in the south-west corridor with established rail connectivity, "
            "which consistently drives price premiums. At $880K median, it "
            "offers a lower entry point than Oran Park while delivering "
            "similar infrastructure upside. The 1.0% vacancy rate and 9.2% "
            "5-year CAGR demonstrate strong demand. Infrastructure score "
            "of 90/100 is the highest in our dataset."
        ),
        "risks": [
            "Higher building approvals could increase future supply",
            "Some pockets still feel 'new estate' with limited character",
            "Reliance on airport timeline for next growth catalyst",
        ],
    },
    "Gledswood Hills": {
        "rank": 3,
        "score": 85,
        "state": "NSW",
        "postcode": "2557",
        "lga": "Camden",
        "median_house_price": "$980K",
        "budget_entry": "$880K-$1M (entry-level 4-bed on smaller lots)",
        "market_phase": "Early Recovery",
        "profile": (
            "Newer residential suburb in Camden LGA, positioned between the "
            "Hume Motorway and Camden Valley Way. Attracts young families "
            "with high owner-occupier ratio (88%) and strong socioeconomic "
            "profile (SEIFA decile 8/10)."
        ),
        "infrastructure_catalysts": [
            "Western Sydney Airport — within the broader south-west growth corridor",
            "Aerotropolis employment precinct",
            "Hume Motorway access — strong connectivity to Sydney CBD and south",
            "Camden Valley Way upgrades",
            "Nearby Gregory Hills and Oran Park provide retail/commercial amenity",
            "Growing school infrastructure in the Camden corridor",
        ],
        "what_to_look_for": [
            "Properties at the lower end of the price range ($880K-$950K) for "
            "maximum capital growth runway",
            "Larger blocks (400sqm+) — land appreciates, buildings depreciate",
            "Corner blocks or properties with side access for future granny flat "
            "potential (rental yield boost)",
            "Proximity to Hume Motorway on-ramps for commuter appeal",
        ],
        "investment_thesis": (
            "Gledswood Hills offers the strongest demographic profile in the "
            "dataset — 88% owner-occupier ratio and SEIFA decile 8. This means "
            "the suburb attracts higher-income families who maintain their "
            "properties and provide a strong price floor. The extremely low "
            "vacancy rate (0.8%) and supply-constrained market (building "
            "approvals trending -6%) create upward pressure on both rents "
            "and prices. The 9.0% 5-year CAGR with early recovery phase "
            "positioning suggests more growth ahead."
        ),
        "risks": [
            "Higher entry price ($980K median) reduces capital growth headroom "
            "within a $1M budget",
            "Less infrastructure directly in the suburb — relies on nearby hubs",
            "Newer suburb still establishing its long-term identity",
        ],
    },
    "Coomera": {
        "rank": 4,
        "score": 83,
        "state": "QLD",
        "postcode": "4209",
        "lga": "Gold Coast",
        "median_house_price": "$820K",
        "budget_entry": "$800K-$950K (4-bed house, 400-600sqm lot)",
        "market_phase": "Early Recovery",
        "profile": (
            "Northern Gold Coast corridor suburb with strong population growth, "
            "established train station, and major retail hub. Benefits from "
            "Queensland's interstate migration boom and the Gold Coast's "
            "lifestyle appeal."
        ),
        "infrastructure_catalysts": [
            "Coomera Town Centre (Westfield Coomera, opened 2018) — major "
            "retail hub with further stages planned",
            "Coomera Connector — planned motorway-grade road linking Coomera "
            "to Nerang, relieving M1 congestion",
            "Coomera Train Station — operational, direct to Brisbane CBD "
            "and Gold Coast stations",
            "Theme parks precinct (Dreamworld, WhiteWater World, Movie World) "
            "— tourism employment base",
            "Gold Coast northern corridor — one of Australia's fastest-growing "
            "population corridors (Coomera, Pimpama, Ormeau)",
        ],
        "what_to_look_for": [
            "Established houses (5-15 years old) on larger Queensland blocks "
            "(450-600sqm) — MUCH more land for your money vs Sydney",
            "Properties near Coomera Station for commuter appeal",
            "Homes in elevated positions — flood mapping is important on the "
            "Gold Coast",
            "Properties with pools — high tenant/buyer demand in QLD climate",
        ],
        "investment_thesis": (
            "Coomera is the DIVERSIFICATION pick. At $820K median, it's the "
            "cheapest entry point in the top 5, and you get significantly more "
            "land than Sydney equivalents. Queensland's interstate migration "
            "from NSW and VIC continues to drive demand. The 4.1% gross yield "
            "is the highest in the top 5, providing better cashflow. The "
            "Coomera Connector road project will be a step-change for "
            "accessibility. Early recovery phase with 9.0% 5-year CAGR "
            "and only 1.1% vacancy."
        ),
        "risks": [
            "Gold Coast market historically more volatile than Sydney",
            "Flood risk in some pockets — due diligence on flood maps essential",
            "M1 congestion remains a quality-of-life issue until Connector opens",
        ],
    },
    "Box Hill (NSW)": {
        "rank": 5,
        "score": 81,
        "state": "NSW",
        "postcode": "2765",
        "lga": "The Hills",
        "median_house_price": "$990K",
        "budget_entry": "$900K-$1M (4-bed house, 300-400sqm lot)",
        "market_phase": "Early Recovery",
        "profile": (
            "Part of the North West Growth Area in The Hills Shire. "
            "Transitioning from semi-rural to master-planned residential. "
            "Benefits from proximity to Sydney Metro Northwest stations "
            "at Rouse Hill and Kellyville."
        ),
        "infrastructure_catalysts": [
            "Sydney Metro Northwest — Rouse Hill and Kellyville stations "
            "within short drive (metro opened 2019)",
            "Box Hill Town Centre — planned retail, commercial, community "
            "facilities, and higher-density housing precinct",
            "Road upgrades — Terry Road, Mason Road, Hezlett Road, "
            "connections to Windsor Road and M7 Motorway",
            "Rouse Hill Town Centre — major nearby shopping/entertainment hub",
            "North West Growth Area — government-backed population growth "
            "with committed infrastructure investment",
            "New schools planned and under construction",
        ],
        "what_to_look_for": [
            "Properties on the eastern side of Box Hill (closer to Rouse Hill "
            "metro station and town centre)",
            "Established homes rather than off-the-plan or display homes",
            "Check flood/creek mapping — some parts of Box Hill have "
            "watercourse constraints",
            "Blocks over 350sqm with potential for future subdivision "
            "(check council zoning)",
        ],
        "investment_thesis": (
            "Box Hill's appeal is its Hills Shire address at a relative "
            "discount. Established Hills suburbs like Castle Hill and "
            "Baulkham Hills trade at $1.5M+, while Box Hill offers new "
            "housing stock near the same metro line at $990K. The suburb "
            "has the highest SEIFA decile (8/10) tied with Gledswood Hills, "
            "attracting higher-income families. As the Box Hill Town Centre "
            "develops and the suburb matures, the gap to established Hills "
            "suburbs should narrow — that convergence is your capital growth."
        ),
        "risks": [
            "Highest entry price ($990K) leaves minimal budget headroom",
            "Box Hill Town Centre development timeline is uncertain",
            "Ongoing construction from new estates may impact liveability "
            "in the short term",
        ],
    },
}


def print_guide(suburb_name: str | None = None):
    """Print the investment guide for one or all suburbs."""
    guides = SUBURB_GUIDES
    if suburb_name and suburb_name in guides:
        guides = {suburb_name: guides[suburb_name]}

    for name, g in guides.items():
        print(f"\n{'='*72}")
        print(f"  #{g['rank']}  {name}, {g['state']} {g['postcode']}")
        print(f"  Overall Score: {g['score']}/100  |  Rating: HIGH  |  Phase: {g['market_phase']}")
        print(f"{'='*72}")

        print(f"\n  PRICE GUIDE")
        print(f"    Median House Price:  {g['median_house_price']}")
        print(f"    Your Budget Entry:   {g['budget_entry']}")

        print(f"\n  SUBURB PROFILE")
        print(f"    {g['profile']}")

        print(f"\n  INFRASTRUCTURE CATALYSTS")
        for item in g["infrastructure_catalysts"]:
            print(f"    * {item}")

        print(f"\n  WHAT TO LOOK FOR")
        for item in g["what_to_look_for"]:
            print(f"    > {item}")

        print(f"\n  INVESTMENT THESIS")
        print(f"    {g['investment_thesis']}")

        print(f"\n  RISKS TO WATCH")
        for item in g["risks"]:
            print(f"    ! {item}")

        print()


if __name__ == "__main__":
    import sys
    suburb = sys.argv[1] if len(sys.argv) > 1 else None
    print_guide(suburb)
    print("  *** DISCLAIMER: This is illustrative analysis based on general market")
    print("  knowledge, NOT live data. Always verify with current listings on")
    print("  realestate.com.au / domain.com.au and consult a qualified buyer's agent.")
    print("  Past performance does not guarantee future capital growth. ***\n")
