# -*- coding: utf-8 -*-
"""
Created on Sun Mar  3 12:05:45 2024

@author: X1 Carbon Gen 7
"""

import pandas as pd
import matplotlib.pyplot as plt

# Load the data
data = pd.read_csv("tiki_test.csv")

data.info()

# Check for missing values
print("Missing values summary:")
print(data.isnull().sum())

# Handle missing values
# You can choose one of the following approaches:

# Option 1: Drop rows with missing values
# Uncomment the following line if you decide to go with this approach
# data.dropna(inplace=True)

# Option 2: Impute missing values with mean/median
# For example, to impute missing values in Sign-up Time with the median
data["Sign-up Time"] = data["Sign-up Time"].fillna(pd.to_datetime("2100-01-01"))

# You can repeat the imputation for other columns with missing values using the appropriate column name and imputation strategy (mean or median)

# Check for outliers using boxplots
print("Outliers analysis:")
data.plot(kind='box')
plt.show()

# You can also use IQR (Interquartile Range) to identify outliers
# This step is optional, but it can help you decide how to handle outliers

# Handle outliers (consider if outliers are a small percentage)
# You can choose one of the following approaches:

# Option 1: Winsorize outliers (capping them to specific percentiles)
# This is a more conservative approach than removing outliers entirely

# Option 2: Remove outliers (if they are a very small percentage of the data)
# Use techniques like IQR to identify outliers and then remove them if they represent a small fraction of the data

# Choose the approach that best suits your data and analysis goals

# Note: Make sure to save the cleaned data to a new DataFrame or overwrite the original one (if suitable) after handling missing values and outliers.


# =============================================================================
#  Data Processing
# =============================================================================

# Ensure Sign-up Time and Activation Time are datetime format
data["Sign-up Time"] = pd.to_datetime(data["Sign-up Time"])
data["Activation Time"] = pd.to_datetime(data["Activation Time"])
data["1st Listing"] = pd.to_datetime(data["1st Listing"])
data["1st Salable"] = pd.to_datetime(data["1st Salable"])

# Calculate time differences between stages (assuming these columns exist)
data['Time to Activation'] = data['Activation Time'] - data['Sign-up Time']
data['Time to Listing'] = data['1st Listing'].fillna(pd.to_datetime("2100-01-01")) - data['Sign-up Time']  # Handle missing values with a far future date
data['Time to 1st Sale'] = data['1st Salable'].fillna(pd.to_datetime("2100-01-01")) - data['Sign-up Time']  # Handle missing values with a far future date

# data.replace({'NaT': '0 day'}, inplace=True)

# Create a new feature indicating active sellers (having a transaction)
data['is_active'] = data['1st Salable'].notnull()

# Note: Remember to replace '1st Listing' and '1st Salable' with the actual column names in your data if they are different

# Keep the cleaned data frame

# =============================================================================
# Data Aggregation
# =============================================================================

# Group data by Seller's Vertical and calculate statistics for time differences
grouped_data = data.groupby('Seller\'s Vertical')['Time to Activation', 'Time to Listing', 'Time to 1st Sale'].agg(['mean', 'median'])

# Display the aggregated data
print(grouped_data)


# =============================================================================
# Data Visualization
# =============================================================================

# data['Time to Listing'] = pd.to_timedelta(data['Time to Listing'])
# data['Time to 1st Sale'] = pd.to_timedelta(data['Time to 1st Sale'])
# data.replace({pd.NaT: "0 days"}, inplace=True)
# data.fillna(0)

# data['Time to Listing'] = data['Time to Listing'].fillna(pd.Timedelta(seconds=0))
# data['Time to 1st Sale'] = data['Time to 1st Sale'].fillna(pd.Timedelta(seconds=0))

