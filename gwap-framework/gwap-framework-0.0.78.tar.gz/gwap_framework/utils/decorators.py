from functools import wraps
from typing import List

from flask import request
from gwap_framework.models.base import BaseModel


def validate_schema(input_schema: BaseModel, output_schema: BaseModel = None):
    def validate(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            partial = True if request.method.lower() == 'patch' else False
            if input_schema:
                input_schema_obj = input_schema(request.json)
                input_schema_obj.validate(partial=partial)
                kwargs.setdefault('request_model', input_schema_obj)
            response_obj = fn(*args, **kwargs)
            if output_schema and response_obj:
                if isinstance(response_obj, List):
                    result = []
                    for obj in response_obj:
                        output_schema_obj = output_schema(obj)
                        output_schema_obj.validate(partial=partial)
                        result.append(output_schema_obj.to_primitive())
                    return result
                output_schema_obj = output_schema(response_obj)
                output_schema_obj.validate(partial=partial)
                return output_schema_obj.to_primitive()
            return response_obj
        return wrapper
    return validate

def query_string():
    def query_string(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            response_obj = fn(*args, **{**kwargs, **request.args.to_dict()})
            return response_obj
        return wrapper
    return query_string
