"""Generate APPLICATIONS table data - 30,000 job applications."""
import csv
import os
import random
from datetime import timedelta

from config import random_date, DATA_START_DATE, DATA_END_DATE

NUM_USERS = 10_000
NUM_JOBS_LISTINGS = 15_000
NUM_APPLICATIONS = 30_000
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")

APPLICATION_STATUSES = ["submitted", "viewed", "shortlisted", "rejected"]
APPLICATION_STATUS_WEIGHTS = [0.30, 0.35, 0.15, 0.20]

APPLICATION_SOURCES = ["Trade Me", "Direct", "Referral"]
APPLICATION_SOURCE_WEIGHTS = [0.70, 0.20, 0.10]


def generate_applications():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    filepath = os.path.join(OUTPUT_DIR, "applications.csv")

    with open(filepath, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "application_id", "listing_id", "user_id",
            "applied_date", "status", "source"
        ])

        for app_id in range(1, NUM_APPLICATIONS + 1):
            # Zipf-like: some jobs get many applications, most get few
            # Use pareto to cluster applications on popular listings
            listing_id = min(int(random.paretovariate(1.2)) + 1, NUM_JOBS_LISTINGS)

            # Applicants are typically Individual segment users
            user_id = random.randint(1, 7000)  # Individual segment range

            applied_date = random_date(DATA_START_DATE, DATA_END_DATE)

            status = random.choices(
                APPLICATION_STATUSES, weights=APPLICATION_STATUS_WEIGHTS, k=1
            )[0]

            source = random.choices(
                APPLICATION_SOURCES, weights=APPLICATION_SOURCE_WEIGHTS, k=1
            )[0]

            writer.writerow([
                app_id, listing_id, user_id,
                applied_date.strftime("%Y-%m-%d %H:%M:%S"),
                status, source
            ])

    print(f"Generated {NUM_APPLICATIONS} applications -> {filepath}")
    return filepath


if __name__ == "__main__":
    generate_applications()
