import pandas as pd
import matplotlib.pyplot as plt

# Read the Excel file into a DataFrame
excel_file_path = r"D:\Hist_data\Duquit_5_day_forecast.xlsx"

# Reading the sheets in the excel file into dictionaries
dfs = pd.read_excel(excel_file_path, sheet_name=None)

# Concatenate all DataFrames into a single DataFrame
df = pd.concat(dfs.values(), ignore_index=True)

# Convert the 'Date & Time' column to datetime format
df['Date & Time'] = pd.to_datetime(df['Date & Time'])

# Set the 'Date & Time' column as the index
df.set_index('Date & Time', inplace=True)

# Plotting historical data
plt.figure(figsize=(10, 6))
plt.plot(df.index, df['Temperature (°C)'], label='Temperature (°C)', marker='o')
plt.plot(df.index, df['Humidity (%)'], label='Humidity (%)', marker='o')
plt.plot(df.index, df['Wind Speed (m/s)'], label='Wind Speed (m/s)', marker='o')
plt.plot(df.index, df['Rain (3h) (mm)'], label='Rain (3h) (mm)', marker='o')

# Plot names
plt.title('Historical Weather Analysis')
plt.xlabel('Date & Time')
plt.ylabel('Values(Refer to the labels)')
plt.legend()
plt.grid(True)
plt.xticks(rotation=45)

# Output plot
plt.tight_layout()
plt.show()
