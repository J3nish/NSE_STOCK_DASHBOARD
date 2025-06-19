import sqlite3
import pandas as pd
from datetime import datetime

# Connect to database
conn = sqlite3.connect('stockindia.db')
df = pd.read_sql_query("SELECT * FROM stocks", conn)

# Convert to correct data types (no symbols or commas)
df['volume'] = df['volume'].astype(int)
df['ltp'] = df['ltp'].astype(float)
df['open_price'] = df['open_price'].astype(float)
df['close_price'] = df['close_price'].astype(float)

# Save to Excel in proper format
latest_file = r"C:\Users\91931\Stock_data\stock_data_latest.xlsx"

with pd.ExcelWriter(latest_file, mode='w') as writer:
    df.to_excel(writer, sheet_name='stock_data_latest_Data', index=False)

print("✅ File saved to:", latest_file)
conn.close()
