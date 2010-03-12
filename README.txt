       Copyright 2009-2010 Adrián Cereto Massagué <ssorgatem@esdebian.org>

video4fuze is free software, distributed under the GPLv3. It may be called in this text "v4f", for short

Icons were created by Ben Brooks <benbrooks.co.uk>, and are under a
Creative Commons Attribution-Noncommercial-Share Alike 3.0 License.

This applications uses mencoder, ffmpeg and fuzemux in order to
convert your video files to be seen in you sansa fuze. All of them are open-source but I only include
their win32 binary for commodity reasons.

Thanks to ewelot, Dunny and  earthcrosser  from the sansa forums, for finding the way to convert the videos,
providing me with all necessary information about the .pla playlist format the fuze uses and writing a great crossplatform remuxer for the fuze. Without their findings this app wouldn't exist. Thank you ;)

For any feedback, suggestions, or if you want to contribute with translations (it's very easy!) or coding,
feel free to email me at <ssorgatem@gmail.com>

If you are using the "universal" distribution of video4fuze, in order for it to work you need on your system:

* Python >=2.5, < 3.0
* PyQt4 >= 4.5 (debian package: python-qt4) OR PySide (experimental support)
* PIL (Python Imaging Library) (debian package: python-imaging)
* Mencoder
* FFMPEG
* fuzemux (sources included in source package. Deb packages available for downloadfrom video4fuze's google code site. win32 build included in win32 versions)
* xterm (not needed, but recommended)

To run video4fuze, just type:

    python video4fuze.pyw

    (or double-click video4fuze.exe or it's shortcut if you installed v4f's windows version)

Make sure "mencoder", "ffmpeg" and "fuzemux" are in your path (or, in win32, the same folder as the main script).

If you downloaded the source package, fuzemux source is included in it. Just cd to its source directory and type "make" to get it compiled for your system.
