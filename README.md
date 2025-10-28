# TruthInBite 🍎

**AI-Powered Food Label Analyzer with Ingredient-Based Health Scoring**

[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Python](https://img.shields.io/badge/Python-3.7+-blue?style=flat&logo=python)](https://www.python.org/downloads/)
[![Google AI](https://img.shields.io/badge/Google%20AI-Gemini-4285F4?style=flat&logo=google)](https://ai.google.dev/)
[![MIT License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

TruthInBite is an intelligent web application that analyzes food product labels using AI-powered OCR and provides comprehensive health insights based on ingredient quality, WHO compliance, and personalized health conditions.

![TruthInBite Demo](https://via.placeholder.com/800x400/4285F4/FFFFFF?text=TruthInBite+-+AI+Food+Analyzer)

## ✨ Key Features

### 🔍 **Advanced Food Label Analysis**
- **AI-Powered OCR**: Extract complete ingredient lists and nutrition facts from any food label image
- **Ingredient Quality Scoring**: 0-100 health score based on ingredient processing level and quality
- **WHO Compliance Check**: Separate analysis for WHO nutritional guidelines compliance
- **Multi-format Support**: Works with JPG, PNG, WebP image formats

### 🏥 **Personalized Health Analysis**
- **27+ Health Conditions**: Support for diabetes, heart disease, allergies, dietary preferences, and more
- **Indian Health Conditions**: Specialized analysis for PCOD/PCOS, Jain dietary restrictions
- **Smart Warnings**: Real-time alerts for harmful ingredients based on your health profile
- **Age-Specific Analysis**: Tailored recommendations for children, elderly, pregnancy, and breastfeeding

### 🌿 **Healthy Alternatives**
- **Indian Food Focus**: Suggests traditional Indian healthy alternatives
- **Budget-Conscious**: Filter alternatives by price range (budget-friendly to premium)
- **Local Availability**: Recommendations available in Indian markets
- **Preparation Tips**: Easy-to-follow preparation instructions for alternatives

## 🚀 Getting Started

### Prerequisites
- Python 3.7 or higher
- Google AI API Key (Gemini)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/vipu18/TruthInBite.git
cd TruthInBite
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```
3. **Get Google AI Studio API Key**

- Get your Google AI Studio API key by visiting [ai.google.dev](https://ai.google.dev/gemini-api/docs/api-key).
- Sign in with your Google account.
- Click"Get API key in Google AI Studio"
- Creating or selecting a Google Cloud project.
- Clicking "Create API key" to generate your free Gemini API key.

4. **Set up environment variables**
Create a `.env` file in the root directory:
```bash
GEMINI_API_KEY="your_google_ai_api_key_here"
```

5. **Run the application**
```bash
streamlit run app.py
```

6. **Access the app**
Open your browser and navigate to `http://localhost:8501`

## 🛠️ Technology Stack

- **Frontend**: Streamlit (Interactive web interface)
- **AI/ML**: Google Gemini 2.5 Flash (OCR and health analysis)
- **Image Processing**: Pillow (PIL) for image handling
- **Data Processing**: Pandas for structured data analysis
- **Environment Management**: python-dotenv for configuration

## 📊 How It Works

### 1. **Image Upload & Processing**
```python
# Upload food label image (JPG, PNG, WebP)
uploaded_file = st.file_uploader("Choose a food label image...")
image = Image.open(uploaded_file)
```

### 2. **AI-Powered Data Extraction**
```python
# Extract structured data using Gemini AI
product_list = get_structured_data_from_gemini(image)
```

### 3. **Ingredient-Based Health Scoring**
- **High Scores (80-100)**: Natural, whole ingredients with minimal processing
- **Medium Scores (50-79)**: Some processed but recognizable ingredients
- **Low Scores (0-49)**: Highly processed with artificial additives

### 4. **Personalized Health Analysis**
```python
# Analyze based on user's health conditions
warnings = run_health_analysis(product, health_profile)
```

## 🏥 Supported Health Conditions

TruthInBite analyzes products for 27+ health conditions:

### **Metabolic Conditions**
- Diabetes Type 1, Type 2, Pre-Diabetes
- High Blood Pressure, Heart Disease, High Cholesterol
- Kidney Disease, Liver Disease, Thyroid Issues

### **Women's Health**
- PCOD/PCOS, Pregnancy, Breastfeeding

### **Digestive Health**
- Gastric Issues, IBS (Irritable Bowel Syndrome)

### **Allergies & Sensitivities**
- Nut Allergy, Gluten Sensitivity, Lactose Intolerance
- Soy Allergy, Egg Allergy, Shellfish Allergy

### **Lifestyle & Age Groups**
- Weight Management, Muscle Building
- Child (2-12 years), Elderly (60+)

### **Dietary Preferences**
- Vegetarian, Vegan, Jain Food

## 📁 Project Structure

```
TruthInBite/
├── app.py                 # Main Streamlit application [17.6KB]
├── ai_functions.py        # AI/ML functions for analysis [8.1KB]
├── helper_functions.py    # Health analysis and utilities [10.3KB]
├── requirements.txt       # Python dependencies [63B]
├── .env                   # Environment variables (API keys) [56B]
├── .gitignore            # Git ignore file [15B]
└── README.md             # Project documentation
```

## 🔬 Core Functions

### **AI Functions**
```python
# Extract structured data from food labels
get_structured_data_from_gemini(pil_image)

# Get ingredient-based health scoring
get_ai_health_summary(product_data, health_profile)

# Suggest healthy Indian alternatives
get_healthy_alternatives(product_data, health_profile, budget_range)
```

### **Helper Functions**
```python
# Analyze health warnings based on conditions
run_health_analysis(product, health_profile)

# Calculate per-serving nutrition with WHO compliance
calculate_per_serve_nutrition(nutrition_per_100g, net_weight)

# Get color-coded health scores
get_health_score_color(score)
```

## 🎯 Use Cases

### **For Health-Conscious Consumers**
- Analyze packaged foods before purchasing
- Understand ingredient quality and processing levels
- Get personalized warnings for health conditions

### **For People with Medical Conditions**
- Diabetes management with sugar content analysis
- Heart disease monitoring with trans fat detection
- Allergy management with comprehensive allergen detection

### **For Indian Families**
- Traditional dietary restriction compliance (Jain, Vegetarian, Vegan)
- Budget-friendly healthy alternatives in Indian markets
- Age-appropriate food selection for children and elderly

## 📈 Scoring Methodology

### **Ingredient Quality Score (0-100)**
- **Deductions**: -10-20 points per artificial additive, -15-25 for trans fats
- **Additions**: +5-10 points for whole food ingredients, +5-15 for natural nutrients
- **WHO Compliance**: Separate check for sugar, sodium, saturated fat limits

### **Health Warnings**
- Real-time analysis of 200+ harmful ingredient keywords
- Condition-specific messaging (e.g., "Contains sugars - monitor blood glucose carefully")
- Severity indicators with emoji coding 🚨

## 🚀 Future Enhancements

- [ ] **Mobile App**: React Native version for on-the-go scanning
- [ ] **Barcode Integration**: Quick product lookup via barcode scanning
- [ ] **Offline Mode**: Local processing for basic ingredient analysis
- [ ] **Community Reviews**: User-generated product ratings and reviews
- [ ] **Recipe Suggestions**: Healthy recipes using alternative ingredients
- [ ] **Multi-language**: Hindi, Tamil, Bengali interface support
- [ ] **Export Reports**: PDF health analysis reports for doctor consultations

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Fork the Project**
2. **Create a Feature Branch** (`git checkout -b feature/AmazingFeature`)
3. **Commit Changes** (`git commit -m 'Add AmazingFeature'`)
4. **Push to Branch** (`git push origin feature/AmazingFeature`)
5. **Open a Pull Request**

### **Development Guidelines**
- Follow PEP 8 Python style guidelines
- Add unit tests for new features
- Update documentation for API changes
- Test with various food label formats

## 🔒 Privacy & Security

- **No Data Storage**: Images are processed in real-time and not stored
- **API Security**: Gemini API calls are secure and encrypted
- **Local Processing**: Health profile analysis happens locally
- **Environment Variables**: Sensitive API keys stored securely

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Vipanshu Suman**
- GitHub: [@vipu18](https://github.com/vipu18)
- Project Link: [TruthInBite](https://github.com/vipu18/TruthInBite)

## 🙏 Acknowledgments

- Google AI for Gemini API integration
- WHO for nutritional guidelines and compliance standards
- Streamlit community for the excellent web framework
- Indian nutrition research for health condition mappings

## 📞 Support

For support, issues, or feature requests:
- Open an issue on GitHub
- Check existing documentation
- Review the troubleshooting guide
