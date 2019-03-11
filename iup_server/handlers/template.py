import logging

from flask import render_template_string

from ..sitepage import SitePage
from . import common

def template_runner(sitepage, template_path, breadcrumb, pathdepth):
    template: str = common.load_raw_template(sitepage, template_path)

    if sitepage.gopher:
        template = template[template.find('\n')+1:template.rfind('\n')]
        template = render_template_string(
            source=template,
            sp=sitepage,
            breadcrumb=breadcrumb,
            pathdepth=pathdepth
        )
        return sitepage.gopher.render_menu_template(
            'layout.gopher',
            body=template,
            sp=sitepage,
            breadcrumb=breadcrumb,
            pathdepth=pathdepth
        )

    return render_template_string(
        source=template,
        sp=sitepage,
        breadcrumb=breadcrumb,
        pathdepth=pathdepth
    )

def TemplateHandler(sitepage: SitePage):
    return common.add_sitepage_rule(sitepage, '.html', template_runner)
