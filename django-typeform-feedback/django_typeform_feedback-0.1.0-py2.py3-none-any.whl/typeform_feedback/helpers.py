class SimpleUserFeedback:
    pk = None
    url = None
    status = None
    object = None

    def __init__(self, id, url, status, user_object=None):
        self.pk = id
        self.url = url
        self.status = status
        self.object = user_object
