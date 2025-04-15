import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
data4 = pd.read_csv('C:/Users/Sneha Maddheshiya/Downloads/Mental_Health_Care_in_the_Last_4_Weeks.csv')


print(data4.info())


print(data4.columns)


print(data4.head())


print(data4.tail())


print(data4.isnull().sum())


# Dropping unnecessary columns

data = data4.drop(columns=['Suppression Flag', 'Quartile Range'])


# Handling missing values and correcting column typo


data = data.fillna(0)


# Converting date columns
data['Time Period Start Date'] = pd.to_datetime(data['Time Period Start Date'], errors='coerce')
data['Time Period End Date'] = pd.to_datetime(data['Time Period End Date'], errors='coerce')

# 1. Demographic Comparison
labels = [
    "Sexual orientation", "Gender identity", "Disability status",
    "State", "Anxiety/Depression Symptoms", "National Estimate",
    "Sex", "Education", "Age", "Race/Ethnicity"
]

# Placeholder values - replace with actual averages if you have them
avg_values = [12.5, 14.2, 10.1, 11.5, 13.6, 9.8, 10.9, 12.1, 11.3, 13.0]

demographic_df = pd.DataFrame({
    'Demographic Group': labels,
    'Average Value (%)': avg_values
})

# Plot the bar chart
plt.figure(figsize=(14, 6))
sns.barplot(x='Demographic Group', y='Average Value (%)', data=demographic_df, palette='coolwarm')
plt.title("Mental Health Care Usage in Different Demographic Groups")
plt.xlabel("Demographic Group")
plt.ylabel("Average Value (%)")
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

# 2. Trends Over Time
import re
from datetime import datetime

def extract_start_date(label):
    # Extract the first date in the format "Apr 14 - Apr 26, 2021"
    match = re.match(r"([A-Za-z]+ \d+)", label)
    year_match = re.search(r"(\d{4})$", label)
    if match and year_match:
        date_str = match.group(1) + ", " + year_match.group(1)
        return datetime.strptime(date_str, "%b %d, %Y")
    return pd.NaT

def analyze_trends_over_time(data):
    data = data.copy()
    # Convert string time periods into sortable datetime values
    data['Start Date'] = data['Time Period Label'].apply(extract_start_date)

    # Group and sort
    trends = (
        data.groupby(['Time Period Label', 'Start Date'])['Value']
        .mean()
        .reset_index()
        .sort_values('Start Date')
    )

    # Plot
    plt.figure(figsize=(14, 6))
    sns.lineplot(data=trends, x='Time Period Label', y='Value', marker='o', color='blue')
    plt.title('How Mental Health Care Help Usage Changed with Time', fontsize=14)
    plt.xlabel('Time Period', fontsize=12)
    plt.ylabel('Average % Value', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.grid(True)
    plt.tight_layout()
    plt.show()
analyze_trends_over_time(data)

# 3. State-Wise Analysis
def state_wise_analysis(data):
    states = data.groupby('State')['Value'].mean().sort_values(ascending=False).reset_index()

    plt.figure(figsize=(12, 6))
    sns.barplot(data=states, x='State', y='Value', hue='State', palette='viridis', legend=False)
    plt.title('State-wise Average Mental Health Care Usage', fontsize=14)
    plt.xlabel('State', fontsize=12)
    plt.ylabel('Average % Value', fontsize=12)
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.show()
state_wise_analysis(data)


# 4. Heatmap (State x Time)
def heatmap_state_time(data):
    heatmap_data = data.pivot_table(
        index='State',
        columns='Time Period Label',
        values='Value',
        aggfunc='mean'
    )

    plt.figure(figsize=(15, 10))
    sns.heatmap(heatmap_data, cmap='YlGnBu', linewidths=0.3, linecolor='gray')
    plt.title('Mental Health Care Usage Over Time by State', fontsize=16)
    plt.xlabel('Time Period', fontsize=12)
    plt.ylabel('State', fontsize=12)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
heatmap_state_time(data)


# 5. Confidence Interval Analysis
def analyze_confidence_intervals(data):
    ci_data = data.dropna(subset=['LowCI', 'HighCI']).copy()
    ci_data['CI Range'] = ci_data['HighCI'] - ci_data['LowCI']

    plt.figure(figsize=(12, 6))
    sns.histplot(ci_data['CI Range'], bins=30, kde=True, color='green')
    plt.axvline(ci_data['CI Range'].mean(), color='red', linestyle='--', label='Mean CI Range')
    plt.title('Distribution of Confidence Interval Ranges', fontsize=14)
    plt.xlabel('CI Range (%)', fontsize=12)
    plt.ylabel('Frequency', fontsize=12)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()
analyze_confidence_intervals(data)



