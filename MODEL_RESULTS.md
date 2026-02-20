# MODEL TRAINING RESULTS - Multi-Crop Dataset

## Dataset Information
- **Dataset File**: agrisim_dataset_multi_crop.csv
- **Total Samples**: 1,350 records
- **Crop Types**: Rice, Wheat, Cotton, Sugarcane, Maize, Groundnut
- **Features**: 9 input features

## Feature Set
1. **soil_ph** - Soil acidity level (range: ~5.5-7.5)
2. **soil_moisture_pct** - Soil water content percentage (range: 30-56%)
3. **humidity_pct** - Atmospheric humidity (range: ~45-95%)
4. **temperature_c** - Mean temperature (range: ~15-45°C)
5. **nitrogen_mgkg** - Nitrogen nutrient level (range: 50-175 mg/kg)
6. **phosphorus_mgkg** - Phosphorus nutrient level (range: 10-55 mg/kg)
7. **potassium_mgkg** - Potassium nutrient level (range: 60-295 mg/kg)
8. **pest_risk_score** - Pest infestation probability (range: 0-1)
9. **water_need_score** - Irrigation requirement score (range: 0-1)

## Target Variable
- **yield_prediction_t_ha** - Predicted yield in tons per hectare
  - Mean: 0.5411 t/ha
  - Std Dev: 0.0894 t/ha
  - Min: 0.5000 t/ha
  - Max: 1.0330 t/ha

## Trained Model Coefficients

### Intercept
```
1.2159874987013832
```

### Feature Coefficients
```
soil_ph:              -0.00407791384
soil_moisture_pct:     0.00172452039
humidity_pct:          0.00859190553
temperature_c:         0.01957344950
nitrogen_mgkg:         0.00035883871
phosphorus_mgkg:       0.00193363152
potassium_mgkg:        0.00024593919
pest_risk_score:      -2.36554394
water_need_score:     -1.07795321
```

## Model Architecture
- **Algorithm**: Linear Regression (Least Squares)
- **Total Coefficients**: 10 (1 intercept + 9 features)
- **Prediction Formula**: 
  ```
  yield = 1.2160 
          - 0.0041*soil_ph 
          + 0.0017*soil_moisture 
          + 0.0086*humidity 
          + 0.0196*temperature 
          + 0.0004*nitrogen 
          + 0.0019*phosphorus 
          + 0.0002*potassium 
          - 2.3655*pest_risk 
          - 1.0780*water_need
  ```

## Test Predictions

### Scenario 1: Normal Conditions (Loamy Soil)
- Soil pH: 6.5, Moisture: 40%, Humidity: 60%, Temp: 25°C
- NPK: 150/40/180, Pest Risk: 0.15, Water Need: 0.15
- **Predicted Yield: 1.9222 t/ha**

### Scenario 2: Adverse Conditions (Clay Soil - High Risk)
- Soil pH: 7.0, Moisture: 50%, Humidity: 80%, Temp: 32°C
- NPK: 130/35/170, Pest Risk: 0.5, Water Need: 0.6
- **Predicted Yield: 0.9140 t/ha** ⚠️ Lower due to high risks

### Scenario 3: Poor Conditions (Sandy Soil)
- Soil pH: 5.5, Moisture: 30%, Humidity: 45%, Temp: 18°C
- NPK: 75/20/90, Pest Risk: 0.2, Water Need: 0.3
- **Predicted Yield: 1.2755 t/ha**

### Scenario 4: Optimal Conditions
- Soil pH: 6.8, Moisture: 55%, Humidity: 70%, Temp: 28°C
- NPK: 160/45/200, Pest Risk: 0.1, Water Need: 0.2
- **Predicted Yield: 2.1741 t/ha** 🌾 Optimal

## Key Insights

1. **Pest Risk Impact**: Strong negative coefficient (-2.37) indicates high pest risk significantly reduces yield
2. **Water Need Impact**: Water stress has strong negative effect (-1.08) on productivity
3. **Temperature**: Positive coefficient (0.0196) shows moderate temperature importance
4. **Humidity**: Slightly positive (0.0086), important for moisture regulation
5. **Nutrients**: NPK coefficients are small but positive, showing consistent benefit

## Model Files Generated
- `yield_model.pkl` - Serialized model coefficients
- `train_model.py` - Training script with new dataset
- `test_model.py` - Test predictions script

## Status
✅ Model successfully trained
✅ Coefficients saved to yield_model.pkl
✅ Flask backend updated with new coefficients
✅ Ready for production deployment

---
**Training Date**: February 20, 2026
**Dataset**: agrisim_dataset_multi_crop.csv (1,350 samples)
