import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

def predict_accident_severity(csv_file: str):
    """
    Predicts accident severity using a Random Forest model based on given historical accident data.

    :param csv_file: Path to the CSV file containing accident data.
    :return: Prints model accuracy and allows user input for predictions.
    """
    # Load dataset
    df = pd.read_csv("data/raw/global_traffic_accidents.csv")

    # Display dataset columns for debugging
    print("Dataset Columns:", df.columns.tolist())

    # Ensure correct feature names
    features = ["Weather Condition", "Road Condition", "Time", "Vehicles Involved"]
    target = "Accident_Severity"

    # Check if all required columns exist
    missing_features = [col for col in features if col not in df.columns]
    if missing_features:
        print(f"Error: Missing columns in dataset: {missing_features}")
        return

    # Convert categorical data to numerical values
    df = pd.get_dummies(df, columns=["Weather Condition", "Road Condition"], drop_first=True)

    # Handle missing values (fill with mode for categorical, median for numerical)
    df.fillna(df.median(numeric_only=True), inplace=True)

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
    input_data = pd.DataFrame([[weather, road, time, vehicles]], columns=["Weather Condition", "Road Condition", "Time", "Vehicles Involved"])
    input_data = pd.get_dummies(input_data, columns=["Weather Condition", "Road Condition"], drop_first=True)

    # Ensure input data matches training features
    for col in df.columns:
        if col not in input_data.columns and col != target:
            input_data[col] = 0  # Add missing columns with default value 0

    # Predict accident severity
    prediction = model.predict(input_data)
    print(f"\nPredicted Accident Severity: {prediction[0]}")

# Run the function if script is executed in terminal
if __name__ == "__main__":
    csv_path = input("Enter path to accident data CSV file: ")
    predict_accident_severity(csv_path)
