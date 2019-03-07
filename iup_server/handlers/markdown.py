import logging

import markdown
from flask import render_template_string

from ..sitepage import SitePage
from . import common

def markdown_runner(sitepage, template_path, breadcrumb, pathdepth):
    template = common.load_raw_template(sitepage, template_path)
    template = (
        "{% include '_header.html' %}\n"
        + markdown.markdown(template, extensions=['extra'])
        + "\n{% include '_footer.html' %}"
    )

    return render_template_string(
        source=template,
        sp=sitepage,
        breadcrumb=breadcrumb,
        pathdepth=pathdepth,
    )

def MarkdownHandler(sitepage: SitePage):
    return common.add_sitepage_rule(sitepage, '.md', markdown_runner)
