import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

def predict_accident_severity(csv_path: str):
    """
    Predicts accident severity using a Random Forest model based on given historical accident data.

    :param csv_path: Path to the CSV file containing accident data.
    :return: Prints model accuracy and allows user input for predictions.
    """
    # Load dataset from the provided path
    df = pd.read_csv(csv_path)

    # Print column names to verify correctness
    print("Dataset Columns:", list(df.columns))

    # Ensure column names match exactly
    features = ["Weather Condition", "Road Condition", "Time", "Vehicles Involved"]
    target = "Accident_Severity"

    # Convert categorical data to numerical values
    df = pd.get_dummies(df, columns=["Weather Condition", "Road Condition"], drop_first=True)

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(df[features], df[target], test_size=0.2, random_state=42)

    # Train the Random Forest model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Evaluate model accuracy
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Model Accuracy: {accuracy:.2f}")

    # Interactive Prediction
    print("\nEnter details to predict accident severity:")
    weather = input("Weather Condition (e.g., Clear, Rain, Fog): ")
    road = input("Road Condition (e.g., Dry, Wet, Icy): ")
    time = int(input("Time (24-hour format, e.g., 15 for 3 PM): "))
    vehicles = int(input("Number of Vehicles Involved: "))

    # Create input DataFrame
    input_data = pd.DataFrame([[weather, road, time, vehicles]], columns=features)
    input_data = pd.get_dummies(input_data, columns=["Weather Condition", "Road Condition"], drop_first=True)

    # Ensure input data matches training features
    missing_cols = set(df.columns) - set(input_data.columns) - {target}
    for col in missing_cols:
        input_data[col] = 0  # Add missing columns with default value 0

    # Predict accident severity
    prediction = model.predict(input_data)
    print(f"\nPredicted Accident Severity: {prediction[0]}")

# Run the function if script is executed in terminal
# if __name__ == "__main__":
#     csv_path = "data/raw/global_traffic_accidents.csv"  # Ask user for path
#     predict_accident_severity(csv_path)  # Pass the path to the function
