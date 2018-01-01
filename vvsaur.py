#!/usr/bin/python
"""
    vvsaur, a very very simple aur helper

    Copyright 2017 Tomás Abril
    GPL3
"""

import os
import sys
import subprocess
import config

mypath = os.path.expanduser(config.folder)
makepkgCmd = config.cmd
folders = []
verbose = False


def init():
    if not os.path.exists(mypath):
        os.makedirs(mypath)
    for root, dirs, files in os.walk(mypath):
        if verbose:
            print("Looking at folder " + root)
        folders.extend(dirs)
        break
    if verbose:
        print("found the aur packages: ")
        for p in folders:
            print(' > ' + p)


def update():
    print("Checking for updates", end='')
    if verbose:
        print('...')
    sys.stdout.flush()
    for pkgName in folders:
        os.chdir(mypath)
        # pull new pkgbuild
        command = 'git -C ' + mypath + pkgName + ' pull'
        output = subprocess.check_output(command, shell=True).decode('utf-8')
        if verbose:
            print('\n+ ' + command)
            print(output, end='')
        else:
            print('.', end='')
            sys.stdout.flush()
        # checking installed version
        try:
            output = subprocess.check_output(
                'pacman -Q ' + pkgName, stderr=subprocess.STDOUT, shell=True).decode('utf-8')
        except subprocess.CalledProcessError as e:
            if verbose:
                print(' >> ' + pkgName + ' is not installed, continuing to next package')
            continue
        installedVer = output.split(' ')[1].strip()
        # check pkgbuild version
        pkgVer = ''
        for line in open(mypath + pkgName + '/PKGBUILD', 'r'):
            if line.startswith('pkgver'):
                pkgVer = line.split('=')[1].strip().strip('\'')
            if line.startswith('pkgrel'):
                pkgVer = pkgVer + '-' + line.split('=')[1].strip().strip('\'')
                break
        if installedVer != pkgVer:
            print(pkgName + ' installed:' +
                  installedVer + ' available:' + pkgVer)
            print("Do you wish to upgrade it? [Y/n]")
            confirm = input()
            if confirm == "" or confirm.lower() == "y" or confirm.lower() == "yes":
                # upgrading package
                print("Upgrading...")
                os.chdir(mypath + pkgName)
                print(makepkgCmd)
                subprocess.call(makepkgCmd, shell=True)
    print('')


def installNew():
    newPkg = sys.argv[1]
    print('>> installing ' + newPkg + '\n')
    command = 'git -C ' + mypath + ' clone https://aur.archlinux.org/' + newPkg + '.git'
    print('+ ' + command)
    subprocess.call(command, shell=True)
    if not os.path.isfile(mypath + newPkg + '/PKGBUILD'):
        print('Could not find package ' + newPkg)
        os.system('rm -r ' + mypath + newPkg)
    else:
        print('')
        os.chdir(mypath + newPkg)
        print('+ ' + makepkgCmd)
        subprocess.call(makepkgCmd, shell=True)


if len(sys.argv) > 1:
    if len(sys.argv) == 3:
        if sys.argv[2] == '-v':
            verbose = True
    init()
    if sys.argv[1] == 'u':
        update()
    else:
        installNew()
else:
    print('usage:\n' +
          ' vvsaur u        - upgrade packages\n' +
          ' vvsaur pkgName  - install pkgName from AUR\n' +
          ' -v              - be verbose\n')
