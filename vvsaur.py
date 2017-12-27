"""
    vvsaur, a very very simple aur helper

    Copyright 2017 Tomás Abril
    GPL3
"""

import os
import subprocess

# TODO: read config file
mypath = '/home/samot/aur/'
makepkgCmd = 'BUILDDIR=/tmp/makepkg makepkg -cCsi --check'

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

print("vvsaur - checking for updates")

for folder in folders:
    os.chdir(mypath)
    # TODO: read version of installed/available package
    process = subprocess.Popen(
        ["git", "-C", mypath + folder, "fetch"], stdout=subprocess.PIPE)
    output = process.communicate()[0]
    print("" + output.decode("utf-8"))
    if len(output.decode("utf-8")) > 0:
        print("Found an update to " + folder)
        # print("Do you with to update it? YES/no")
        # confirm = input()
        # if confirm == "" or confirm.lower() == "y" or confirm.lower() == "yes":
        # pulling new pkgbuild
        command = 'git -C ' + mypath + folder + ' pull'
        print(command)
        os.system(command)
        # upgrading package
        print("Upgrading...")
        os.chdir(mypath + folder)
        print(makepkgCmd)
        os.system(makepkgCmd)
