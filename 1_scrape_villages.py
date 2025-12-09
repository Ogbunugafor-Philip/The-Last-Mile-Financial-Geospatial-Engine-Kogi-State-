import osmnx as ox
import pandas as pd
import time
import numpy as np

# 1. Define LGAs
lgas = [
    "Adavi", "Ajaokuta", "Ankpa", "Bassa", "Dekina", 
    "Ibaji", "Idah", "Igalamela-Odolu", "Ijumu", "Kabba/Bunu", 
    "Kogi", "Lokoja", "Mopa-Muro", "Ofu", "Ogori/Magongo", 
    "Okehi", "Okene", "Olamaboro", "Omala", "Yagba East", "Yagba West"
]

all_settlements = []

print("--- STARTING SMART VILLAGE SCRAPE (FIXED NAMES) ---")

def estimate_pop(place_type):
    p_type = str(place_type).lower()
    if 'city' in p_type: return "High (100k+)"
    if 'town' in p_type: return "High (20k-50k)"
    if 'village' in p_type: return "Medium (2k-10k)"
    if 'hamlet' in p_type: return "Low (<1k)"
    return "Unknown"

# Helper to find ANY valid name in the row
def get_best_name(row, lga, lat):
    # List of columns where names might hide
    name_cols = ['name', 'name:en', 'alt_name', 'int_name', 'loc_name']
    
    for col in name_cols:
        if col in row and pd.notna(row[col]) and str(row[col]).strip() != "":
            return row[col]
            
    # If still no name, generate a Unique ID so you can find it later
    return f"Unmapped Cluster ({lga} - {str(lat)[:6]})"

for lga in lgas:
    query = f"{lga}, Kogi State, Nigeria"
    print(f"Scanning {query}...")
    
    try:
        tags = {"place": ["village", "town", "hamlet", "suburb"]}
        gdf = ox.features_from_place(query, tags)
        
        if not gdf.empty:
            gdf = gdf.reset_index()
            
            for _, row in gdf.iterrows():
                # Get Coordinates first
                lat = row.geometry.centroid.y
                lon = row.geometry.centroid.x
                
                # 1. USE THE NEW NAMING FUNCTION
                name = get_best_name(row, lga, lat)
                
                # Get Type & Pop
                place_type = row['place'] if 'place' in row else "village"
                
                real_pop = row['population'] if 'population' in row and pd.notna(row['population']) else None
                if real_pop:
                    pop_display = f"Confirmed: {int(real_pop)}"
                    priority = 1 if int(real_pop) > 5000 else 2
                else:
                    pop_display = estimate_pop(place_type)
                    priority = 1 if "High" in pop_display else (2 if "Medium" in pop_display else 3)
                
                # If it's an "Unmapped Cluster", it might actually be a GOLDMINE (hidden market)
                # So we keep the priority high enough to check.
                if "Unmapped" in name:
                    priority = 2 

                all_settlements.append({
                    "Name": name,
                    "Type": place_type,
                    "LGA": lga,
                    "Population_Info": pop_display,
                    "Priority_Tier": priority,
                    "Latitude": lat,
                    "Longitude": lon
                })
            print(f"  -> Found {len(gdf)} settlements in {lga}")
        else:
            print(f"  -> No data found for {lga}")

    except Exception as e:
        print(f"  -> Error scanning {lga}: {e}")
    
    time.sleep(1)

# Save
if all_settlements:
    df = pd.DataFrame(all_settlements)
    filename = "kogi_villages_smart.csv"
    df.to_csv(filename, index=False)
    print(f"\nSUCCESS! Scraped {len(df)} locations.")
    print(f"Data saved to {filename}")
else:
    print("\nFAILED. No data collected.")