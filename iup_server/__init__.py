from datetime import datetime
import os
import typing as t

from flask import Flask, send_file
import toml

from .constants import PAGEATTRIBS
from .sitepage import SitePage
from .handlers import HANDLERS


def register_pages(app, pagesdict, path, page=None):
    ''' Walk through pages tree and registers every page within '''
    if not page:
        page = pagesdict

    handler = HANDLERS[page['handler']]

    subpage_indices = list(filter(lambda x: x not in PAGEATTRIBS, page))
    subpages = [page[x] for x in subpage_indices]

    SitePage(
        handler=handler, pagesdict=pagesdict, dictpath=path, app=app
    ).register()

    for name, sp in zip(subpage_indices, subpages):
        register_pages(app, pagesdict, path + [name], sp)


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'iup.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Set up default Jinja context
    @app.context_processor
    def default_context():
        return {'now': datetime.now()}

    # Add page definitions
    with app.open_resource('content/content.toml', mode='r') as f:
        pages = toml.load(f)
    register_pages(app, pages, [])

    # Add favicon definition, because it is special
    @app.route('/favicon.ico')
    def route_favicon():
        return send_file('static/favicon.ico')

    return app
