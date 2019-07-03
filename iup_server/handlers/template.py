import logging
import lxml.etree as E
import distro

from flask import render_template_string, request

from ..sitepage import SitePage
from ..html2gopher import html2gopher
from . import common

def template_runner(sitepage, template_path, breadcrumb, pathdepth):
    template: str = common.load_raw_template(sitepage, template_path)

    if request.scheme == 'gopher':
        template = template[template.find('\n')+1:template.rfind('\n')]
        template = render_template_string(
            source=template,
            sp=sitepage,
            breadcrumb=breadcrumb,
            pathdepth=pathdepth
        )
        template = html2gopher(
            E.fromstring('<root>' + template + '</root>', E.HTMLParser()),
            request.path, sitepage.gopher.width
        )
        return sitepage.gopher.render_menu_template(
            'layout.gopher',
            body=template,
            sp=sitepage,
            breadcrumb=breadcrumb,
            pathdepth=pathdepth,
            distro=distro
        )

    return render_template_string(
        source=template,
        sp=sitepage,
        breadcrumb=breadcrumb,
        pathdepth=pathdepth
    )

def TemplateHandler(sitepage: SitePage):
    return common.add_sitepage_rule(sitepage, '.html', template_runner)
