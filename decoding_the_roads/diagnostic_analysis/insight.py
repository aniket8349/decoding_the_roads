import pandas as pd

df = pd.read_csv("data/raw/global_traffic_accidents.csv")

def generate_insights_and_recommendations(df: pd.DataFrame):


    print("\n=== Key Insights ===")

    # 1. Identify Peak Accident Times
    if "Hour" in df.columns:
        peak_hours = df["Hour"].value_counts().nlargest(3)
        print(f"\n High-Risk Time Periods: Most accidents occur during {list(peak_hours.index)} hours.")

    # 2. Identify High-Risk Locations
    if "Location" in df.columns:
        top_locations = df["Location"].value_counts().nlargest(3)
        print("\n High-Risk Locations:")
        for location, count in top_locations.items():
            print(f"- {location}: {count} accidents")

    # 3. Impact of Weather Conditions
    if "Weather Condition" in df.columns:
        weather_impact = df.groupby("Weather Condition")["Casualties"].sum().sort_values(ascending=False)
        worst_weather = weather_impact.index[0]
        print(f"\n Weather Impact: Highest casualties occur during '{worst_weather}' conditions.")

    # 4. Accident Severity Distribution
    if "Accident Severity" in df.columns:
        severity_counts = df["Accident Severity"].value_counts()
        print("\n Accident Severity Distribution:")
        for severity, count in severity_counts.items():
            print(f"- {severity}: {count} cases")

    # 5. Vehicle Involvement
    if "Vehicle Type" in df.columns:
        vehicle_involvement = df["Vehicle Type"].value_counts().nlargest(3)
        print("\n Vehicle Types Most Involved in Accidents:")
        for vehicle, count in vehicle_involvement.items():
            print(f"- {vehicle}: {count} accidents")

    print("\n=== Actionable Recommendations ===")

    # 1. Time-Based Interventions
    print("\n **Time-Based Recommendations:**")
    print("- Increase police patrols and traffic monitoring during peak accident hours.")
    print("- Implement speed checks and red-light cameras during high-risk times.")

    # 2. Location-Based Safety Measures
    print("\n **Location-Based Safety Measures:**")
    print("- Improve street lighting and signage in high-risk areas.")
    print("- Introduce speed bumps or stricter traffic rules in accident-prone zones.")

    # 3. Weather-Specific Safety Measures
    print("\n **Weather-Specific Strategies:**")
    print("- Deploy real-time weather alerts to drivers during hazardous conditions.")
    print("- Improve road drainage and maintenance in areas prone to rain or fog-related accidents.")

    # 4. Vehicle Safety Regulations
    print("\n **Vehicle Safety Improvements:**")
    print("- Enforce stricter vehicle safety inspections, especially for high-risk vehicle types.")
    print("- Promote advanced braking and collision avoidance systems in vehicles.")

    # 5. Public Awareness Campaigns
    print("\n **Public Awareness Initiatives:**")
    print("- Launch driver education programs focusing on high-risk behaviors.")
    print("- Encourage responsible driving habits through awareness campaigns.")

    print("\n **Conclusion:**")
    print("By implementing these recommendations, authorities can significantly reduce traffic accident risks and improve road safety.")

if __name__ == "__main__":
    result = generate_insights_and_recommendations(df)