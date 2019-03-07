from flask import abort

from ..sitepage import SitePage
from ..constants import PAGEATTRIBS

from .template import TemplateHandler
from .markdown import MarkdownHandler
from . import common

def NullHandler(sitepage: SitePage):
    return common.add_sitepage_rule(
        sitepage, '.html',
        lambda sitepage, template_path, breadcrumb, pathdepth: abort(404)
    )

HANDLERS = {
    'TemplateHandler': TemplateHandler,
    'MarkdownHandler': MarkdownHandler,
    'NullHandler': NullHandler
}
