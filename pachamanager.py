import os
import sys
import wget
import shutil
import zipfile
from argparse import ArgumentParser

ASCII_ART = '''--------------------------------------------------------------
  _____           _                                           
 |  __ \         | |                                          
 | |__) |_ _  ___| |__   __ _ _ __ ___   __ _ _ __   ___ __ _ 
 |  ___/ _` |/ __| '_ \ / _` | '_ ` _ \ / _` | '_ \ / __/ _` |
 | |  | (_| | (__| | | | (_| | | | | | | (_| | | | | (_| (_| |
 |_|   \__,_|\___|_| |_|\__,_|_| |_| |_|\__,_|_| |_|\___\__,_|
 -------------------------------------------------------------
 '''

FW_FILES = ['package.json', 'webpack.config.js', 'webpack.production.config.js', '.gitignore']
FW_DIRS = ['app']
SOURCE_URL = 'https://github.com/j0t3x/examplePWA/archive/master.zip'

cwd = os.path.curdir

def build_parser():
    parser = ArgumentParser()
    parser.add_argument('-f', '--folder', help='project path', metavar='PATH')
    return parser

def print_menu(menu, vars, header = None):
    if header:
        print(header)

    print(menu['text'] % vars)

    while True:
        try:
            option = int(input('>> '))
        except KeyboardInterrupt:
            print()
            sys.exit()
        except:
            print('Invalid option!')
        else:
            if option > menu['options']:
                print('Invalid question.')
            else:
                break

    return option

def new_wd():
    global cwd

    while True:
        path = input('New project path: ')
        
        if os.path.exists(path):
            if os.path.isdir(path):
                if len(os.listdir(path)) > 0:
                    print('The path is not empty...')
                else:
                    break
            else:
                print('The path is not a directory...')
        else:
            os.makedirs(path)
            break

    cwd = os.path.realpath(path)
    print('Using: [%s]' % cwd)

def select_wd():
    global cwd

    while True:
        path = input('Input project path: ')
        
        if os.path.exists(path):
            if os.path.isdir(path):
                break
            else:
                print('The path is not a directory...')
        else:
            print('The path does not exists...')

    cwd = os.path.realpath(path)
    print('Using: [%s]' % cwd)

def continue_with_wd():
    global cwd

    print('Using: [%s]' % cwd)

def salir(*args):
    print('bye...')
    quit()

def check_wd(wd, fw_files, fw_dirs):
    wd_files = os.listdir(wd)
    if len(wd_files) == 0:
        return 'empty'

    fw_files = fw_files + fw_dirs
    missing_files = []
    extra_files = []

    for file in fw_files:
        if file not in wd_files:
            missing_files.append(file)

    for file in wd_files:
        if file not in fw_files:
            extra_files.append(file)

    for i, file in enumerate(missing_files):
        if file in fw_dirs:
            missing_files[i] += '/'

    if len(missing_files) != 0:
        print('The following files are missing:')
        print('\n'.join(missing_files))
        return 'missing'

    if len(extra_files) != 0:
        print('The following files will be ignored:')
        print('\n'.join(extra_files))

    return 'ok'

def initialize_project(wd):
    zip_file = wget.download(SOURCE_URL, wd)
    with zipfile.ZipFile(zip_file, 'r') as f:
        f.extractall(wd)

    os.remove(zip_file)
    temp_folder = os.path.join(wd, os.listdir(wd)[0])
    
    for f in FW_FILES+FW_DIRS:
        temp_f = os.path.join(temp_folder, f)
        shutil.move(temp_f, wd)

    shutil.rmtree(temp_folder)
    print('\n--- Project initialized :D ---')

MAIN_MENU = {'text': '''[current project: '%s']
1. Create new project
2. Select project
3. Continue with this project
4. Exit
--------------------------------------------------------------''',
'options': 4,
'action': {1: new_wd, 2: select_wd, 3: continue_with_wd, 4: salir} }

EMPTY_PROJECT_MENU = {'text': '''--------------------------------------------------------------
[current project: '%s']
The current project path is empty:
1. Initialize pachamanca on selected folder
2. Exit
--------------------------------------------------------------''',
'options': 2,
'action': {1: initialize_project, 2: salir} }

PROJECT_MENU = {'text': '''--------------------------------------------------------------
[current project: '%s']
1. Create new project
2. Select project
3. Continue with this project
4. Exit
--------------------------------------------------------------''',
'options': 4,
'action': {1: new_wd, 2: select_wd, 3: continue_with_wd, 4: salir} }

def main():
    # Global vars
    global cwd, FW_FILES, FW_DIRS

    # Parser
    parser = build_parser()
    options = parser.parse_args()
    
    # Project folder
    if options.folder:
        cwd = options.folder

    while not os.path.isdir(cwd):
        print('wrong folder path (%s)...' % cwd)
        cwd = input('Project folder path: ')

    cwd = os.path.realpath(cwd)

    # Main menu
    option = print_menu(MAIN_MENU, cwd, ASCII_ART)
    MAIN_MENU['action'][option]()

    # Check if empty
    status = check_wd(cwd, FW_FILES, FW_DIRS)

    if status == 'empty':
        option = print_menu(EMPTY_PROJECT_MENU, cwd)
        EMPTY_PROJECT_MENU['action'][option](cwd)
        status = 'ok'

    elif status == 'missing':
        print('\n༼ つ ◕_◕ ༽つ Pls fix missing files.')

    if status == 'ok':
        option = print_menu(PROJECT_MENU, cwd)


if __name__ == '__main__':
    main()

