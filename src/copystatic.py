import os
import shutil

def movefiles():

    curpath = f"{os.path.curdir}/static"
    destpath = f"{os.path.curdir}/public"
    if not os.path.isdir(curpath):
            raise Exception(f'Error: "{curpath}" is not a folder')
    if os.path.isdir(destpath):
            print("deleting public folder")
            shutil.rmtree(destpath) 
    os.mkdir(destpath)

    items = os.listdir(curpath)

    copied = copyfiles(curpath, destpath, items)

    print(os.listdir(destpath))

    return copied


def copyfiles(srcdir, dstdir, items):
    
    if len(items) == 0:
        return "finished"
    
    if os.path.isdir(os.path.join(srcdir, items[0])):
        os.mkdir(os.path.join(dstdir, items[0]))
        copyfiles(os.path.join(srcdir, items[0]), os.path.join(dstdir, items[0]), os.listdir(os.path.join(srcdir, items[0])))
        return copyfiles(srcdir, dstdir, items[1:])
    else:
        shutil.copy(f"{srcdir}/{items[0]}", dstdir)
        return copyfiles(srcdir, dstdir, items[1:])

    




