from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import joblib
import numpy as np
import re
from bs4 import BeautifulSoup

app = Flask(__name__)
CORS(app)

# Load model or use default coefficients
try:
    coeff = joblib.load('yield_model.pkl')
except FileNotFoundError:
    # Default coefficients from training with multi-crop dataset
    coeff = np.array([1.21598750e+00, -4.07791384e-03, 1.72452039e-03, 8.59190553e-03,
                      1.95734495e-02, 3.58838709e-04, 1.93363152e-03, 2.45939194e-04,
                      -2.36554394e+00, -1.07795321e+00])
    print("Warning: yield_model.pkl not found. Using default coefficients from multi-crop dataset.")

# Crop-specific parameters mapping
CROP_PARAMS = {
    'rice': {'pestSensitivity': 0.7, 'waterNeed': 0.8, 'heatTolerance': 0.5, 'name': 'Rice'},
    'wheat': {'pestSensitivity': 0.5, 'waterNeed': 0.5, 'heatTolerance': 0.6, 'name': 'Wheat'},
    'cotton': {'pestSensitivity': 0.9, 'waterNeed': 0.6, 'heatTolerance': 0.7, 'name': 'Cotton'},
    'sugarcane': {'pestSensitivity': 0.4, 'waterNeed': 0.9, 'heatTolerance': 0.6, 'name': 'Sugarcane'},
    'maize': {'pestSensitivity': 0.5, 'waterNeed': 0.6, 'heatTolerance': 0.7, 'name': 'Maize'},
    'groundnut': {'pestSensitivity': 0.3, 'waterNeed': 0.4, 'heatTolerance': 0.8, 'name': 'Groundnut'},
}

SOIL_PARAMS = {
    'clay': {'moisture': 0.8, 'nutrient': 0.7, 'ph': 7.0},
    'loam': {'moisture': 0.6, 'nutrient': 0.9, 'ph': 6.5},
    'sandy': {'moisture': 0.3, 'nutrient': 0.4, 'ph': 5.5},
    'black': {'moisture': 0.7, 'nutrient': 0.8, 'ph': 7.2},
    'red': {'moisture': 0.4, 'nutrient': 0.5, 'ph': 6.0},
}

