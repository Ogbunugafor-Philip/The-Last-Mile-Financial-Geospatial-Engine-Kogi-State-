# The Last-Mile Financial Geospatial Engine (Kogi State)

## Introduction

In the highly competitive financial landscape of Kogi State, relying on traditional "word-of-mouth" prospecting is no longer sufficient to guarantee market leadership. While most financial institutions aggressively compete for the same saturated clients in major urban centers like Lokoja, Okene, Anyigba and Kabba, a vast reservoir of low-cost deposits and mass-market opportunities lies untapped in the hinterlands. These opportunities exist in the thousands of unmapped villages, rural agrarian clusters, and undocumented trade associations that form the backbone of the state's economy but remain invisible to the corporate banking radar.
This project is a strategic intervention designed to bridge this gap. It proposes the development of a proprietary, data-driven intelligence engine that systematically scrapes, maps, and analyzes every potential economic point of interest across all 21 Local Government Areas. By converting raw geospatial data into an interactive Streamlit dashboard, this project transforms the entire state into a navigable grid of opportunities.
This initiative is not merely about finding locations; it is about operational efficiency and first-mover advantage. It aims to eliminate the guesswork from deposit mobilization by equipping our field teams with precise targets, down to the exact GPS coordinate and estimated population size; ensuring that every liter of fuel and every hour of field work translate directly into account acquisition. This is the transition from random prospecting to precision banking.

## Statement of Problem
The bank’s ability to aggressively expand its customer base is currently paralyzed by a "visibility gap" that hides the vast majority of potential mass-market clients located in rural and semi-urban Kogi State. The fundamental problem is not a lack of market potential, but a lack of precise location intelligence; field teams cannot acquire customers they cannot find. Consequently, our acquisition strategy is reactive and confined to saturated urban centers, leaving thousands of potential new accounts in unmapped villages and markets completely untouched. This failure to systematically identify and reach these "invisible" populations at the top of the funnel creates a bottleneck that stifles all downstream banking activities, rendering effective deposit mobilization impossible in these territories. Without a tool to guide officers to these untapped reservoirs of customers, the bank continues to lose critical market share and brand presence in the "last mile" of the state.

## Project Objectives

i.	To scrape and catalogue every village, market, and institution across all 21 LGAs into a unified target database.

ii.	To estimate population density for every settlement to prioritize high-potential locations for field visits.

iii.	To develop an interactive Streamlit dashboard for visualizing target clusters and tracking field coverage.

iv.	To integrate direct navigation links that guide field teams to the exact coordinates of remote locations.

v.	To generate a secondary contact list of institutional leaders to facilitate entry into community-wide account acquisition.

## Technology Stack

1. Core Development Engine
  - Python (v3.10+): The primary programming language selected for its robust ecosystem in data science, geospatial analysis, and web scraping capabilities.

2. Data Acquisition & Scraping Layer

  - OSMnx: For querying OpenStreetMap data to extract road networks, village boundaries, and building footprints in remote areas.
  - Selenium & BeautifulSoup: For automating web browsers to scrape directory listings of schools, associations, and businesses that lack API access.
  - Requests: For handling HTTP requests to interact with web servers and APIs efficiently.

3. Geospatial Intelligence & Processing
  - Pandas & NumPy: For high-performance data manipulation, cleaning, and structuring of the scraped datasets into a usable format.
  - Geopy: For calculating geodesic distances between the branch and the target locations to optimize travel routes.
  - GRID3 Data Layers: Integration of third-party population and settlement extents to validate village density and size.

4. Visualization & User Interface

  - Streamlit: For building the interactive, mobile-responsive web dashboard that allows users to filter data and view the map without writing code.
  - Folium / Streamlit-Folium: To render the interactive maps that display clusters, pins, and heatmaps of potential customer zones.

5. Deployment & Navigation
  - Google Maps Protocol: For generating deep links that trigger the native Google Maps app on mobile devices for turn-by-turn navigation.
  - Excel/CSV Export: For generating offline-ready contact lists that field officers can use in areas with poor internet connectivity.

## Project Implementation Steps

### Phase 1: Environment Setup & Configuration
This initial phase establishes the digital infrastructure required to host and run the Pathfinder Engine. It focuses on configuring the Contabo Virtual Private Server (VPS) with a robust Linux environment and installing the precise Python framework necessary to handle complex geospatial data processing. The objective is to create a stable, isolated workspace that ensures the application operates continuously (24/7) and processes large datasets reliably without system conflicts or downtime.

