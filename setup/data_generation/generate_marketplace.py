"""Generate MARKETPLACE_LISTINGS table data - 50,000 listings."""
import csv
import os
import random
from datetime import datetime, timedelta

from config import (
    MARKETPLACE_CATEGORIES, MARKETPLACE_CONDITIONS, MARKETPLACE_CONDITION_WEIGHTS,
    pick_region_city, random_date, seasonal_weight,
    DATA_START_DATE, DATA_END_DATE
)

NUM_USERS = 10_000
NUM_LISTINGS = 50_000
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")

TITLES_BY_CATEGORY = {
    "Electronics": ["{condition} {brand} {item}", "{brand} {item} - {detail}"],
    "Sports": ["{brand} {item} - {detail}", "{item} {detail}"],
    "Home & Living": ["{item} - {detail}", "{brand} {item}"],
    "Clothing": ["{brand} {item} - Size {detail}", "{item} {detail}"],
    "Toys & Games": ["{item} - {detail}", "{brand} {item}"],
    "Books & Music": ["{item} - {detail}", "{item}"],
    "Baby & Kids": ["{brand} {item} - {detail}", "{item}"],
    "Computers": ["{brand} {item} - {detail}", "{item} {detail}"],
    "Collectables": ["{item} - {detail}", "Vintage {item}"],
    "Health & Beauty": ["{brand} {item}", "{item} - {detail}"],
}

BRANDS = ["Samsung", "Apple", "Sony", "LG", "Dyson", "Nike", "Adidas", "Trek", "Giant",
           "Shimano", "Breville", "Fisher & Paykel", "Lego", "Hasbro", "Kathmandu"]


def generate_title(category, subcategory, condition):
    brand = random.choice(BRANDS)
    return f"{condition} {brand} {subcategory} Item"


def load_user_registration_dates():
    """Load user_id -> registration_date from the generated users CSV."""
    users_filepath = os.path.join(OUTPUT_DIR, "users.csv")
    reg_dates = {}
    with open(users_filepath, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            reg_dates[int(row["user_id"])] = datetime.strptime(row["registration_date"], "%Y-%m-%d")
    return reg_dates


def generate_marketplace_listings():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    filepath = os.path.join(OUTPUT_DIR, "marketplace_listings.csv")

    user_reg_dates = load_user_registration_dates()
    categories = list(MARKETPLACE_CATEGORIES.keys())

    with open(filepath, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "listing_id", "user_id", "category", "subcategory", "title",
            "condition", "asking_price", "buy_now_price", "region", "city",
            "status", "listed_date", "close_date", "sold_date",
            "shipping_available", "accepts_offers", "view_count",
            "watchlist_count", "bid_count"
        ])

        for listing_id in range(1, NUM_LISTINGS + 1):
            user_id = random.randint(1, NUM_USERS)
            category = random.choice(categories)
            subcategory = random.choice(MARKETPLACE_CATEGORIES[category])

            condition = random.choices(
                MARKETPLACE_CONDITIONS, weights=MARKETPLACE_CONDITION_WEIGHTS, k=1
            )[0]

            title = generate_title(category, subcategory, condition)

            # Price varies by category
            if category == "Electronics":
                asking_price = round(random.uniform(20, 3000), 2)
            elif category in ("Collectables", "Computers"):
                asking_price = round(random.uniform(10, 5000), 2)
            elif category == "Sports":
                asking_price = round(random.uniform(15, 2000), 2)
            else:
                asking_price = round(random.uniform(5, 500), 2)

            # Buy now price: 60% have one, typically 10-30% above asking
            if random.random() < 0.60:
                buy_now_price = round(asking_price * random.uniform(1.1, 1.3), 2)
            else:
                buy_now_price = "NULL"

            region, city = pick_region_city()

            # Listed date must be on or after user's registration date
            earliest_date = max(DATA_START_DATE, user_reg_dates[user_id])
            listed_date = random_date(earliest_date, DATA_END_DATE)
            days_since_listed = (DATA_END_DATE - listed_date).days

            # Close date: 7-14 days after listing
            close_date = listed_date + timedelta(days=random.randint(7, 14))

            # Status based on age
            if days_since_listed < 14:
                status = random.choices(["active", "sold", "closed"], weights=[0.6, 0.2, 0.2], k=1)[0]
            else:
                status = random.choices(["sold", "closed", "withdrawn"], weights=[0.5, 0.4, 0.1], k=1)[0]

            sold_date = "NULL"
            if status == "sold":
                sell_days = random.randint(1, max(2, min(days_since_listed, 14)))
                sold_date = (listed_date + timedelta(days=sell_days)).strftime("%Y-%m-%d %H:%M:%S")

            shipping_available = random.choice([True, True, True, False])
            accepts_offers = random.choice([True, True, False])

            # Engagement metrics correlated with age
            view_count = random.randint(5, 50) + int(days_since_listed * random.uniform(0.5, 3))
            watchlist_count = max(0, int(view_count * random.uniform(0.05, 0.20)))
            bid_count = random.randint(0, 8) if status == "sold" else random.randint(0, 3)

            writer.writerow([
                listing_id, user_id, category, subcategory, title,
                condition, asking_price, buy_now_price, region, city,
                status, listed_date.strftime("%Y-%m-%d %H:%M:%S"),
                close_date.strftime("%Y-%m-%d %H:%M:%S"), sold_date,
                shipping_available, accepts_offers,
                view_count, watchlist_count, bid_count
            ])

    print(f"Generated {NUM_LISTINGS} marketplace listings -> {filepath}")
    return filepath


if __name__ == "__main__":
    generate_marketplace_listings()