def parse_html_input(html_content):
    """Extract parameters from HTML input"""
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Extract crop type
    crop_type = 'rice'  # default
    crop_select = soup.find('select', {'id': 'cropType'})
    if crop_select:
        selected = crop_select.find('option', selected=True)
        if not selected:
            # Try to find option with value attribute
            options = crop_select.find_all('option')
            for opt in options:
                if opt.get('value'):
                    crop_type = opt.get('value', 'rice')
                    break
        else:
            crop_type = selected.get('value', 'rice')
    
    # Extract soil type
    soil_type = 'loam'  # default
    soil_select = soup.find('select', {'id': 'soilType'})
    if soil_select:
        selected = soil_select.find('option', selected=True)
        if not selected:
            options = soil_select.find_all('option')
            for opt in options:
                if opt.get('value'):
                    soil_type = opt.get('value', 'loam')
                    break
        else:
            soil_type = selected.get('value', 'loam')
    
    # Extract humidity
    humidity = 65  # default
    humidity_input = soup.find('input', {'id': 'humidity'})
    if humidity_input:
        try:
            humidity = float(humidity_input.get('value', 65))
        except (ValueError, TypeError):
            humidity = 65
    
    # Extract temperature
    temperature = 28  # default
    temp_input = soup.find('input', {'id': 'temperature'})
    if temp_input:
        try:
            temperature = float(temp_input.get('value', 28))
        except (ValueError, TypeError):
            temperature = 28
    
    # Extract rainfall
    rainfall = 'Medium'  # default
    rainfall_input = soup.find('input', {'id': 'rainfall'})
    if rainfall_input:
        try:
            rain_val = int(rainfall_input.get('value', 2))
            rainfall_map = {1: 'Low', 2: 'Medium', 3: 'High'}
            rainfall = rainfall_map.get(rain_val, 'Medium')
        except (ValueError, TypeError):
            rainfall = 'Medium'
    
    # Map rainfall to mm
    rainfall_mm_map = {'Low': 50, 'Medium': 150, 'High': 400}
    rainfall_mm = rainfall_mm_map.get(rainfall, 150)
    
    # Get soil parameters
    soil_info = SOIL_PARAMS.get(soil_type, SOIL_PARAMS['loam'])
    crop_info = CROP_PARAMS.get(crop_type, CROP_PARAMS['rice'])
    
    # Calculate detailed parameters
    soil_ph = soil_info['ph']
    soil_moisture_pct = soil_info['moisture'] * 100
    volumetric_water_content = soil_info['moisture'] * 0.8
    
    # Estimate NPK based on soil type
    base_npk = {
        'clay': {'n': 100, 'p': 25, 'k': 120},
        'loam': {'n': 150, 'p': 40, 'k': 180},
        'sandy': {'n': 50, 'p': 10, 'k': 60},
        'black': {'n': 120, 'p': 30, 'k': 150},
        'red': {'n': 80, 'p': 20, 'k': 100},
    }
    npk = base_npk.get(soil_type, base_npk['loam'])
    
    # Calculate NDVI based on crop health (estimated)
    ndvi_mean = 0.6  # default moderate health
    
    # Calculate pest risk based on humidity, temperature, and crop sensitivity
    humidity_factor = humidity / 100
    temp_factor = (temperature - 15) / 30
    pest_risk_score = min(1.0, humidity_factor * 0.35 * crop_info['pestSensitivity'] + 
                         temp_factor * 0.25 + (1 - soil_info['nutrient']) * 0.2)
    
    # Calculate water need
    water_need_score = min(1.0, crop_info['waterNeed'] * (1 - soil_info['moisture']) * 0.6 + 
                           temp_factor * 0.25)
    
    return {
        'crop_type': crop_type,
        'soil_type': soil_type,
        'humidity': humidity,
        'temperature': temperature,
        'rainfall': rainfall,
        'soil_ph': soil_ph,
        'soil_moisture_pct': soil_moisture_pct,
        'volumetric_water_content': volumetric_water_content,
        'nitrogen_mgkg': npk['n'],
        'phosphorus_mgkg': npk['p'],
        'potassium_mgkg': npk['k'],
        'rainfall_30d_mm': rainfall_mm,
        'temp_mean_c': temperature,
        'humidity_mean_pct': humidity,
        'ndvi_mean': ndvi_mean,
        'pest_risk_score': pest_risk_score,
        'water_need_score': water_need_score,
    }

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/retrain', methods=['POST'])
def retrain():
    """Retrain model with current dataset and return new coefficients"""
    try:
        import pandas as pd
        from sklearn.linear_model import LinearRegression
        
        # Load dataset
        data = pd.read_csv('agrisim_dataset_multi_crop.csv')
        
        # Features and target
        features = ['soil_ph', 'soil_moisture_pct', 'humidity_pct', 'temperature_c', 
                   'nitrogen_mgkg', 'phosphorus_mgkg', 'potassium_mgkg', 
                   'pest_risk_score', 'water_need_score']
        X = data[features].values
        y = data['yield_prediction_t_ha'].values
        
        # Train linear regression
        model = LinearRegression()
        model.fit(X, y)
        
        # Extract coefficients
        new_coeff = np.concatenate([[model.intercept_], model.coef_])
        
        # Update global coefficient
        global coeff
        coeff = new_coeff
        
        # Calculate statistics
        predictions = model.predict(X)
        stats = {
            'num_samples': len(data),
            'mean_yield': float(y.mean()),
            'std_yield': float(y.std()),
            'min_yield': float(y.min()),
            'max_yield': float(y.max()),
            'mean_prediction': float(predictions.mean()),
            'safe_zones_pct': float(np.sum(predictions < 1.0) / len(predictions) * 100),
            'moderate_zones_pct': float(np.sum((predictions >= 1.0) & (predictions < 2.0)) / len(predictions) * 100),
            'high_yield_zones_pct': float(np.sum(predictions >= 2.0) / len(predictions) * 100),
        }
        
        return jsonify({
            'success': True,
            'coefficients': [float(c) for c in new_coeff],
            'statistics': stats,
            'message': f'Model retrained with {len(data)} samples'
        })
    except Exception as e:
        import traceback
        return jsonify({'success': False, 'error': str(e), 'trace': traceback.format_exc()}), 500

