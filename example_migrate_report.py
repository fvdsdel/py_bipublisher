import os
from pyoraclebip import BipDir
from pathlib import Path

def migrate_dir(path2file,file,env_from,env_to,suffix="tst"):
    bip_dir_file = os.path.join(path2file,file)
    bipdir = BipDir(bip_dir_file, f_out = None,suffix=suffix)
    bipdir.change_environment(env_from, env_to)



if __name__ == "__main__":
    report_path = Path(os.getcwd()) /"reports"
    filename = "report.xdrz"
    env_from = "biptst"
    env_to = "bipprd"
    if os.path.isfile(os.path.join(report_path,filename)):
        migrate_dir(report_path,filename,env_from,env_to,suffix="tst2prd")
    else:
        print(f"File not found: {os.path.join(report_path,filename)}")
    # print(BIP_DIR)
    