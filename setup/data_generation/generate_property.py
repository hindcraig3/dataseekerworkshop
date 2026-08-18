"""Generate PROPERTY_LISTINGS table data - 15,000 listings."""
import csv
import os
import random
from datetime import timedelta

from config import (
    PROPERTY_LISTING_TYPES, PROPERTY_LISTING_TYPE_WEIGHTS,
    PROPERTY_TYPES, PROPERTY_TYPE_WEIGHTS,
    SUBURBS, REGIONS_CITIES,
    pick_region_city, random_date,
    DATA_START_DATE, DATA_END_DATE
)

NUM_USERS = 10_000
NUM_LISTINGS = 15_000
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")

# Agents (Business users) list most properties
AGENT_USER_IDS = list(range(7001, 9001))


def get_suburb(city):
    """Get a suburb for the city, or return a generic one."""
    if city in SUBURBS:
        return random.choice(SUBURBS[city])
    return random.choice(["Central", "North", "South", "East", "West"])


def generate_price_display(asking_price, listing_type):
    if listing_type == "Tender":
        return "Tender"
    elif listing_type == "Auction":
        return "Auction"
    elif asking_price is None:
        return "By Negotiation"
    elif asking_price >= 1_000_000:
        return f"${asking_price/1_000_000:.2f}M"
    else:
        return f"${int(asking_price):,}"


def generate_property_listings():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    filepath = os.path.join(OUTPUT_DIR, "property_listings.csv")

    with open(filepath, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "listing_id", "user_id", "listing_type", "property_type",
            "bedrooms", "bathrooms", "parking_spaces", "land_area_sqm",
            "floor_area_sqm", "year_built", "region", "city", "suburb",
            "asking_price", "price_display", "status", "listed_date",
            "sold_date", "view_count", "enquiry_count", "rateable_value"
        ])

        for listing_id in range(1, NUM_LISTINGS + 1):
            # 80% from agents, 20% private
            if random.random() < 0.80:
                user_id = random.choice(AGENT_USER_IDS)
            else:
                user_id = random.randint(1, NUM_USERS)

            listing_type = random.choices(
                PROPERTY_LISTING_TYPES, weights=PROPERTY_LISTING_TYPE_WEIGHTS, k=1
            )[0]
            property_type = random.choices(
                PROPERTY_TYPES, weights=PROPERTY_TYPE_WEIGHTS, k=1
            )[0]

            # Bedrooms/bathrooms based on property type
            if property_type == "Section":
                bedrooms = "NULL"
                bathrooms = "NULL"
                parking_spaces = "NULL"
                floor_area_sqm = "NULL"
            elif property_type == "Apartment":
                bedrooms = random.choice([1, 1, 2, 2, 3])
                bathrooms = random.choice([1, 1, 2])
                parking_spaces = random.choice([0, 1, 1, 2])
                floor_area_sqm = round(random.uniform(40, 150), 1)
            else:
                bedrooms = random.choice([2, 3, 3, 3, 4, 4, 5])
                bathrooms = random.choice([1, 1, 2, 2, 3])
                parking_spaces = random.choice([1, 2, 2, 3])
                floor_area_sqm = round(random.uniform(80, 350), 1)

            # Land area
            if property_type in ("Apartment", "Unit"):
                land_area_sqm = "NULL"
            elif property_type == "Section":
                land_area_sqm = round(random.uniform(400, 5000), 1)
            elif property_type in ("Lifestyle", "Rural"):
                land_area_sqm = round(random.uniform(5000, 100000), 1)
            else:
                land_area_sqm = round(random.uniform(200, 1200), 1)

            year_built = random.choice([
                "NULL"] * 3 + [str(random.randint(1920, 2026))] * 7
            )
            if year_built != "NULL":
                year_built = int(year_built)

            region, city = pick_region_city()
            suburb = get_suburb(city)

            # Price based on region and type
            if region == "Auckland":
                base_price = random.uniform(600000, 2500000)
            elif region == "Wellington":
                base_price = random.uniform(500000, 1800000)
            elif region in ("Canterbury", "Waikato", "Bay of Plenty"):
                base_price = random.uniform(400000, 1500000)
            elif region == "Otago":
                base_price = random.uniform(450000, 2000000)  # Queenstown effect
            else:
                base_price = random.uniform(300000, 900000)

            if property_type == "Apartment":
                base_price *= 0.5
            elif property_type == "Section":
                base_price *= 0.4
            elif property_type in ("Lifestyle", "Rural"):
                base_price *= 1.3

            # Rental listings
            if listing_type == "Rent":
                asking_price = round(random.uniform(350, 1200), 2)  # weekly rent
                price_display = f"${int(asking_price)}pw"
            elif listing_type in ("Tender", "Auction") and random.random() < 0.5:
                asking_price = "NULL"
                price_display = generate_price_display(None, listing_type)
            else:
                asking_price = round(base_price, 2)
                price_display = generate_price_display(asking_price, listing_type)

            listed_date = random_date(DATA_START_DATE, DATA_END_DATE)
            days_since_listed = (DATA_END_DATE - listed_date).days

            # Status
            if days_since_listed < 30:
                status = random.choices(
                    ["active", "sold", "under_offer", "withdrawn"],
                    weights=[0.5, 0.2, 0.2, 0.1], k=1
                )[0]
            else:
                status = random.choices(
                    ["sold", "expired", "under_offer", "withdrawn"],
                    weights=[0.45, 0.30, 0.15, 0.10], k=1
                )[0]

            sold_date = "NULL"
            if status == "sold":
                sell_days = random.randint(7, max(8, min(days_since_listed, 120)))
                sold_date = (listed_date + timedelta(days=sell_days)).strftime("%Y-%m-%d %H:%M:%S")

            view_count = random.randint(30, 200) + int(days_since_listed * random.uniform(2, 8))
            enquiry_count = max(0, int(view_count * random.uniform(0.03, 0.12)))

            # Rateable value: typically 70-90% of asking for sales
            if listing_type != "Rent" and asking_price != "NULL":
                rv = int(float(asking_price) * random.uniform(0.70, 0.95))
                rateable_value = f"${rv:,}"
            else:
                rateable_value = "NULL"

            writer.writerow([
                listing_id, user_id, listing_type, property_type,
                bedrooms, bathrooms, parking_spaces, land_area_sqm,
                floor_area_sqm, year_built, region, city, suburb,
                asking_price, price_display, status,
                listed_date.strftime("%Y-%m-%d %H:%M:%S"), sold_date,
                view_count, enquiry_count, rateable_value
            ])

    print(f"Generated {NUM_LISTINGS} property listings -> {filepath}")
    return filepath


if __name__ == "__main__":
    generate_property_listings()
