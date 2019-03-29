from flask import (
    current_app, abort, json, render_template, make_response, Response)
from flask.views import MethodView


class BaseView(MethodView):
    def __init__(self, *args, **kwargs):
        self.app = current_app._get_current_object()
        super(BaseView, self).__init__(*args, **kwargs)

    def json_response(self, status=200, data={}, headers={}):
        """
        Json response that allows headers injection
        """
        mimetype = 'application/json'
        return Response(
            json.dumps(data), status=status, mimetype=mimetype,
            headers=headers)

    def render_template(self, template_name, **values):
        return render_template(template_name, **values)

    def template_response(self, template_name, headers={}, **values):
        """
        Constructs a response, allowing custom template name and content_type
        """
        response = make_response(
            self.render_template(template_name, **values))

        for field, value in headers.items():
            response.headers.set(field, value)

        return response

    def get(self, *args, **kwargs):
        abort(400)

    def post(self, *args, **kwargs):
        abort(400)

    def put(self, *args, **kwargs):
        abort(400)

    def patch(self, *args, **kwargs):
        abort(400)

    def delete(self, *args, **kwargs):
        abort(400)


class BaseResourceView(BaseView):

    def get(self, *args, **kwargs):
        return self.json_response(400)

    def post(self, *args, **kwargs):
        return self.json_response(400)

    def put(self, *args, **kwargs):
        return self.json_response(400)

    def patch(self, *args, **kwargs):
        return self.json_response(400)

    def delete(self, *args, **kwargs):
        return self.json_response(400)
