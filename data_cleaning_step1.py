import pandas as pd
import numpy as np

# --- 1. Data Loading ---
print("Attempting to load files...")
try:
    df_master = pd.read_csv("Customer_Master_Data.csv")
    df_trans = pd.read_csv("Customer_Transactions.csv")
    print("Files loaded successfully.")
except FileNotFoundError as e:
    print(f"Error: {e}\n*** STOP! FILE NOT FOUND. ***")
    print("Please make sure your .py script is saved in the EXACT same folder as your CSV files.")
    exit()

print("\n--- Initial 'Customer_Transactions' Info (Top 5 rows) ---")
print(df_trans.head())

# --- 2. Data Cleaning (df_trans) ---
DATE_COLUMN = 'TransactionDate'
AMOUNT_COLUMN = 'TransactionAmount'
ID_COLUMN = 'CustomerID'

print(f"\n--- Starting Cleaning Process ---")

# --- 2a. Clean TransactionDate ---
print(f"Cleaning '{DATE_COLUMN}'...")
# Replace '####' with NaN to mark it as missing
df_trans[DATE_COLUMN] = df_trans[DATE_COLUMN].replace('####', np.nan)

# *** FIXED THE DATE FORMAT ***
# We are now using '%m/%d/%y' (two-digit year) which matches your data '7/31/23'
try:
    df_trans[DATE_COLUMN] = pd.to_datetime(df_trans[DATE_COLUMN], format='%m/%d/%y', errors='coerce')
    print("Dates converted using 'M/D/YY' format.")
except Exception as e:
    print(f"Format 'M/D/YY' failed, trying default parser... Error: {e}")
    # Fallback just in case some dates are different
    df_trans[DATE_COLUMN] = pd.to_datetime(df_trans[DATE_COLUMN], errors='coerce')


# --- 2b. Clean TransactionAmount ---
print(f"Cleaning '{AMOUNT_COLUMN}'...")
if df_trans[AMOUNT_COLUMN].dtype == 'object':
    print("Amount column is 'object' type. Removing symbols like '$', '€', ','...")
    df_trans[AMOUNT_COLUMN] = df_trans[AMOUNT_COLUMN].astype(str).str.replace(r'[$,€,]', '', regex=True)

df_trans[AMOUNT_COLUMN] = pd.to_numeric(df_trans[AMOUNT_COLUMN], errors='coerce')
print("Amount column converted to numeric.")


# --- 2c. Diagnostic Check (NEW) ---
print("\n--- Diagnostic Check before Dropping ---")
null_dates = df_trans[DATE_COLUMN].isna().sum()
null_amounts = df_trans[AMOUNT_COLUMN].isna().sum()
print(f"Found {null_dates} invalid dates (NaT).")
print(f"Found {null_amounts} invalid amounts (NaN).")

if null_dates == len(df_trans) or null_amounts == len(df_trans):
    print("\n*** STOP! ***")
    print("All dates or all amounts failed to convert. This is a data format issue.")
    print("Please check your original CSV file or the format string in the script.")
    exit()

# --- 2d. Handle Missing & Duplicate Values ---
print("\n--- Handling Missing & Duplicate Values ---")
original_count = len(df_trans)
print(f"Original transaction count: {original_count}")

# Drop rows where any of the key RFM columns are missing
df_trans.dropna(subset=[ID_COLUMN, DATE_COLUMN, AMOUNT_COLUMN], inplace=True)
count_after_drop = len(df_trans)
print(f"Transaction count after dropping missing values: {count_after_drop}")
print(f"Total rows removed: {original_count - count_after_drop}")

# Drop duplicate transactions
df_trans.drop_duplicates(inplace=True)
count_after_duplicates = len(df_trans)
print(f"Transaction count after dropping duplicates: {count_after_duplicates}")


# --- 3. Merge Data ---
if count_after_duplicates == 0:
    print("\n*** STOP! ***")
    print("No data remaining after cleaning. Cannot proceed to merge.")
    print("The 'cleaned_customer_data.csv' file will be empty.")
    exit()
    
print("\n--- Merging Cleaned Data ---")
df_merged = pd.merge(df_trans, df_master, on=ID_COLUMN, how='left')
print("--- Merged DataFrame Info (Top 5 rows) ---")
print(df_merged.head())


# --- 4. Save Cleaned File ---
output_filename = "cleaned_customer_data.csv"
df_merged.to_csv(output_filename, index=False)

print(f"\n*** SUCCESS! ***")
print(f"Cleaned and merged data saved to: {output_filename}")
print("You can now move to Step 2.")