import os
import stat
import pathlib
import shutil


def onerror(func, path, exc_info):
    """
    Error handler for ``shutil.rmtree``.

    If the error is due to an access error (read only file)
    it attempts to add write permission and then retries.

    If the error is for another reason it re-raises the error.

    Usage : ``shutil.rmtree(path, onerror=onerror)``
    """
    import stat
    if not os.access(path, os.W_OK):
        # Is the error an access error ?
        os.chmod(path, stat.S_IWUSR)
        func(path)
    else:
        raise


def remove_files(path):
    for file in os.listdir(path):
        if file == '.git':
            continue
        p = f'{path}/{file}'
        if pathlib.Path(p).is_dir():
            shutil.rmtree(p, onerror=onerror)
        else:
            os.remove(p)


def copy_files(src, dst):
    for file in os.listdir(src):
        if file == '.git':
            continue
        s = f'{src}/{file}'
        if pathlib.Path(s).is_dir():
            dst_dir = f'{dst}/{file}'
            print(dst_dir)
            if os.path.exists(dst_dir):
                print(f'removing {dst_dir}')
                shutil.rmtree(dst_dir)
            shutil.copytree(s, dst_dir)
        else:
            shutil.copy(s, dst)


def reset_directory(dst):
    if pathlib.Path(dst).exists():
        shutil.rmtree(dst, onerror=onerror)
    os.makedirs(dst)
