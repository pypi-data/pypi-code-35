from falcon import HTTP_NOT_FOUND


class Resource:
    use_token = False
    storage = {}

    def on_get(self, req, resp, **kwargs):
        resp.status = HTTP_NOT_FOUND

    def on_post(self, req, resp, **kwargs):
        resp.status = HTTP_NOT_FOUND

    def on_put(self, req, resp, **kwargs):
        resp.status = HTTP_NOT_FOUND

    def on_delete(self, req, resp, **kwargs):
        resp.status = HTTP_NOT_FOUND
