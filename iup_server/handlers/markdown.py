import logging
import lxml.etree as E
import distro

import markdown
from flask import render_template_string, request

from ..sitepage import SitePage
from ..html2gopher import html2gopher
from . import common

def markdown_runner(sitepage, template_path, breadcrumb, pathdepth):
    template = common.load_raw_template(sitepage, template_path)
    template = markdown.markdown(template, extensions=['extra'])
    template = html2gopher(
        E.fromstring('<root>' + template + '</root>', E.HTMLParser()),
        request.path, sitepage.gopher.width
    )
    if request.scheme == 'gopher':
        return sitepage.gopher.render_menu_template(
            'layout.gopher',
            body=template,
            sp=sitepage,
            breadcrumb=breadcrumb,
            pathdepth=pathdepth,
        )

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
        distro=distro
    )

def MarkdownHandler(sitepage: SitePage):
    return common.add_sitepage_rule(sitepage, '.md', markdown_runner)
