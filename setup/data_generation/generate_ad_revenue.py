"""Generate AD_REVENUE table data - 50,000 daily ad events."""
import csv
import json
import os
import random
from datetime import timedelta

from config import (
    AD_TYPES, AD_TYPE_WEIGHTS,
    random_date, DATA_START_DATE, DATA_END_DATE
)

NUM_AD_EVENTS = 50_000
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")

LISTING_SOURCES = {
    "marketplace": 50_000,
    "motors": 20_000,
    "property": 15_000,
    "jobs": 15_000,
}

# Ad spending is weighted toward high-value product areas
SOURCE_WEIGHTS = [0.35, 0.25, 0.25, 0.15]

ADVERTISER_NAMES = {
    "marketplace": ["NZ Retail Group", "Tech Deals NZ", "HomeStyle NZ", "Sports Direct NZ",
                    "Fashion Forward", "Baby Warehouse", "Game On NZ", "Collectables Plus"],
    "motors": ["NZ Motors Ltd", "Auckland Auto Group", "Turners Cars", "Wellington Motors",
               "Canterbury Car Sales", "Drive NZ", "Pacific Motors", "Kiwi Auto"],
    "property": ["Harcourts", "Barfoot & Thompson", "Ray White", "Bayleys",
                 "LJ Hooker", "Tommy's Real Estate", "Property Brokers"],
    "jobs": ["Seek NZ", "Trade Me Jobs", "Hays Recruitment", "Robert Half",
             "Michael Page", "Hudson", "Randstad"],
}

CAMPAIGN_TYPES = ["awareness", "conversion", "retargeting", "seasonal", "launch"]
TARGET_AUDIENCES = ["18-25", "25-35", "35-45", "45-55", "55+", "All Ages",
                    "Auckland 25-45", "Wellington Professionals", "Canterbury Families"]


def generate_campaign_metadata(source, ad_type):
    advertiser = random.choice(ADVERTISER_NAMES.get(source, ADVERTISER_NAMES["marketplace"]))
    budget = random.choice([500, 1000, 2000, 5000, 10000, 20000, 50000])
    return json.dumps({
        "advertiser_name": advertiser,
        "budget_nzd": budget,
        "target_audience": random.choice(TARGET_AUDIENCES),
        "duration_days": random.choice([7, 14, 30, 60, 90]),
        "campaign_type": random.choice(CAMPAIGN_TYPES),
    })


def generate_ad_revenue():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    filepath = os.path.join(OUTPUT_DIR, "ad_revenue.csv")

    sources = list(LISTING_SOURCES.keys())
    campaign_counter = 0

    with open(filepath, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "ad_id", "campaign_id", "listing_id", "listing_source",
            "product_area", "ad_type", "impressions", "clicks",
            "revenue", "event_date", "campaign_metadata"
        ])

        for ad_id in range(1, NUM_AD_EVENTS + 1):
            # New campaign every ~10 events
            if ad_id % 10 == 1:
                campaign_counter += 1
            campaign_id = f"CMP-{campaign_counter:05d}"

            source = random.choices(sources, weights=SOURCE_WEIGHTS, k=1)[0]
            product_area = source.capitalize()
            listing_id = random.randint(1, LISTING_SOURCES[source])
            listing_source = source

            ad_type = random.choices(AD_TYPES, weights=AD_TYPE_WEIGHTS, k=1)[0]

            # Impressions based on ad type
            if ad_type == "Banner":
                impressions = random.randint(500, 10000)
            elif ad_type == "Sponsored":
                impressions = random.randint(200, 5000)
            elif ad_type == "Featured":
                impressions = random.randint(100, 2000)
            else:
                impressions = random.randint(50, 1000)

            # CTR: 1-5% depending on type
            ctr = random.uniform(0.01, 0.05)
            if ad_type == "Featured":
                ctr *= 1.5  # Higher engagement
            clicks = max(1, int(impressions * ctr))

            # Revenue: CPC model ($0.20-$2.50 per click)
            cpc = random.uniform(0.20, 2.50)
            if source == "property":
                cpc *= 2.0  # Property ads cost more
            elif source == "motors":
                cpc *= 1.5
            revenue = round(clicks * cpc, 2)

            event_date = random_date(DATA_START_DATE, DATA_END_DATE).strftime("%Y-%m-%d")
            campaign_metadata = generate_campaign_metadata(source, ad_type)

            writer.writerow([
                ad_id, campaign_id, listing_id, listing_source,
                product_area, ad_type, impressions, clicks,
                revenue, event_date, campaign_metadata
            ])

    print(f"Generated {NUM_AD_EVENTS} ad revenue events -> {filepath}")
    return filepath


if __name__ == "__main__":
    generate_ad_revenue()