- Connect to your Contabo VPS. Open your terminal (Command Prompt/PowerShell) and log in. Run;
```
ssh root@123.456.78.90
```
- Update the linux termina. Run;
```
apt update && apt upgrade -y
``` 
<img width="975" height="423" alt="image" src="https://github.com/user-attachments/assets/4387a65b-d73e-48e5-ae1a-96fcb599cf6d" />

- Install Python 3.10 tools & Virtual Environment. Run; 
```
sudo apt install python3-pip python3-venv -y
```
- Create the Project Directory. Run; 
```
mkdir kogi_pathfinder
cd kogi_pathfinder
```

- Create & Activate the Virtual Environment. Run; 
```
python3 -m venv venv
source venv/bin/activate
```
- Install the Libraries (The Tech Stack)
```
pip install --upgrade pip
pip install streamlit osmnx pandas geopandas selenium webdriver-manager
pip install folium streamlit-folium
```
<img width="975" height="526" alt="image" src="https://github.com/user-attachments/assets/ffee3b85-4093-4285-9de6-94cff770f27c" />


### Phase 2: Comprehensive Data Acquisition & Intelligence Fusion
This phase represents the operational core of the Pathfinder Engine, unifying the processes of data harvesting and strategic enrichment into a single, high-efficiency workflow. Rather than treating scraping and analysis as separate stages, the system now deploys "smart crawlers" that simultaneously map the physical landscape of Kogi State while instantly assessing the economic potential of every discovery. The objective is to execute a total digital sweep of the state, capturing every village, market, and institution and immediately calculating their tentative population density and commercial traffic. By embedding priority scoring and navigation logic directly at the point of extraction, this phase transforms raw geospatial data into a "battle-ready" target list, eliminating the need for post-processing and delivering actionable intelligence in real-time.

The execution of this phase follows a streamlined, three-step "Fusion Pipeline":

1. The Smart Settlement Scan (The "Dragnet"): We deploy the modified OSMnx engine to map the foundational "skeleton" of the state. As the script identifies remote villages and hamlets, it simultaneously applies a Population Proxy Algorithm. This logic instantly categorizes settlements (e.g., "Medium: 2k-10k residents") based on their mapped density and status, assigning a "Priority Tier" before the data is even saved.

2. The Commercial Ecosystem Hunt (The "Muscle"): Parallel to the settlement scan, the commercial scraper targets high-velocity economic hubs like markets, schools, religious bodies, and industries. It utilizes a Traffic Estimation Engine to distinguish between high-volume targets (e.g., "Kogi State University") and lower-priority units, ensuring the sales team focuses on the highest value accounts first.

3. Data Fusion & Activation: The final step merges these two datasets into a unified "Master Grid." During this merger, the system programmatically generates Deep-Link Navigation URLs for every entry. This means the final output is not just a passive list of names, but an active control board where every target is one click away from a turn-by-turn navigation route.

- Create a Python script named 1_scrape_villages.py and paste the below
```
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
```

- Execute the script to start the scraping process. Run;
```
python3 1_scrape_villages.py
```
 
- Create a Python script named 2_scrape_commercial.py and paste the below
```
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
```

- Execute the script to start the scraping process. Run;
```
python3 2_scrape_commercial.py
``` 




- Create a Python script named 3_merge_data.py and paste the below
```
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
```

- Execute the script to start the scraping process. Run;
```
python3 3_merge_data.py
``` 
<img width="975" height="544" alt="image" src="https://github.com/user-attachments/assets/1823e823-ae90-46d6-a421-19922ff5f835" />




### Phase 3: Dashboard Development (The Visual Command Center) 
With the "Master Grid" of data successfully harvested and enriched, the project now transitions from back-end intelligence gathering to front-end operational deployment. This phase focuses on constructing the Visual Command Center; the interactive interface that your field teams will actually use on their phones while in the car. We will leverage Streamlit, a rapid-deployment Python framework, to convert our static CSV files into a dynamic, mobile-responsive dashboard.
The objective here is not just to display points on a map, but to create a tactical navigation tool. By integrating the Folium mapping engine, we will render thousands of scraped coordinates as an interactive geospatial layer, allowing officers to filter targets by "LGA" (e.g., Ankpa vs. Okene) or "Category" (e.g., High-Traffic Market vs. Rural Village). This interface serves as the bridge between raw data and physical action, ensuring that every insight generated in previous phases is accessible, searchable, and instantly actionable for the sales force.

