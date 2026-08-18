"""
Trade Me Workshop Data Generator - Orchestrator
================================================
Runs all generators in dependency order and validates output.

Usage:
    cd setup/data_generation
    pip install -r requirements.txt
    python generate_all.py
"""
import os
import sys
import time

# Ensure we can import sibling modules
sys.path.insert(0, os.path.dirname(__file__))

from generate_users import generate_users
from generate_marketplace import generate_marketplace_listings
from generate_motors import generate_motors_listings
from generate_property import generate_property_listings
from generate_jobs import generate_jobs_listings
from generate_contacts import generate_contacts
from generate_ad_revenue import generate_ad_revenue
from generate_applications import generate_applications

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")


def validate_csv(filepath, expected_min_rows):
    """Quick validation: check file exists and has expected row count."""
    if not os.path.exists(filepath):
        print(f"  ERROR: {filepath} not found!")
        return False
    with open(filepath, "r") as f:
        row_count = sum(1 for _ in f) - 1  # subtract header
    if row_count < expected_min_rows:
        print(f"  ERROR: {filepath} has {row_count} rows, expected >= {expected_min_rows}")
        return False
    print(f"  OK: {os.path.basename(filepath)} — {row_count:,} rows")
    return True


def main():
    start = time.time()
    print("=" * 60)
    print("Trade Me Workshop Data Generator")
    print("=" * 60)

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Phase 1: Independent tables
    print("\n[Phase 1] Generating USERS...")
    generate_users()

    # Phase 2: Listing tables (depend on users)
    print("\n[Phase 2] Generating listing tables...")
    generate_marketplace_listings()
    generate_motors_listings()
    generate_property_listings()
    generate_jobs_listings()

    # Phase 3: Dependent tables (depend on listings + users)
    print("\n[Phase 3] Generating dependent tables...")
    generate_contacts()
    generate_ad_revenue()
    generate_applications()

    # Validation
    print("\n" + "=" * 60)
    print("Validation")
    print("=" * 60)

    validations = [
        ("users.csv", 10_000),
        ("marketplace_listings.csv", 50_000),
        ("motors_listings.csv", 20_000),
        ("property_listings.csv", 15_000),
        ("jobs_listings.csv", 15_000),
        ("contacts.csv", 25_000),
        ("ad_revenue.csv", 50_000),
        ("applications.csv", 30_000),
    ]

    all_ok = True
    for filename, min_rows in validations:
        filepath = os.path.join(OUTPUT_DIR, filename)
        if not validate_csv(filepath, min_rows):
            all_ok = False

    elapsed = time.time() - start
    print(f"\n{'=' * 60}")
    if all_ok:
        print(f"SUCCESS - All files generated in {elapsed:.1f}s")
        print(f"Output directory: {OUTPUT_DIR}")
    else:
        print("FAILED - Some files did not pass validation")
        sys.exit(1)

    print(f"{'=' * 60}")
    print("\nNext steps:")
    print("  1. Run setup/01_create_objects.sql in Snowflake")
    print("  2. Upload CSVs: PUT file://setup/data_generation/output/*.csv @workshop_data_stage;")
    print("  3. Run setup/02_load_data.sql to load data into tables")


if __name__ == "__main__":
    main()
