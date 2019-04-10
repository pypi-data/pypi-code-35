from json import loads, dumps

from pandas.io.json import json_normalize
from rest_framework import exceptions, status
from rest_framework.exceptions import APIException

from shipmnts_utils.firestore.firestore_init import initialize_firestore

fs_client = initialize_firestore()


class GeneratorCheck:
    def __init__(self, iter):
        self.source = iter
        self.stored = False

    def __iter__(self):
        return self

    def __nonzero__(self):
        if self.stored:
            return True
        try:
            self.value = next(self.source)
            self.stored = True
        except StopIteration:
            return False
        return True

    def __next__(self):
        if self.stored:
            self.stored = False
            return self.value
        return next(self.source)


def make_keys_to_dot(d):
    """
    Flattens the dictionary containing other dictionaries like here:
    https://stackoverflow.com/questions/6027558/flatten-nested-python-dictionaries-compressing-keys
    """
    df = json_normalize(d, sep=".")
    return df.to_dict(orient="records")[0]


def document_exists(collection, job_id, child_doc_id=None):
    """
    :param collection: name of firestore collection
    :param job_id: job id
    :param child_doc_id: child document id
    :return: document_ref (persistent generator) and flag
    """
    if child_doc_id:
        document_ref = (
            fs_client.collection(collection)
            .where("job_id", "==", job_id)
            .where("child_doc_id", "==", child_doc_id)
            .where("type", "==", "saved")
            .get()
        )
    else:
        document_ref = (
            fs_client.collection(collection)
            .where("job_id", "==", job_id)
            .where("type", "==", "saved")
            .get()
        )

    # return list(document_ref), True if GeneratorCheck(document_ref) else False
    return list(document_ref), bool(GeneratorCheck(document_ref))


def does_data_exist_in_generator(doc):
    """
    :param doc: generator obj
    :return: flag
    """
    for _data in doc:
        yield _data
        return True
    return False


def nested_ordered_dict_to_dict(input_ordered_dict):
    return loads(dumps(input_ordered_dict))


def record_not_found_error(message):
    """
    :param message: the message to be printed
    """
    raise exceptions.NotFound(message)


class RequestBodyNotAcceptable(APIException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    default_detail = "Unprocessable Entity"
    default_code = "unprocessable_entity"