"""
ml4k module
"""
import io
import base64
import requests
import time
import collections
from PIL import Image

from . import errors

BASE_URL = 'https://machinelearningforkids.co.uk/api/scratch/{api_key}'
DATA_LIMIT_MB = 2  # taxinomitis has a 3mb limit for base64-encoded data
THROTTLE_SECONDS = 1  # throttle requests to at one second between each call


def optimize_image(image):
    output = io.BytesIO()
    image.thumbnail((1920, 1920), Image.ANTIALIAS)
    image.save(output, optimize=True, quality=85, format=image.format)
    return output.getvalue()


def check_response(response):
    if not response.ok:
        try:
            response.raise_for_status()
        except Exception as error:
            error_data = None
            if hasattr(error, 'response'):
                try:
                    error_data = error.response.json()
                except Exception:
                    pass

            if error_data is None:
                # No useful error data, raise original error
                raise

            if error_data.get('error'):
                raise errors.APIError(error_data['error'])
            else:
                raise errors.APIError(str(error))


class Model:
    """
    Represents a ML4K model with a given API key
    """
    def __init__(self, api_key, project_type='text'):
        self.api_key = api_key
        self.project_type = project_type
        self.base_url = BASE_URL.format(api_key=api_key)

    def classify(self, data):
        """
        Classify the given text using your model
        """
        url = self.base_url + '/classify'

        # Handle binary data
        if isinstance(data, bytes):
            data_limit = DATA_LIMIT_MB * 1024 * 1024

            # Check if data is an image and try to optimize it if it's too big.
            try:
                image = Image.open(io.BytesIO(data))
            except IOError:
                pass
            else:
                if len(data) > data_limit:
                    data = optimize_image(image)

            # Ensure final data is within the size limit
            if len(data) > data_limit:
                raise ValueError('Data must be less than {} MB'.format(DATA_LIMIT_MB))

            # Convert to Base64
            data = base64.b64encode(data).decode()

        response = requests.post(url, json={'data': data})
        check_response(response)
        time.sleep(THROTTLE_SECONDS)

        response_data = response.json()
        return response_data[0]

    def add_training_data(self, label, data):
        """
        Add training data to your model using Python instead of the train page.

        Parameters:
        label (string): The label you want to add data to
        data: A string or list with the training data you want to add
        """
        url = self.base_url + '/train'

        # build params (the API doesn't have a POST method for adding training data)
        body = {
            'label': label,
            'data': None
        }
        if isinstance(data, str):
            body['data'] = data
        elif isinstance(data, collections.Iterable):
            body['data'] = []
            for item in data:
                body['data'].append(item)
        else:
            raise ValueError("data must be a string or a list")

        response = requests.post(url, json=body)
        check_response(response)
        time.sleep(THROTTLE_SECONDS)

        return response.json()
