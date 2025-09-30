import google.generativeai as genai
import os
import json
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

if API_KEY:
    try:
        genai.configure(api_key=API_KEY)
    except Exception as e:
        print(f"Error configuring API: {e}")
else:
    print("API Key not found!")

# Cache for model instances
_model_cache = {}


def get_model(model_name="gemini-2.5-flash"):
    """Get cached model instance for better performance"""
    if model_name not in _model_cache:
        _model_cache[model_name] = genai.GenerativeModel(model_name)
    return _model_cache[model_name]


def get_structured_data_from_gemini(pil_image):
    """Extract structured data from food label image"""
    try:
        model = get_model("gemini-2.5-flash")

        prompt = """
        Analyze this food label image and extract data accurately.
        Return ONLY a valid JSON array with this structure:

        [
            {
                "product_name": "Product Name",
                "net_weight": 100.0,
                "ingredients": [
                    {"name": "Ingredient Name", "details": "additional info"}
                ],
                "nutrition_facts": [
                    {"Nutrient": "Energy", "Value": "200 kcal"},
                    {"Nutrient": "Total Fat", "Value": "10g"},
                    {"Nutrient": "Saturated Fat", "Value": "5g"},
                    {"Nutrient": "Trans Fat", "Value": "0g"},
                    {"Nutrient": "Cholesterol", "Value": "0mg"},
                    {"Nutrient": "Sodium", "Value": "150mg"},
                    {"Nutrient": "Total Carbohydrates", "Value": "25g"},
                    {"Nutrient": "Dietary Fiber", "Value": "3g"},
                    {"Nutrient": "Total Sugars", "Value": "12g"},
                    {"Nutrient": "Added Sugars", "Value": "8g"},
                    {"Nutrient": "Protein", "Value": "4g"}
                ],
                "allergens": ["Contains milk", "May contain nuts"]
            }
        ]

        Rules:
        - Extract ALL visible nutrition facts
        - Be precise with numerical values
        - Include serving size information if available
        - List ingredients in order of quantity (if possible)
        - Include all allergen warnings
        """

        response = model.generate_content([prompt, pil_image])
        json_text = response.text.strip().replace("``````", "").strip()

        # Clean up JSON
        start_idx = json_text.find("[")
        end_idx = json_text.rfind("]") + 1

        if start_idx != -1 and end_idx != 0:
            json_text = json_text[start_idx:end_idx]

        data = json.loads(json_text)
        return data

    except json.JSONDecodeError:
        return {"error": "AI returned invalid JSON. Please try with a clearer image."}
    except Exception as e:
        return {"error": f"Error processing image: {str(e)}"}


def get_ai_health_summary(product_data, health_profile=None):
    """Get ingredient-based health score with separate WHO compliance check"""
    try:
        model = get_model("gemini-2.5-flash")

        prompt = f"""
        Analyze this food product as a nutrition expert. Score based on INGREDIENT QUALITY, then separately check WHO compliance.

        Product: {json.dumps(product_data, indent=2)}
        User Health Conditions: {health_profile if health_profile else "None specified"}

        INGREDIENT-BASED SCORING (0-100):
        
        HIGH SCORES (80-100):
        - Natural, whole ingredients (fruits, vegetables, whole grains, nuts, seeds)
        - Minimal processing (steamed, roasted, dried)
        - No artificial additives
        - Traditional preparation methods
        
        MEDIUM SCORES (50-79):
        - Some processed ingredients but recognizable
        - Natural preservatives (salt, sugar, vinegar)
        - Basic processing (grinding, cooking, fermentation)
        
        LOW SCORES (0-49):
        - Highly processed ingredients (modified starches, artificial flavors)
        - Chemical preservatives (BHA, BHT, sodium benzoate)
        - Artificial colors, flavors, sweeteners
        - Hydrogenated oils, trans fats
        - Long lists of unpronounceable chemicals

        Scoring Formula:
        - Start with 100
        - Subtract 10-20 points per artificial additive
        - Subtract 15-25 points for trans fats/hydrogenated oils
        - Subtract 5-15 points per chemical preservative
        - Add 5-10 points for whole food ingredients
        - Add 5-15 points for natural nutrients (fiber, protein, vitamins)

        SEPARATE WHO COMPLIANCE CHECK:
        - Free sugars: <10% of energy
        - Saturated fats: <10% of energy  
        - Trans fats: eliminate completely
        - Sodium: <2g per day per serving

        Return ONLY this JSON:
        {{
            "score": 65,
            "verdict": "Moderately processed with some concerning ingredients",
            "reasons": [
                "Contains artificial preservatives (sodium benzoate) - reduces score by 15 points",
                "High sugar content from refined sugars - reduces score by 10 points", 
                "Good protein content - adds 5 points",
                "Contains whole grain flour - adds 8 points"
            ],
            "who_compliance": [
                "Sugar content exceeds WHO recommendation of 10% daily energy",
                "Sodium level is within WHO guidelines (under 2g per serving)",
                "Contains trans fats - WHO recommends complete elimination"
            ],
            "ingredient_quality": [
                "Highly processed ingredients detected",
                "Contains 3 artificial additives",
                "Some natural ingredients present"
            ]
        }}
        """

        response = model.generate_content(prompt)
        json_text = response.text.strip().replace("``````", "").strip()

        # Extract JSON
        start_idx = json_text.find("{")
        end_idx = json_text.rfind("}") + 1

        if start_idx != -1 and end_idx != 0:
            json_text = json_text[start_idx:end_idx]

        return json.loads(json_text)

    except Exception as e:
        return {
            "score": 0,
            "verdict": "Analysis failed",
            "reasons": [f"Error: {str(e)}"],
            "who_compliance": ["Could not check WHO compliance"],
            "ingredient_quality": ["Could not assess ingredient quality"],
        }


def get_healthy_alternatives(
    product_data, health_profile=None, budget_range="Same Price (±10%)"
):
    """Get Indian healthy alternatives at similar cost"""
    try:
        model = get_model("gemini-2.5-flash")

        prompt = f"""
        Suggest healthier Indian alternatives for this food product:
        
        Product: {json.dumps(product_data, indent=2)}
        Health Profile: {health_profile if health_profile else "General"}
        Budget: {budget_range}
        
        Focus on alternatives with BETTER INGREDIENT QUALITY:
        - Natural, minimally processed ingredients
        - Traditional Indian healthy foods
        - Locally available, fresh ingredients
        - Similar taste/convenience but with cleaner ingredients
        - Cost-effective options
        - Available in Indian markets
        
        Use this format JSON array:
        [
            {{
                "name": "name",
                "why_better": "why better,
                "price_range": "₹price",
                "availability": "",
                "preparation_tip": "preparation tip"
            }},
        ]
        
        Provide 3-5 alternatives focusing on cleaner, more natural ingredients.
        """

        response = model.generate_content(prompt)
        json_text = response.text.strip().replace("``````", "").strip()

        # Extract JSON
        start_idx = json_text.find("[")
        end_idx = json_text.rfind("]") + 1

        if start_idx != -1 and end_idx != 0:
            json_text = json_text[start_idx:end_idx]

        return json.loads(json_text)

    except Exception as e:
        return []
