video4fuze is free software, distributed under the GPLv3.

Icons were created by Ben Brooks <benbrooks.co.uk>, and are under a
Creative Commons Attribution-Noncommercial-Share Alike 3.0 License.

This applications uses mencoder and avi-mux GUI (under wine where necessary) in order to convert your video files to be seen in you sansa fuze. Both are open-source but I only include the win32 binary for commodity reasons.

Thanks to ewelot from the sansa forums for finding the way to convert the videos, without his findings this app wouldn't exist

For any feedback, suggestions, or if you want to contribute with translations (it's very easy!) or coding,
feel free to email me at <ssorgatem@esdebian.og>

If you are using the "universal" distribution of video4fuze, in order for it to work you need on your system:

* Python >=2.5, < 3.0
* PyQt4 >= 4.5 (debian package: python-qt4)
* PIL (Python Imaging Library) (debian package: python-imaging)
* Mencoder
* FFMPEG

To run video4fuze, just type:

    python video4fuze.pyw

    (or run video4fuze.exe if you're on win32 and have downloaded a py2exe'd version)

If you prefer the commandline version, just type:

    python fuze.py INPUTFILE1 INPUTFILE2 ...

    and it will conver every video you throw at it, and put the result in the same folder as the original, with postfix "_fuze" and extension ".avi".


Make sure "mencoder" is in your path (or, in win32, the same folder as the main script),
and that avi-mux GUI executable is in the root of the folder "avimuxgui" included in the package.
