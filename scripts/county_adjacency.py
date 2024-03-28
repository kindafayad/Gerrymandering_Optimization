import pandas as pd

df = pd.read_csv('data/County_Adjacency_Matrix.csv', header=0, index_col=0)
counties_geoId = df.index # list of all counties geoid 

def check_county_adjacency(county1GeoId, county2GeoId) -> int:
    return df.loc[county1GeoId, f"{county2GeoId}"]