@app.route('/patterns', methods=['GET'])
def patterns():
    """Analyze dataset and return patterns and thresholds"""
    try:
        import pandas as pd
        
        # Load dataset
        data = pd.read_csv('agrisim_dataset_multi_crop.csv')
        
        # Analyze patterns by crop type if it exists
        patterns_data = {}
        if 'crop_type' in data.columns:
            for crop in data['crop_type'].unique():
                crop_data = data[data['crop_type'] == crop]
                patterns_data[crop] = {
                    'count': len(crop_data),
                    'avg_yield': float(crop_data['yield_prediction_t_ha'].mean()),
                    'yield_range': f"{crop_data['yield_prediction_t_ha'].min():.2f} - {crop_data['yield_prediction_t_ha'].max():.2f}",
                    'ideal_temp': f"{crop_data['temperature_c'].quantile(0.25):.1f} - {crop_data['temperature_c'].quantile(0.75):.1f}",
                    'ideal_moisture': f"{crop_data['soil_moisture_pct'].quantile(0.25):.1f} - {crop_data['soil_moisture_pct'].quantile(0.75):.1f}",
                    'ideal_humidity': f"{crop_data['humidity_pct'].quantile(0.25):.1f} - {crop_data['humidity_pct'].quantile(0.75):.1f}",
                }
        
        # Feature thresholds
        thresholds = {
            'soil_ph': {
                'critical_low': 4.5,
                'optimal_low': 6.0,
                'optimal_high': 8.0,
                'critical_high': 9.0,
                'current': {
                    'min': float(data['soil_ph'].min()),
                    'max': float(data['soil_ph'].max()),
                    'q1': float(data['soil_ph'].quantile(0.25)),
                    'q3': float(data['soil_ph'].quantile(0.75)),
                }
            },
            'soil_moisture_pct': {
                'critical_low': 20,
                'optimal_low': 40,
                'optimal_high': 70,
                'critical_high': 100,
                'current': {
                    'min': float(data['soil_moisture_pct'].min()),
                    'max': float(data['soil_moisture_pct'].max()),
                    'q1': float(data['soil_moisture_pct'].quantile(0.25)),
                    'q3': float(data['soil_moisture_pct'].quantile(0.75)),
                }
            },
            'temperature_c': {
                'critical_low': 5,
                'optimal_low': 20,
                'optimal_high': 35,
                'critical_high': 50,
                'current': {
                    'min': float(data['temperature_c'].min()),
                    'max': float(data['temperature_c'].max()),
                    'q1': float(data['temperature_c'].quantile(0.25)),
                    'q3': float(data['temperature_c'].quantile(0.75)),
                }
            },
            'pest_risk_score': {
                'low': 0.3,
                'moderate': 0.6,
                'high': 1.0,
                'current': {
                    'min': float(data['pest_risk_score'].min()),
                    'max': float(data['pest_risk_score'].max()),
                    'mean': float(data['pest_risk_score'].mean()),
                }
            },
        }
        
        # Model coefficients interpretation
        feature_names = ['soil_ph', 'soil_moisture_pct', 'humidity_pct', 'temperature_c', 
                        'nitrogen_mgkg', 'phosphorus_mgkg', 'potassium_mgkg', 
                        'pest_risk_score', 'water_need_score']
        coeff_importance = {}
        for i, fname in enumerate(feature_names):
            coeff_importance[fname] = {
                'coefficient': float(coeff[i+1]),
                'direction': 'positive' if coeff[i+1] > 0 else 'negative',
                'impact': 'increases yield' if coeff[i+1] > 0 else 'decreases yield'
            }
        
        return jsonify({
            'success': True,
            'crop_patterns': patterns_data,
            'feature_thresholds': thresholds,
            'model_coefficients': coeff_importance,
            'intercept': float(coeff[0]),
            'total_samples': len(data)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    # New features from multi-crop dataset
    features = [
        data.get('soil_ph', 6.5),
        data.get('soil_moisture_pct', 50),
        data.get('humidity_pct', 65),
        data.get('temperature_c', 28),
        data.get('nitrogen_mgkg', 150),
        data.get('phosphorus_mgkg', 40),
        data.get('potassium_mgkg', 180),
        data.get('pest_risk_score', 0.3),
        data.get('water_need_score', 0.4)
    ]
    # Add intercept
    features = [1] + features
    prediction = np.dot(coeff, features)
    return jsonify({'predicted_yield': max(0, prediction)})

@app.route('/parse_html', methods=['POST'])
def parse_html():
    """Parse HTML input and return extracted parameters"""
    try:
        html_content = request.json.get('html', '')
        if not html_content:
            return jsonify({'error': 'No HTML content provided'}), 400
        
        params = parse_html_input(html_content)
        
        # Calculate yield prediction
        features = [
            params['soil_ph'],
            params['soil_moisture_pct'],
            params['volumetric_water_content'],
            params['nitrogen_mgkg'],
            params['phosphorus_mgkg'],
            params['potassium_mgkg'],
            params['rainfall_30d_mm'],
            params['temp_mean_c'],
            params['humidity_mean_pct'],
            params['ndvi_mean'],
            params['pest_risk_score'],
            params['water_need_score']
        ]
        features = [1] + features
        predicted_yield = np.dot(coeff, features)
        
        return jsonify({
            'success': True,
            'parameters': params,
            'predicted_yield': float(predicted_yield),
            'digitalization': params,
            'visualization_data': {
                'crop_type': params['crop_type'],
                'soil_type': params['soil_type'],
                'humidity': params['humidity'],
                'temperature': params['temperature'],
                'rainfall': params['rainfall'],
                'yield': float(predicted_yield),
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("=" * 50)
    print("Starting Flask Server...")
    print("Server will be available at: http://localhost:5000")
    print("=" * 50)
    app.run(host='127.0.0.1', port=5000, debug=True)