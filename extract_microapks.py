#!/usr/bin/env python3
# *-- coding: utf-8 --*

import subprocess
import sys
import os
import zipfile
import shutil


ADB_COMMAND = 'adb'
try:
    HOMEDIR = os.environ['HOME']
    APPDIR = HOMEDIR + "/Extracted"
    BASEAPK = APPDIR + "/BASE"
    MICROAPK = APPDIR + "/MICRO"
except KeyError:
    HOMEDIR = os.environ['HOMEDRIVE'] + os.environ['HOMEPATH']
    APPDIR = HOMEDIR + "/Extracted"
    BASEAPK = APPDIR + "/BASE"
    MICROAPK = APPDIR + "/MICRO"


def main():
    # Make dirs
    print('Extracting to ' + APPDIR)
    if not os.path.exists(APPDIR):
        os.mkdir(APPDIR)
    if not os.path.exists(BASEAPK):
        os.mkdir(BASEAPK)
    if not os.path.exists(MICROAPK):
        os.mkdir(MICROAPK)
    # Start ADB & Waiting for devices
    print('Checking if ADB is installed...')
    output = subprocess.check_output([ADB_COMMAND, 'version'])
    print(output.decode())
    print('Starting ADB Server...')
    output = subprocess.check_output([ADB_COMMAND, 'start-server'])
    print('Waiting for device to connect...')
    sys.stdout.flush()
    output = subprocess.check_output([ADB_COMMAND, 'wait-for-device'])
    print('Devices Found.')
    output = subprocess.check_output([ADB_COMMAND, 'devices'])
    print(output.decode())
    sys.stdout.flush()

    # Require ROOT & List Apps
    output = subprocess.check_output([ADB_COMMAND, 'shell', "su - root -c 'ls /data/app'"])
    appList = list(filter(lambda x: (x != '' and not x.endswith('.tmp')), output.decode().split("\n")))
    total = len(appList)
    for i, app in enumerate(appList):
        print('[%d/%d] Extracting %s...' % (i+1, total, app))
        sys.stdout.flush()
        command = [ADB_COMMAND, 'pull', '/data/app/' + app + '/base.apk', BASEAPK + '/' + app + '.apk']
        try:
            output = subprocess.check_output(command)
        except Exception as e:
            print('Failed. Ignoring...')
            sys.stdout.flush()
            continue
        # print(output)
        print('Done.')
        sys.stdout.flush()
    print('Finished.')
    sys.stdout.flush()

    # Unzip apks
    for i, app in enumerate(appList):
        if os.path.exists(BASEAPK + '/' + app + '.apk'):
            print('[%d/%d] Unzipping %s...' % (i+1, total, BASEAPK + '/' + app + '.apk'))
            sys.stdout.flush()
            apkfile = zipfile.ZipFile(BASEAPK + '/' + app + '.apk')
            for name in apkfile.namelist(): 
                if name.endswith('.apk') and 'res/raw' in name:
                    print('MicroAPK Found.')
                    sys.stdout.flush()
                    apkfile.extract(name, BASEAPK + '/' + app + '/')
            apkfile.close()
            print('Done.')
            sys.stdout.flush()
        else:
            print('[%d/%d] Ignoring %s... (Not Found)' % (i+1, total, BASEAPK + '/' + app + '.apk'))
            sys.stdout.flush()
    print('Unzip finished.')
    sys.stdout.flush()

    count1 = 0
    # move microapks to MICROAPK
    for i, app in enumerate(appList):
        if os.path.exists(BASEAPK + '/' + app + '/res/raw'):
            items = os.listdir(BASEAPK + '/' + app + '/res/raw')
            for item in items:
                if item.endswith('.apk'):
                    count1 += 1
                    print('[%d] Found MicroAPK: %s' % (count1, app))
                    sys.stdout.flush()
                    shutil.copy(BASEAPK + '/' + app + '/res/raw/' + item, MICROAPK + '/' + app + '-micro.apk')
                    print('Done.')
                    sys.stdout.flush()
                    break
    print('%d MicroAPKs found.' % count1)
    sys.stdout.flush()
    print('Job finished. Saved to %s' % MICROAPK)


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(e)
