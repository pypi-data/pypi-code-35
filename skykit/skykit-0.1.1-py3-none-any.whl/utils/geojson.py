def point_to_geojson(coordinates):
    (x, y) = coordinates
    return {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {},
                "geometry": {
                    "type": "Point",
                    "coordinates": [x, y]
                }
            }
        ]
    }
