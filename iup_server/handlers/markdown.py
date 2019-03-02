import functools
import logging

import markdown
from flask import render_template_string

from ..sitepage import SitePage

def MarkdownRunner(sitepage, template_path, breadcrumb, pathdepth):
    try:
        with sitepage.app.open_resource(
            'content' + template_path, mode='r'
        ) as f:
            template = f.read()
    except FileNotFoundError:
        logging.exception('Content file not found')
        return

    template = (
        "{% include '_header.html' %}\n"
        + markdown.markdown(template)
        + "\n{% include '_footer.html' %}"
    )

    return render_template_string(
        source=template,
        sp=sitepage,
        breadcrumb=breadcrumb,
        pathdepth=pathdepth,
    )


def MarkdownHandler(sitepage: SitePage):
    page = sitepage.page
    if not 'template' in page['dir']:
        template_path = page['dir'] + '/index.md'
    else:
        template_path = page['template']
    bc = sitepage.get_breadcrumb(sitepage.pagesdict, sitepage.dictpath)
    pd = sitepage.get_path_depth()

    sitepage.app.add_url_rule(
        rule=page['dir'] + '/',
        endpoint='/'.join(bc) + '/',
        view_func=functools.partial(
            MarkdownRunner,
            sitepage=sitepage,
            template_path=template_path,
            breadcrumb=bc,
            pathdepth=pd
        ),
    )
