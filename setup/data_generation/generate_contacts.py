"""Generate CONTACTS table data - 25,000 contacts across all listing types."""
import csv
import json
import os
import random
from datetime import timedelta

from config import (
    CONTACT_REASONS, CONTACT_REASON_WEIGHTS_BY_AREA,
    CONTACT_CHANNELS, CONTACT_CHANNEL_WEIGHTS,
    CONTACT_PRIORITIES, CONTACT_PRIORITY_WEIGHTS,
    random_date, DATA_START_DATE, DATA_END_DATE
)

NUM_USERS = 10_000
NUM_CONTACTS = 25_000
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")

# Listing counts per source (must match generators)
LISTING_SOURCES = {
    "marketplace": 50_000,
    "motors": 20_000,
    "property": 15_000,
    "jobs": 15_000,
}

# Contact likelihood by product area
SOURCE_WEIGHTS = [0.40, 0.25, 0.20, 0.15]  # marketplace, motors, property, jobs

DESCRIPTION_TEMPLATES = {
    "Billing": [
        "Charged incorrectly for listing fee",
        "Payment not processed correctly",
        "Need refund for cancelled listing",
        "Double-charged for feature upgrade",
        "Subscription billing query",
    ],
    "Fraud": [
        "Suspicious listing - possible scam",
        "Seller not responding after payment",
        "Item received does not match description",
        "Fake listing reported by multiple users",
        "Account appears to be compromised",
    ],
    "Technical": [
        "Unable to upload photos to listing",
        "Page not loading correctly on mobile",
        "Search results not showing my listing",
        "Payment gateway error",
        "Cannot edit listing details",
    ],
    "Listing Quality": [
        "Listing has incorrect category",
        "Price seems unrealistic",
        "Description contains misleading information",
        "Photos are stock images not actual item",
        "Duplicate listing reported",
    ],
    "Delivery": [
        "Item not received after 14 days",
        "Tracking number not valid",
        "Item arrived damaged",
        "Wrong item delivered",
        "Courier lost package",
    ],
    "Account": [
        "Cannot reset password",
        "Need to update email address",
        "Account suspended without explanation",
        "Two-factor authentication issue",
        "Requesting account deletion",
    ],
}

AGENT_IDS = [f"AGT-{i:04d}" for i in range(1, 51)]


def generate_metadata(reason, channel, priority):
    tags = [reason.lower().replace(" ", "_")]
    if priority in ("High", "Critical"):
        tags.append("escalation_risk")
    if reason == "Fraud":
        tags.append("trust_safety")

    return json.dumps({
        "channel": channel,
        "priority": priority,
        "agent_id": random.choice(AGENT_IDS),
        "tags": tags,
        "escalated": priority == "Critical" and random.random() < 0.6,
    })


def generate_contacts():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    filepath = os.path.join(OUTPUT_DIR, "contacts.csv")

    sources = list(LISTING_SOURCES.keys())

    with open(filepath, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "contact_id", "listing_id", "listing_source", "user_id",
            "product_area", "reason", "created_date", "resolved_date",
            "resolution_time_hours", "description", "metadata"
        ])

        for contact_id in range(1, NUM_CONTACTS + 1):
            # Pick product area
            source = random.choices(sources, weights=SOURCE_WEIGHTS, k=1)[0]
            product_area = source.capitalize()
            if product_area == "Marketplace":
                product_area = "Marketplace"

            # Link to a random listing in that source (or no listing for Account issues)
            reason_weights = CONTACT_REASON_WEIGHTS_BY_AREA.get(product_area, CONTACT_REASON_WEIGHTS_BY_AREA["Marketplace"])
            reason = random.choices(CONTACT_REASONS, weights=reason_weights, k=1)[0]

            if reason == "Account":
                listing_id = "NULL"
                listing_source = "NULL"
            else:
                listing_id = random.randint(1, LISTING_SOURCES[source])
                listing_source = source

            user_id = random.randint(1, NUM_USERS)

            created_date = random_date(DATA_START_DATE, DATA_END_DATE)

            # Resolution time varies by reason and priority
            channel = random.choices(CONTACT_CHANNELS, weights=CONTACT_CHANNEL_WEIGHTS, k=1)[0]
            priority = random.choices(CONTACT_PRIORITIES, weights=CONTACT_PRIORITY_WEIGHTS, k=1)[0]

            # Some contacts are unresolved (10%)
            if random.random() < 0.10:
                resolved_date = "NULL"
                resolution_time_hours = "NULL"
            else:
                base_hours = {"Billing": 24, "Fraud": 48, "Technical": 12,
                              "Listing Quality": 8, "Delivery": 72, "Account": 6}
                hours = base_hours.get(reason, 24) * random.uniform(0.3, 3.0)
                if priority == "Critical":
                    hours *= 0.5
                resolution_time_hours = round(hours, 2)
                resolved_date = (created_date + timedelta(hours=hours)).strftime("%Y-%m-%d %H:%M:%S")

            description = random.choice(DESCRIPTION_TEMPLATES.get(reason, ["General enquiry"]))
            metadata = generate_metadata(reason, channel, priority)

            writer.writerow([
                contact_id, listing_id, listing_source, user_id,
                product_area, reason,
                created_date.strftime("%Y-%m-%d %H:%M:%S"), resolved_date,
                resolution_time_hours, description, metadata
            ])

    print(f"Generated {NUM_CONTACTS} contacts -> {filepath}")
    return filepath


if __name__ == "__main__":
    generate_contacts()
