from google import genai
import os
import json
import time
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

if API_KEY:
    try:
        _client = genai.Client(api_key=API_KEY)
    except Exception as e:
        print(f"Error configuring API: {e}")
        _client = None
else:
    print("API Key not found!")
    _client = None

_MODEL_FALLBACK_CHAIN = ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-2.0-flash-lite"]


def _log(msg):
    print(f"[TruthInBite] {msg}", flush=True)


def _generate_with_retry(contents, retries=3, delay=5):
    """Try each model in the fallback chain with retries on 503; skip on 429."""
    last_exc = None
    for model in _MODEL_FALLBACK_CHAIN:
        for attempt in range(retries):
            _log(f"Calling {model} (attempt {attempt + 1}/{retries})...")
            try:
                response = _client.models.generate_content(model=model, contents=contents)
                _log(f"Response received from {model}.")
                return response
            except Exception as e:
                msg = str(e)
                if "429" in msg or "RESOURCE_EXHAUSTED" in msg:
                    _log(f"{model} quota exhausted (429). Skipping to next model.")
                    last_exc = e
                    break  # no point retrying same model
                elif "503" in msg or "UNAVAILABLE" in msg:
                    if attempt < retries - 1:
                        wait = delay * (attempt + 1)
                        _log(f"{model} overloaded (503). Retrying in {wait}s...")
                        time.sleep(wait)
                    else:
                        _log(f"{model} failed after {retries} attempts. Trying next model.")
                        last_exc = e
                else:
                    raise
    raise last_exc


def get_structured_data_from_gemini(pil_image):
    """Extract structured data from food label image"""
    try:
        _log("Step 1/3 — Extracting structured data from image...")
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

        response = _generate_with_retry([prompt, pil_image])
        json_text = response.text.strip().replace("``````", "").strip()

        # Clean up JSON
        start_idx = json_text.find("[")
        end_idx = json_text.rfind("]") + 1

        if start_idx != -1 and end_idx != 0:
            json_text = json_text[start_idx:end_idx]

        data = json.loads(json_text)
        _log(f"Extracted product: {data[0].get('product_name', 'Unknown') if isinstance(data, list) and data else 'Unknown'}")
        return data

    except json.JSONDecodeError:
        _log("ERROR: AI returned invalid JSON.")
        return {"error": "AI returned invalid JSON. Please try with a clearer image."}
    except Exception as e:
        _log(f"ERROR: {e}")
        return {"error": f"Error processing image: {str(e)}"}


def get_ai_health_summary(product_data, health_profile=None):
    """Get ingredient-based health score with separate WHO compliance check"""
    try:
        _log("Step 2/3 — Generating health summary & WHO compliance check...")
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

        response = _generate_with_retry(prompt)
        json_text = response.text.strip().replace("``````", "").strip()

        # Extract JSON
        start_idx = json_text.find("{")
        end_idx = json_text.rfind("}") + 1

        if start_idx != -1 and end_idx != 0:
            json_text = json_text[start_idx:end_idx]

        result = json.loads(json_text)
        _log(f"Health score: {result.get('score', 'N/A')}/100 — {result.get('verdict', '')}")
        return result

    except Exception as e:
        _log(f"ERROR: {e}")
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
        _log("Step 3/3 — Finding healthy Indian alternatives...")
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

        response = _generate_with_retry(prompt)
        json_text = response.text.strip().replace("``````", "").strip()

        # Extract JSON
        start_idx = json_text.find("[")
        end_idx = json_text.rfind("]") + 1

        if start_idx != -1 and end_idx != 0:
            json_text = json_text[start_idx:end_idx]

        result = json.loads(json_text)
        _log(f"Found {len(result)} alternative(s). Done.")
        return result

    except Exception as e:
        _log(f"ERROR: {e}")
        return []
