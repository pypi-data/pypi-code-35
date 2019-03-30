import logging

class Experiment():
    """
    Returned when an experiment has been loaded.

    Contains helper methods.
    """

    def __init__(self, experiment, mr_client, cache_location=None):

        self._logger = logging.getLogger("Experiment")

        self._cache_location = cache_location

        self.files = experiment['files']
        self.meta = experiment['meta']
        self.parents = experiment['parents']

        self.id = experiment['id']

        self._mr = mr_client

        self._logger.info('Experiment Info:')
        for k_m, v_m in experiment['meta'].items():
            self._logger.info('%s: %s' % (k_m, str(v_m)))

    def get_file(self, filename):
        """
        Get a file handle by it's filename
        :return: a BufferedReader containing the file
        """

        if self._cache_location is None:
            return None

        file_info = self.get_file_info(filename)
        cached_filename = self._cache_location.joinpath(file_info['id'])
        return open(str(cached_filename), 'rb')

    def get_file_info(self, filename):
        """
        Get a file info by it's filename
        :param filename:
        :return:
        """

        for f in self.files:
            if f['filename'] == filename:
                return f

    def load_parents(self, ignore_files=False):
        """
        Loads all the parents
        :param ignore_files: Will not automatically download files associated with the parent
        :return:
        """

        loaded_parents = []

        for parent in self.parents:
            loaded_parent = self._mr.load(parent['id'], parent['metaCategory'], ignore_files)
            loaded_parents.append(loaded_parent)

        return loaded_parents