# Bar chart for average time to different stages
plt.figure(figsize=(10, 6))  # Adjust figure size as needed
data.groupby('is_active')['Time to Listing', 'Time to 1st Sale'].mean().astype('timedelta64[D]').plot(kind='bar', color=['skyblue', 'lightgreen'])
plt.xlabel("Seller Status")
plt.ylabel("Average Time (days)")
plt.title("Average Time to Listing and 1st Sale by Seller Status")
plt.xticks(rotation=0)  # Rotate x-axis labels for better readability
plt.tight_layout()
plt.show()

# Boxplots for time distribution by Seller's Vertical
plt.figure(figsize=(12, 6))  # Adjust figure size as needed

data['Time to Activation 2'] = data['Time to Activation'].dt.days.astype('int16')
data['Time to Listing 2'] = data['Time to Listing'].dt.days.astype('int16')
data['Time to 1st Sale 2'] = data['Time to 1st Sale'].dt.days.astype('int16')



data.boxplot(by='Seller\'s Vertical', column=['Time to Activation 2', 'Time to Listing 2', 'Time to 1st Sale 2'], notch=True)
plt.xlabel("Seller's Vertical")
plt.ylabel("Time (days)")
plt.title("Distribution of Time to Different Stages by Seller's Vertical")
plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for better readability
plt.tight_layout()
plt.show()

# Scatter plot (optional): Time to 1st Sale vs. Number of Listings (assuming you have a 'Number of Listings' column)
# You can uncomment and adjust the code below if this analysis is relevant
# plt.figure(figsize=(8, 6))  # Adjust figure size as needed
# plt.scatter(data['Number of Listings'], data['Time to 1st Sale'])
# plt.xlabel("Number of Listings")
# plt.ylabel("Time to 1st Sale (days)")
# plt.title("Time to 1st Sale vs. Number of Listings")
# plt.tight_layout()
# plt.show()


# =============================================================================
# 
# =============================================================================
from statsmodels.tsa.seasonal import seasonal_decompose  # for time series decomposition

# 1. Seller Activity Over Time (Time Series Analysis)
# Assuming you have a 'Sign-up Time' column with datetime format
monthly_data = data.resample('M', on='Sign-up Time')['Seller ID'].count()  # Count sellers by month

# decomposition = seasonal_decompose(monthly_data, model='additive')
# plt.figure(figsize=(12, 6))
# decomposition.plot()
# plt.title("Seasonal Decomposition of Monthly Seller Signups")
# plt.show()

# You can repeat this for other events (activation, listing, etc.)

# 2. Conversion Rates
# Assuming 'Activation Time' and '1st Listing' are datetime format
activated_sellers = len(data.dropna(subset=['Activation Time']))
listed_sellers = len(data.dropna(subset=['1st Listing']))
total_sellers = len(data)

activation_rate = (activated_sellers / total_sellers) * 100
listing_rate = ((listed_sellers - activated_sellers) / activated_sellers) * 100  # Assuming all activated sellers eventually list

print(f"Activation Rate: {activation_rate:.2f}%")
print(f"Listing Rate: {listing_rate:.2f}%")

# You can calculate similar rates for other stages

# 3. Impact of Seller Characteristics (replace 'Location' with your actual column name)
location_data = data.groupby('Location')['Time to 1st Sale'].agg(['mean', 'median'])
print(location_data)

# Explore similar analysis for other seller characteristics

# 4. Seller Performance (assuming 'Number of Transactions' exists)
seller_performance = data.groupby('Seller ID')['Time to 1st Sale', 'Number of Transactions'].agg(['mean', 'median'])
correlation = seller_performance['Time to 1st Sale'].corr(seller_performance['Number of Transactions'])
print(f"Correlation between Time to 1st Sale and Number of Transactions: {correlation:.2f}")

# 5. Impact of Marketing/Promotions (assuming a 'Marketing Campaign' column)
data['Marketing Campaign'] = data['Marketing Campaign'].fillna(False)  # Impute missing values with False
campaign_data = data.groupby('Marketing Campaign')['Time to Activation'].agg(['mean', 'median'])
print(campaign_data)

# You can use statistical tests to compare time to activation between groups with/without marketing campaigns











