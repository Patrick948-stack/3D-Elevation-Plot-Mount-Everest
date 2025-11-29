import rasterio
import csv

# --- Input and Output ---
input_path = "1984_AP_DEM.tif"        # my DEM file
output_path = "everest_elevations.csv"  # output CSV file

with rasterio.open(input_path) as src:
    band = src.read(1)            # elevation values
    transform = src.transform     # pixel-to-coordinate transform

    rows, cols = band.shape

    with open(output_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["lat", "lon", "elevation"])

        for i in range(rows):
            for j in range(cols):
                lon, lat = rasterio.transform.xy(transform, i, j)
                elev = band[i, j]

                # Some DEMs use a fill value like -32768 or -9999 for "no data"
                if elev == src.nodata:
                    continue

                writer.writerow([lat, lon, float(elev)])
