""" Installs and updates modules for the current user.
    Updates pip if needed.
    Overwrites any rubbish currently installed for each module.
"""
import os
import sys
import subprocess

MODULES_TO_INSTALL = ['numpy', 'matplotlib']
CONFLICTING_FILE_NAMES = {'numpy.py', 'matplotlib.py', 'random.py'}
PATH = sys.executable


def update_pip():
    """ Tries to ensure pip is installed and updated for the current user """
    print('Upgrading pip to latest version... \n')
    subprocess.run(
        [PATH] +
        '-m pip install --user --upgrade pip'.split(),
        check=True)


def install_module_for_user(module):
    """
    Installs module if needed.
    Updates module if already installed.
    Forces install/update over top of any rubbish that's already there
    """
    print(f'Installing {module} for the current user... \n')
    subprocess.run(
        [PATH] +
        f'-m pip install --user {module} --upgrade --ignore-installed'.split(),
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
            print(
                f"IMPORTANT WARNING: You have a file called '{file}' in the same directory as this script.")
            print(
                "                   This will conflict with the use of numpy or matplotlib.")
            print(
                "                   Please remove or rename this file then run this script again.")
            print()
            has_conflicts = True
    return has_conflicts


def main():
    """ Feel free to add other modules to the list of things to install """
    print(f'Python executable at: {PATH}\n')
    if check_for_conflicting_files():
        return

    update_pip()
    try:
        for module in MODULES_TO_INSTALL:
            install_module_for_user(module)
    except subprocess.CalledProcessError:
        for module in ['msvc-runtime'] + MODULES_TO_INSTALL:
            install_module_for_user(module)


if __name__ == "__main__":
    main()
