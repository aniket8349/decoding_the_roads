import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split

# Load Dataset
df = pd.read_csv("gloabal_traffic_accidentss.csv")

# Step 1: Handle Missing Values
for col in df.select_dtypes(include=[np.number]):  # Numerical Columns
    df[col].fillna(df[col].median(), inplace=True)

for col in df.select_dtypes(include=[object]):  # Categorical Columns
    df[col].fillna(df[col].mode()[0], inplace=True)

# Step 2: Convert Data Types
df['Date'] = pd.to_datetime(df['Date'])
df['Time'] = pd.to_datetime(df['Time'], format='%H:%M:%S').dt.time

# Step 3: Feature Engineering (Extracting Useful Information)
df['Year'] = df['Date'].dt.year
df['Month'] = df['Date'].dt.month
df['Day'] = df['Date'].dt.day
df['Weekday'] = df['Date'].dt.weekday

df['Hour'] = pd.to_datetime(df['Time'], format='%H:%M:%S').dt.hour

# Define Time Periods
def time_period(hour):
    if 5 <= hour < 12:
        return 'Morning'
    elif 12 <= hour < 17:
        return 'Afternoon'
    elif 17 <= hour < 21:
        return 'Evening'
    else:
        return 'Night'

df['Time Period'] = df['Hour'].apply(time_period)

# Step 4: Encode Categorical Variables
label_encoders = {}
for col in df.select_dtypes(include=[object]):  # Encoding Categorical Data
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    label_encoders[col] = le  # Store encoder for inverse transform if needed

# Step 5: Detect & Remove Outliers using IQR
numerical_cols = df.select_dtypes(include=[np.number]).columns
Q1 = df[numerical_cols].quantile(0.25)
Q3 = df[numerical_cols].quantile(0.75)
IQR = Q3 - Q1

df = df[~((df[numerical_cols] < (Q1 - 1.5 * IQR)) | (df[numerical_cols] > (Q3 + 1.5 * IQR))).any(axis=1)]

# Step 6: Normalize or Standardize Data
scaler = StandardScaler()
df[numerical_cols] = scaler.fit_transform(df[numerical_cols])

# Step 7: Split Data into Train & Test Sets
train_df, test_df = train_test_split(df, test_size=0.2, random_state=42)

# ✅ Final Processed Data
print("Train Data Shape:", train_df.shape)
print("Test Data Shape:", test_df.shape)
