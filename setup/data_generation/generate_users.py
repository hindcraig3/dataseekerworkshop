"""Generate USERS table data - 10,000 users."""
import csv
import json
import os
import random
import string

from config import (
    USER_SEGMENTS, USER_SEGMENT_WEIGHTS,
    pick_region_city, random_date, USER_REGISTRATION_START, DATA_END_DATE,
    MARKETPLACE_CATEGORIES, JOBS_INDUSTRIES
)

NUM_USERS = 10_000
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")

# Common NZ first and last names
FIRST_NAMES = [
    "James", "Oliver", "Jack", "William", "Noah", "Liam", "Thomas", "Henry",
    "Lucas", "Ethan", "Charlotte", "Olivia", "Amelia", "Isla", "Ava",
    "Sophie", "Mia", "Ella", "Grace", "Harper", "Aroha", "Nikau", "Tane",
    "Maia", "Kaia", "Hemi", "Wiremu", "Manaia", "Aria", "Anika",
    "Daniel", "Samuel", "Benjamin", "Matthew", "Joshua", "Ryan", "Connor",
    "Emma", "Sarah", "Hannah", "Jessica", "Kate", "Rachel", "Lauren",
]

LAST_NAMES = [
    "Smith", "Williams", "Brown", "Wilson", "Taylor", "Anderson", "Thomas",
    "Harris", "Jones", "Martin", "Thompson", "White", "Walker", "King",
    "Robinson", "Clark", "Mitchell", "Lee", "Campbell", "Stewart",
    "Te Whare", "Ngata", "Henare", "Tamati", "Wiremu", "Patel", "Singh",
    "Chen", "Wang", "Kim", "Nguyen", "van der Berg", "O'Brien", "McDonald",
    "Fraser", "Murray", "Reid", "Robertson", "Scott", "Henderson",
]

BUSINESS_NAMES = [
    "NZ Motors Group", "Auckland Auto Centre", "Canterbury Car Sales",
    "Wellington Motors Ltd", "Kiwi Deals Trading", "Pacific Trade Co",
    "Southern Cross Autos", "Harbour City Motors", "Capital Cars",
    "Harcourts", "Ray White", "Barfoot & Thompson", "Bayleys",
    "LJ Hooker", "Tommy's Real Estate", "Property Brokers",
    "First National", "Century 21", "Professionals",
    "Seek NZ Recruiting", "Hays NZ", "Robert Half Wellington",
    "Michael Page Auckland", "Randstad NZ", "Hudson Recruitment",
    "Trade Supplies NZ", "Office Furniture Direct", "Tech Resellers Ltd",
    "Farm Source", "Turners Auctions", "NZ Post Marketplace",
    "Mighty Ape", "PB Tech", "Noel Leeming Outlet",
    "Placemakers Trade", "Mitre 10 Clearance", "Warehouse Stationery",
]

EMAIL_DOMAINS = ["gmail.com", "outlook.com", "yahoo.co.nz", "hotmail.com",
                 "xtra.co.nz", "trademe.co.nz", "proton.me", "icloud.com"]


def generate_username(segment, first_name, last_name, business_name, user_id):
    """Generate a username - could be email or any string."""
    style = random.random()
    if segment in ("Business", "Power Seller") and style < 0.4:
        # Business-style username
        clean = business_name.lower().replace(" ", "").replace("&", "")[:15]
        return f"{clean}@{random.choice(EMAIL_DOMAINS)}"
    elif style < 0.7:
        # Email-style username
        domain = random.choice(EMAIL_DOMAINS)
        formats = [
            f"{first_name.lower()}.{last_name.lower()}@{domain}",
            f"{first_name.lower()}{last_name.lower()[0]}@{domain}",
            f"{first_name.lower()}_{random.randint(1, 99)}@{domain}",
            f"{first_name.lower()}.{last_name.lower()}{random.randint(1, 9)}@{domain}",
        ]
        return random.choice(formats)
    else:
        # Handle-style username (no email)
        formats = [
            f"{first_name.lower()}{last_name.lower()[0]}{random.randint(10, 99)}",
            f"{first_name.lower()}_{random.randint(100, 999)}",
            f"kiwi{random.choice(['trader', 'seller', 'buyer', 'deals'])}{random.randint(1, 999)}",
            f"nz_{first_name.lower()}_{random.randint(1, 99)}",
        ]
        return random.choice(formats)


def generate_preferences(segment):
    """Generate realistic JSON preferences for a user."""
    interests = random.sample(
        ["Marketplace", "Motors", "Property", "Jobs"],
        k=random.randint(1, 3)
    )
    prefs = {
        "notifications": {
            "email": random.choice([True, True, True, False]),
            "push": random.choice([True, True, False]),
            "sms": random.choice([True, False, False, False]),
        },
        "display": {
            "currency": "NZD",
            "distance_unit": "km",
        },
        "interests": interests,
        "saved_searches": random.randint(0, 15) if segment != "Individual" else random.randint(0, 5),
    }
    return json.dumps(prefs)


def generate_users():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    filepath = os.path.join(OUTPUT_DIR, "users.csv")

    with open(filepath, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "user_id", "username", "first_name", "last_name", "business_name",
            "user_segment", "region", "city", "registration_date", "preferences"
        ])

        for user_id in range(1, NUM_USERS + 1):
            segment = random.choices(USER_SEGMENTS, weights=USER_SEGMENT_WEIGHTS, k=1)[0]
            region, city = pick_region_city()
            reg_date = random_date(USER_REGISTRATION_START, DATA_END_DATE).strftime("%Y-%m-%d")
            preferences = generate_preferences(segment)

            first_name = random.choice(FIRST_NAMES)
            last_name = random.choice(LAST_NAMES)

            if segment in ("Business", "Power Seller"):
                business_name = random.choice(BUSINESS_NAMES)
                display_first = "NULL"
                display_last = "NULL"
            else:
                business_name = "NULL"
                display_first = first_name
                display_last = last_name

            username = generate_username(segment, first_name, last_name, business_name, user_id)

            writer.writerow([
                user_id, username, display_first, display_last, business_name,
                segment, region, city, reg_date, preferences
            ])

    print(f"Generated {NUM_USERS} users -> {filepath}")
    return filepath


if __name__ == "__main__":
    generate_users()
