import geopandas as gpd
import pandas as pd


def load_gtfs_stops(path_to_stops_txt):
    """
    Load GTFS stops.txt and return as projected GeoDataFrame (EPSG:3857)
    """
    df = pd.read_csv(path_to_stops_txt)
    df = df.dropna(subset=['stop_lat', 'stop_lon'])  # remove missing coordinates
    gdf = gpd.GeoDataFrame(
        df,
        geometry=gpd.points_from_xy(df.stop_lon, df.stop_lat),
        crs='EPSG:4326'
    )
    return gdf.to_crs(epsg=3857)


def create_buffers(stops_gdf, distances=[300, 500, 800]):
    """
    Add buffer columns (in meters) for each specified distance
    """
    for d in distances:
        stops_gdf[f'buffer_{d}'] = stops_gdf.geometry.buffer(d)
    return stops_gdf


def union_buffers(stops_gdf, distances=[300, 500, 800]):
    """
    Merge all buffers for each distance into one geometry (MultiPolygon)
    """
    return {
        d: stops_gdf[f'buffer_{d}'].unary_union
        for d in distances
    }


def load_districts(path_to_geojson):
    """
    Load district polygons and project to EPSG:3857
    """
    districts = gpd.read_file(path_to_geojson)
    return districts.to_crs(epsg=3857)


def calculate_coverage(districts_gdf, buffer_geom):
    """
    Calculate coverage ratio for each district:
    share of district area covered by buffer geometry
    """
    return districts_gdf.geometry.apply(
        lambda x: x.intersection(buffer_geom).area / x.area
    )


def add_coverage_columns(districts, buffer_unions):
    """
    Add columns with raw and percentage coverage for each distance
    """
    for d, geom in buffer_unions.items():
        districts[f'coverage_{d}'] = calculate_coverage(districts, geom)
        districts[f'coverage_{d}_pct'] = (districts[f'coverage_{d}'] * 100).round(1)
    return districts
