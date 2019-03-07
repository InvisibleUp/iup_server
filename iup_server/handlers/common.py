import functools
import logging
import typing as t

from flask import send_from_directory, abort
from ..sitepage import SitePage

def send_dir_contents(dir: str, path: str):
    return send_from_directory('content' + dir, path)

def load_raw_template(
    sitepage: SitePage,
    template_path: str
) -> t.Optional[str]:
    try:
        with sitepage.app.open_resource('content' + template_path) as f:
            return f.read().decode()
    except FileNotFoundError:
        abort(404)

def add_sitepage_rule(sitepage: SitePage, ext: str, fcn):
    page = sitepage.page
    template_path = page['dir'] + '/index' + ext
    bc = sitepage.get_breadcrumb(sitepage.pagesdict, sitepage.dictpath)
    pd = sitepage.get_path_depth()

    sitepage.app.add_url_rule(
        rule=page['dir'] + '/',
        endpoint='/'.join(bc) + '/',
        view_func=functools.partial(
            fcn,
            sitepage=sitepage,
            template_path=template_path,
            breadcrumb=bc,
            pathdepth=pd
        ),
    )

    sitepage.app.add_url_rule(
        rule=page['dir'] + '/<path:path>',
        endpoint='/'.join(bc) + '/<path:path>',
        view_func=functools.partial(send_dir_contents, dir=page['dir'])
    )