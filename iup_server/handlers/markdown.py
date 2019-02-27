import functools
import logging

import markdown
from flask import render_template_string

from ..sitepage import SitePage


def MarkdownHandler(sitepage: SitePage):
    page = sitepage.page
    if not 'template' in page['dir']:
        template_path = page['dir'] + '/index.md'
    else:
        template_path = page['template']
    bc = sitepage.get_breadcrumb(sitepage.pagesdict, sitepage.dictpath)
    pd = sitepage.get_path_depth()

    try:
        with sitepage.app.open_resource(
            'content' + template_path, mode='r'
        ) as f:
            template = f.read()
    except FileNotFoundError:
        logging.exception('Content file not found')
        return

    template = markdown.markdown(template)

    sitepage.app.add_url_rule(
        rule=page['dir'] + '/',
        endpoint='/'.join(bc) + '/',
        view_func=functools.partial(
            render_template_string,
            template,
            breadcrumb=bc,
            pathdepth=pd,
            siblings=sitepage.siblings,
            subpages=sitepage.subpages,
            parent=sitepage.parent,
        ),
    )
