# How to build "Ra" from DF9DQ

Here I'll show you how you can easily set up, flash, configure and test a "Ra" from DF9DQ (https://github.com/einergehtnochrein).<br>

<b>Setting up the Ra app</b><br>
First, the folder structure must be created on the SD card or the internal memory of the phone.<br>
I saved the folder structure as a ZIP file in the “Copy to SD” folder.<br>
The map files and elevation profiles required for the map view.<br>
These are available here https://ftp-stud.hs-esslingen.de/pub/Mirrors/download.mapsforge.org/maps/v5/ (map files) and here https://gliding.lxnav.com/lxdownloads/hgt-maps/ (elevation profile).<br>
The map files are stored on the SD card in the folder structure /ra/map/.<br>
The height profiles (.hgt) are stored in /ra/hgt/.<br>
The downloaded firmware (.hex) https://github.com/einergehtnochrein/ra-firmware/wiki/FirmwareReleases is stored in the folder /ra/firmware/.<br>

The apk can be downloaded here:<br>
https://github.com/einergehtnochrein/ra-hardware/wiki#android-app<br>

Original installation instructions from DF9DQ:<br>
https://github.com/einergehtnochrein/ra-hardware/wiki/app_installation<br>


<b>Flash the loader</b><br>
In order to be able to use the Ra, this requires a "secondary bootloader". This enables the firmware to be updated via the app. Since creating this loader is a bit more complex. I have already compiled the latest loader version (v4) and uploaded it here. If you are interested in compiling, please contact me.
To flash the loader to the NXP chip you need an "LPC Link 2" or a similar programmer. These are available on the Internet. I did the flashing with the software "J-Flash Lite V6.86f".
->	Set jumper "J7" on the LPC Link 2<br>
->	Start the "J-Flash Lite V6.86f" software<br>
->	"LPC54114J256" must be selected as the device<br>
->	Interface remains with SWD with 4000 kHz<br>
->	Click on "OK"<br>
->	"ra2_loader_V4.hex" is now selected<br>
->	The “Prog. Addr. “Must be on 0x00000000!<br>
->	Now the loader can be flashed onto the chip with "Program Device"<br><br>

<b>Flash firmware</b><br>
The firmware of the Ra‘ is flashed via the Android app. Here the app must be installed on the phone or tablet.
The latest firmware can be downloaded here: https://github.com/einergehtnochrein/ra-firmware/wiki/FirmwareReleases/
->	Connect the phone to the Ra via Bluetooth<br>
->	Start the "Ra" app<br>
->	Click on the three dots at the top right<br>
->	Click on the menu item “Aktuelle Ra-Firmware laden”<br>
->	Select the latest firmware<br>
->	The process takes about 10 minutes (the app must remain in the foreground during this time!)<br>
->	The current versions can be read out using the "Über" menu item<br><br>

<b>Update the BLE module</b><br>
As outdated firmware is installed on the BLE modules, it must be replaced by a newer one (v28.9.5.0) so that the BT name of the Ra‘ can also be individually adapted.
It is imperative to ensure that the Loader V4 has been flashed on the NXP chip. If this is not the case, the BLE module can be destroyed under certain circumstances.
->	Before connecting the Ra’s, the test point (TP2) between the NXP chip and the BLE module must be grounded.<br>
->	The Ra is now recognized as a "serial device" on the computer<br>
->	Start BL65xUartFwUpgrade.exe<br>
->	Select the COM port of the Ra’s<br>
->	Click Proceed (extreme caution! The BLE module can very easily be made unusable)<br>
->	With the UWTerminalX program, the current firmware can be checked with the command "at i 3"<br><br>

<b>Creating the Ra configuration</b><br>
A small Python script was written to create the configuration files for the Ra.
Here, the config.ini must first be adapted to the specific values.<br>
referenceFrequency = reference frequency of the oscillator<br>
rssiCorrectionLnaOn = RSSI correction when the preamp is switched on<br>
rssiCorrectionLnaOff = RSSI correction when the preamp is switched off<br>
nameBluetooth = Bluetooth name of the Ra<br>
If all values are adjusted to your own Ra, the script can be started with the call "python ra_conf.py". Shortly afterwards, all configurations are created and stored in the same directory.
If the error “module crcmod not found” appears, the named module must be installed with “pip install crcmod”.<br>
In windows 10, Python has to be installed first. This can be easily downloaded and installed from the app store.<br>
https://www.microsoft.com/de-de/p/python-39/9p7qfqmjrfp7?activetab=pivot:overviewtab

<b>Flashing the Ra configuration</b><br>
The configuration is flashed exactly like that of the loader. The only difference is the address. This must be here at 0x3800.
->	Set jumper "J7" on the LPC Link 2<br>
->	Start the "J-Flash Lite V6.86f" software<br>
->	"LPC54114J256" must be selected as the device<br>
->	Interface remains with SWD with 4000 kHz<br>
->	Click on "OK"<br>
->	"conf_XX.bin" is now selected<br>
->	The “Prog. Addr. “Must be on 0x3800!<br>
->	Now the loader can be flashed onto the chip with "Program Device"<br><br>

Finished! The Ra is now ready for use.
