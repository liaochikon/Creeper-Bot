from util.file import *
from pynput import keyboard
import os
import webbrowser

search_results_path_list = find_files_in_root_directory("search_results.json")
search_results = []

state = 0
file_idx = 0
file_max_idx = len(search_results_path_list) - 1 
result_idx = 0
result_max_idx = 0

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def search_results_selector(search_results_path_list, idx):
    search_results = load_info_json(search_results_path_list[idx])
    return search_results

def file_viewer():
    for i, search_results_path in enumerate(search_results_path_list):
        if i == file_idx:
            print(bcolors.OKCYAN + bcolors.UNDERLINE + search_results_path + bcolors.ENDC)
        else:
            print(search_results_path)
    print(" esc Quit | ↑ Last file | Next file ↓ | → Select file ")

def search_results_viewer(search_results, idx):
    s = search_results['search_results'][idx]
    print(idx + 1)
    print(bcolors.OKGREEN + bcolors.BOLD + s['title'])
    print(bcolors.ENDC + bcolors.OKGREEN + s['intro'])
    print(bcolors.OKCYAN + "Rating : " + str(s['rating']))
    print(bcolors.WARNING + bcolors.UNDERLINE + s['url'])
    print(bcolors.ENDC + s['briefing'] + bcolors.ENDC)
    print(" esc Quit | ← Return to file selection | ↑ Last search | Next search ↓ | → Open webpage ")

def on_release(key):
    global search_results_path_list, search_results, state, file_idx, file_max_idx, result_idx, result_max_idx
    os.system("cls")
    if key == keyboard.Key.esc:
        return False
    
    #control
    if state == 0:
        if key == keyboard.Key.right:
            search_results = search_results_selector(search_results_path_list, file_idx)
            state = 1
            result_idx = 0
            result_max_idx = len(search_results['search_results']) - 1
        if key == keyboard.Key.up:
            file_idx -= 1
        if key == keyboard.Key.down:
            file_idx += 1
        
        if file_idx < 0:
            file_idx = 0
        if file_idx > file_max_idx:
            file_idx = file_max_idx
    elif state == 1:
        if key == keyboard.Key.left:
            state = 0
            result_idx = 0
        if key == keyboard.Key.up:
            result_idx -= 1
        if key == keyboard.Key.down:
            result_idx += 1
        if key == keyboard.Key.right:
            if search_results != []:
                webbrowser.open(search_results['search_results'][result_idx]['url'])

        if result_idx < 0:
            result_idx = 0
        if result_idx > result_max_idx:
            result_idx = result_max_idx
        
    #render
    if state == 0:
        file_viewer()
    elif state == 1:
        search_results_viewer(search_results, result_idx)
    
if __name__ == "__main__":
    os.system("cls")
    file_viewer()
    with keyboard.Listener(on_release=on_release) as listener:
        listener.join()
    listener = keyboard.Listener(on_release=on_release)
    listener.start()