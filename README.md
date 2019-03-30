# mscorepluginconverter
Simple converter of MuseScore 2 plugins to MuseScore 3

The [MuseScore 3 plugin 
API](https://musescore.org/en/handbook/developers-handbook/plugins-3x) has a 
number of changes from that of MuseScore 2. Most of the changes are not very 
large though, so it is possible to resolve them with simple textual replacements 
(import statements, properties names/namespaces etc.) This repository contains a 
simple script automating such changes and thus allowing simple porting of 
MuseScore 2 plugins to MuseScore 3 in most cases.

## Usage
Simply run
```
./mscorepluginconverter.py plugin.qml plugin_converted.qml
```
where `plugin.qml` is the name of the MuseScore 2 plugin to convert, 
`plugin_converted.qml` is the name for the converted `.qml` file that should be 
(probably) usable with MuseScore 3.

On Windows, you will need to install Python first and run the script with it:
```
python3.exe mscorepluginconverter.py plugin.qml plugin_converted.qml
```

## On elements placement conversion
In order to place the added elements, MuseScore 2 plugins often used assigning 
`pos.x` and `pos.y` element properties. Due to an introduction of the [automatic 
placement](https://musescore.org/en/handbook/3/automatic-placement) in MuseScore 
3, it is no longer possible to specify exact element position. At least the 
following options are available here:
1. Remove `pos.x` and `pos.y` assignments letting the automatic placement do its 
job
2. Use `offsetX` and `offsetY` instead to specify position offsets (used by this 
converter)
3. Use `placement` property in case it was intended to specify the element 
placement above or below the staff:
```el.placement = Placement.BELOW```

This converter uses the option 2 but you may need to reconsider such cases 
manually in case setting position offsets does not match what is needed in a 
certain plugin's context.
