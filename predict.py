import sys
import pickle
import pandas as pd
import numpy as np
import warnings

warnings.filterwarnings("ignore")

def predict():
    
    if len(sys.argv) < 9:
        sys.exit(1)

    try:
        
        model = pickle.load(open('car_model.pkl', 'rb'))
        le_map = pickle.load(open('encoders.pkl', 'rb'))

        
        brand_input = sys.argv[1]
        model_input = sys.argv[2]
        year_input  = int(sys.argv[3])
        km_input    = int(sys.argv[4])
        fuel_input  = sys.argv[5]
        seller_input= sys.argv[6]
        trans_input = sys.argv[7]
        owner_input = sys.argv[8]

        
        brand = le_map['brand'].transform([brand_input])[0]
        
        try:
            model_val = le_map['model'].transform([model_input])[0]
        except:
            
            model_val = le_map['model'].transform([le_map['model'].classes_[0]])[0]

        fuel   = le_map['fuel'].transform([fuel_input])[0]
        seller = le_map['seller_type'].transform([seller_input])[0]
        trans  = le_map['transmission'].transform([trans_input])[0]
        owner  = le_map['owner'].transform([owner_input])[0]

        feature_names = ['year', 'km_driven', 'fuel', 'seller_type', 'transmission', 'owner', 'brand', 'model']
        features = pd.DataFrame([[year_input, km_input, fuel, seller, trans, owner, brand, model_val]], 
                                columns=feature_names)

        prediction = model.predict(features)

        print(round(prediction[0], 2))

    except Exception as e:
        sys.exit(1)

if __name__ == "__main__":
    predict()