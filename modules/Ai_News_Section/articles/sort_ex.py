import pandas as pd

# Read the Excel file into a DataFrame
df = pd.read_excel("articles.xlsx")

# Sort the DataFrame by the 'Date' column
df = df.sort_values(by='Date')

# Save the sorted DataFrame back to the Excel file
df.to_excel("articles.xlsx", index=False)
