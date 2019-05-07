"""permute files"""
import os


def get_new_dirs(old_root):
    paths = []
    for folder in os.listdir(old_root):
        for path in os.listdir(os.path.join(old_root,folder)):
            paths.append(path[:7])
    return list(set(paths))

if __name__ == '__main__':
    import sys
    import shutil

    old_root = sys.argv[1]
    new_root = sys.argv[2]
    if not os.path.exists(new_root):
        os.mkdir(new_root)
    new_dirs = get_new_dirs(old_root)
    print(new_dirs)
    for dir in new_dirs:
        if not os.path.exists(os.path.join(new_root,dir)):
            os.mkdir(os.path.join(new_root,dir))

    for user in os.listdir(old_root):
        for tile in os.listdir(os.path.join(old_root,user)):
            shutil.copyfile(os.path.join(old_root,user,tile),os.path.join(new_root,tile[:7],user))
