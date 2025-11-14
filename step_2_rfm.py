import pandas as pd
import datetime as dt

# --- 1. Load Cleaned Data ---
# We'll use the CSV file you created in Step 1.
input_filename = "cleaned_customer_data.csv"

print(f"Loading '{input_filename}'...")
try:
    # 'parse_dates' tells pandas to read the date column as a datetime object
    df = pd.read_csv(input_filename, parse_dates=['TransactionDate'])
    print("Cleaned data loaded successfully.")
except FileNotFoundError:
    print(f"*** STOP! FILE NOT FOUND: {input_filename} ***")
    print("Please make sure you have successfully run Step 1 and this script is in the same folder.")
    exit()
except Exception as e:
    print(f"An error occurred loading the file: {e}")
    exit()

print("\n--- Cleaned Data Info (Top 5 rows) ---")
print(df.head())

# --- 2. RFM Column Names ---
# These must match the columns in your cleaned CSV
DATE_COLUMN = 'TransactionDate'
AMOUNT_COLUMN = 'TransactionAmount'
ID_COLUMN = 'CustomerID'

# --- 3. Calculate RFM Values ---
print("\n--- Calculating RFM Values ---")

# --- 3a. Set the "Snapshot Date" ---
# This is the reference date for calculating "how recent" a purchase is.
# We'll set it to one day *after* the most recent transaction in the data.
snapshot_date = df[DATE_COLUMN].max() + dt.timedelta(days=1)
print(f"Snapshot date (Today) set to: {snapshot_date.strftime('%Y-%m-%d')}")

# --- 3b. Group by Customer and Calculate R, F, M ---
# We will group all transactions by CustomerID and then perform 3 calculations
rfm_data = df.groupby(ID_COLUMN).agg(
    Recency=('TransactionDate', lambda x: (snapshot_date - x.max()).days),
    Frequency=('TransactionDate', 'count'),
    Monetary=(AMOUNT_COLUMN, 'sum')
)

# Reset the index so 'CustomerID' becomes a column again
rfm_data = rfm_data.reset_index()

# --- 4. Final Inspection and Save ---
print("\n--- RFM Calculation Complete (Top 5 rows) ---")
print(rfm_data.head())

# Save the RFM data to a new file
output_filename = "rfm_data.csv"
rfm_data.to_csv(output_filename, index=False)

print(f"\n*** SUCCESS! ***")
print(f"RFM data saved to: {output_filename}")
print("You can now move to Step 3.")