# TruthInBite

**AI-Powered Food Label Analyzer with Ingredient-Based Health Scoring**

[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Python](https://img.shields.io/badge/Python-3.7+-blue?style=flat&logo=python)](https://www.python.org/downloads/)
[![Google Gemini](https://img.shields.io/badge/Google%20Gemini-4285F4?style=flat&logo=google)](https://ai.google.dev/)
[![MIT License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

TruthInBite is a Streamlit web app that scans food product labels using Google Gemini, extracts ingredients and nutrition facts via OCR, and returns a 0–100 health score, WHO compliance check, and personalized warnings for 27+ health conditions — with budget-friendly Indian alternatives suggested at the end.

---

## Features

**Label Analysis**
- AI-powered OCR extracts ingredients, nutrition facts, and allergens from any food label image (JPG, PNG, WebP)
- 0–100 ingredient quality score based on processing level and additive content
- Separate WHO compliance check for sugar, sodium, saturated fat, and trans fat

**Personalized Health Profile**
- 27+ conditions including diabetes, heart disease, allergies, PCOD/PCOS, and Jain dietary restrictions
- Real-time warnings keyed to 200+ harmful ingredient keywords
- Age-specific guidance for children, elderly, pregnancy, and breastfeeding

**Healthy Alternatives**
- 3–5 traditional Indian alternatives suggested per product
- Filterable by budget: same price, budget-friendly, or premium
- Includes price range, availability, and preparation tips

---

## Getting Started

### Prerequisites
- Python 3.7+
- A free [Google AI Studio](https://ai.google.dev/gemini-api/docs/api-key) API key

### Installation

```bash
git clone https://github.com/vipu18/TruthInBite.git
cd TruthInBite
pip install -r requirements.txt
```

### Configuration

Create a `.env` file in the project root:

```
GEMINI_API_KEY="your_api_key_here"
```

### Run

```bash
streamlit run app.py
```

Open `http://localhost:8501` in your browser.

---

## How It Works

1. **Upload** — Drop a food label image into the uploader
2. **Extract** — Gemini parses the label into structured JSON (product name, ingredients, nutrition facts, allergens)
3. **Score** — Ingredient quality is scored 0–100; WHO compliance is checked separately
4. **Personalize** — Warnings are generated against your selected health conditions
5. **Suggest** — Healthier Indian alternatives are recommended at your budget

### Scoring Guide

| Range | Meaning |
|-------|---------|
| 80–100 | Natural, whole ingredients, minimal processing |
| 50–79 | Some processing; recognizable ingredients |
| 0–49 | Highly processed; artificial additives, hydrogenated oils |

---

## Supported Health Conditions

| Category | Conditions |
|----------|-----------|
| Metabolic | Diabetes Type 1 & 2, Pre-Diabetes, High Blood Pressure, Heart Disease, High Cholesterol, Kidney Disease, Liver Disease, Thyroid Issues |
| Women's Health | PCOD/PCOS, Pregnancy, Breastfeeding |
| Digestive | Gastric Issues, IBS |
| Allergies | Nut, Gluten, Lactose, Soy, Egg, Shellfish |
| Lifestyle | Weight Management, Muscle Building, Child (2–12 yrs), Elderly (60+) |
| Dietary | Vegetarian, Vegan, Jain Food |

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Streamlit |
| AI / OCR | Google Gemini 2.5 Flash (with 2.0 Flash fallback) |
| Image Handling | Pillow (PIL) |
| Data Processing | Pandas |
| Config | python-dotenv |

---

## Project Structure

```
TruthInBite/
├── app.py               # Streamlit UI and session state
├── ai_functions.py      # Gemini API calls (OCR, scoring, alternatives)
├── helper_functions.py  # Health warnings, nutrition calculations, score coloring
├── requirements.txt     # Python dependencies
├── DataSet/             # Sample food label images for testing
└── .env                 # API key (not committed)
```

---

## Contributing

1. Fork the repo and create a feature branch: `git checkout -b feature/my-feature`
2. Follow PEP 8 style guidelines
3. Add tests for new functionality
4. Open a pull request — see [CONTRIBUTING.md](CONTRIBUTING.md) for details

---

## Privacy & Security

- Images are processed in real-time and never stored
- Health profile analysis runs locally in the browser session
- API keys are read from environment variables, never hardcoded

---

## License

MIT — see [LICENSE](LICENSE) for details.

---

## Author

**Vipanshu Suman** — [@vipu18](https://github.com/vipu18)
