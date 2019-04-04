from cocktail_apikit import ValidationError


def validate_payload_required_fields(payload: dict = None, required_fields: list = None, allow_null: bool = False):
    """
    Util method used to check if required field list are all including in payload data, allow_null means accept None value 
    """
    payload = payload or {}
    required_fields = required_fields or []


    for key in required_fields:
        if key not in payload:
            raise ValidationError({"msg":"Required field: <{}> is missing!".format(key)})
        elif not allow_null and not payload.get(key):
            raise ValidationError({"msg": "Required field: <{}> can not be <null> !".format(key)})

    return True
