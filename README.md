# Wear OS Helper

## Simple scripts to make Wear OS great again. Linux + macOS

### extract_microapks.py

Pull all user applications from your android and try to extract microapks for Wear OS inside from them.

#### Note

    1. Make sure that `adb` is in your PATH. 2. You've configured udev rules or started adb service with root permission.
    3. Make sure your android is connected to your computer after the script showing `Waiting for device to connect...`.

### install_wear_apks.py

Install all extracted apks to Wear OS, if possible.

#### Note

    1. Make sure your android is connected before running.
    2. Make sure your wear has enabled ADB debug and bluetooth adb debug in developer options.
    3. Check the android Wear OS app, and enable bluetooth debug in andvanced settings.

### WINDOWS?

    Maybe working with some workarounds. PR is welcomed.