The dashboard is architected to perform three critical functions simultaneously:

i.	Visual Filtering: Allowing the user to "zoom in" on specific territories or opportunities (e.g., "Show me all Secondary Schools in Dekina").

ii.	Route Activation: Converting the filtered results into a "Hit List" where clicking a button triggers the Google Maps app for turn-by-turn navigation.

iii.	Offline Accessibility: Providing a "Download Data" feature that allows teams to export their daily route to Excel for use in areas with poor internet connectivity.

- Create the main application file named app.py and paste the below script.
```
import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from folium.plugins import MarkerCluster, Fullscreen, MousePosition, HeatMap, MiniMap, MeasureControl
import altair as alt

# 1. ENTERPRISE PAGE CONFIG
st.set_page_config(
    page_title="Kogi Pathfinder Pro",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------------------------------------------------------
# 2. OFFICIAL KOGI STATE POPULATION DATA & VIABILITY TIERS
# ------------------------------------------------------
LGA_DATA = {
    "Okene": {"pop": 420000, "tier": "Tier 1: Critical Mass", "desc": "Commercial Hub"},
    "Dekina": {"pop": 360000, "tier": "Tier 1: Critical Mass", "desc": "Agrarian Giant"},
    "Ankpa": {"pop": 350000, "tier": "Tier 1: Critical Mass", "desc": "Trade & Coal"},
    "Lokoja": {"pop": 305000, "tier": "Tier 1: Critical Mass", "desc": "State Capital"},
    "Adavi": {"pop": 298000, "tier": "Tier 1: Critical Mass", "desc": "Industrial Hub"},
    "Okehi": {"pop": 280000, "tier": "Tier 2: Growth Engine", "desc": "Semi-Urban"},
    "Ofu": {"pop": 245000, "tier": "Tier 2: Growth Engine", "desc": "Connector Hub"},
    "Olamaboro": {"pop": 215000, "tier": "Tier 2: Growth Engine", "desc": "Border Trade"},
    "Igalamela-Odolu": {"pop": 205000, "tier": "Tier 2: Growth Engine", "desc": "Farming Cluster"},
    "Bassa": {"pop": 195000, "tier": "Tier 2: Growth Engine", "desc": "Remote Agrarian"},
    "Yagba East": {"pop": 195000, "tier": "Tier 2: Growth Engine", "desc": "Okun Hub"},
    "Kabba/Bunu": {"pop": 190000, "tier": "Tier 2: Growth Engine", "desc": "Education/Admin"},
    "Yagba West": {"pop": 185000, "tier": "Tier 3: Niche Market", "desc": "Border/Trade"},
    "Ibaji": {"pop": 168000, "tier": "Tier 3: Niche Market", "desc": "Riverine/Rice"},
    "Ajaokuta": {"pop": 165000, "tier": "Tier 3: Niche Market", "desc": "Industrial Zone"},
    "Omala": {"pop": 158000, "tier": "Tier 3: Niche Market", "desc": "Agrarian"},
    "Ijumu": {"pop": 155000, "tier": "Tier 3: Niche Market", "desc": "Remittance Hub"},
    "Kogi": {"pop": 152000, "tier": "Tier 3: Niche Market", "desc": "Fishing/River"},
    "Idah": {"pop": 105000, "tier": "Tier 3: Niche Market", "desc": "Cultural/Inst."},
    "Mopa-Muro": {"pop": 65000, "tier": "Tier 3: Niche Market", "desc": "Community"},
    "Ogori/Magongo": {"pop": 55000, "tier": "Tier 3: Niche Market", "desc": "Small Community"}
}

# 3. DATA LOADING
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("kogi_master_leads.csv")
        
        # Scoring & Address
        def get_score(pop_str):
            p = str(pop_str).lower()
            if "high" in p: return 100
            if "medium" in p: return 50
            if "low" in p: return 10
            return 5
        df['Market_Score'] = df['Tentative_Population'].apply(get_score)
        df['Full_Address'] = df['Name'] + ", " + df['LGA'] + " LGA, Kogi State"
        
        # Merge Actual LGA Data
        df['LGA_Actual_Pop'] = df['LGA'].map(lambda x: LGA_DATA.get(x, {}).get('pop', 0))
        df['Viability_Tier'] = df['LGA'].map(lambda x: LGA_DATA.get(x, {}).get('tier', 'Unknown'))
        df['LGA_Desc'] = df['LGA'].map(lambda x: LGA_DATA.get(x, {}).get('desc', ''))
        
        # Simplified Chart Type
        df['Chart_Type'] = df['Category'].apply(lambda x: 'Village/Settlement' if x == 'Settlement' else 'Commercial/Inst.')
        
        return df
    except FileNotFoundError:
        return pd.DataFrame()

df = load_data()

# 4. SIDEBAR CONTROLS
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/c/c8/Sterling_Bank_Logo.svg/2560px-Sterling_Bank_Logo.svg.png", width=160)
st.sidebar.markdown("## 🛰️ Mission Controls")

available_lgas = sorted(df['LGA'].unique()) if not df.empty else []
selected_lgas = st.sidebar.multiselect(
    "📍 Select LGAs:", 
    available_lgas,
    default=available_lgas[:1] if available_lgas else None,
    help="Select LGAs to see detailed analysis."
)

available_cats = sorted(df['Category'].unique()) if not df.empty else []
selected_cats = st.sidebar.multiselect("🏢 Facility Types:", available_cats, default=available_cats)
priority = st.sidebar.slider("🔥 Priority Tier", 1, 3, (1, 3))

# 5. FILTERING
if not df.empty:
    filtered_df = df[
        (df['Category'].isin(selected_cats)) &
        (df['Priority_Tier'].between(priority[0], priority[1]))
    ]
    if selected_lgas:
        filtered_df = filtered_df[filtered_df['LGA'].isin(selected_lgas)]

    # 6. TABS
    tab1, tab2, tab3 = st.tabs(["🗺️ COMMAND MAP", "📊 STRATEGIC INTELLIGENCE", "📋 TARGET GRID"])

    # ==========================================
    # TAB 1: THE ULTIMATE MAP
    # ==========================================
    with tab1:
        c1, c2 = st.columns([3, 1])
        with c1:
            st.markdown(f"### 📍 Operational View ({len(filtered_df)} Targets)")
        with c2:
            total_selected_pop = filtered_df.drop_duplicates('LGA')['LGA_Actual_Pop'].sum()
            st.metric("Total Addressable Market (TAM)", f"{int(total_selected_pop):,}")

        if not filtered_df.empty:
            center_lat = filtered_df['Latitude'].mean()
            center_lon = filtered_df['Longitude'].mean()
            zoom = 12 if len(selected_lgas) == 1 else 9

            m = folium.Map(location=[center_lat, center_lon], zoom_start=zoom, control_scale=True)

            folium.TileLayer('CartoDB positron', name="Light Map (Clean)").add_to(m)
            folium.TileLayer('CartoDB dark_matter', name="Dark Map (High Contrast)").add_to(m)
            folium.TileLayer('OpenStreetMap', name="Street Map (Detailed)").add_to(m)
            folium.TileLayer(
                tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
                attr='Esri',
                name='Satellite Imagery',
                overlay=False
            ).add_to(m)

            heat_data = filtered_df[['Latitude', 'Longitude']].values.tolist()
            HeatMap(heat_data, name="Density Heatmap", radius=15, blur=10, show=False).add_to(m)

            marker_cluster = MarkerCluster(name="Target Clusters").add_to(m)

            for _, row in filtered_df.iterrows():
                if "Market" in str(row['Type']) or "Shop" in str(row['Type']):
                    color, icon_name = "red", "shopping-cart"
                elif "School" in str(row['Type']) or "College" in str(row['Type']):
                    color, icon_name = "green", "book"
                elif "Relig" in str(row['Category']):
                    color, icon_name = "purple", "bell"
                elif row['Category'] == "Settlement":
                    color, icon_name = "blue", "home"
                elif "Bank" in str(row['Type']) or "Finance" in str(row['Type']):
                     color, icon_name = "darkblue", "briefcase"
                else:
                    color, icon_name = "gray", "info-sign"

                popup_html = f"""
                <div style='font-family: "Segoe UI", sans-serif; width: 250px; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 5px rgba(0,0,0,0.3);'>
                    <div style="background-color: {color}; color: white; padding: 10px; font-weight: bold; font-size: 14px;">
                        <i class="fa fa-{icon_name}"></i> {row['Name']}
                    </div>
                    <div style="padding: 15px; background-color: #fff; color: #333;">
                        <p style="margin: 5px 0; font-size: 13px;"><b>📍 LGA:</b> {row['LGA']} ({row.get('Viability_Tier', 'N/A')})</p>
                        <p style="margin: 5px 0; font-size: 13px;"><b>🏢 Type:</b> {row['Type']}</p>
                        <p style="margin: 5px 0; font-size: 13px;"><b>👥 Estimate:</b> {row['Tentative_Population']}</p>
                        <hr style="margin: 10px 0; border: 0; border-top: 1px solid #eee;">
                        <a href="{row['Navigation_Link']}" target="_blank" style="text-decoration:none;">
                            <button style='width:100%; background-color:{color}; color:white; border:none; padding: 10px; border-radius: 4px; cursor:pointer; font-weight: bold; font-size: 13px; transition: background-color 0.3s;'>
                            <i class="fa fa-location-arrow"></i> NAVIGATE HERE
                            </button>
                        </a>
                    </div>
                </div>
                """
                folium.Marker(
                    [row['Latitude'], row['Longitude']],
                    popup=folium.Popup(popup_html, max_width=300),
                    tooltip=f"{row['Name']} | {row['Type']}",
                    icon=folium.Icon(color=color, icon=icon_name, prefix='fa')
                ).add_to(marker_cluster)

            Fullscreen(position='topright').add_to(m)
            MousePosition(position='bottomleft').add_to(m)
            MeasureControl(position='topleft', primary_length_unit='kilometers').add_to(m)
            MiniMap(toggle_display=True, position='bottomright').add_to(m)
            folium.LayerControl(collapsed=False).add_to(m)

            legend_html = """
             <div style="position: fixed; 
                         bottom: 50px; left: 50px; width: 180px; height: auto; 
                         border:1px solid #ccc; z-index:9999; font-size:13px;
                         background-color:rgba(255, 255, 255, 0.95); padding: 10px;
                         color: black !important;
                         border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.2);">
                 <b style="color:black;">🎯 Target Legend</b><br>
                 <div style="margin-top:5px; color:black;"><i class="fa fa-shopping-cart" style="color:red"></i> Markets/Comm.</div>
                 <div style="color:black;"><i class="fa fa-book" style="color:green"></i> Education</div>
                 <div style="color:black;"><i class="fa fa-bell" style="color:purple"></i> Religious</div>
                 <div style="color:black;"><i class="fa fa-home" style="color:blue"></i> Settlements</div>
                 <div style="color:black;"><i class="fa fa-briefcase" style="color:darkblue"></i> Financial</div>
                 <div style="color:black;"><i class="fa fa-info-sign" style="color:gray"></i> Other</div>
              </div>
             """
            m.get_root().html.add_child(folium.Element(legend_html))

            st_folium(m, width="100%", height=750)
        else:
            st.warning("No targets found.")

    # ==========================================
    # TAB 2: STRATEGIC INTELLIGENCE
    # ==========================================
    with tab2:
        st.markdown("### 📊 Market Viability Matrix")
        
        viability_summary = filtered_df.groupby('LGA').agg(
            Tier=('Viability_Tier', 'max'),
            Description=('LGA_Desc', 'max'),
            Actual_Population=('LGA_Actual_Pop', 'max'),
            Captured_Targets=('Name', 'count')
        ).reset_index().sort_values('Actual_Population', ascending=False)

        st.dataframe(
            viability_summary,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Actual_Population": st.column_config.ProgressColumn("Population Size", format="%d", min_value=0, max_value=420000),
                "Tier": st.column_config.TextColumn("Strategic Tier"),
            }
        )
        
        st.divider()

        st.markdown("### 🔬 Micro-Territory Analysis (Deep Dive)")
        
        if not selected_lgas:
            st.info("👈 Select LGAs in the sidebar to see detailed village breakdowns.")
        else:
            for lga_name in selected_lgas:
                lga_df = filtered_df[filtered_df['LGA'] == lga_name]
                if lga_df.empty: continue
                
                with st.expander(f"📍 {lga_name} Deep Dive ({len(lga_df)} Targets Found)", expanded=True):
                    m1, m2, m3 = st.columns(3)
                    lga_pop = LGA_DATA.get(lga_name, {}).get('pop', 0)
                    tier = LGA_DATA.get(lga_name, {}).get('tier', 'Unknown')
                    
                    m1.metric("Official Population", f"{lga_pop:,}", delta=tier)
                    m2.metric("Scraped Targets", len(lga_df))
                    m3.metric("Most Common Sector", lga_df['Type'].mode()[0] if not lga_df.empty else "N/A")
                    
                    st.divider()
                    
                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.markdown("#### 🏘️ Top Settlements (By Density)")
                        settlements = lga_df[lga_df['Category'] == 'Settlement'].sort_values('Market_Score', ascending=False).head(10)
                        st.dataframe(settlements[['Name', 'Tentative_Population', 'Navigation_Link']], hide_index=True, use_container_width=True, column_config={"Navigation_Link": st.column_config.LinkColumn("Map")})
                        
                    with col_b:
                        st.markdown("#### 💰 Top Commercial Hubs (By Traffic)")
                        commercial = lga_df[lga_df['Category'] != 'Settlement'].sort_values('Market_Score', ascending=False).head(10)
                        st.dataframe(commercial[['Name', 'Type', 'Tentative_Population', 'Navigation_Link']], hide_index=True, use_container_width=True, column_config={"Navigation_Link": st.column_config.LinkColumn("Map")})

    # ==========================================
    # TAB 3: DATA GRID
    # ==========================================
    with tab3:
        st.subheader("📋 Raw Data Explorer")
        st.dataframe(filtered_df[['Name', 'LGA', 'Viability_Tier', 'Type', 'Tentative_Population']], use_container_width=True)
        csv = filtered_df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download Report", csv, "Kogi_Report.csv", "text/csv")

else:
    st.warning("⚠️ No data loaded.")

# --- FOOTER (Added per request) ---
st.markdown("---")
st.caption("Created by Philip Osita | State Cluster Manager | Sterling Bank Plc")
```

