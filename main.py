import pandas as pd
import geopandas as gpd

# --------------------------
# 1. Convert shapefiles to GeoJSON
# --------------------------
gdf_points = gpd.read_file("ne_10m_geography_regions_points/ne_10m_geography_regions_points.shp")
gdf_points.to_file("ne_10m_geography_regions_points.json", driver="GeoJSON")

gdf_polys = gpd.read_file("ne_110m_geography_regions_polys/ne_110m_geography_regions_polys.shp")
gdf_polys.to_file("ne_110m_geography_regions_polys.geojson", driver="GeoJSON")

# --------------------------
# 2. Fix aliases in IHME dataset (Côte d'Ivoire, Laos, etc.)
# --------------------------
file_path = "IHME-GBD_2021_DATA-6b23a41d-1.csv"
df = pd.read_csv(file_path)

# Handle Côte d'Ivoire alias variations
ivory_rows = df[df["location_name"] == "Côte d'Ivoire"]

# Add alternative name variations
ivory_aliases = []
for alt_name in ["Côte d’Ivoire", "Ivory Coast"]:
    temp = ivory_rows.copy()
    temp["location_name"] = alt_name
    ivory_aliases.append(temp)

# Handle Laos alias
laos_rows = df[df["location_name"] == "Lao People's Democratic Republic"]
laos_alias = laos_rows.copy()
laos_alias["location_name"] = "Laos"

# Combine everything
df_updated = pd.concat([df] + ivory_aliases + [laos_alias], ignore_index=True)

# Save cleaned version
df_updated.to_csv(file_path, index=False)
print(f"IHME dataset cleaned and saved to {file_path}")

# --------------------------
# 3. Generate cause_of_deaths_total.csv with clean country names
# --------------------------
df = pd.read_csv("cause_of_deaths.csv")

# Clean known country mismatches for mapping
df["Country/Territory"] = df["Country/Territory"].replace({
    "Democratic Republic of Congo": "Dem. Rep. Congo",
    "Côte d'Ivoire": "Ivory Coast",
    "Lao People's Democratic Republic": "Laos",
    "United States": "United States of America",
    "Syrian Arab Republic": "Syria",
    "South Sudan": "S. Sudan"
})

# Identify cause columns (everything except these three)
cause_cols = [c for c in df.columns if c not in ["Country/Territory", "Code", "Year"]]

# Sum across all causes per country per year
df["TotalDeaths"] = df[cause_cols].sum(axis=1)

# Save new CSV
df.to_csv("cause_of_deaths_total.csv", index=False)
print("✅ cause_of_deaths_total.csv generated successfully.")
