import pandas as pd

# Read the CSV file
df = pd.read_('data.csv')

# Convert to JSON
json_data = df.to_json(orient='records')

# Write JSON to a file
with open('cars_data.json', 'w') as f:
    f.write(json_data)

print("CSV has been converted to JSON and saved as 'cars_data.json'")

# If you want to print the JSON data to console as well, you can uncomment the next line
# print(json_data)