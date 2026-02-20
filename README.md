# AgroGenesis AI — Digital Twin Simulator (Enhanced)

This workspace contains `agrogenesis-enhanced.html` (or `agrogenai.html`), an interactive 3D digital twin simulator for field terrain, crops, weeds, and an autonomous robot.

## Features
- 3D terrain and crop surface (Plotly surface)
- Weed clusters with pest contagion dynamics
- Weed-aware A* navigation: path cost increases for weed-dense cells
- Robot auto-play animation along A* path
- Spray action to clear weeds along the route
- Hotspot mode: click 3D cells to toggle weeds
- Analytics: growth curve, weed forecast, EcoScore, environmental impact
- 2D heatmap with robot path overlay
- EcoScore canvas ring showing combined score (temp, rain, yield, weeds)
- Events: Pest Outbreak (spreads weeds), Drought Scenario (reduces yield)
- Compare mode: CURRENT vs DAY 1 snapshots
- Layer toggles for weeds, crops, path, heatmap, robot
- Animated loading screen and UI controls

## Quick Start
You can open the HTML directly or serve it with a simple local HTTP server (recommended).

Option A — Open directly
- Double-click `agrogenai.html` or open it in your browser.
- Note: some browsers restrict local file features; using a local server avoids this.

Option B — Python 3 HTTP server (recommended)
Open PowerShell in this folder and run:

```powershell
# start simple server on port 8000
python -m http.server 8000
# then open file in default browser (Windows)
Start-Process "http://localhost:8000/agrogenai.html"
```

---

# agroGen.ai - AI-Powered Agricultural Intelligence

This project provides AI-driven agricultural yield prediction and farm intelligence using machine learning on soil and weather data.

## Features

- **Dual Input Modes**: Choose between high-level parameter simulation or detailed characteristic input
- **ML-Powered Predictions**: Linear regression model trained on agricultural dataset for accurate yield forecasting
- **Interactive Grid Visualization**: 3×3 scenario grid for simulation mode showing yield predictions across different conditions
- **Real-time Bar Chart**: Single prediction visualization for direct input mode
- **High-Level Parameters**: User-friendly inputs like soil type, weather conditions, fertilizer levels, and crop health
- **Detailed Characteristics**: Technical inputs for precise predictions
- **AI Recommendations**: Automated insights based on current conditions

## Input Modes

### Simulation Mode
- **Soil Type**: Sandy, Loamy, Clay
- **Weather Condition**: Dry, Normal, Wet
- **Fertilizer Level**: Low, Medium, High
- **Season**: Winter, Summer, Monsoon
- **Crop Health**: Poor, Good, Excellent
- **Pest Pressure**: Low, Medium, High
- **Water Need**: Low, Medium, High

Generates a 3×3 grid varying soil type and weather conditions.

### Direct Input Mode
The model uses the following detailed characteristics for prediction:
- **Soil pH**: Acidity level affecting nutrient availability (4-9)
- **Soil Moisture %**: Water content in soil (0-100%)
- **Volumetric Water Content**: 3D water distribution (0-1)
- **Nitrogen (mg/kg)**: Essential nutrient levels (0-300)
- **Phosphorus (mg/kg)**: Phosphorus concentration (0-100)
- **Potassium (mg/kg)**: Potassium levels (0-400)
- **Rainfall 30d (mm)**: Recent precipitation (0-500)
- **Temperature Mean (°C)**: Average temperature (0-50)
- **Humidity Mean %**: Atmospheric moisture (0-100%)
- **NDVI Mean**: Vegetation health index (0-1)
- **Pest Risk Score**: Pest infestation probability (0-1)
- **Water Need Score**: Irrigation requirements (0-1)

## Setup

1. Install dependencies: `pip install pandas numpy scikit-learn joblib flask flask-cors`
2. Train model: `python train_model.py`
3. Run server: `python app.py`
4. Open `http://localhost:5000`

## Usage

- **Simulation Mode**: Select high-level parameters and click "Generate Yield Grid" to see predictions across scenarios
- **Direct Input Mode**: Enter detailed characteristics and click "Predict Yield" for single prediction
- Switch between modes using the radio buttons at the top of the sidebar
- Grid cells show yield values with color coding (green=high, yellow=medium, red=low)
- Hover over grid cells for detailed information

## Files

- `agrisim_dataset_sulur.csv`: Training dataset
- `train_model.py`: Model training script
- `app.py`: Flask backend server
- `index.html`: Frontend interface
- `yield_model.pkl`: Trained model coefficients
