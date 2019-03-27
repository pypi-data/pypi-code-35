from logging import getLogger

import os
import flask.views
import flasgger

from gumo.task_emulator._configuration import configure
from gumo.task_emulator.domain.configuration import TaskEmulatorConfiguration
from gumo.task_emulator.presentation.cli.worker import BackgroundWorker


def task_emulator_app():
    from gumo.task_emulator.presentation.restapi import emulator_api_blueprint
    from gumo.task_emulator.presentation.ui import emulator_ui_blueprint

    flask_app = flask.Flask(__name__)
    flask_app.config['JSON_AS_ASCII'] = False
    flask_app.config['SWAGGER'] = {
        'title': 'Task Emulator',
        'doc_dir': os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'apidoc',
        )
    }
    flask_app.register_blueprint(emulator_api_blueprint)
    flask_app.register_blueprint(emulator_ui_blueprint)

    flasgger.Swagger(
        flask_app,
        template_file=os.path.join(flask_app.config['SWAGGER']['doc_dir'], 'template.yml')
    )

    return flask_app, BackgroundWorker.get_instance()


__all__ = [
    configure.__name__,

    TaskEmulatorConfiguration.__name__,

    task_emulator_app.__name__,
]

logger = getLogger('gumo.task_emulator')
