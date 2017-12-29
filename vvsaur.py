"""
    vvsaur, a very very simple aur helper

    Copyright 2017 Tomás Abril
    GPL3
"""

import os
import config

mypath = os.path.expanduser(config.folder)
makepkgCmd = config.cmd

if not os.path.exists(mypath):
    os.makedirs(mypath)

folders = []
for root, dirs, files in os.walk(mypath):
    print("Looking at folder " + root)
    folders.extend(dirs)
    break

print("found the aur packages: ")
for p in folders:
    print(' > ' + p)

print("checking for updates...")

for pkgName in folders:
    os.chdir(mypath)
    # pull new pkgbuild
    command = 'git -C ' + mypath + pkgName + ' pull'
    print('\n' + command)
    os.system(command)
    # checking installed version
    output = os.popen('pacman -Q ' + pkgName).read()
    if not output.startswith(pkgName):
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
        print(pkgName + ' installed:' + installedVer + ' available:' + pkgVer)
        print("Do you wish to upgrade it? YES/no")
        confirm = input()
        if confirm == "" or confirm.lower() == "y" or confirm.lower() == "yes":
            # upgrading package
            print("Upgrading...")
            os.chdir(mypath + pkgName)
            print(makepkgCmd)
            os.system(makepkgCmd)
