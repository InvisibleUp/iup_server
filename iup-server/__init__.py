from datetime import datetime
import functools
import operator
import os
import typing as t
import logging

from flask import Flask, render_template
import toml

PAGEATTRIBS = ['title', 'series', 'dir', 'handler', 'template']

# https://stackoverflow.com/a/1469274/
def _subdict_from_key_list(d, l, subkey=None):
    return functools.reduce(operator.getitem, l, d)


class SitePage:
    handler: t.Callable
    pagesdict: t.Dict[str, t.Any]
    dictpath: t.List[str]
    app: t.Any

    # Derived from pages dict
    page: t.Dict[str, t.Any]
    subpages: t.List[t.Dict[str, t.Any]]
    parent: t.Optional[t.Dict[str, t.Any]]
    siblings: t.List[t.Dict[str, t.Any]]

    def __init__(self, handler, pagesdict, dictpath, app):
        self.handler = handler
        self.pagesdict = pagesdict
        self.dictpath = dictpath
        self.app = app

        self.page = _subdict_from_key_list(pagesdict, dictpath)
        subpage_indices = list(
            filter(lambda x: x not in PAGEATTRIBS, self.page)
        )
        self.subpages = [self.page[x] for x in subpage_indices]
        if len(dictpath) > 0:
            self.parent = _subdict_from_key_list(pagesdict, dictpath[0:-1])
            sib_indices = list(
                filter(lambda x: x not in PAGEATTRIBS, self.parent)
            )
            self.siblings = [self.parent[x] for x in sib_indices]
        else:
            self.parent = None
            self.siblings = []

    def get_breadcrumb(self, pages, path, bc=None) -> t.List[str]:
        if bc == None:
            bc = []

        if len(path) > 0:
            subpage = pages[path[0]]
            if subpage['title']:
                bc.append(subpage['title'])
            return self.get_breadcrumb(subpage, path[1:], bc)
        else:
            return bc

    def get_path_depth(self):
        if self.page['dir'] == '/':
            return 0
        return self.page['dir'].count('/')

    def register(self):
        self.handler(self)


def TemplateHandler(sitepage: SitePage):
    page = sitepage.page
    if not 'template' in page['dir']:
        template = page['dir'] + '/index.html'
    else:
        template = page['template']
    bc = sitepage.get_breadcrumb(sitepage.pagesdict, sitepage.dictpath)
    pd = sitepage.get_path_depth()

    sitepage.app.add_url_rule(
        rule=page['dir'],
        endpoint='/'.join(bc),
        view_func=functools.partial(
            render_template,
            template,
            breadcrumb=bc,
            pathdepth=pd,
            siblings=sitepage.siblings,
            subpages=sitepage.subpages,
            parent=sitepage.parent,
        ),
    )


HANDLERS = {
    'TemplateHandler': TemplateHandler,
    'MarkdownHandler': TemplateHandler,
}


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

    return app
