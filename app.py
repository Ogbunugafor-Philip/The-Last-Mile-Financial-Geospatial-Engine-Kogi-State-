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