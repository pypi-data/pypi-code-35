def handle_raise_exception(payload):
    raise Exception()


def handle_raise_proto_exception(payload):
    raise Exception()


def handle_json(payload):
    print(f"JSON received:\n{payload}")


def handle_proto(payload):
    print(f"Proto received:\n{str(payload)}")
