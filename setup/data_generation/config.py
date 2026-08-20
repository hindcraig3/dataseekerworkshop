"""
Shared configuration for Trade Me workshop data generation.
NZ-specific reference data, distributions, and constants.
"""
import random
from datetime import datetime, timedelta

# =============================================================================
# Time range for data generation
# =============================================================================
DATA_START_DATE = datetime(2023, 8, 1)
DATA_END_DATE = datetime(2026, 8, 26)
USER_REGISTRATION_START = datetime(2001, 1, 1)

# =============================================================================
# NZ Regions and Cities (weighted by population)
# =============================================================================
REGIONS_CITIES = {
    "Auckland": {
        "weight": 0.34,
        "cities": ["Auckland City", "North Shore", "Manukau", "Waitakere", "Papakura", "Franklin"]
    },
    "Wellington": {
        "weight": 0.14,
        "cities": ["Wellington City", "Lower Hutt", "Upper Hutt", "Porirua", "Kapiti Coast"]
    },
    "Canterbury": {
        "weight": 0.13,
        "cities": ["Christchurch", "Selwyn", "Waimakariri", "Ashburton", "Timaru"]
    },
    "Waikato": {
        "weight": 0.10,
        "cities": ["Hamilton", "Tauranga", "Rotorua", "Taupo", "Cambridge"]
    },
    "Bay of Plenty": {
        "weight": 0.07,
        "cities": ["Tauranga", "Rotorua", "Whakatane", "Mount Maunganui"]
    },
    "Otago": {
        "weight": 0.05,
        "cities": ["Dunedin", "Queenstown", "Wanaka", "Oamaru"]
    },
    "Manawatu-Wanganui": {
        "weight": 0.04,
        "cities": ["Palmerston North", "Whanganui", "Levin", "Feilding"]
    },
    "Hawkes Bay": {
        "weight": 0.04,
        "cities": ["Napier", "Hastings", "Havelock North"]
    },
    "Taranaki": {
        "weight": 0.03,
        "cities": ["New Plymouth", "Stratford", "Hawera"]
    },
    "Northland": {
        "weight": 0.03,
        "cities": ["Whangarei", "Kerikeri", "Kaitaia", "Paihia"]
    },
    "Southland": {
        "weight": 0.02,
        "cities": ["Invercargill", "Gore", "Te Anau"]
    },
    "Nelson-Marlborough": {
        "weight": 0.02,
        "cities": ["Nelson", "Blenheim", "Richmond"]
    },
    "West Coast": {
        "weight": 0.01,
        "cities": ["Greymouth", "Hokitika", "Westport"]
    },
    "Gisborne": {
        "weight": 0.01,
        "cities": ["Gisborne"]
    },
}

REGIONS = list(REGIONS_CITIES.keys())
REGION_WEIGHTS = [REGIONS_CITIES[r]["weight"] for r in REGIONS]

# =============================================================================
# User segments
# =============================================================================
USER_SEGMENTS = ["Individual", "Business", "Power Seller"]
USER_SEGMENT_WEIGHTS = [0.70, 0.20, 0.10]

# =============================================================================
# Marketplace categories
# =============================================================================
MARKETPLACE_CATEGORIES = {
    "Electronics": ["Laptops", "Phones", "Tablets", "TVs", "Gaming Consoles", "Cameras", "Audio"],
    "Sports": ["Cycling", "Fishing", "Camping", "Golf", "Water Sports", "Gym Equipment", "Running"],
    "Home & Living": ["Furniture", "Kitchen", "Bedding", "Lighting", "Garden", "Appliances"],
    "Clothing": ["Men's", "Women's", "Children's", "Shoes", "Accessories"],
    "Toys & Games": ["Board Games", "Puzzles", "Outdoor Toys", "Dolls", "Building Sets"],
    "Books & Music": ["Fiction", "Non-Fiction", "Vinyl Records", "CDs", "Instruments"],
    "Baby & Kids": ["Prams", "Car Seats", "Nursery", "Feeding", "Maternity"],
    "Computers": ["Desktops", "Components", "Networking", "Storage", "Peripherals"],
    "Collectables": ["Coins", "Stamps", "Antiques", "Art", "Vintage"],
    "Health & Beauty": ["Skincare", "Fragrance", "Supplements", "Haircare"],
}

MARKETPLACE_CONDITIONS = ["New", "Used - Like New", "Used - Good", "Used - Average"]
MARKETPLACE_CONDITION_WEIGHTS = [0.25, 0.30, 0.30, 0.15]

# =============================================================================
# Motors reference data
# =============================================================================
VEHICLE_TYPES = ["Car", "SUV", "Ute", "Van", "Motorcycle", "Boat", "Motorhome"]
VEHICLE_TYPE_WEIGHTS = [0.45, 0.20, 0.10, 0.05, 0.10, 0.05, 0.05]

