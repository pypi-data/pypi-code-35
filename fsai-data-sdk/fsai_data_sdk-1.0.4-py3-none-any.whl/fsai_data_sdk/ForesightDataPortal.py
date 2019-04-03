
from .foresight_request_helper import get
from .data_object.Dataset import Dataset

ROOT_END_POINT = "https://demo.foresight.ai/public-api"

GET_DATA_END_POINT = ROOT_END_POINT + "/v10/data"


class ForesightDataPortal:
    """ForesightDataPortal class provide entry functions to get data from Foresight Data Portal"""
    def __init__(self, api_key, secret):
        self.api_key = api_key
        self.secret = secret

    def get_data_at(self, lng, lat, radius, layers):
        """Receive data at a specific location.
        Parameters
        ----------
        lng : number
            Longitude of the locations
        lat : number
            Latitude of location
        radius: int
            Radius in meter of the area, must between 200...5000
        layers: list of string
            layers to be received. Supported: 'SEMANTIC_2D', 'DYNAMIC_OBJECTS'
        Returns
        ----------
        List
         list of data_object.Dataset objects.
        """
        assert len(layers) > 0, 'layers must be provided'
        assert (lng is not None and lat is not None),  'Lng and lat of the position must be provided'
        assert 200 <= radius <= 5000, 'radius should be between 200 and 5000'

        # create query parameters and call rest API
        request_params = {'lng': lng, 'lat': lat, 'radius': radius, 'layers': ','.join(layers)}
        datasets = get(self.api_key, self.secret, GET_DATA_END_POINT, request_params)

        # build result Dataset list
        result = []
        if datasets:
            for dataset in datasets:
                result.append(Dataset(dataset))

        return result


