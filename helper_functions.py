import re
from typing import List, Dict, Optional, Union

# Pre-compiled regex patterns
NUMERIC_PATTERN = re.compile(r"[\d.]+")
UNIT_PATTERN = re.compile(r"[a-zA-Z]+")

# Comprehensive Indian health condition mappings (same as before)
HEALTH_CONDITIONS = {
    # Diabetes variants
    "Diabetes Type 1": {
        "keywords": [
            "sugar",
            "glucose",
            "fructose",
            "syrup",
            "honey",
            "jaggery",
            "corn syrup",
        ],
        "message": "Contains sugars - monitor blood glucose carefully",
    },
    "Diabetes Type 2": {
        "keywords": [
            "sugar",
            "glucose",
            "fructose",
            "refined flour",
            "maida",
            "corn starch",
        ],
        "message": "High glycemic ingredients present - check with doctor",
    },
    "Pre-Diabetes": {
        "keywords": ["sugar", "glucose", "refined", "processed", "high fructose"],
        "message": "Contains processed sugars - may affect blood sugar",
    },
    # Cardiovascular conditions
    "High Blood Pressure": {
        "keywords": [
            "sodium",
            "salt",
            "msg",
            "monosodium glutamate",
            "sodium chloride",
            "baking soda",
        ],
        "message": "High sodium content - may increase blood pressure",
    },
    "Heart Disease": {
        "keywords": [
            "trans fat",
            "hydrogenated",
            "saturated fat",
            "palm oil",
            "coconut oil",
        ],
        "message": "Contains fats that may affect heart health",
    },
    "High Cholesterol": {
        "keywords": [
            "saturated fat",
            "trans fat",
            "cholesterol",
            "butter",
            "ghee",
            "coconut oil",
        ],
        "message": "May increase cholesterol levels",
    },
    # Organ-specific conditions
    "Kidney Disease": {
        "keywords": ["sodium", "potassium", "phosphorus", "protein", "msg"],
        "message": "May strain kidney function",
    },
    "Liver Disease": {
        "keywords": [
            "artificial colors",
            "preservatives",
            "alcohol",
            "high fat",
            "processed",
        ],
        "message": "Contains additives that may burden liver",
    },
    "Thyroid Issues": {
        "keywords": ["iodine", "soy", "cruciferous", "goitrogenic", "cabbage"],
        "message": "May interfere with thyroid function",
    },
    # Women's health
    "PCOD/PCOS": {
        "keywords": ["sugar", "refined flour", "trans fat", "artificial sweeteners"],
        "message": "May worsen PCOD/PCOS symptoms",
    },
    "Pregnancy": {
        "keywords": [
            "artificial sweeteners",
            "high mercury",
            "raw",
            "unpasteurized",
            "alcohol",
        ],
        "message": "Not recommended during pregnancy",
    },
    "Breastfeeding": {
        "keywords": ["caffeine", "alcohol", "artificial colors", "msg"],
        "message": "May affect milk quality - consult doctor",
    },
    # Digestive conditions
    "Gastric Issues": {
        "keywords": ["spicy", "acidic", "citric acid", "vinegar", "chili", "pepper"],
        "message": "May trigger gastric problems",
    },
    "IBS": {
        "keywords": ["lactose", "gluten", "artificial sweeteners", "high fat", "spicy"],
        "message": "May trigger IBS symptoms",
    },
    # Allergies
    "Nut Allergy": {
        "keywords": [
            "nut",
            "almond",
            "cashew",
            "peanut",
            "walnut",
            "hazelnut",
            "pistachio",
        ],
        "message": "Contains nuts - severe allergy risk",
    },
    "Gluten Sensitivity": {
        "keywords": ["wheat", "barley", "rye", "gluten", "flour", "malt", "semolina"],
        "message": "Contains gluten - may cause sensitivity reaction",
    },
    "Lactose Intolerance": {
        "keywords": ["milk", "lactose", "dairy", "whey", "casein", "butter", "cheese"],
        "message": "Contains dairy - may cause digestive issues",
    },
    "Soy Allergy": {
        "keywords": ["soy", "soybean", "lecithin", "tofu", "soya"],
        "message": "Contains soy - allergy risk",
    },
    "Egg Allergy": {
        "keywords": ["egg", "albumin", "lecithin", "mayonnaise"],
        "message": "Contains egg - allergy risk",
    },
    # Lifestyle conditions
    "Weight Management": {
        "keywords": ["high calorie", "sugar", "saturated fat", "trans fat", "refined"],
        "message": "High calorie - may affect weight management",
    },
    "Muscle Building": {
        "keywords": ["low protein", "high sugar", "processed", "artificial"],
        "message": "Not optimal for muscle building goals",
    },
    # Age-specific
    "Child (2-12 years)": {
        "keywords": [
            "artificial colors",
            "high sugar",
            "caffeine",
            "preservatives",
            "msg",
        ],
        "message": "May not be suitable for children",
    },
    "Elderly (60+)": {
        "keywords": ["high sodium", "hard to digest", "artificial", "high sugar"],
        "message": "May not be suitable for elderly",
    },
    # Dietary preferences
    "Vegetarian": {
        "keywords": ["gelatin", "animal fat", "lard", "chicken", "beef", "fish"],
        "message": "Contains non-vegetarian ingredients",
    },
    "Vegan": {
        "keywords": ["milk", "dairy", "honey", "gelatin", "whey", "casein", "egg"],
        "message": "Contains animal-derived ingredients",
    },
    "Jain Food": {
        "keywords": ["onion", "garlic", "potato", "ginger", "root vegetables"],
        "message": "Contains ingredients not suitable for Jain diet",
    },
}