MOTORS_MAKES_MODELS = {
    "Toyota": ["Corolla", "Hilux", "RAV4", "Camry", "Yaris", "Land Cruiser", "Aqua", "C-HR"],
    "Mazda": ["CX-5", "Mazda3", "Mazda2", "CX-3", "BT-50", "CX-9", "MX-5", "CX-30"],
    "Ford": ["Ranger", "Focus", "Falcon", "Fiesta", "Everest", "Escape", "Mustang"],
    "Holden": ["Commodore", "Colorado", "Captiva", "Cruze", "Trax", "Astra"],
    "Nissan": ["Navara", "X-Trail", "Qashqai", "Leaf", "Note", "Juke", "Pathfinder"],
    "Mitsubishi": ["Triton", "Outlander", "ASX", "Eclipse Cross", "Pajero", "Lancer"],
    "Honda": ["Jazz", "Civic", "HR-V", "CR-V", "Accord", "City", "Fit"],
    "Subaru": ["Outback", "Forester", "Impreza", "XV", "Legacy", "WRX"],
    "Hyundai": ["Tucson", "i30", "Kona", "Santa Fe", "Venue", "Ioniq"],
    "Suzuki": ["Swift", "Vitara", "Jimny", "S-Cross", "Ignis", "Baleno"],
    "BMW": ["3 Series", "X3", "X5", "1 Series", "5 Series", "X1"],
    "Mercedes-Benz": ["C-Class", "A-Class", "GLC", "E-Class", "CLA"],
    "Audi": ["A3", "Q5", "A4", "Q3", "Q7", "A1"],
    "Volkswagen": ["Golf", "Tiguan", "Polo", "T-Cross", "Amarok", "Touareg"],
    "Kia": ["Sportage", "Seltos", "Cerato", "Sorento", "Stonic", "Niro"],
}

MOTORS_MAKE_WEIGHTS = [0.18, 0.12, 0.10, 0.08, 0.09, 0.08, 0.07, 0.05, 0.05, 0.04, 0.03, 0.03, 0.02, 0.03, 0.03]

FUEL_TYPES = ["Petrol", "Diesel", "Electric", "Hybrid", "LPG"]
FUEL_TYPE_WEIGHTS = [0.50, 0.25, 0.08, 0.15, 0.02]

TRANSMISSIONS = ["Automatic", "Manual", "CVT"]
TRANSMISSION_WEIGHTS = [0.60, 0.25, 0.15]

BODY_TYPES = ["Sedan", "Hatchback", "Wagon", "SUV", "Coupe", "Convertible", "Ute", "Van"]
BODY_TYPE_WEIGHTS = [0.20, 0.20, 0.10, 0.20, 0.05, 0.03, 0.12, 0.10]

COLOURS = ["White", "Silver", "Black", "Grey", "Blue", "Red", "Green", "Bronze", "Gold", "Orange"]
COLOUR_WEIGHTS = [0.18, 0.15, 0.15, 0.12, 0.12, 0.10, 0.06, 0.05, 0.04, 0.03]

REGISTRATION_STATUSES = ["Registered", "On Hold", "Expired", "Imported - Compliance Required"]
REGISTRATION_STATUS_WEIGHTS = [0.75, 0.10, 0.10, 0.05]

# =============================================================================
# Property reference data
# =============================================================================
PROPERTY_LISTING_TYPES = ["Sale", "Rent", "Auction", "Tender", "Deadline Sale"]
PROPERTY_LISTING_TYPE_WEIGHTS = [0.40, 0.25, 0.15, 0.10, 0.10]

PROPERTY_TYPES = ["House", "Apartment", "Townhouse", "Section", "Lifestyle", "Rural", "Unit"]
PROPERTY_TYPE_WEIGHTS = [0.40, 0.15, 0.15, 0.08, 0.08, 0.06, 0.08]

SUBURBS = {
    "Auckland City": ["Ponsonby", "Grey Lynn", "Mt Eden", "Remuera", "Parnell", "Epsom", "Newmarket", "Mission Bay", "St Heliers", "Herne Bay"],
    "North Shore": ["Takapuna", "Devonport", "Milford", "Browns Bay", "Albany", "Birkenhead", "Beach Haven"],
    "Wellington City": ["Thorndon", "Kelburn", "Mt Victoria", "Oriental Bay", "Karori", "Miramar", "Island Bay", "Breaker Bay", "Newtown"],
    "Lower Hutt": ["Petone", "Eastbourne", "Wainuiomata", "Stokes Valley"],
    "Christchurch": ["Merivale", "Fendalton", "Riccarton", "Sumner", "New Brighton", "Cashmere", "Halswell", "Ilam"],
    "Hamilton": ["Hillcrest", "Rototuna", "Flagstaff", "Te Rapa", "Chartwell"],
    "Tauranga": ["Mount Maunganui", "Papamoa", "Bethlehem", "Otumoetai", "Welcome Bay"],
    "Dunedin": ["St Clair", "Maori Hill", "Roslyn", "South Dunedin", "North East Valley"],
    "Queenstown": ["Frankton", "Kelvin Heights", "Arrowtown", "Jack's Point"],
}

