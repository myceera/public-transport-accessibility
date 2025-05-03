# Public Transport Accessibility (Training Project)

This is a practice project to visualize the coverage of public transport stops in a city using buffer zones and geospatial analysis with Python.

## What it does

- Loads GTFS stop data and city districts
- Creates buffers around transport stops (300/500/800 meters)
- Calculates % of each district's area within walking distance
- Generates PNG maps showing accessibility

## Tools

- Python (geopandas, matplotlib, shapely)
- GTFS `stops.txt` file
- City district polygons in GeoJSON

## Output

Three maps for 300m, 500m, and 800m accessibility zones plus a combined map with all of them together.

## License

MIT
