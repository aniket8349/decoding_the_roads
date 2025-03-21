import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
import os

def predict_casualties(csv_file):
    #  Check if file exists
    if not os.path.exists(csv_file):
        print("Error: File not found. Please provide the correct path.")
        return

    #  Load dataset
    df = pd.read_csv(csv_file)

    #  Normalize column names
    df.columns = df.columns.str.lower().str.replace(" ", "_")
    print("\nCleaned Dataset Columns:", list(df.columns))

    #  Drop non-relevant columns
    drop_cols = ["accident_id", "date", "time", "location", "latitude", "longitude", "cause"]
    df = df.drop(columns=[col for col in drop_cols if col in df.columns], errors="ignore")

    #  Handle categorical variables
    label_encoders = {}
    for col in ["weather_condition", "road_condition"]:
        if col in df.columns:
            le = LabelEncoder()
            df[col] = le.fit_transform(df[col])
            label_encoders[col] = le

    #  Split into training and test sets
    X = df.drop(columns=["casualties"])
    y = df["casualties"]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    #  Train model using Gradient Boosting Regressor
    model = GradientBoostingRegressor(n_estimators=200, learning_rate=0.1, max_depth=5, random_state=42)
    model.fit(X_train, y_train)

    #  Evaluate model
    y_pred = model.predict(X_test)
    print("\nModel Performance:")
    print("MAE:", round(mean_absolute_error(y_test, y_pred), 2))
    print("MSE:", round(mean_squared_error(y_test, y_pred), 2))

    #  Take user input
    print("\nEnter details to predict casualties:")
    weather = input("Weather Condition (e.g., Clear, Rain, Fog): ").strip().lower()
    road = input("Road Condition (e.g., Dry, Wet, Icy): ").strip().lower()
    vehicles = input("Number of Vehicles Involved (Press Enter to skip): ").strip()

    #  Process inputs
    input_data = {}

    # Convert categorical inputs using LabelEncoders
    if "weather_condition" in label_encoders and weather in label_encoders["weather_condition"].classes_:
        input_data["weather_condition"] = label_encoders["weather_condition"].transform([weather])[0]
    else:
        print("Warning: Unknown weather condition, using default.")
        input_data["weather_condition"] = 0

    if "road_condition" in label_encoders and road in label_encoders["road_condition"].classes_:
        input_data["road_condition"] = label_encoders["road_condition"].transform([road])[0]
    else:
        print("Warning: Unknown road condition, using default.")
        input_data["road_condition"] = 0

    if vehicles.isdigit():
        input_data["vehicles_involved"] = int(vehicles)
    elif "vehicles_involved" in df.columns:
        input_data["vehicles_involved"] = int(df["vehicles_involved"].median())

    # Convert to DataFrame
    input_df = pd.DataFrame([input_data])

    #  Predict casualties
    prediction = model.predict(input_df)[0]
    print("\nPredicted Casualties:", round(prediction))

#  Run the script
if __name__ == "__main__":
    csv_path = input("Enter path to accident data CSV file: ").strip()
    predict_casualties(csv_path)