# =============================================================================
# Jobs reference data
# =============================================================================
JOBS_INDUSTRIES = {
    "Technology": ["Software Engineers", "Data Analysts", "DevOps", "Product Managers", "QA/Testing", "UX Designers", "System Administrators"],
    "Healthcare": ["Nurses", "Doctors", "Pharmacists", "Allied Health", "Caregivers", "Mental Health"],
    "Construction": ["Project Managers", "Site Managers", "Carpenters", "Electricians", "Plumbers", "Quantity Surveyors"],
    "Hospitality": ["Chefs", "Restaurant Managers", "Bar Staff", "Hotel Management", "Events"],
    "Retail": ["Store Managers", "Sales Assistants", "Merchandising", "Buyers", "E-commerce"],
    "Finance": ["Accountants", "Financial Analysts", "Auditors", "Management Accountants", "Payroll"],
    "Education": ["Teachers", "Early Childhood", "Teacher Aides", "Administration", "Tutors"],
    "Government": ["Policy Analysts", "Project Managers", "Administration", "Regulatory", "Communications"],
    "Agriculture": ["Farm Managers", "Farm Workers", "Horticulture", "Viticulture", "Dairy"],
    "Manufacturing": ["Production Managers", "Machine Operators", "Quality Control", "Warehouse", "Logistics"],
    "Accounting": ["Accountants", "Management Accountants", "Tax Specialists", "Bookkeepers", "Financial Controllers"],
    "Legal": ["Lawyers", "Paralegals", "Legal Secretaries", "Compliance Officers"],
}

ROLE_TYPES = ["Permanent", "Contract", "Temporary"]
ROLE_TYPE_WEIGHTS = [0.65, 0.25, 0.10]

EMPLOYMENT_TYPES = ["Full Time", "Part Time", "Casual"]
EMPLOYMENT_TYPE_WEIGHTS = [0.70, 0.20, 0.10]

EXPERIENCE_LEVELS = ["Entry", "Mid", "Senior", "Executive"]
EXPERIENCE_LEVEL_WEIGHTS = [0.20, 0.40, 0.30, 0.10]

# =============================================================================
# Contact reasons
# =============================================================================
CONTACT_REASONS = ["Billing", "Fraud", "Technical", "Listing Quality", "Delivery", "Account"]
CONTACT_REASON_WEIGHTS_BY_AREA = {
    "Marketplace": [0.15, 0.15, 0.10, 0.25, 0.25, 0.10],
    "Motors":      [0.10, 0.25, 0.10, 0.30, 0.05, 0.20],
    "Property":    [0.25, 0.10, 0.15, 0.25, 0.05, 0.20],
    "Jobs":        [0.20, 0.10, 0.20, 0.20, 0.05, 0.25],
}

CONTACT_CHANNELS = ["Web", "Email", "Phone", "App"]
CONTACT_CHANNEL_WEIGHTS = [0.40, 0.25, 0.15, 0.20]

CONTACT_PRIORITIES = ["Low", "Medium", "High", "Critical"]
CONTACT_PRIORITY_WEIGHTS = [0.20, 0.45, 0.25, 0.10]

# =============================================================================
# Ad types and revenue
# =============================================================================
AD_TYPES = ["Featured", "Highlight", "Gallery", "Banner", "Sponsored"]
AD_TYPE_WEIGHTS = [0.30, 0.25, 0.15, 0.15, 0.15]

# =============================================================================
# Helper functions
# =============================================================================

def pick_region_city():
    """Return a (region, city) tuple weighted by population."""
    region = random.choices(REGIONS, weights=REGION_WEIGHTS, k=1)[0]
    city = random.choice(REGIONS_CITIES[region]["cities"])
    return region, city


def random_date(start, end):
    """Return a random datetime between start and end."""
    delta = end - start
    random_seconds = random.randint(0, int(delta.total_seconds()))
    return start + timedelta(seconds=random_seconds)


def seasonal_weight(dt):
    """Return a multiplier (0.7 - 1.3) based on NZ seasonality. 
    More listings in spring/summer (Oct-Feb), fewer in winter (Jun-Aug)."""
    month = dt.month
    weights = {1: 1.2, 2: 1.1, 3: 1.0, 4: 0.9, 5: 0.8, 6: 0.7,
               7: 0.7, 8: 0.8, 9: 0.9, 10: 1.1, 11: 1.2, 12: 1.3}
    return weights[month]
