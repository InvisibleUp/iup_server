from ..sitepage import SitePage
from ..constants import PAGEATTRIBS

from .template import TemplateHandler
from .markdown import MarkdownHandler

HANDLERS = {
    'TemplateHandler': TemplateHandler,
    'MarkdownHandler': MarkdownHandler,
}
