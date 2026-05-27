import streamlit as st
from PIL import Image
import os
from dotenv import load_dotenv
import pandas as pd
from ai_functions import (
    get_structured_data_from_gemini,
    get_ai_health_summary,
    get_healthy_alternatives,
)
from helper_functions import (
    run_health_analysis,
    calculate_per_serve_nutrition,
    get_health_score_color,
)

# Load environment variables
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

# Page configuration
st.set_page_config(
    page_title="TruthInBite - AI Health Analyzer",
    page_icon="🍎",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Fixed CSS - Background highlights for text visibility
st.markdown(
    """
<style>
    .main > div {
        padding-top: 2rem;
    }
    
    /* Health Score Styling */
    .health-score {
        text-align: center;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .score-green { 
        background-color: #d4edda; 
        color: #155724 !important; 
        border: 2px solid #28a745;
    }
    .score-yellow { 
        background-color: #fff3cd; 
        color: #856404 !important; 
        border: 2px solid #ffc107;
    }
    .score-orange { 
        background-color: #ffeaa7; 
        color: #8b6914 !important; 
        border: 2px solid #fd7e14;
    }
    .score-red { 
        background-color: #f8d7da; 
        color: #721c24 !important; 
        border: 2px solid #dc3545;
    }
    
    /* WHO Guidelines Box */
    .who-guidelines {
        background-color: #e8f4fd !important;
        padding: 1rem;
        border-left: 4px solid #007bff;
        border-radius: 5px;
        margin: 1rem 0;
        box-shadow: 0 2px 5px rgba(0,123,255,0.1);
    }
    .who-guidelines strong {
        color: #0056b3 !important;
        font-weight: 600 !important;
    }
    
    /* Alternative Box */
    .alternative-box {
        background-color: #f8fff8 !important;
        padding: 1.5rem;
        border-left: 4px solid #28a745;
        border-radius: 5px;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(40,167,69,0.1);
    }
    .alternative-box strong {
        color: #155724 !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
    }
    
    /* Text highlight backgrounds for better readability */
    .stTabs [data-baseweb="tab-panel"] {
        background-color: rgba(255, 255, 255, 0.05) !important;
        padding: 1rem !important;
        border-radius: 5px !important;
        backdrop-filter: blur(10px);
    }
    
    /* Ingredient analysis text with background */
    .ingredient-highlight {
        background-color: rgba(255, 255, 255, 0.1) !important;
        padding: 0.8rem !important;
        border-radius: 8px !important;
        margin: 0.5rem 0 !important;
        backdrop-filter: blur(5px);
    }
    
    /* Quality assessment section */
    .ingredient-quality-section {
        background-color: rgba(248, 249, 250, 0.95) !important;
        padding: 1rem !important;
        border-radius: 8px !important;
        margin: 1rem 0 !important;
        border-left: 4px solid #007bff !important;
        color: #495057 !important;
    }
    
    .ingredient-quality-section strong {
        color: #212529 !important;
        font-weight: 700 !important;
    }
    
    /* Alternative item styling with background */
    .alternative-item {
        background-color: rgba(255, 255, 255, 0.95) !important;
        padding: 1rem;
        margin: 0.8rem 0;
        border-radius: 8px;
        border: 1px solid rgba(224, 224, 224, 0.5);
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        backdrop-filter: blur(5px);
    }
    .alternative-item h4 {
        color: #2c3e50 !important;
        margin-bottom: 0.5rem !important;
        font-weight: 600 !important;
    }
    .alternative-item p {
        color: #34495e !important;
        margin-bottom: 0.3rem !important;
        line-height: 1.4 !important;
    }
    
    /* Markdown text with subtle background for readability */
    .markdown-highlight {
        background-color: rgba(255, 255, 255, 0.08) !important;
        padding: 0.3rem 0.5rem !important;
        border-radius: 4px !important;
        display: inline-block;
        margin: 0.1rem 0 !important;
    }
</style>
""",
    unsafe_allow_html=True,
)

# Check API key
if not API_KEY:
    st.error("API Key not found! Please create a .env file with GEMINI_API_KEY.")
    st.stop()

# Header
st.title("TruthInBite - AI Health Analyzer")
st.caption("Ingredient-Based Health Scoring with WHO Compliance Check")

# Sidebar - Expanded Health Profile
with st.sidebar:
    st.header("🩺 Your Health Profile")

    health_profile = st.multiselect(
        "Select your health conditions:",
        [
            "Diabetes Type 1",
            "Diabetes Type 2",
            "Pre-Diabetes",
            "High Blood Pressure",
            "Heart Disease",
            "High Cholesterol",
            "Kidney Disease",
            "Liver Disease",
            "Thyroid Issues",
            "PCOD/PCOS",
            "Gastric Issues",
            "IBS",
            "Nut Allergy",
            "Gluten Sensitivity",
            "Lactose Intolerance",
            "Soy Allergy",
            "Egg Allergy",
            "Shellfish Allergy",
            "Weight Management",
            "Muscle Building",
            "Pregnancy",
            "Breastfeeding",
            "Child (2-12 years)",
            "Elderly (60+)",
            "Vegetarian",
            "Vegan",
            "Jain Food",
        ],
        help="Select all conditions that apply to you for personalized analysis",
    )

    st.markdown("---")

    # Budget range for alternatives
    budget_range = st.selectbox(
        "💰 Budget Range for Alternatives:",
        [
            "Same Price (±10%)",
            "Budget Friendly (25% less)",
            "Premium (+25% more)",
            "Any Price",
        ],
    )

    st.markdown("---")
    st.info(
        "📋 **Analysis Method:**\n- Score based on ingredient quality\n- WHO compliance separately checked\n- Personalized health warnings\n- Indian alternative suggestions"
    )

# File upload
st.subheader("📸 Upload Food Label")
uploaded_file = st.file_uploader(
    "Choose a food label image...",
    type=["jpg", "jpeg", "png", "webp"],
    help="Upload a clear image of the food product label",
)

# Initialize session state
if "processed_data" not in st.session_state:
    st.session_state.processed_data = None
if "current_image" not in st.session_state:
    st.session_state.current_image = None

# Main processing
if uploaded_file is not None:
    image = Image.open(uploaded_file)

    # new image
    image_changed = st.session_state.current_image != uploaded_file.name

    if image_changed or st.session_state.processed_data is None:
        st.session_state.current_image = uploaded_file.name

        # Progress bar
        progress = st.progress(0)
        status = st.empty()

        # Extract data
        status.text("🔍 Analyzing food label...")
        progress.progress(25)

        try:
            product_list = get_structured_data_from_gemini(image)
            progress.progress(50)

            if isinstance(product_list, dict) and "error" in product_list:
                st.error(f"❌ {product_list['error']}")
                st.stop()

            st.session_state.processed_data = product_list
            progress.progress(100)
            status.text("✅ Analysis complete!")

        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            st.stop()

    # Display results
    product_list = st.session_state.processed_data

    if product_list and isinstance(product_list, list):
        for i, product in enumerate(product_list):
            product_name = product.get("product_name", f"Product #{i+1}")

            st.markdown("---")
            st.subheader(f"🏷️ {product_name}")

            # Main analysis columns
            col1, col2 = st.columns([1, 2])

            with col1:
                st.image(image, caption="Product Label", width='stretch')

            with col2:
                # Health Score Analysis
                try:
                    summary = get_ai_health_summary(product, health_profile)

                    if summary:
                        score = summary.get("score", 0)
                        verdict = summary.get("verdict", "Analysis unavailable")
                        reasons = summary.get("reasons", [])
                        who_compliance = summary.get("who_compliance", [])

                        # Color-coded score
                        color_class, emoji = get_health_score_color(score)

                        st.markdown(
                            f"""
                        <div class="health-score {color_class}">
                            <h2>{emoji} {score}/100 Health Score</h2>
                            <p><strong>{verdict}</strong></p>
                        </div>
                        """,
                            unsafe_allow_html=True,
                        )

                        # Key points with better visibility
                        if reasons:
                            st.markdown("**📋 Ingredient Analysis:**")
                            for reason in reasons:
                                st.markdown(f"• {reason}")

                        # WHO Guidelines Compliance (separate from score)
                        if who_compliance:
                            st.markdown(
                                f"""
                            <div class="who-guidelines">
                                <strong>🌍 WHO Guidelines Compliance Check:</strong>
                            </div>
                            """,
                                unsafe_allow_html=True,
                            )

                            for compliance in who_compliance:
                                if (
                                    "exceeds" in compliance.lower()
                                    or "high" in compliance.lower()
                                    or "above" in compliance.lower()
                                ):
                                    st.warning(f"⚠️ {compliance}")
                                else:
                                    st.success(f"✅ {compliance}")

                except Exception as e:
                    st.error(f"Health analysis failed: {str(e)}")

            # Detailed tabs
            tab1, tab2, tab3, tab4, tab5 = st.tabs(
                [
                    "🧪 Ingredients",
                    "📊 Nutrition",
                    "⚠️ Allergens",
                    "🩺 Personal Health",
                    "🔄 Healthy Alternatives",
                ]
            )

            with tab1:
                st.markdown("### 🧪 Ingredient Analysis")

                if product.get("ingredients"):
                    ingredients_df = pd.DataFrame(product["ingredients"])
                    st.dataframe(
                        ingredients_df, width='stretch', hide_index=True
                    )

                    # Enhanced quality assessment with background highlight
                    st.markdown(
                        """
                    <div class="ingredient-quality-section">
                        <strong>📋 Quality Assessment:</strong>
                    </div>
                    """,
                        unsafe_allow_html=True,
                    )

                    ingredient_names = [
                        ing.get("name", "").lower()
                        for ing in product.get("ingredients", [])
                    ]

                    # Check for concerning ingredients
                    concerning = [
                        "artificial",
                        "synthetic",
                        "modified",
                        "hydrogenated",
                        "trans",
                        "msg",
                        "aspartame",
                        "acesulfame",
                    ]
                    natural = ["whole", "organic", "natural", "pure", "fresh"]

                    concerning_found = [
                        ing
                        for ing in ingredient_names
                        if any(c in ing for c in concerning)
                    ]
                    natural_found = [
                        ing
                        for ing in ingredient_names
                        if any(n in ing for n in natural)
                    ]

                    if concerning_found:
                        st.error(
                            f"⚠️ Concerning ingredients detected: {', '.join(concerning_found[:3])}"
                        )
                    if natural_found:
                        st.success(
                            f"Natural ingredients found: {', '.join(natural_found[:3])}"
                        )

            with tab2:
                if product.get("nutrition_facts"):
                    nutrition_df = pd.DataFrame(product["nutrition_facts"])
                    net_weight = product.get("net_weight")

                    if net_weight:
                        per_serve_values = calculate_per_serve_nutrition(
                            product["nutrition_facts"], net_weight
                        )
                        if per_serve_values:
                            nutrition_df[f"Per Serving ({net_weight}g)"] = (
                                per_serve_values
                            )

                    nutrition_df.rename(columns={"Value": "Per 100g"}, inplace=True)
                    st.dataframe(
                        nutrition_df, width='stretch', hide_index=True
                    )
                else:
                    st.warning("No nutrition information found")

            with tab3:
                if product.get("allergens"):
                    allergen_df = pd.DataFrame(
                        product["allergens"], columns=["Allergen"]
                    )
                    st.dataframe(allergen_df, width='stretch', hide_index=True)
                else:
                    st.success("✅ No allergen information found")

            with tab4:
                if health_profile:
                    warnings = run_health_analysis(product, health_profile)
                    if warnings:
                        for warning in warnings:
                            st.error(f"🚨 {warning}")
                    else:
                        st.success("✅ No specific concerns for your health profile")
                else:
                    st.info(
                        "👆 Select your health conditions in the sidebar for personalized analysis"
                    )

            with tab5:
                # Indian Healthy Alternatives
                st.markdown("### 🔄 Healthy Alternatives")

                try:
                    alternatives = get_healthy_alternatives(
                        product, health_profile, budget_range
                    )

                    if alternatives:
                        st.markdown(
                            f"""
                        <div class="alternative-box">
                            <strong>🌿 Healthier Indian Alternatives at Similar Cost:</strong>
                        </div>
                        """,
                            unsafe_allow_html=True,
                        )

                        for idx, alt in enumerate(alternatives):
                            name = alt.get("name", "Unknown")
                            why_better = alt.get("why_better", "")
                            price_range = alt.get("price_range", "")
                            availability = alt.get("availability", "")

                            st.markdown(
                                f"""
                            <div class="alternative-item">
                                <h4>🌿 {name}</h4>
                                <p><strong>💚 Why it's better:</strong> {why_better}</p>
                                <p><strong>💰 Price:</strong> {price_range}</p>
                                <p><strong>🛒 Where to buy:</strong> {availability}</p>
                            </div>
                            """,
                                unsafe_allow_html=True,
                            )

                    else:
                        st.info("No specific alternatives found for this product.")

                except Exception as e:
                    st.error(f"Could not fetch alternatives: {str(e)}")

            # Debug info (optional)
            with st.expander("🔧 Raw Data (Debug)"):
                st.json(product)

    else:
        st.error(
            "❌ Could not analyze the uploaded image. Please try with a cleaner food label."
        )

else:
    # Welcome message
    st.markdown(
        """
    ### 👋 Welcome to TruthInBite!
    
    **Features:**
    - 🔍 AI-powered ingredient analysis
    - 🌍 WHO compliance checking (separate from score)
    - 🩺 Personalized health warnings
    - 🌿 Indian healthy alternatives suggestions
    - 💰 Budget-friendly recommendations
    
    **Scoring Method:**
    - Score based on ingredient quality (natural vs processed)
    - WHO compliance checked separately
    - Personalized warnings based on health conditions
    
    **How to use:**
    1. Select your health conditions in the sidebar
    2. Upload a clear food label image
    3. Get ingredient-based health score and WHO compliance check!
    """
    )
