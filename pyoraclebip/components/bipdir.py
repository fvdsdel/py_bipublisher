""""""
from zipfile import ZipFile, ZIP_DEFLATED
from zipfile import Path as Zpath
from io import StringIO, BytesIO
import os

from . import BipRep, BipDM, BipSub, BipFile
from .const import SKIP_EXT, EXT_Z_DMOD,EXT_Z_RPT,EXT_Z_DIR

class BipDir:
    def __init__(self, fpath, f_out=None, suffix="EDIT"):
        # print(fpath, f_out, suffix)
        self._path = fpath
        if not f_out:
            f_out = fpath.replace(fpath.split(os.sep)[-1],'')
        self.file_out = os.path.join(f_out, f"{(fpath.split('.')[0]).split(os.sep)[-1]}_{suffix}.{EXT_Z_DIR}")
        # print(self.file_out)
        self.content = self.file_contents()
        self.metafiles = [x for x in self.content if x.split(".")[-1] == "meta"]
        self.folders = [x for x in self.content if len(x.split(".")) == 1]
        self.dms = [x for x in self.content if x.split(".")[-1] == EXT_Z_DMOD]
        self.sublist = [x for x in self.content if x.split(".")[-1]=="xsbz"]
        self.reportlist = [x for x in self.content if x.split(".")[-1]== EXT_Z_RPT]
        self.setup_outputfile()
    
    def create_bip_comp(self, path, bip_type):
        file_contents = {}
        with ZipFile(file=self._path, mode="r") as archive:
            subzip_data = BytesIO(archive.read(path))
            with ZipFile(file=subzip_data, mode="r") as subzip:
                for item in subzip.namelist():
                    if item.split(".")[-1] in SKIP_EXT:
                        file_contents[item] = subzip.read(item)
                    else:
                        try:
                            file_contents[item] = subzip.read(item).decode()
                        except:
                            print(item)
        return bip_type(path, file_contents)
    
    def create_subzip_io(self, files):
        stream = BytesIO()
        with ZipFile(stream, "w", compression=ZIP_DEFLATED) as archive:
            for key, value in files.items():
                if key.split(".")[-1] in SKIP_EXT:
                    archive.writestr(key, data=value)
                else:
                    archive.writestr(key, data=value.encode())
        return stream

    def append_subzip_to_dir(self, subpath, files):
        data = self.create_subzip_io(files)
        with ZipFile(file=self.file_out, mode="a") as archive:
            with archive.open(subpath, "w") as sub:
                sub.write(data.getbuffer())         
        return
    
    def append_file_to_dir(self, path, data:str):
        with ZipFile(file=self.file_out, mode="a") as archive:
            archive.writestr(path, data=data.encode())
        return
    
    def change_metafiles(self, old, new):
        with ZipFile(file=self._path, mode="r") as archive:
            for meta in self.metafiles:
                data = archive.read(meta).decode()
                data = data.replace(old, new)
                self.append_file_to_dir(meta, data)

    def change_environment(self, old, new):
        self.change_metafiles(old, new)
        change_list = []      
        for item in self.reportlist:
            change_list.append((item, BipRep))
        for item in self.dms:
            change_list.append((item, BipDM))
        for item in self.sublist:
            change_list.append((item, BipSub))
        
        for bipcomp in change_list:
            comp: BipFile = self.create_bip_comp(bipcomp[0], bipcomp[1])
            try:
                comp.change_environment(old, new)
                new_content = comp.files
                self.append_subzip_to_dir(bipcomp[0], new_content)
            except (Exception) as err:
                print(err)
                print(bipcomp)
            # print(comp)
        print("Done")
        print(f"Saved to: {self.file_out}")
        return
    
    def file_contents(self):
        with ZipFile(file=self._path, mode="r") as file:
            contentlist = file.namelist()
        file.close()
        return contentlist
    
    def setup_outputfile(self):
        try:
            with ZipFile(file=self.file_out, mode="x") as archive:
                pass
        except(FileExistsError) as err:
            # TODO: better error handling
            print(err)
        return self