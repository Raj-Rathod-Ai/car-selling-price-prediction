import os
import pickle
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder

# Load dataset to dynamically fit encoders to match training exactly
CSV_PATH = os.path.join(os.path.dirname(__file__), 'cardekho_data (1).csv')
if os.path.exists(CSV_PATH):
    df_car = pd.read_csv(CSV_PATH)
    CAR_NAMES = sorted(df_car['Car_Name'].unique().tolist())
else:
    raise FileNotFoundError(f"Dataset cardekho_data (1).csv not found at {CSV_PATH}")

# Fit LabelEncoder for Car_Name dynamically
le_car = LabelEncoder()
le_car.fit(df_car['Car_Name'])

# Other mappings used during training (alphabetical order check)
# Fuel_Type: CNG -> 0, Diesel -> 1, Petrol -> 2
FUEL_MAPPING = {'CNG': 0, 'Diesel': 1, 'Petrol': 2}

# Seller_Type: Dealer -> 0, Individual -> 1
SELLER_MAPPING = {'Dealer': 0, 'Individual': 1}

# Transmission: Automatic -> 0, Manual -> 1
TRANSMISSION_MAPPING = {'Automatic': 0, 'Manual': 1}

DEFAULTS = {
    'Present_Price': 6.4,  # Lakhs
    'Kms_Driven': 32000,
    'Owner': 0,
    'Year': 2014
}

MODEL_PATH = os.path.join(os.path.dirname(__file__), 'best_model.pkl')

def load_model():
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"Model file not found at {MODEL_PATH}")
    with open(MODEL_PATH, 'rb') as f:
        model = pickle.load(f)
    return model

def predict_selling_price(car_name, year, present_price, kms_driven, fuel_type, seller_type, transmission, owner):
    """
    Predict selling price for the car.
    Inputs are user-friendly strings/numbers and get encoded to the expected format.
    """
    model = load_model()
    
    # 1. Encode Car_Name using the fitted LabelEncoder
    encoded_car = int(le_car.transform([car_name])[0])
    
    # 2. Encode Fuel_Type
    encoded_fuel = FUEL_MAPPING.get(fuel_type, FUEL_MAPPING['Petrol'])
    
    # 3. Encode Seller_Type
    encoded_seller = SELLER_MAPPING.get(seller_type, SELLER_MAPPING['Individual'])
    
    # 4. Encode Transmission
    encoded_trans = TRANSMISSION_MAPPING.get(transmission, TRANSMISSION_MAPPING['Manual'])
    
    # 5. Handle numeric fallbacks
    val_price = present_price if present_price is not None else DEFAULTS['Present_Price']
    val_kms = kms_driven if kms_driven is not None else DEFAULTS['Kms_Driven']
    val_year = year if year is not None else DEFAULTS['Year']
    val_owner = owner if owner is not None else DEFAULTS['Owner']
    
    # Create DataFrame matching model feature names
    # Features order in model: ['Car_Name', 'Year', 'Present_Price', 'Kms_Driven', 'Fuel_Type', 'Seller_Type', 'Transmission', 'Owner']
    features_df = pd.DataFrame([{
        'Car_Name': encoded_car,
        'Year': int(val_year),
        'Present_Price': float(val_price),
        'Kms_Driven': float(val_kms),
        'Fuel_Type': encoded_fuel,
        'Seller_Type': encoded_seller,
        'Transmission': encoded_trans,
        'Owner': int(val_owner)
    }])
    
    prediction = model.predict(features_df)
    return float(prediction[0])
