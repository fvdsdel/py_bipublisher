""""""
from . import BipFile
from .const import META,REP_XDO, XDO_CFG, SKIP_EXT

class BipRep(BipFile):
    def __init__(self, path, data:dict):
        super().__init__()
        self.path = path
        self._sysfiles = {META: data.get(META), REP_XDO: data.get(REP_XDO), XDO_CFG:data.get(XDO_CFG)}
        self.reportfiles = {key: val for key, val in data.items() if key.split(".")[-1] == "rtf"}
        self.other = {key: val for key, val in data.items() if key.split(".")[-1] in SKIP_EXT}
        self._files = {}
        # self.files = {}
        self.files.update(self._sysfiles)
        self.files.update(self.reportfiles)
        self.files.update(self.other)