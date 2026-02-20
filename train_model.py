import pandas as pd
import numpy as np
import joblib

# Load data
data = pd.read_csv('agrisim_dataset_multi_crop.csv')

# Features and target - match the new dataset columns
features = ['soil_ph', 'soil_moisture_pct', 'humidity_pct', 'temperature_c', 'nitrogen_mgkg', 'phosphorus_mgkg', 'potassium_mgkg', 'pest_risk_score', 'water_need_score']
X = data[features].values
y = data['yield_prediction_t_ha'].values

# Add intercept
X = np.column_stack([np.ones(X.shape[0]), X])

# Linear regression using least squares
coeff, residuals, rank, s = np.linalg.lstsq(X, y, rcond=None)
print(f'Coefficients: {coeff}')
print(f'Number of samples: {len(data)}')
print(f'Mean Yield: {y.mean():.4f}')
print(f'Std Yield: {y.std():.4f}')
print(f'Min Yield: {y.min():.4f}')
print(f'Max Yield: {y.max():.4f}')

# Save coefficients
joblib.dump(coeff, 'yield_model.pkl')
print('Model saved to yield_model.pkl')
joblib.dump(coeff, 'yield_model.pkl')
print('Model saved as yield_model.pkl')