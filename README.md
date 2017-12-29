# vvsaur ![no alt text](logo.png)

Very very simple aur helper 

>Author: Tomás Abril

This very very simple aur helper was created primarily for my personal use.

**Current functions:**
- check and update packages
- install new packages

**Planned functions:**
- see pkgbuild file changes
- install dependencies from AUR during install

# How it works

vvsaur checks for updates in the pkgbuilds with git, if there is something new it will be built and installed.

The files are saved in ~/aur/ by default
