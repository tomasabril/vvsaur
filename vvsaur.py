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
        command = 'git -C ' + mypath + pkgName + ' pull --no-rebase'
        output = subprocess.check_output(command, shell=True).decode('utf-8')
        if verbose:
            print('\n+ ' + command)
            print(output, end='')
        else:
            print('.', end='')
            sys.stdout.flush()
        # checking installed version
        try:
            p = subprocess.run('pacman -Q ' + pkgName, stdout=subprocess.PIPE, stderr=subprocess.PIPE ,check=True, shell=True, bufsize=1, universal_newlines=True)
        except subprocess.CalledProcessError as e:
            if verbose:
                print(' >> ' + pkgName +
                      ' is not installed, continuing to next package')
            continue
        installedVer = p.stdout.split(' ')[1].strip()
        # check pkgbuild version
        pkgVer = ''
        for line in open(mypath + pkgName + '/PKGBUILD', 'r'):
            if line.startswith('pkgver'):
                pkgVer = line.split('=')[1].strip().strip('\'')
            if line.startswith('pkgrel'):
                pkgVer = pkgVer + '-' + line.split('=')[1].strip().strip('\'')
                break
        if installedVer != pkgVer:
            print('\n' + pkgName + ' installed:' +
                  installedVer + ' available:' + pkgVer)
            print("Do you wish to upgrade it? [Y/n]")
            confirm = input()
            if confirm == "" or confirm.lower() == "y" or confirm.lower() == "yes":
                # upgrading package
                print("Upgrading...")
                os.chdir(mypath + pkgName)
                print(makepkgCmd)
                subprocess.run(makepkgCmd, shell=True,
                               bufsize=1, universal_newlines=True)
    print('')


def installNew(newPkg):
    print('>> installing ' + newPkg + '\n')
    # get pkgbuild from git
    command = 'git -C ' + mypath + ' clone https://aur.archlinux.org/' + newPkg + '.git'
    print('+ ' + command)
    subprocess.call(command, shell=True)
    # if not found show error and delete folder
    if not os.path.isfile(mypath + newPkg + '/PKGBUILD'):
        print('Could not find package ' + newPkg)
        os.system('rm -r ' + mypath + newPkg)
    else:
        print('')
        os.chdir(mypath + newPkg)
        print('+ ' + makepkgCmd)
        # build and install package
        # try:
        p = subprocess.Popen(makepkgCmd, shell=True, bufsize=1 , universal_newlines=True
                        # ,stdout=subprocess.PIPE
                        # ,stderr=subprocess.PIPE
                        ).wait()
        # pcode = p.returncode
        pcode = p
        # on error
        if pcode != 0:
        # if dependecies are not found search AUR
            print('Some dependencies not found on official repositories')
            # missingPkg = errorText.splitlines()[0].split(':')[2].strip()
            # if verbose:
            #     print('\nError on package install: \n' + errorText)
            # print(missingPkg + ' not found on repositories. Search AUR? [Y/n]')
            # confirm = input()
            # if confirm == "" or confirm.lower() == "y" or confirm.lower() == "yes":
            #     installNew(missingPkg)


if len(sys.argv) > 1:
    if len(sys.argv) == 3:
        if sys.argv[2] == '-v':
            verbose = True
    init()
    if sys.argv[1] == 'u':
        update()
    else:
        installNew(sys.argv[1])
else:
    print('usage:\n' +
          ' vvsaur u        - upgrade packages\n' +
          ' vvsaur pkgName  - install pkgName from AUR\n' +
          ' -v              - be verbose\n')
