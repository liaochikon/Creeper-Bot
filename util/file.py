import pickle
import json
import os

def find_file(file_name, path):
    for root, dirs, files in os.walk(path):
        if file_name in files:
            return os.path.join(root, file_name)
    return ""

def get_sub_directories():
    return [name for name in os.listdir(".") if os.path.isdir(name)]

def find_files_in_root_directory(file_name):
    file_path_list = []
    root_directory = os.getcwd()
    sub_directory_name_list = get_sub_directories()
    for sub_directory_name in sub_directory_name_list:
        sub_directory_path = os.path.join(root_directory, sub_directory_name)
        file_path = find_file(file_name, sub_directory_path)
        if file_path == "":
            continue
        file_path_list.append(file_path)
    return file_path_list

def create_folder(path):
    illegal_symbal_list = ['\\', "/",  ":",  "*",  "?",  "\"", "<",  ">",  "|"]
    save_path = path
    for illegal_symbal in illegal_symbal_list:
        save_path = save_path.replace(illegal_symbal, "")

    ret = not os.path.exists(save_path)
    if ret:
        os.makedirs(save_path)
    return ret, save_path

def save_info_bin(info_path, info):
    outfile = open(info_path, "wb")
    pickle.dump(info, outfile)
    outfile.close()

def load_info_bin(info_path):
    readfile = open(info_path, "rb")
    info = pickle.load(readfile)
    readfile.close()
    return info

def save_info(info_path, info):
    outfile = open(info_path, "w")
    outfile.write(info)
    outfile.close()

def load_info(info_path):
    readfile = open(info_path, "r")
    info = readfile.read()
    readfile.close()
    return info

def save_info_json(info_path, info):
    outfile = open(info_path, "w", encoding="utf8")
    outfile.write(json.dumps(info, indent=1, ensure_ascii=False))
    outfile.close()

def load_info_json(info_path):
    readfile = open(info_path, "r", encoding="utf8")
    info = json.load(readfile)
    readfile.close()
    return info
