#!/usr/bin/env python3
# *-- coding: utf-8 --*

import subprocess
import sys
import os
import time


ADB_COMMAND = 'adb'
try:
    HOMEDIR = os.environ['HOME']
    APPDIR = HOMEDIR + "/Extracted"
    MICROAPK = APPDIR + "/MICRO"
except KeyError:
    HOMEDIR = os.environ['HOMEDRIVE'] + os.environ['HOMEPATH']
    APPDIR = HOMEDIR + "/Extracted"
    MICROAPK = APPDIR + "/MICRO"


def main():
    if not os.path.exists(MICROAPK):
        print('Run extract script first.')
    else:
        input('继续安装前请保持手机已连接至电脑，手表端开启蓝牙调试，Wear OS 端打开「通过蓝牙调试」高级选项，回车继续 Ctrl-C 取消: ')
        print('等待手表端点击允许ADB调试...')
        sys.stdout.flush()
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
        
        output = subprocess.check_output([ADB_COMMAND, 'forward', 'tcp:4444', 'localabstract:/adb-hub'])
        output = subprocess.check_output([ADB_COMMAND, 'connect', 'localhost:4444'])
        print('Connected.')
        sys.stdout.flush()

        print('Waiting 5 seconds to start. Ctrl+C to cancel...')
        sys.stdout.flush()
        time.sleep(5)

        apklist = os.listdir(MICROAPK)
        for file in apklist:
            if file.endswith('.apk'):
                print('Installing %s:' % file)
                sys.stdout.flush()
                try:
                    output = subprocess.check_output([ADB_COMMAND, '-s', 'localhost:4444', 'install', MICROAPK + '/' + file])
                    print('%s installed:' % file)
                    sys.stdout.flush()
                except Exception as e:
                    print("Error:\n%s" % e)
                    continue
        output = subprocess.check_output([ADB_COMMAND, 'disconnect', 'localhost:4444'])
        output = subprocess.check_output([ADB_COMMAND, 'forward', '--remove', 'tcp:4444'])
        print('All done. Have fun.')


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(e)
