import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# --- 0. Create a folder to save charts ---
output_folder = "charts"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)
    print(f"Created folder: '{output_folder}' to save charts.")

# --- 1. Load Segmented Data ---
input_filename = "rfm_segmented_data.csv"

print(f"Loading '{input_filename}'...")
try:
    df_final = pd.read_csv(input_filename)
    print("Segmented data loaded successfully.")
except FileNotFoundError:
    print(f"*** STOP! FILE NOT FOUND: {input_filename} ***")
    print("Please make sure you have successfully run Step 3 and this script is in the same folder.")
    exit()

print("\n--- Final Data (Top 5 rows) ---")
print(df_final.head())

# --- Set Style for all charts ---
sns.set(style="whitegrid")
# Get the order of segments from largest to smallest
segment_counts = df_final['Segment'].value_counts()
segment_order = segment_counts.index


# --- 2. Visualization 1: Segment Distribution (Bar Chart) ---
print("\n--- Creating Visualization 1: Segment Distribution (Bar Chart) ---")
plt.figure(figsize=(12, 7))
sns.countplot(
    data=df_final, 
    y='Segment',  # Use y-axis for horizontal bars
    order=segment_order,
    palette="viridis"
)
plt.title('Customer Segment Distribution (Bar Chart)', fontsize=16)
plt.xlabel('Number of Customers', fontsize=12)
plt.ylabel('Segment', fontsize=12)
plt.tight_layout() 

chart_path1 = os.path.join(output_folder, "segment_distribution.png")
plt.savefig(chart_path1)
print(f"Chart 1 saved to: {chart_path1}")


# --- 3. Visualization 2: Segment Distribution (Pie Chart) [NEW] ---
print("\n--- Creating Visualization 2: Segment Distribution (Pie Chart) ---")
plt.figure(figsize=(12, 9))
# We use the 'segment_counts' we calculated earlier
plt.pie(
    segment_counts, 
    labels=segment_counts.index, 
    autopct='%1.1f%%',  # Show percentage
    startangle=140,
    pctdistance=0.85, # Position of the percentage text
    colors=sns.color_palette("viridis", len(segment_counts))
)
plt.title('Customer Segment Proportions (Pie Chart)', fontsize=16)
plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
plt.tight_layout()

chart_path2 = os.path.join(output_folder, "segment_pie_chart.png")
plt.savefig(chart_path2)
print(f"Chart 2 saved to: {chart_path2}")


# --- 4. Visualization 3: RFM Segment Heatmap [NEW] ---
print("\n--- Creating Visualization 3: RFM Segment Heatmap ---")
# Calculate the average R, F, and M for each segment
rfm_averages = df_final.groupby('Segment')[['Recency', 'Frequency', 'Monetary']].mean()

plt.figure(figsize=(12, 7))
sns.heatmap(
    rfm_averages, 
    annot=True,  # Show the values in the cells
    fmt='.0f',   # Format as whole numbers
    cmap="coolwarm",
    linewidths=.5
)
plt.title('Average RFM Values by Segment (Heatmap)', fontsize=16)
plt.xlabel('RFM Metric', fontsize=12)
plt.ylabel('Segment', fontsize=12)
plt.tight_layout()

chart_path3 = os.path.join(output_folder, "rfm_heatmap.png")
plt.savefig(chart_path3)
print(f"Chart 3 saved to: {chart_path3}")


# --- 5. Visualization 4: Average Age by Segment ---
print("\n--- Creating Visualization 4: Average Age by Segment ---")
plt.figure(figsize=(12, 7))
sns.barplot(
    data=df_final,
    x='Segment',
    y='Age',
    order=segment_order, # Use the same order
    palette="coolwarm"
)
plt.title('Average Age by Customer Segment', fontsize=16)
plt.xlabel('Segment', fontsize=12)
plt.ylabel('Average Age', fontsize=12)
plt.xticks(rotation=45, ha='right') # Rotate x-axis labels
plt.tight_layout()

chart_path4 = os.path.join(output_folder, "segment_by_age.png")
plt.savefig(chart_path4)
print(f"Chart 4 saved to: {chart_path4}")


# --- 6. Visualization 5: Top Cities for Key Segments ---
print("\n--- Creating Visualization 5: Top Cities for Key Segments ---")
key_segments_df = df_final[df_final['Segment'].isin(['Best Customers', 'At Risk'])]
plt.figure(figsize=(12, 7))
sns.countplot(
    data=key_segments_df,
    y='City', # Use y-axis
    hue='Segment',
    palette="rocket",
    order=key_segments_df['City'].value_counts().iloc[:10].index # Top 10 cities
)
plt.title('Top 10 Cities for "Best" vs. "At Risk" Customers', fontsize=16)
plt.xlabel('Number of Customers', fontsize=12)
plt.ylabel('City', fontsize=12)
plt.tight_layout()

chart_path5 = os.path.join(output_folder, "segment_by_city.png")
plt.savefig(chart_path5)
print(f"Chart 5 saved to: {chart_path5}")


# --- 7. Visualization 6: Recency vs. Frequency Scatter Plot ---
print("\n--- Creating Visualization 6: Recency vs. Frequency Scatter Plot ---")
plt.figure(figsize=(12, 8))
sns.scatterplot(
    data=df_final,
    x='Recency',
    y='Frequency',
    hue='Segment',
    palette='deep', 
    alpha=0.7,
    s=80 
)
plt.title('Recency vs. Frequency by Segment', fontsize=16)
plt.xlabel('Recency (Days since last purchase)', fontsize=12)
plt.ylabel('Frequency (Total purchases)', fontsize=12)
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.) 
plt.tight_layout()

chart_path6 = os.path.join(output_folder, "rfm_scatter.png")
plt.savefig(chart_path6, bbox_inches='tight') # Use bbox_inches to include legend
print(f"Chart 6 saved to: {chart_path6}")


print("\n\n*** SUCCESS! ***")
print(f"All 6 charts have been saved to the '{output_folder}' folder.")
print("Your project is now complete!")