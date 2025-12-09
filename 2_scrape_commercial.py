import osmnx as ox
import pandas as pd
import time

lgas = [
    "Adavi", "Ajaokuta", "Ankpa", "Bassa", "Dekina", 
    "Ibaji", "Idah", "Igalamela-Odolu", "Ijumu", "Kabba/Bunu", 
    "Kogi", "Lokoja", "Mopa-Muro", "Ofu", "Ogori/Magongo", 
    "Okehi", "Okene", "Olamaboro", "Omala", "Yagba East", "Yagba West"
]

commercial_leads = []

target_tags = {
    "amenity": ["marketplace", "school", "college", "university", "bank", "fuel", "clinic", "hospital", "place_of_worship", "police", "townhall"],
    "office": ["government", "association", "ngo", "cooperative"],
    "shop": ["supermarket", "wholesale", "mall", "general", "department_store"],
    "tourism": ["hotel", "guest_house"],
    "industrial": ["factory", "industrial_park", "sawmill"]
}

print("--- STARTING COMMERCIAL HUNT (WITH TRAFFIC ESTIMATES) ---")

# --- THE NEW LOGIC ENGINE ---
def estimate_traffic(obj_type, category):
    t = str(obj_type).lower()
    
    # 1. HUGE CROWDS (Massive Cash Flow)
    if any(x in t for x in ['university', 'market', 'mall', 'hospital']):
        return "High (Thousands Daily)"
    
    # 2. LARGE GATHERINGS (Weekly/Daily peaks)
    if any(x in t for x in ['college', 'worship', 'church', 'mosque', 'supermarket', 'factory']):
        return "Medium-High (Hundreds Daily/Weekly)"
    
    # 3. STEADY BUSINESS
    if any(x in t for x in ['hotel', 'bank', 'fuel', 'school', 'secondary']):
        return "Medium (Steady Flow)"
        
    # 4. SMALLER UNITS
    return "Low-Medium (Local Traffic)"

for lga in lgas:
    query = f"{lga}, Kogi State, Nigeria"
    print(f"Scanning {query}...")
    
    try:
        gdf = ox.features_from_place(query, target_tags)
        
        if not gdf.empty:
            gdf = gdf.reset_index()
            for _, row in gdf.iterrows():
                # Categorize
                category = "Business"
                if 'amenity' in row and row['amenity'] == 'place_of_worship': category = "Religious"
                elif 'amenity' in row and row['amenity'] in ['school', 'college', 'university']: category = "Education"
                elif 'tourism' in row: category = "Hospitality"
                elif 'office' in row: category = "Office/Govt"
                elif 'industrial' in row: category = "Industrial"
                
                # Naming
                name = None
                for col in ['name', 'name:en', 'alt_name']:
                    if col in row and pd.notna(row[col]):
                        name = row[col]
                        break
                
                obj_type = row.get('amenity') or row.get('shop') or row.get('office') or row.get('tourism') or row.get('industrial') or "Business"
                
                if not name:
                    name = f"Unnamed {str(obj_type).title()}"

                # GET THE ESTIMATE
                traffic = estimate_traffic(obj_type, category)

                commercial_leads.append({
                    "Name": name,
                    "Type": str(obj_type).title(),
                    "Category": category,
                    "LGA": lga,
                    "Tentative_Population": traffic,  # <--- HERE IT IS
                    "Priority_Tier": 1, 
                    "Latitude": row.geometry.centroid.y,
                    "Longitude": row.geometry.centroid.x
                })
            print(f"  -> Found {len(gdf)} targets in {lga}")
        else:
            print(f"  -> No data found for {lga}")

    except Exception as e:
        print(f"  -> No data/error for {lga}")
    
    time.sleep(1)

if commercial_leads:
    df = pd.DataFrame(commercial_leads)
    df.drop_duplicates(subset=['Name', 'Latitude'], inplace=True)
    df.to_csv("kogi_commercial.csv", index=False)
    print(f"\nSUCCESS! Scraped {len(df)} targets with traffic estimates.")
else:
    print("\nFAILED.")