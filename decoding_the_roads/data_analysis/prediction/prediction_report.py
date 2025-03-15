import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error

def predict_casualties(csv_file: str):
    """
    Predicts the number of casualties using a Random Forest model based on accident data.

    :param csv_file: Path to the CSV file containing accident data.
    """
    # Load dataset
    df = pd.read_csv(csv_file)

    # Display dataset columns for debugging
    print("Dataset Columns:", df.columns.tolist())

    # Define features and target variable
    features = ["Weather Condition", "Road Condition", "Time", "Vehicles Involved"]
    target = "Casualties"

    # Check if all required columns exist
    missing_features = [col for col in features if col not in df.columns]
    if missing_features:
        print(f"Error: Missing columns in dataset: {missing_features}")
        return

    # Handle missing values (fill with mode for categorical, median for numerical)
    df.fillna(df.median(numeric_only=True), inplace=True)

    # Convert categorical features to numerical using one-hot encoding
    df = pd.get_dummies(df, columns=["Weather Condition", "Road Condition"], drop_first=True)

    # Splitting data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(df[features], df[target], test_size=0.2, random_state=42)

    # Train the Random Forest model
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Evaluate model performance
    y_pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)

    print(f"\nModel Performance:")
    print(f"Mean Absolute Error (MAE): {mae:.2f}")
    print(f"Mean Squared Error (MSE): {mse:.2f}")

    # Interactive Prediction
    print("\nEnter details to predict casualties:")
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

    # Predict casualties
    prediction = model.predict(input_data)
    print(f"\nPredicted Casualties: {round(prediction[0])}")

# Run the function if script is executed in terminal
if __name__ == "__main__":
    csv_path = input("Enter path to accident data CSV file: ")
    predict_casualties(csv_path)
