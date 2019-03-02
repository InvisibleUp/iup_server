import logging

from flask import render_template_string

from ..sitepage import SitePage
from . import common

def template_runner(sitepage, template_path, breadcrumb, pathdepth):
    template = common.load_raw_template(sitepage, template_path)
    return render_template_string(
        source=template,
        sp=sitepage,
        breadcrumb=breadcrumb,
        pathdepth=pathdepth
    )

def TemplateHandler(sitepage: SitePage):
    return common.add_sitepage_rule(sitepage, '.html', template_runner)
