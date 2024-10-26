#!/bin/bash

rm ./downloader-site-x86_64.AppImage
pip install pyinstaller
pyinstaller ./downloader-site.spec

cp -fv ./dist/downloader-site ./kdownload-site.AppDir/

chmod -R 777 ./kdownload-site.AppDir
ARCH=x86_64 ./appimagetool-x86_64.AppImage ./kdownload-site.AppDir

rm -r ./build
