import sys
import os
import re
import string
import sys
import glob

from os import listdir
from os.path import isfile, join

def printUsage():
    print('Usage: movpkgmerge.py (-r) <target directory>')
    print('-r: Recursively convert all .movpkg folders inside the target directory.')
    print('If not using -r, target directory should be the movpkg to convert')

def isMp4(trackPath):
    trackName = os.path.basename(os.path.normpath(trackPath))
    m3u8_files = glob.glob(join(trackPath, '*.m3u8'))
    if len(m3u8_files) != 1:
        raise ValueError(f"Expect one m3u8 file but found {len(m3u8_files)}")
    trackInfoPath = m3u8_files[0]
    trackInfoFile = open(trackInfoPath, "r")
    lines = trackInfoFile.readlines()
    trackInfoFile.close()
    for line in lines:
        if '#EXT-X-MAP:URI=' in line:
            return 1
    return 0

def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    return [ atoi(c) for c in re.split(r'(\d+)', text) ]

def find_folders_with_m3u8_files(dir_path):
    folders_with_m3u8 = []
    for folder_name in os.listdir(dir_path):
        folder_path = os.path.join(dir_path, folder_name)
        if os.path.isdir(folder_path):
            if glob.glob(os.path.join(folder_path, "*.m3u8")):
                folders_with_m3u8.append(folder_path)
    return folders_with_m3u8

def find_track_folders(dir_path):
    track_folders = []
    for folder_path in find_folders_with_m3u8_files(dir_path):
        if os.path.basename(folder_path) not in ('Data', 'boot.xml', 'root.xml'):
            track_folders.append(folder_path)
    return track_folders

    
def mergeMovPkg(pathToMovPkg):
    trackDirectories = find_track_folders(pathToMovPkg)

    for trackDirectory in trackDirectories:
        trackDirectoryPath = join(pathToMovPkg,trackDirectory)
        trackIsMp4 = isMp4(trackDirectoryPath)
        trackNum = trackDirectory.split('-')[0]
        
        extension = 'ts'
        if trackIsMp4:
            extension = 'mp4'

        if len(trackDirectories) > 1:
            exportFilePath = os.path.splitext(pathToMovPkg)[0] + '_track' + trackNum + '.' + extension
        else:
            exportFilePath = os.path.splitext(pathToMovPkg)[0] + '.' + extension
        
        if os.path.exists(exportFilePath):
            print("%s already exists, skipping" % os.path.basename(os.path.normpath(exportFilePath)))
            continue
        exportFile = open(exportFilePath,'ab+')
        
        trackFragments = [f for f in listdir(trackDirectoryPath) if str.endswith(f, '.frag') or str.endswith(f, '.initfrag')]
        trackFragments.sort(key=natural_keys)
        for fragmentFileName in trackFragments:
            fragmentFile = open(join(trackDirectoryPath, fragmentFileName), 'rb')
            exportFile.write(fragmentFile.read())
            fragmentFile.close()
        exportFile.close()
        print('Merged track %s of %s to %s' %(trackDirectory, os.path.basename(os.path.normpath(pathToMovPkg)), os.path.basename(os.path.normpath(exportFilePath))))

recursive = 0


    
specifiedPath = r"C:\Users\vivira\Music\iTunes\iTunes Media\Apple Music\Compilations\Metomate Collection I\31 Chained to Your Sense (2022).movpkg"
if not os.path.exists(specifiedPath):
    print('Error: No directory at path %s' % specifiedPath)
    sys.exit(1)

if recursive:
    movPkgNames = [f for f in listdir(specifiedPath) if str.endswith(f, '.movpkg')]
    for movPkgName in movPkgNames:
        movPkgPath = join(specifiedPath, movPkgName)
        mergeMovPkg(movPkgPath)
else:
    mergeMovPkg(specifiedPath)