- Run the below command to view the dashboard;
```
  streamlit run app.py --server.port 5010
```
 <img width="975" height="414" alt="image" src="https://github.com/user-attachments/assets/405ed16b-3dc1-46e8-92eb-0fda0a1ad20e" />

<img width="975" height="530" alt="image" src="https://github.com/user-attachments/assets/2a00435d-a15f-4e11-8771-d9fcf8eb2db9" />


#### Now, we are going to make our dashboard always running with out running the python command

- Create the Service File. Run;
```
vi /etc/systemd/system/kogi_dashboard.service
```
- Paste the below;
```
[Unit]
Description=Kogi Pathfinder Dashboard Service
After=network.target

[Service]
# 1. User
User=root

# 2. Directory (UPDATED TO MATCH YOUR PATH)
WorkingDirectory=/root/projects/kogi_pathfinder

# 3. Command (UPDATED TO MATCH YOUR PATH)
ExecStart=/root/projects/kogi_pathfinder/venv/bin/streamlit run app.py --server.port 5010 --server.address 0.0.0.0

# 4. Restart Logic
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

- Start the Service. Run;
```
systemctl daemon-reload
systemctl enable kogi_dashboard
systemctl start kogi_dashboard
```

- Check the status service. Run;
```
systemctl status kogi_dashboard
```
<img width="975" height="333" alt="image" src="https://github.com/user-attachments/assets/49f8be74-646b-48c5-b50a-5f90fe6d945e" />

### Conclusion
Project Pathfinder represents a paradigm shift in how Sterling Bank approaches market penetration in Kogi State. By moving from intuition-based prospecting to a data-driven "Precision Banking" model, we have effectively illuminated the blind spots where our competitors are absent and where the next wave of low-cost deposits resides.

This system delivers three immediate strategic advantages:

i.	Total Visibility: We now possess a live, navigable inventory of every economic cluster from the bustling markets of Okene to the remote rice farms of Ibaji eliminating the "visibility gap" that previously stalled our rural expansion.

ii.	Operational Efficiency: Field teams are no longer driving aimlessly. With GPS-guided targets and population estimates, every trip is optimized for maximum account acquisition, significantly reducing fuel costs and man-hours per lead.

iii.	Competitive Dominance: By identifying and rating "Tier 1" and "Tier 2" markets before others do, we secure the first-mover advantage, locking down critical mass-market territories and institutional relationships.

The successful deployment of this Geospatial Engine on a dedicated VPS ensures that this intelligence is available 24/7 to decision-makers and field officers alike. As we move into the execution phase, this tool will serve as the central nervous system for our customer acquisition and deposit mobilization strategy, ensuring that Sterling Bank does not just compete in Kogi State, but dominates it.

