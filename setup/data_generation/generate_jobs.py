"""Generate JOBS_LISTINGS table data - 15,000 listings."""
import csv
import os
import random
from datetime import timedelta

from config import (
    JOBS_INDUSTRIES, ROLE_TYPES, ROLE_TYPE_WEIGHTS,
    EMPLOYMENT_TYPES, EMPLOYMENT_TYPE_WEIGHTS,
    EXPERIENCE_LEVELS, EXPERIENCE_LEVEL_WEIGHTS,
    pick_region_city, random_date,
    DATA_START_DATE, DATA_END_DATE
)

NUM_USERS = 10_000
NUM_LISTINGS = 15_000
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")

# Employers/recruiters are Business segment users
EMPLOYER_USER_IDS = list(range(7001, 9001))

SALARY_RANGES_BY_LEVEL = {
    "Entry":     (45000, 65000),
    "Mid":       (65000, 100000),
    "Senior":    (100000, 160000),
    "Executive": (150000, 280000),
}

JOB_TITLE_TEMPLATES = {
    "Technology": ["{level} Software Engineer", "Data {role}", "{level} DevOps Engineer", "Product Manager", "QA Engineer", "UX Designer"],
    "Healthcare": ["Registered Nurse", "General Practitioner", "Pharmacist", "Physiotherapist", "Healthcare Assistant"],
    "Construction": ["Site Manager", "Project Manager", "Quantity Surveyor", "{level} Carpenter", "Electrician"],
    "Hospitality": ["Head Chef", "Restaurant Manager", "Duty Manager", "Events Coordinator", "Barista"],
    "Retail": ["Store Manager", "Sales Consultant", "Visual Merchandiser", "Buyer", "E-commerce Manager"],
    "Finance": ["Financial Analyst", "Accounts Manager", "Credit Controller", "Finance Manager", "Payroll Officer"],
    "Education": ["Primary Teacher", "Secondary Teacher", "ECE Teacher", "Teacher Aide", "SENCO"],
    "Government": ["Policy Analyst", "Project Manager", "Communications Advisor", "Regulatory Officer"],
    "Agriculture": ["Farm Manager", "Farm Hand", "Viticulturist", "Dairy Manager", "Orchard Supervisor"],
    "Manufacturing": ["Production Manager", "Machine Operator", "Quality Controller", "Warehouse Manager"],
    "Accounting": ["Management Accountant", "Financial Controller", "Tax Accountant", "Bookkeeper", "Audit Manager"],
    "Legal": ["Senior Lawyer", "Legal Executive", "Paralegal", "Compliance Officer"],
}


def generate_salary_display(salary_min, salary_max, role_type):
    if salary_min is None:
        return "Negotiable"
    if role_type == "Contract":
        hourly = int(salary_max / 2080)
        return f"${hourly}/hour"
    if salary_max >= 100000:
        return f"${int(salary_min/1000)}k-${int(salary_max/1000)}k"
    else:
        return f"${int(salary_min):,}-${int(salary_max):,}"


def generate_jobs_listings():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    filepath = os.path.join(OUTPUT_DIR, "jobs_listings.csv")

    industries = list(JOBS_INDUSTRIES.keys())

    with open(filepath, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "listing_id", "user_id", "industry", "subcategory",
            "role_type", "employment_type", "title", "salary_min",
            "salary_max", "salary_display", "region", "city", "status",
            "listed_date", "close_date", "remote_option",
            "experience_level", "view_count", "application_count"
        ])

        for listing_id in range(1, NUM_LISTINGS + 1):
            user_id = random.choice(EMPLOYER_USER_IDS)

            industry = random.choice(industries)
            subcategory = random.choice(JOBS_INDUSTRIES[industry])

            role_type = random.choices(ROLE_TYPES, weights=ROLE_TYPE_WEIGHTS, k=1)[0]
            employment_type = random.choices(EMPLOYMENT_TYPES, weights=EMPLOYMENT_TYPE_WEIGHTS, k=1)[0]
            experience_level = random.choices(EXPERIENCE_LEVELS, weights=EXPERIENCE_LEVEL_WEIGHTS, k=1)[0]

            # Title from templates
            if industry in JOB_TITLE_TEMPLATES:
                title_template = random.choice(JOB_TITLE_TEMPLATES[industry])
                title = title_template.format(
                    level=experience_level if experience_level != "Entry" else "Junior",
                    role=subcategory.rstrip("s")
                )
            else:
                title = f"{experience_level} {subcategory}"

            # Salary based on experience level
            salary_range = SALARY_RANGES_BY_LEVEL[experience_level]
            if random.random() < 0.15:  # 15% don't show salary
                salary_min = "NULL"
                salary_max = "NULL"
                salary_display = "Negotiable"
            else:
                salary_min = round(random.uniform(salary_range[0], salary_range[1] * 0.8), 2)
                salary_max = round(salary_min * random.uniform(1.1, 1.3), 2)
                salary_display = generate_salary_display(salary_min, salary_max, role_type)

            region, city = pick_region_city()

            # Remote more common for Tech
            if industry == "Technology":
                remote_option = random.choice([True, True, True, False])
            elif industry in ("Finance", "Accounting", "Legal"):
                remote_option = random.choice([True, True, False, False])
            else:
                remote_option = random.choice([True, False, False, False, False])

            listed_date = random_date(DATA_START_DATE, DATA_END_DATE)
            days_since_listed = (DATA_END_DATE - listed_date).days

            # Close date: 14-45 days after listing
            close_date = listed_date + timedelta(days=random.randint(14, 45))

            # Status
            if days_since_listed < 30:
                status = random.choices(["active", "closed", "filled"], weights=[0.6, 0.2, 0.2], k=1)[0]
            else:
                status = random.choices(["filled", "closed", "expired"], weights=[0.4, 0.35, 0.25], k=1)[0]

            view_count = random.randint(30, 150) + int(days_since_listed * random.uniform(2, 6))

            # Application count: Zipf-like distribution
            if status == "active":
                application_count = random.randint(0, 15)
            else:
                application_count = int(random.paretovariate(1.5)) + random.randint(0, 5)
                application_count = min(application_count, 50)

            writer.writerow([
                listing_id, user_id, industry, subcategory,
                role_type, employment_type, title, salary_min,
                salary_max, salary_display, region, city, status,
                listed_date.strftime("%Y-%m-%d %H:%M:%S"),
                close_date.strftime("%Y-%m-%d %H:%M:%S"),
                remote_option, experience_level, view_count, application_count
            ])

    print(f"Generated {NUM_LISTINGS} jobs listings -> {filepath}")
    return filepath


if __name__ == "__main__":
    generate_jobs_listings()