def run_health_analysis(product: Dict, health_profile: List[str]) -> List[str]:
    """Enhanced health analysis for Indian health conditions"""
    if not health_profile or not product:
        return []

    warnings = set()

    # Combine all text for analysis
    ingredient_names = " ".join(
        ing.get("name", "").lower() for ing in product.get("ingredients", [])
    )
    allergen_info = " ".join(product.get("allergens", [])).lower()
    combined_text = f"{ingredient_names} {allergen_info}"

    # Check each health condition
    for condition in health_profile:
        if condition in HEALTH_CONDITIONS:
            condition_data = HEALTH_CONDITIONS[condition]

            # Check if any keywords match
            if any(keyword in combined_text for keyword in condition_data["keywords"]):
                warnings.add(f"🚨 {condition}: {condition_data['message']}")

    return list(warnings)


def calculate_per_serve_nutrition(
    nutrition_per_100g: List[Dict], net_weight: Union[int, float]
) -> Optional[List[str]]:
    """Calculate per-serving nutrition with WHO compliance check"""
    if not net_weight or not isinstance(net_weight, (int, float)) or net_weight <= 0:
        return None

    if not nutrition_per_100g or not isinstance(nutrition_per_100g, list):
        return None

    per_serve_facts = []

    # WHO limits per 100g (approximate)
    who_limits = {
        "saturated": 10,  # <10% of energy (roughly 10g per 100g)
        "trans": 1,  # <1% of energy (roughly 1g per 100g)
        "sodium": 500,  # <5g per day (roughly 500mg per 100g)
        "sugar": 12,  # <10% of energy (roughly 12g per 100g)
    }

    for fact in nutrition_per_100g:
        if not isinstance(fact, dict):
            per_serve_facts.append("N/A")
            continue

        value_str = str(fact.get("Value", ""))

        try:
            numeric_match = NUMERIC_PATTERN.search(value_str)
            if not numeric_match:
                per_serve_facts.append("N/A")
                continue

            value_100g = float(numeric_match.group())
            unit_matches = UNIT_PATTERN.findall(value_str)
            unit = "".join(unit_matches) if unit_matches else ""

            # Calculate per-serve value
            per_serve_value = (value_100g / 100) * net_weight

            # Format value
            if per_serve_value < 1:
                formatted_value = f"{per_serve_value:.2f}"
            else:
                formatted_value = f"{per_serve_value:.1f}"

            # Add WHO warning if needed
            nutrient_lower = fact.get("Nutrient", "").lower()
            warning = ""

            for limit_nutrient, limit_value in who_limits.items():
                if limit_nutrient in nutrient_lower and value_100g > limit_value:
                    warning = " ⚠️"
                    break

            per_serve_facts.append(f"{formatted_value} {unit}{warning}")

        except (ValueError, AttributeError, TypeError):
            per_serve_facts.append("N/A")

    return per_serve_facts


def get_health_score_color(score: int) -> tuple:
    """Get color coding for health scores based on WHO compliance"""
    if score >= 90:
        return ("score-green", "🟢")
    elif score >= 80:
        return ("score-green", "🟢")
    elif score >= 70:
        return ("score-yellow", "🟡")
    elif score >= 60:
        return ("score-orange", "🟠")
    else:
        return ("score-red", "🔴")


def check_who_compliance(nutrition_facts: List[Dict]) -> List[str]:
    """Check WHO compliance for nutrition facts"""
    compliance_issues = []

    # WHO limits per 100g
    limits = {
        "saturated fat": 10,
        "trans fat": 1,
        "sodium": 500,
        "total sugars": 12,
        "added sugars": 6,
    }

    for fact in nutrition_facts:
        nutrient = fact.get("Nutrient", "").lower()
        value_str = fact.get("Value", "")

        try:
            value = float(NUMERIC_PATTERN.search(value_str).group())

            for limit_nutrient, limit_value in limits.items():
                if limit_nutrient in nutrient and value > limit_value:
                    compliance_issues.append(
                        f"⚠️ {fact.get('Nutrient')} ({value}) exceeds WHO recommendations ({limit_value})"
                    )
        except (AttributeError, ValueError):
            continue

    if not compliance_issues:
        compliance_issues.append("✅ Meets WHO nutritional guidelines")

    return compliance_issues
