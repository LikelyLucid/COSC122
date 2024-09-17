""" Installs and updates modules for the current user.
    Updates pip if needed.
    Overwrites any rubbish currently installed for each module.
    Run from Wing101 or wherever you normall run your python code.
    NOTES: 
    - You will need to install graphviz for your OS first.
       - General OS install instructions are at:  https://www.graphviz.org/download/
       - Windows install instructions are at:
            https://forum.graphviz.org/t/new-simplified-installation-procedure-on-windows/224
"""
import os
import sys
import subprocess

MODULES_TO_INSTALL = ['graphviz']
CONFLICTING_FILE_NAMES = {'graphviz.py'}
PATH = sys.executable


def update_pip():
    """ Tries to ensure pip is installed and updated for the current user """
    print('Upgrading pip to latest version... \n')
    subprocess.run([PATH] +
                   '-m pip install --user --upgrade pip'.split(),
                   check=True)



def install_module_for_user(module):
    """
    Installs module if needed.
    Updates module if already installed.
    Forces install/update over top of any rubbish that's already there
    """
    print(f'Installing {module} for the current user... \n')
    subprocess.run([PATH] + 
                    f'-m pip install --user {module} --upgrade --force-reinstall'.split(),
                    check=True)



def check_for_conflicting_files():
    """"
    Checks if there are any files that might confict with the use of
    matplotlib or numpy. Returns True if any conflicts are found.
    """
    has_conflicts = False
    files = [file for file in os.listdir('.') if os.path.isfile(file)]
    for file in files:
        if file.lower() in CONFLICTING_FILE_NAMES:
            print(f"IMPORTANT WARNING: You have a file called '{file}' in the same directory as this script.")
            print( "                   This will conflict with the use of numpy or matplotlib.")
            print( "                   Please remove or rename this file then run this script again.")
            print()
            has_conflicts = True
    return has_conflicts


def main():
    """ Feel free to add other modules to the list of things to install """
    print('Python executable at: {}\n'.format(PATH))
    print()
    print('NOTE:')
    print('You must install graphviz on your OS before installing the Python package...\n')
    has_graphviz = input('Have you installed graphviz on your OS (y/n)? ')
    if has_graphviz.lower() == 'y':
        if check_for_conflicting_files():
            return
        update_pip()
        try:
            for module in MODULES_TO_INSTALL:
                install_module_for_user(module)
        except subprocess.CalledProcessError:
            for module in ['msvc-runtime'] + MODULES_TO_INSTALL:
                install_module_for_user(module)
    else:
        print('\n\nNOTES:\n')
        print('- You should download/install the relevant OS files from')
        print('    https://www.graphviz.org/download/')
        print('     before installing the python package.')
        print(" - If you're running an Ubuntu/Debian based linux like Mint")
        print('     you can simply do sudo apt install graphviz in the terminal')
        print('     to install the graphviz package on your system')
        print('- IMPORTANT: In Windows make sure you at graphviz to the PATH when installing')
        print('- Windoze instructions -> https://forum.graphviz.org/t/new-simplified-installation-procedure-on-windows/224')
        print('- The OS software and python package should already be')
        print('  installed on CSSE lab computers, and possibly even UC ')
        print('  Windoze machines...')


if __name__ == "__main__":
    main()
