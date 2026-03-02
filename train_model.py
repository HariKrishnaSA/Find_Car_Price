import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.preprocessing import LabelEncoder
import pickle
import os


file_path = 'CAR DATASET.csv'

if not os.path.exists(file_path):
    print(f"Error: {file_path} not found. Please check the file location.")
else:
    df = pd.read_csv(file_path)


    df['brand'] = df['name'].apply(lambda x: x.split(' ')[0])
    df['model'] = df['name'].apply(lambda x: x.split(' ')[1] if len(x.split(' ')) > 1 else 'Generic')


    le_map = {}
    categorical_cols = ['brand', 'model', 'fuel', 'seller_type', 'transmission', 'owner']

    for col in categorical_cols:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
        le_map[col] = le  


    X = df[['year', 'km_driven', 'fuel', 'seller_type', 'transmission', 'owner', 'brand', 'model']]
    y = df['selling_price']


    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    print("Training the AI Brain (Version 2.0 with Models)...")
    model = GradientBoostingRegressor(n_estimators=100, learning_rate=0.1, max_depth=5)
    model.fit(X_train, y_train)

    pickle.dump(model, open('car_model.pkl', 'wb'))
    pickle.dump(le_map, open('encoders.pkl', 'wb'))

    print("-" * 30)
    print("SUCCESS: Model saved as car_model.pkl")
    print("SUCCESS: Encoders saved as encoders.pkl")
    print("-" * 30)
    print("You can now run 'node server.js' to start your website.")