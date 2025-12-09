import pandas as pd
import os

print("--- STARTING DATA MERGE ---")

# 1. Load the files
try:
    df_villages = pd.read_csv("kogi_villages_smart.csv")
    df_commercial = pd.read_csv("kogi_commercial.csv")
    
    print(f"Loaded: {len(df_villages)} Villages/Towns")
    print(f"Loaded: {len(df_commercial)} Businesses/Institutions")

    # 2. Standardize Columns (Make them match)
    # We want one column called "Tentative_Population" for everyone
    if 'Population_Info' in df_villages.columns:
        df_villages.rename(columns={'Population_Info': 'Tentative_Population'}, inplace=True)

    # Ensure Categories exist
    df_villages['Category'] = 'Settlement'  # Label all these as Settlements
    
    # 3. Combine them
    # We select only the columns we need to keep the file clean
    cols = ['Name', 'Category', 'Type', 'LGA', 'Tentative_Population', 'Priority_Tier', 'Latitude', 'Longitude']
    
    # Align both dataframes to these columns (fill missing with N/A)
    df_master = pd.concat([df_villages, df_commercial], ignore_index=True)
    
    # Keep only relevant columns if others exist
    df_master = df_master[cols]

    # 4. GENERATE THE "MAGIC LINK" (Google Maps)
    # This creates the URL: http://maps.google.com/?q=LAT,LONG
    def create_link(lat, lon):
        return f"https://www.google.com/maps/search/?api=1&query={lat},{lon}"

    df_master['Navigation_Link'] = df_master.apply(
        lambda row: create_link(row['Latitude'], row['Longitude']), axis=1
    )

    # 5. Clean Duplicates
    # If a Village and a Market have the EXACT same name and location, keep just one.
    initial_len = len(df_master)
    df_master.drop_duplicates(subset=['Name', 'LGA', 'Latitude'], keep='first', inplace=True)
    print(f"Removed {initial_len - len(df_master)} duplicates.")

    # 6. Save Final Master List
    output_file = "kogi_master_leads.csv"
    df_master.to_csv(output_file, index=False)
    
    print(f"\nSUCCESS! Master Database Created: {output_file}")
    print(f"TOTAL TARGETS: {len(df_master)}")
    print("-" * 30)
    print("Sample Row:")
    print(df_master.iloc[0])

except FileNotFoundError:
    print("ERROR: Could not find one of the CSV files. Did you run Step 1 and Step 2?")