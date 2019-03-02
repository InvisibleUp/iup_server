import functools
import logging

from flask import render_template_string

from ..sitepage import SitePage
from ..constants import PAGEATTRIBS

def TemplateRunner(sitepage, template_path, breadcrumb, pathdepth):
    try:
        with sitepage.app.open_resource(
            'content' + template_path, mode='r'
        ) as f:
            template = f.read()
    except FileNotFoundError:
        logging.exception('Content file not found')
        return

    return render_template_string(
        source=template,
        sp=sitepage,
        breadcrumb=breadcrumb,
        pathdepth=pathdepth
    )

def TemplateHandler(sitepage: SitePage):
    page = sitepage.page
    if not 'template' in page['dir']:
        template_path = page['dir'] + '/index.html'
    else:
        template_path = page['template']
    bc = sitepage.get_breadcrumb(sitepage.pagesdict, sitepage.dictpath)
    pd = sitepage.get_path_depth()

    sitepage.app.add_url_rule(
        rule=page['dir'] + '/',
        endpoint='/'.join(bc) + '/',
        view_func=functools.partial(
            TemplateRunner,
            sitepage=sitepage,
            template_path=template_path,
            breadcrumb=bc,
            pathdepth=pd
        ),
    )

