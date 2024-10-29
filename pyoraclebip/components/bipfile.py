""" Python object for a BI Publisher file """
from .const import SKIP_EXT, META, SUB_TEMP, DM_FILE, DM_SAMPLE
class BipFile:
    def __init__(self):
        self.path = None
        self.files = {}
    def change_environment(self, old, new):
        for key, value in self.files.items():
            if key.split(".")[-1] not in SKIP_EXT:
                self.files[key] = value.replace(old, new)
        return self
    
    def return_file(self):
        pass

    def __repr__(self):
        return str(self.files)
    
    def __str__(self):
        return str(self.files)


class BipSub(BipFile):
    def __init__(self, path, data:dict):
        super().__init__()
        self.files = {META: data.get(META), SUB_TEMP: data.get(SUB_TEMP)}

class BipDM(BipFile):
    def __init__(self, path, data:dict):
        super().__init__()
        self.files = {META: data.get(META), DM_FILE: data.get(DM_FILE), DM_SAMPLE: data.get(DM_SAMPLE,"")}