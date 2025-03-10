import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv("data/raw/global_traffic_accidents.csv")
#root_cause_comparative_analysis(df)


def root_cause_comparative_analysis(df: pd.DataFrame):


    # 1. Identify High-Risk Locations
    high_risk_locations = df["Location"].value_counts().head(10)
    print("Top 10 High-Risk Locations:\n", high_risk_locations)

    plt.figure(figsize=(10, 5))
    sns.barplot(x=high_risk_locations.values, y=high_risk_locations.index, palette="Reds_r")
    plt.xlabel("Number of Accidents")
    plt.ylabel("Location")
    plt.title("Top 10 High-Risk Locations for Accidents")
    plt.grid(axis="x", linestyle="--", alpha=0.7)
    plt.show()

    # 2. Identify High-Risk Weather Conditions
    high_risk_weather = df["Weather Condition"].value_counts()
    print("\nAccidents by Weather Condition:\n", high_risk_weather)

    plt.figure(figsize=(10, 5))
    sns.barplot(x=high_risk_weather.values, y=high_risk_weather.index, palette="coolwarm")
    plt.xlabel("Number of Accidents")
    plt.ylabel("Weather Condition")
    plt.title("Accidents by Weather Condition")
    plt.grid(axis="x", linestyle="--", alpha=0.7)
    plt.show()

    # 3. Identify High-Risk Time Periods
    if "Hour" not in df.columns:
        df["Hour"] = pd.to_datetime(df["Time"], errors="coerce").dt.hour

    high_risk_hours = df["Hour"].value_counts().sort_index()
    print("\nAccidents by Time of Day:\n", high_risk_hours)

    plt.figure(figsize=(12, 5))
    sns.lineplot(x=high_risk_hours.index, y=high_risk_hours.values, marker="o", color="blue")
    plt.xlabel("Hour of the Day")
    plt.ylabel("Number of Accidents")
    plt.title("Accidents by Time of Day")
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.xticks(range(0, 24))
    plt.show()

    # 4. Compare Accident Rates Based on Severity & Location
    plt.figure(figsize=(12, 6))
    sns.boxplot(x="Accident Severity", y="Casualties", data=df, palette="muted")
    plt.xlabel("Accident Severity")
    plt.ylabel("Number of Casualties")
    plt.title("Casualties by Accident Severity")
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.show()

    return("\nRoot Cause & Comparative Analysis Completed.")


if __name__ == "__main__":
    result = root_cause_comparative_analysis(df)