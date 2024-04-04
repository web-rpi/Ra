# How to build "Ra" from DF9DQ

Here I'll show you how you can easily set up, flash, configure and test a "Ra" from DF9DQ.<br>
[DF9DQ Github Page](https://github.com/einergehtnochrein)

## Setting up the Ra app
First, the folder structure must be created on the SD card or the internal memory of the phone.<br>
I saved the folder structure as a ZIP file in the “Copy to SD” folder.<br>
The map files and elevation profiles required for the map view.<br>
These are available [here](https://ftp-stud.hs-esslingen.de/pub/Mirrors/download.mapsforge.org/maps/v5/) (map files) and [here](https://drive.google.com/drive/folders/0BxphPoRgwhnoWkRoTFhMbTM3RDA) (elevation profile).<br>
The map files are stored on the SD card in the folder structure `/ra/map/`.<br>
The height profiles (hgt files) are stored in `/ra/hgt/`.<br>
Map-Tiles can downloaded [here](https://www.thunderforest.com/maps/outdoors/).<br>
The downloaded [firmware](https://github.com/einergehtnochrein/ra-firmware/wiki/FirmwareReleases) is stored in the folder `/ra/firmware/`.<br>

The apk can be downloaded [here](https://github.com/einergehtnochrein/ra-hardware/wiki#android-app).<br>

[Original installation instructions from DF9DQ](https://github.com/einergehtnochrein/ra-hardware/wiki/app_installation)


## Flash the loader
In order to be able to use the Ra, this requires a "secondary bootloader". This enables the firmware to be updated via the app. Since creating this loader is a bit more complex. I have already compiled the latest loader version (v4) and uploaded it here. If you are interested in compiling, please contact me.
To flash the loader to the NXP chip you need an "LPC Link 2" or a similar programmer. These are available on the Internet. I did the flashing with the software "J-Flash Lite V6.86f".
->	Set jumper "J7" on the LPC Link 2<br>
->	Start the "J-Flash Lite V6.86f" software<br>
->	"LPC54114J256" must be selected as the device<br>
->	Interface remains with SWD with 4000 kHz<br>
->	Click on "OK"<br>
->	"ra2_loader_V4.hex" is selected<br>
->	The “Prog. Addr. “Must be on 0x00000000!<br>
->	Now the loader can be flashed onto the chip with "Program Device"

## Flash firmware
The firmware of the Ra‘ is flashed via the Android app. Here the app must be installed on the phone or tablet.
The latest firmware can be downloaded [here](https://github.com/einergehtnochrein/ra-firmware/wiki/FirmwareReleases/).<br>
->	Connect the phone to the Ra (LAIRD BL652) via Bluetooth<br>
->	Start the "Ra" app<br>
->	Click on the three dots at the top right<br>
->	Click on the menu item "Load new Ra firmware"/“Aktuelle Ra-Firmware laden”<br>
->	Select the latest firmware<br>
->	The process takes about 10 minutes (the app must remain in the foreground during this time!)<br>
->	The current versions can be read out using the "About"/"Über" menu item

## Update the BLE module
As outdated firmware is installed on the BLE modules, it must be replaced by a newer one (v28.9.5.0) so that the BT name of the Ra‘ can also be individually adapted.
It is imperative to ensure that the Loader V4 has been flashed on the NXP chip. If this is not the case, the BLE module can be destroyed under certain circumstances.<br>
->	Before connecting the Ra’s, the test point (TP2) between the NXP chip and the BLE module must be grounded.<br>
->	The Ra is now recognized as a "serial device" on the computer<br>
->	Start BL65xUartFwUpgrade.exe<br>
->	Select the COM port of the Ra’s<br>
->	Click Proceed (extreme caution! The BLE module can very easily be made unusable)<br>
->	With the UWTerminalX program, the current firmware can be checked with the command `at i 3`

## Upload the script to the BLE module to increase energy efficiency
### Required is:
-> [UwTerminalX](https://github.com/LairdCP/UwTerminalX/releases)<br>
-> [precompiled BLE script](https://github.com/einergehtnochrein/ra-firmware/tree/master/smartbasic/ra_power/1) "ra_power_xx.xx.x.x.uwc" from DF9DQ<br>
-> a piece of wire to set a bridge

### Procedure:
-> Update Ra firmware using the app<br>
-> Remove the batteries from the Ra<br>
-> Open Ra housing (loosen four screws and open cover)<br>
-> Bridge test point 2 (TP2, between microcontroller and BLE module) to ground (shield can be used)<br>
-> Connect Ra to a PC via USB<br>
-> Start UwTerminalX<br>
-> Set COM port and baud manually or use the "AUTO" button<br>
-> enter the command `at i 3` in the terminal to retrieve the current version of the BLE firmware<br>
-> Download precompiled BLE script from DF9DQ (see link above) with the correct version or compile it yourself if necessary<br>
-> Rename the downloaded file to "ra_power.uwc"<br>
-> In the terminal [right-click] and select the "Load" field<br>
-> Select the "ra_power.uwc" file<br>
-> use the command `at+dir` to check whether the file has been uploaded<br>
-> Assemble Ra


### Additional, helpful commands:
`at i 3` -> display BLE firmware<br>
`at+dir` -> display memory contents<br>
`at&f 1` -> delete memory contents<br>
`atz`    -> reboot the BLE module

## Creating the Ra configuration
A small Python script was written to create the configuration files for the Ra.
Here, the config.ini must first be adapted to the specific values.<br>
`referenceFrequency` -> reference frequency of the oscillator<br>
`rssiCorrectionLnaOn` -> RSSI correction when the preamp is switched on<br>
`rssiCorrectionLnaOff` -> RSSI correction when the preamp is switched off<br>
`nameBluetooth` -> Bluetooth name of the Ra<br>
If all values are adjusted to your own Ra, the script can be started with the call "python ra_conf.py". Shortly afterwards, all configurations are created and stored in the same directory.<br>
If the error “module crcmod not found” appears, the named module must be installed with “pip install crcmod”.<br>
In windows 10, Python has to be installed first. This can be easily downloaded and installed from the app store.<br>
[Download Python 3.9](https://www.microsoft.com/de-de/p/python-39/9p7qfqmjrfp7?activetab=pivot:overviewtab)

## Flashing the Ra configuration
The configuration is flashed exactly like that of the loader. The only difference is the address. This must be here at 0x38000.<br>
->	Set jumper "J7" on the LPC Link 2<br>
->	Start the "J-Flash Lite V6.86f" software<br>
->	"LPC54114J256" must be selected as the device<br>
->	Interface remains with SWD with 4000 kHz<br>
->	Click on "OK"<br>
->	"conf_XX.bin" is selected<br>
->	The “Prog. Addr. “Must be on 0x38000!<br>
->	Now the configuration can be flashed onto the chip with "Program Device"

## Finished!
The Ra is now ready for use.<br>
Have fun with this great Radiosonde receiver!<br>
Thank you DF9DQ for this nice project! ❤️
