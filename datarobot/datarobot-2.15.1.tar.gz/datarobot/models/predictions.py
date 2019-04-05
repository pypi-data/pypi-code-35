from six.moves.urllib_parse import urlencode
import trafaret as t
from datarobot import enums
from ..utils import from_api, raw_prediction_response_to_dataframe, encode_utf8_if_py2
from .api_object import APIObject

_base_path = 'projects/{}/predictions/'
_get_path = _base_path + '{}/'


class Predictions(APIObject):
    """
    Represents predictions metadata and provides access to prediction results.

    Attributes
    ----------
    project_id : str
        id of the project the model belongs to
    model_id : str
        id of the model
    prediction_id : str
        id of generated predictions

    Examples
    --------

    List all predictions for a project

    .. code-block:: python

        import datarobot as dr

        # Fetch all predictions for a project
        all_predictions = dr.Predictions.list(project_id)

        # Inspect all calculated predictions
        for predictions in all_predictions:
            print(predictions)  # repr includes project_id, model_id, and dataset_id

    Retrieve predictions by id

    .. code-block:: python

        import datarobot as dr

        # Getting predictions by id
        predictions = dr.Predictions.get(project_id, prediction_id)

        # Dump actual predictions
        df = predictions.get_all_as_dataframe()
        print(df)
    """

    def __init__(self, project_id, prediction_id, model_id=None, dataset_id=None):
        self.project_id = project_id
        self.model_id = model_id
        self.dataset_id = dataset_id
        self.prediction_id = prediction_id
        self.path = _get_path.format(self.project_id, self.prediction_id)

    @classmethod
    def _build_list_path(cls, project_id, model_id=None, dataset_id=None):
        args = {}
        if model_id:
            args['modelId'] = model_id
        if dataset_id:
            args['datasetId'] = dataset_id

        path = _base_path.format(project_id)
        if args:
            path = '{}?{}'.format(path, urlencode(args))

        return path

    @classmethod
    def list(cls, project_id, model_id=None, dataset_id=None):
        """
        Fetch all the computed predictions metadata for a project.

        Parameters
        ----------
        project_id : str
            id of the project
        model_id : str, optional
            if specified, only predictions metadata for this model will be retrieved
        dataset_id : str, optional
            if specified, only predictions metadata for this dataset will be retrieved

        Returns
        -------
        A list of :py:class:`Predictions <datarobot.models.Predictions>` objects
        """
        _trafaret = t.Dict({
            t.Key('data'): t.List(t.Dict({
                t.Key('id'): t.String(),
                t.Key('url'): t.String(),
                t.Key('model_id'): t.String(),
                t.Key('dataset_id'): t.String(),
            }).ignore_extra('*')),
        }).ignore_extra('*')

        path = cls._build_list_path(project_id, model_id=model_id, dataset_id=dataset_id)
        converted = from_api(cls._server_data(path))
        validated = _trafaret.check(converted)['data']
        return [
            cls(project_id,
                prediction_id=item['id'],
                model_id=item['model_id'],
                dataset_id=item['dataset_id'])
            for item in validated]

    @classmethod
    def get(cls, project_id, prediction_id):
        """
        Retrieve the specific predictions metadata

        Parameters
        ----------
        project_id : str
            id of the project the model belongs to
        prediction_id : str
            id of the prediction set

        Returns
        -------
        :py:class:`Predictions <datarobot.models.Predictions>` object representing specified
        predictions
        """
        return cls(project_id, prediction_id)

    def get_all_as_dataframe(self, class_prefix=enums.PREDICTION_PREFIX.DEFAULT):
        """
        Retrieve all prediction rows and return them as a pandas.DataFrame.

        Parameters
        ----------
        class_prefix : str, optional
            The prefix to append to labels in the final dataframe. Default is ``class_``
            (e.g., apple -> class_apple)

        Returns
        -------
        dataframe: pandas.DataFrame
        """
        data = self._server_data(self.path)
        return raw_prediction_response_to_dataframe(data, class_prefix)

    def download_to_csv(self, filename, encoding='utf-8'):
        """
        Save prediction rows into CSV file.

        Parameters
        ----------
        filename : str or file object
            path or file object to save prediction rows
        encoding : string, optional
            A string representing the encoding to use in the output file, defaults to
            'utf-8'
        """
        df = self.get_all_as_dataframe()
        df.to_csv(
            path_or_buf=filename,
            header=True,
            index=False,
            encoding=encoding,
        )

    def __repr__(self):
        template = u'{}(prediction_id={!r}, project_id={!r}, model_id={!r}, dataset_id={!r})'
        return encode_utf8_if_py2(template.format(
            type(self).__name__,
            self.prediction_id,
            self.project_id,
            self.model_id,
            self.dataset_id))
