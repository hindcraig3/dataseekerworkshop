"""Generate MOTORS_LISTINGS table data - 20,000 listings."""
import csv
import os
import random
from datetime import timedelta

from config import (
    VEHICLE_TYPES, VEHICLE_TYPE_WEIGHTS,
    MOTORS_MAKES_MODELS, MOTORS_MAKE_WEIGHTS,
    FUEL_TYPES, FUEL_TYPE_WEIGHTS,
    TRANSMISSIONS, TRANSMISSION_WEIGHTS,
    BODY_TYPES, BODY_TYPE_WEIGHTS,
    COLOURS, COLOUR_WEIGHTS,
    REGISTRATION_STATUSES, REGISTRATION_STATUS_WEIGHTS,
    pick_region_city, random_date,
    DATA_START_DATE, DATA_END_DATE
)

NUM_USERS = 10_000
NUM_LISTINGS = 20_000
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")

# Business users (dealers) more likely to list Motors
DEALER_USER_IDS = list(range(7001, 9001))  # user_ids 7001-9000 = Business segment approx
PRIVATE_USER_IDS = list(range(1, 7001))


def generate_motors_listings():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    filepath = os.path.join(OUTPUT_DIR, "motors_listings.csv")

    makes = list(MOTORS_MAKES_MODELS.keys())

    with open(filepath, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "listing_id", "user_id", "vehicle_type", "make", "model",
            "year", "mileage_km", "fuel_type", "transmission", "body_type",
            "colour", "engine_cc", "registration_status", "asking_price",
            "region", "city", "status", "listed_date", "sold_date",
            "view_count", "watchlist_count", "enquiry_count"
        ])

        for listing_id in range(1, NUM_LISTINGS + 1):
            # 40% from dealers, 60% private
            if random.random() < 0.40:
                user_id = random.choice(DEALER_USER_IDS)
            else:
                user_id = random.randint(1, NUM_USERS)

            vehicle_type = random.choices(VEHICLE_TYPES, weights=VEHICLE_TYPE_WEIGHTS, k=1)[0]
            make = random.choices(makes, weights=MOTORS_MAKE_WEIGHTS, k=1)[0]
            model = random.choice(MOTORS_MAKES_MODELS[make])

            # Year: weighted toward newer
            current_year = 2026
            year = current_year - int(abs(random.gauss(5, 6)))
            year = max(1990, min(current_year, year))

            # Mileage correlated with age
            age = current_year - year
            mileage_km = int(age * random.uniform(8000, 18000))
            if vehicle_type == "Motorcycle":
                mileage_km = int(mileage_km * 0.4)

            fuel_type = random.choices(FUEL_TYPES, weights=FUEL_TYPE_WEIGHTS, k=1)[0]
            # Electric cars are newer
            if fuel_type == "Electric" and year < 2015:
                fuel_type = "Petrol"

            transmission = random.choices(TRANSMISSIONS, weights=TRANSMISSION_WEIGHTS, k=1)[0]
            body_type = random.choices(BODY_TYPES, weights=BODY_TYPE_WEIGHTS, k=1)[0]
            colour = random.choices(COLOURS, weights=COLOUR_WEIGHTS, k=1)[0]

            # Engine CC based on vehicle type and fuel
            if fuel_type == "Electric":
                engine_cc = "NULL"
            elif vehicle_type in ("Motorcycle",):
                engine_cc = random.choice([125, 250, 300, 500, 600, 650, 750, 900, 1000, 1200])
            else:
                engine_cc = random.choice([1000, 1200, 1300, 1500, 1600, 1800, 2000, 2200, 2500, 3000, 3500, 4000])

            registration_status = random.choices(
                REGISTRATION_STATUSES, weights=REGISTRATION_STATUS_WEIGHTS, k=1
            )[0]

            # Price based on age, make (premium brands cost more)
            base_price = 35000 - (age * 2000) + random.uniform(-5000, 5000)
            if make in ("BMW", "Mercedes-Benz", "Audi"):
                base_price *= 1.5
            if vehicle_type == "Motorcycle":
                base_price *= 0.4
            elif vehicle_type == "Boat":
                base_price *= 1.8
            asking_price = round(max(1500, base_price), 2)

            region, city = pick_region_city()

            listed_date = random_date(DATA_START_DATE, DATA_END_DATE)
            days_since_listed = (DATA_END_DATE - listed_date).days

            # Status
            if days_since_listed < 21:
                status = random.choices(["active", "sold", "expired"], weights=[0.6, 0.25, 0.15], k=1)[0]
            else:
                status = random.choices(["sold", "expired", "withdrawn"], weights=[0.55, 0.35, 0.10], k=1)[0]

            sold_date = "NULL"
            if status == "sold":
                sell_days = random.randint(3, max(4, min(days_since_listed, 60)))
                sold_date = (listed_date + timedelta(days=sell_days)).strftime("%Y-%m-%d %H:%M:%S")

            view_count = random.randint(20, 100) + int(days_since_listed * random.uniform(1, 5))
            watchlist_count = max(0, int(view_count * random.uniform(0.08, 0.25)))
            enquiry_count = max(0, int(view_count * random.uniform(0.02, 0.08)))

            writer.writerow([
                listing_id, user_id, vehicle_type, make, model,
                year, mileage_km, fuel_type, transmission, body_type,
                colour, engine_cc, registration_status, asking_price,
                region, city, status, listed_date.strftime("%Y-%m-%d %H:%M:%S"),
                sold_date, view_count, watchlist_count, enquiry_count
            ])

    print(f"Generated {NUM_LISTINGS} motors listings -> {filepath}")
    return filepath


if __name__ == "__main__":
    generate_motors_listings()
