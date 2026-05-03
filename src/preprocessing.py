import pandas as pd
import scipy.sparse as sp
import pickle
import os
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
import yaml

# Params load 
params = yaml.safe_load(open("params.yaml")) 

# Preprocessing: Load raw data, transform features, and save processed data for training
def preprocessing():
    df = pd.read_csv("src/data/raw/ship_fuel_raw.csv")
    print(f"Data Loaded — Shape: {df.shape}")

    df = df.drop(columns=['ship_id', 'route_id', 'CO2_emissions'])
    print(f"Columns after drop: {list(df.columns)}")

    x = df.drop(columns=['fuel_consumption'])
    y = df['fuel_consumption']
    print(f"Features: {x.shape} | Target: {y.shape}")

    categorical_cols = ["ship_type", "month", "fuel_type", "weather_conditions"]
    numeric_cols = ["distance", "engine_efficiency"]

    preprocessor = ColumnTransformer([
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_cols),
        ("num", StandardScaler(), numeric_cols)
    ])

    x = preprocessor.fit_transform(x)
    print(f"After preprocessing — Shape: {x.shape}")

    # x_train, x_test, y_train, y_test = train_test_split(
    #     x, y, test_size=0.2, random_state=42
    # )

    # Train-test split using params from params.yaml
    x_train, x_test, y_train, y_test = train_test_split(
        #x,y, test_size=0.2, random_state=42
        x, y, test_size=params["data"]["test_size"], random_state=params["data"]["random_state"]
    )
    print(f"Train: {x_train.shape} | Test: {x_test.shape}")

    # Processed data save 
    os.makedirs("src/data/processed", exist_ok=True)

    # Save sparse matrices in .npz format and target variable in .csv
    sp.save_npz("src/data/processed/x_train.npz", x_train)
    sp.save_npz("src/data/processed/x_test.npz", x_test)
    y_train.to_csv("src/data/processed/y_train.csv", index=False)
    y_test.to_csv("src/data/processed/y_test.csv", index=False)

    # Preprocessor save to pkl 
    os.makedirs("src/models", exist_ok=True)
    with open("src/models/preprocessor.pkl", "wb") as f:
        pickle.dump(preprocessor, f)

    print("Processed data saved to src/data/processed/")
    print("Preprocessor saved to src/models/preprocessor.pkl")


if __name__ == "__main__":
    preprocessing()