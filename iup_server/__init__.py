from datetime import datetime
import os
import typing as t

from flask import Flask, send_file, render_template, request
from flask_gopher import GopherExtension
import toml

from .constants import PAGEATTRIBS
from .sitepage import SitePage
from .handlers import HANDLERS
from .atom import generate_atom


def register_pages(app, gopher, pagesdict, path, page=None):
    ''' Walk through pages tree and registers every page within '''
    if not page:
        page = pagesdict

    handler = HANDLERS[page['handler']]

    subpage_indices = list(filter(lambda x: x not in PAGEATTRIBS, page))
    subpages = [page[x] for x in subpage_indices]

    SitePage(
        handler=handler, pagesdict=pagesdict,
        dictpath=path, app=app, gopher=gopher
    ).register()

    for name, sp in zip(subpage_indices, subpages):
        register_pages(app, gopher, pagesdict, path + [name], sp)


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    gopher = GopherExtension(app)

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
    register_pages(app, gopher, pages, [])

    # Add favicon definition, because it is special
    @app.route('/favicon.ico')
    def route_favicon():
        return send_file('static/favicon.ico')

    # Add error handlers
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    # Add Atom/RSS feed
    @app.route('/atom.xml')
    def route_atom():
        return generate_atom(pages)

    return app
