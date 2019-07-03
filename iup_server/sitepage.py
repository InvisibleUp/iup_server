import typing as t

from . import helpers
from .constants import PAGEATTRIBS


class SitePage:
    handler: t.Callable
    pagesdict: t.Dict[str, t.Any]
    dictpath: t.List[str]
    app: t.Any

    # Derived from pages dict
    page: t.Dict[str, t.Any]
    subpages: t.List[t.Dict[str, t.Any]]
    parent: t.Optional[t.Dict[str, t.Any]]
    siblings: t.List[t.Dict[str, t.Any]]

    def __init__(self, handler, pagesdict, dictpath, app, gopher):
        self.handler = handler
        self.pagesdict = pagesdict
        self.dictpath = dictpath
        self.app = app
        self.gopher = gopher

        self.page = helpers.subdict_from_key_list(pagesdict, dictpath)
        subpage_indices = list(
            filter(lambda x: x not in PAGEATTRIBS, self.page)
        )
        self.subpages = [self.page[x] for x in subpage_indices]
        if len(dictpath) > 0:
            self.parent = helpers.subdict_from_key_list(
                pagesdict, dictpath[0:-1]
            )
            sib_indices = list(
                filter(lambda x: x not in PAGEATTRIBS, self.parent)
            )
            self.siblings = [self.parent[x] for x in sib_indices]
        else:
            self.parent = None
            self.siblings = []

    def get_breadcrumb(self, pages, path, bc=None) -> t.List[str]:
        if bc == None:
            bc = ['InvisibleUp']

        if len(path) > 0:
            subpage = pages[path[0]]
            if subpage['title']:
                bc.insert(0, subpage['title'])
            return self.get_breadcrumb(subpage, path[1:], bc)
        else:
            return bc

    def get_path_depth(self):
        if self.page['dir'] == '/':
            return 0
        return self.page['dir'].count('/')

    def register(self):
        self.handler(self)
