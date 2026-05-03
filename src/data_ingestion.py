import kagglehub
from kagglehub import KaggleDatasetAdapter
import pandas as pd
import os

# Data Ingestion: Load raw data from Kaggle and save locally for preprocessing
def data_ingestion():
    print("Data ingestion start...")

    df = kagglehub.load_dataset(
        KaggleDatasetAdapter.PANDAS,
        "jeleeladekunlefijabi/ship-fuel-consumption-and-co2-emissions-analysis",
        "ship_fuel_efficiency.csv",
    )

    print(f"Data Loaded from Kaggle — Shape: {df.shape}")
    print(f"First 5 Records:\n{df.head()}")
    print(f"Null Values:\n{df.isnull().sum()}")
    print(f"Duplicated Rows: {df.duplicated().sum()}")

    os.makedirs("src/data/raw", exist_ok=True)
    df.to_csv("src/data/raw/ship_fuel_raw.csv", index=False)
    print("Raw data saved to src/data/raw/ship_fuel_raw.csv")


if __name__ == "__main__":
    data_ingestion()