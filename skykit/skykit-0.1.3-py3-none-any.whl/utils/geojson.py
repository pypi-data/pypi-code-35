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


def polygon_to_geojson(coordinates):
    new_coordinates = [[x, y] for (x, y) in coordinates]
    return {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [new_coordinates]
                }
            }
        ]
    }
