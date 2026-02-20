import joblib
import numpy as np

# Load the newly trained model
coeff = joblib.load('yield_model.pkl')
print('='*60)
print('NEW TRAINED MODEL RESULTS')
print('='*60)
print('\nTrained Coefficients:', coeff)
print('Number of coefficients:', len(coeff))
print('\nIntercept:', coeff[0])
print('Feature Coefficients:', coeff[1:])
print('\nDataset: agrisim_dataset_multi_crop.csv')
print('Features: soil_ph, soil_moisture_pct, humidity_pct, temperature_c,')
print('          nitrogen_mgkg, phosphorus_mgkg, potassium_mgkg,')
print('          pest_risk_score, water_need_score')
print('='*60)
print()

# Test predictions with new feature set (9 features + 1 intercept = 10 total)
test_cases = [
    {
        'name': 'Test 1: Loamy soil, normal conditions',
        'features': [6.5, 40, 60, 25, 150, 40, 180, 0.15, 0.15]
    },
    {
        'name': 'Test 2: Clay soil, high humidity, high temp',
        'features': [7.0, 50, 80, 32, 130, 35, 170, 0.5, 0.6]
    },
    {
        'name': 'Test 3: Sandy soil, low moisture, low temp',
        'features': [5.5, 30, 45, 18, 75, 20, 90, 0.2, 0.3]
    },
    {
        'name': 'Test 4: Optimal conditions',
        'features': [6.8, 55, 70, 28, 160, 45, 200, 0.1, 0.2]
    }
]

for test in test_cases:
    features = [1] + test['features']
    prediction = np.dot(coeff, features)
    prediction = max(0, prediction)
    print(test['name'])
    print('  Features: soil_pH={}, moisture={}%, humidity={}%, temp={}C'.format(
        test['features'][0], test['features'][1], test['features'][2], test['features'][3]))
    print('  NPK: N={}, P={}, K={}'.format(
        test['features'][4], test['features'][5], test['features'][6]))
    print('  Risk: pest={}, water={}'.format(
        test['features'][7], test['features'][8]))
    print('  PREDICTION: {:.4f} t/ha'.format(prediction))
    print()

print('='*60)
print('Model successfully trained and loaded!')
print('='*60)
