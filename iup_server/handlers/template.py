import functools
from flask import render_template
from ..sitepage import SitePage


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
