video4fuze
==========

Copyright 2009-2010 Adrián Cereto Massagué <ssorgatem@esdebian.org>

This repository is a clone of [this Subversion repository](https://code.google.com/p/video4fuze/).

video4fuze is free software, distributed under the GPLv3. It may be called in this text "v4f", for short.

Icons were created by Ben Brooks <benbrooks.co.uk>, and are licensed under Creative Commons Attribution-Noncommercial-Share Alike 3.0.

This application uses `mencoder`, `ffmpeg` and `fuzemux` in order to convert your video files so they can be played by the Sansa Fuze media player. All three of those dependencies are open-source but their win32 binaries have been included within this repository for commodity reasons.

Adrián Cereto Massagué would like to thank: ewelot, Dunny and  earthcrosser  from the sansa forums, for finding the way to convert the videos,
providing me with all necessary information about the .pla playlist format the fuze uses and writing a great crossplatform remuxer for the fuze. Without their findings this app wouldn't exist. Thank you ;)
Thanks also to M.A.E.M. Hanson for his (or her) useful help and testing.
Thanks to Peter Müller and Stefan Meier for the german translation.

For any feedback, suggestions, or if you want to contribute with translations (it's very easy!) or coding,
feel free to email Adrián Cereto Massagué at <ssorgatem@gmail.com>

If you are using the source distribution of video4fuze, you need the following in your system for it to work:

* Python >=2.5, < 3.0
* PyQt4 >= 4.5 (debian package: python-qt4)
* PIL (Python Imaging Library) (debian package: python-imaging)
* Mencoder (debian package: mencoder)
* FFMPEG (debian package: ffmpeg)
* fuzemux (Deb packages available for downloadfrom video4fuze's google code site. win32 build included in win32 versions, source at http://code.google.com/p/fuzemux/)
* xterm (not needed, but recommended)

To run video4fuze, just type:

    python video4fuze.pyw

or double-click video4fuze.exe or its shortcut if you installed v4f's Windows version

Make sure "mencoder", "ffmpeg" and "fuzemux" are in your path.
