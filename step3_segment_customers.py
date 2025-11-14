import pandas as pd

# --- 1. Load RFM Data ---
# We'll use the CSV file you created in Step 2.
rfm_filename = "rfm_data.csv"

print(f"Loading '{rfm_filename}'...")
try:
    rfm_data = pd.read_csv(rfm_filename)
    print("RFM data loaded successfully.")
except FileNotFoundError:
    print(f"*** STOP! FILE NOT FOUND: {rfm_filename} ***")
    print("Please make sure you have successfully run Step 2 and this script is in the same folder.")
    exit()

print("\n--- RFM Data (Top 5 rows) ---")
print(rfm_data.head())

# --- 2. Calculate RFM Scores ---
# We will use 'pd.qcut' (quantile-based cut) to split customers into 5 equal groups.
# A score of 5 is always the BEST.
#
# For Recency: Low days (e.g., 5 days) is BEST (Score=5). High days (e.g., 500 days) is WORST (Score=1).
# For Frequency/Monetary: High value (e.g., 50 purchases) is BEST (Score=5). Low value is WORST (Score=1).

print("\n--- Calculating RFM Scores (1-5) ---")

# Note: We use rfm_data['Recency'].rank(method='first') to handle duplicate values, 
# which can cause errors in qcut.
rfm_data['R_Score'] = pd.qcut(rfm_data['Recency'].rank(method='first'), 5, labels=[5, 4, 3, 2, 1])
rfm_data['F_Score'] = pd.qcut(rfm_data['Frequency'].rank(method='first'), 5, labels=[1, 2, 3, 4, 5])
rfm_data['M_Score'] = pd.qcut(rfm_data['Monetary'].rank(method='first'), 5, labels=[1, 2, 3, 4, 5])

# Convert scores to strings to combine them
rfm_data['RFM_Score'] = rfm_data['R_Score'].astype(str) + rfm_data['F_Score'].astype(str) + rfm_data['M_Score'].astype(str)

print("RFM Scores calculated (Top 5 rows):")
print(rfm_data.head())

# --- 3. Define Customer Segments ---
# This is the core of the analysis. We define segments based on the scores.
# You can customize these rules.
print("\n--- Segmenting Customers ---")

# Define a function to map RFM scores to segments
def rfm_to_segment(rfm_score):
    # We use regex (regular expressions) to find matching patterns
    # [4-5] means 4 or 5. [1-2] means 1 or 2.
    if pd.isna(rfm_score):
        return 'Unknown'
    
    # Best Customers: R=5, F=5, M=5
    if rfm_score == '555':
        return 'Best Customers'
    
    # Loyal Customers: R=[4-5], F=[4-5], M is not 5 (or they'd be 'Best')
    if rfm_score[0] in ['4', '5'] and rfm_score[1] in ['4', '5']:
        return 'Loyal Customers'
    
    # Big Spenders: M=5, but R or F are not high
    if rfm_score[2] == '5':
        return 'Big Spenders'
    
    # At Risk: Bought recently (R=[3-5]) but are low frequency/monetary (F/M=[1-2])
    # OR were good customers (F/M=[3-5]) but haven't bought in a while (R=[1-2])
    if rfm_score[0] in ['1', '2'] and rfm_score[1] in ['3', '4', '5']:
        return 'At Risk'
    
    # New Customers: High Recency (R=5) but low Frequency (F=1)
    if rfm_score == '511':
        return 'New Customers'
        
    # Lost Customers: Low R and F scores
    if rfm_score[0] in ['1', '2'] and rfm_score[1] in ['1', '2']:
        return 'Lost Customers'
    
    # Default for all others
    return 'Other'

rfm_data['Segment'] = rfm_data['RFM_Score'].apply(rfm_to_segment)

print("Segmentation complete. Segment counts:")
print(rfm_data['Segment'].value_counts())

# --- 4. Merge with Original Data ---
# Now we add the segment data back to the original cleaned data
print("\n--- Merging Segments with Customer Master Data ---")

try:
    # We only need the customer master data, not all 23,000 transactions
    df_master = pd.read_csv("Customer_Master_Data.csv")
    
    # Merge the RFM and Segment data with the master customer list
    # We use 'on=CustomerID' to link the two tables
    final_data = pd.merge(df_master, rfm_data, on='CustomerID', how='left')
    
    # Drop customers from master list who never made a purchase (if any)
    final_data.dropna(subset=['RFM_Score'], inplace=True)
    
except FileNotFoundError:
    print("Customer_Master_Data.csv not found. Saving RFM data only.")
    final_data = rfm_data
except Exception as e:
    print(f"An error occurred during merging: {e}. Saving RFM data only.")
    final_data = rfm_data


# --- 5. Save Final Segmented File ---
output_filename = "rfm_segmented_data.csv"
final_data.to_csv(output_filename, index=False)

print(f"\n*** SUCCESS! ***")
print(f"Final segmented data saved to: {output_filename}")
print("This file contains all your customers, their demographics, their RFM scores, and their segment.")
print("You can now move to Step 4.")