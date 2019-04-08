from functools import lru_cache
from setupy.core.model import Setup
from setupy.core.serialize import serialize
from setupy.errors import FeatureNotFoundError, SettingNotFoundError
import os
from flask import Flask, render_template, Response, request
from setupy.loaders import FileDependencyLoader

DIR_PATH = os.path.dirname(os.path.realpath(__file__))

app = Flask(__name__)

feature_path = os.environ.get('SETUPY_FEATURES',
                              os.path.join(DIR_PATH, "../features"))
settings_path = os.environ.get('SETUPY_SETTINGS',
                               os.path.join(DIR_PATH, "../settings"))

dependency_loader = FileDependencyLoader(feature_path, settings_path)


@lru_cache()
def _feature_names():
    return dependency_loader.feature_names()


@lru_cache()
def _setting_names():
    return dependency_loader.setting_names()


def _make_setup_file(features, settings, include_help):
    if 'base' not in settings:
        settings.insert(0, 'base')
    if 'merge' not in features:
        features.insert(0, 'merge')

    setup = Setup(dependency_loader)

    missing_features = []
    missing_settings = []

    try:
        for f in features:
            setup.add_feature(f)
    except FeatureNotFoundError:
        missing_features.append(f)

    try:
        for s in settings:
            setup.add_setting(s)
    except SettingNotFoundError:
        missing_settings.append(s)

    setup_file_contents = serialize(setup, include_help)

    not_found_features = '\n'.join(f'# Feature {f} was not found' for f in missing_features)
    not_found_settings = '\n'.join(f'# Setting {s} was not found' for s in missing_settings)
    error_text = f'{not_found_features}\n{not_found_settings}'
    return f'{setup_file_contents}\n\n{error_text}'

@app.route('/')
def index():
    return render_template(
            'index.html',
            features=dependency_loader.feature_names(),
            settings=dependency_loader.setting_names())


@app.route('/get', methods=['GET'])
def get_setup_file():
    setting_names = request.args.get('settings', '').split(',')
    feature_names = request.args.get('features', '').split(',')

    response_text = _make_setup_file(
        feature_names,
        setting_names,
        request.args.get('include_help', False) != False)

    return Response(response_text, mimetype='text/plain')


@app.route('/post', methods=['POST'])
def get_setup_file_posted():
    """
    This method does the same thing as get but exists as a fallback
    for when javascript is not enabled in the browser.  In that case
    the multiselect contents cannot be sent as a comma delineated list
    and must be read out of the form contents.
    """
    setting_names = request.form.getlist('settings')
    feature_names = request.form.getlist('features')

    response_text = _make_setup_file(
        feature_names,
        setting_names,
        request.form.get('include_help') == 'on')

    return Response(response_text, mimetype='text/plain')
