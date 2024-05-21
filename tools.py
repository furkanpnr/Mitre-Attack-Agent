import os
import json
import shutil
import datetime
_path_joiner = lambda base_path, *args: os.path.join(base_path, *args)

_tojson = lambda _dict, indent=2: json.dumps(_dict, indent=indent)

create_new_dir = lambda path: os.makedirs(path)

def check_folder_exits(path, raise_exception=False):
    _is = os.path.isdir(path)
    if raise_exception and not _is:
        raise FileNotFoundError(f"path not exists: {path}")
    return _is

def check_file_exists(path, raise_exception=False, exception_message="asset file could not found:"):
    _is = os.path.isfile(path)
    if raise_exception and not _is:
        raise FileNotFoundError(f'{exception_message} {path}')
    return _is

def create_empty_file(total_path): 
    with open(total_path, 'w') as f:
        pass

def get_file_content(total_path, read_type):
    with open(total_path, read_type) as f:
        data = f.read()
    return data

def move_file(src: str, dest: str):
    shutil.move(src, dest)

def remove_file(path):
    if check_file_exists(path):
        os.remove(path)

def get_current_time(string: bool = False):
    now = datetime.datetime.now()
    if string:
        return now.strftime("%Y-%m-%d %H:%M:%S").replace(" ", "#")
    return now
    