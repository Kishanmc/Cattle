# backend/app/static_data.py
# Paste your static dictionaries here (kept same as original app.py).
BREED_STATIC_DATA = {
    "ayshire": {
        "breed": "Ayrshire",
        "origin": "Scotland",
        "milk_type": "Moderate fat, high quality",
        "average_milk_yield": "5,000–7,000 liters/year",
        "primary_color": "Red and white",
        "size": "Medium",
        "temperament": "Hardy, active grazer",
        "use_case": "Pasture-based dairy",
        "fun_fact": "Known for strong feet—excellent for grazing pastures.",
        "history": "Developed in Ayr, Scotland in the 18th century.",
        "cross_breeding": "Improves grazing efficiency & udder quality.",
        "future_potential": "Perfect for sustainable & low-input dairy farming."
    },
    "brown_swiss": {
        "breed": "Brown Swiss",
        "origin": "Switzerland",
        "milk_type": "Ideal for cheese, high protein",
        "average_milk_yield": "6,000–9,000 liters/year",
        "primary_color": "Brown with light muzzle",
        "size": "Large",
        "temperament": "Calm",
        "use_case": "Cheese and dairy farms",
        "fun_fact": "One of the world's oldest dairy breeds.",
        "history": "Originated in the Swiss Alps.",
        "cross_breeding": "Improves robustness and cheese yield quality.",
        "future_potential": "High tolerance to heat and stress."
    },
    "holstein": {
        "breed": "Holstein Friesian",
        "origin": "Netherlands",
        "milk_type": "Very high yield, lower fat",
        "average_milk_yield": "8,000–12,000+ liters/year",
        "primary_color": "Black & white pattern",
        "size": "Large",
        "temperament": "Calm",
        "use_case": "High-production dairy farms",
        "fun_fact": "World's highest milk-producing breed.",
        "history": "Selective breeding for milk yield for 100+ years.",
        "cross_breeding": "Boosts yield efficiency in mixed herds.",
        "future_potential": "Essential for precision dairy automation."
    },
    "jersey": {
        "breed": "Jersey",
        "origin": "Jersey Island",
        "milk_type": "High fat & protein",
        "average_milk_yield": "4,000–6,000 liters/year",
        "primary_color": "Fawn/light brown",
        "size": "Small",
        "temperament": "Alert & friendly",
        "use_case": "Ghee, butter, premium dairy",
        "fun_fact": "Milk appears golden due to beta-carotene.",
        "history": "Closed herd book since 1800s.",
        "cross_breeding": "Improves fat %, fertility, calving ease.",
        "future_potential": "Great for premium dairy startups."
    },
    "reddane": {
        "breed": "Red Dane",
        "origin": "Denmark",
        "milk_type": "Balanced composition",
        "average_milk_yield": "6,000–8,000 liters/year",
        "primary_color": "Red",
        "size": "Medium-Large",
        "temperament": "Robust & adaptable",
        "use_case": "Health-focused dairy systems",
        "fun_fact": "Built for longevity and fertility.",
        "history": "Improved using European dairy lines.",
        "cross_breeding": "Boosts fertility and long life.",
        "future_potential": "Ideal for low-antibiotic dairy systems."
    },
}

DISEASE_STATIC_DATA = {
    "FMD": {
        "name": "Foot-and-Mouth Disease",
        "severity": "High",
        "pathogen": "Aphthovirus",
        "symptoms": [
            "Blisters on mouth & feet",
            "Lameness",
            "High fever",
            "Severe drooling"
        ],
        "transmission": "Airborne, direct contact, equipment",
        "treatment": "Supportive only – no direct cure",
        "prevention": "Vaccination, isolation, biosecurity",
        "danger_level": "Extremely contagious"
    },
    "IBK": {
        "name": "Pinkeye (IBK)",
        "severity": "Medium",
        "pathogen": "Moraxella bovis",
        "symptoms": [
            "Red swollen eyes",
            "Light sensitivity",
            "Corneal ulcer",
            "Watery discharge"
        ],
        "transmission": "Flies, dust, environment",
        "treatment": "Antibiotics + eye protection",
        "prevention": "Fly control, sanitation",
        "danger_level": "Can cause permanent blindness"
    },
    "LSD": {
        "name": "Lumpy Skin Disease",
        "severity": "High",
        "pathogen": "Capripoxvirus",
        "symptoms": [
            "Hard skin nodules",
            "Fever",
            "Swollen lymph nodes",
            "Drop in milk production"
        ],
        "transmission": "Mosquitoes & biting flies",
        "treatment": "Supportive only",
        "prevention": "Vaccination & insect control",
        "danger_level": "Rapid farm-wide spread"
    },
}

# maintain consistent order for disease class names
DISEASE_CLASS_NAMES = ["IBK", "FMD", "LSD"]
