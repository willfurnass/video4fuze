       Copyright 2009 Adrián Cereto Massagué <ssorgatem@esdebian.org>

       This program is free software; you can redistribute it and/or modify
       it under the terms of the GNU General Public License as published by
       the Free Software Foundation; either version 3 of the License, or
       (at your option) any later version.

       This program is distributed in the hope that it will be useful,
       but WITHOUT ANY WARRANTY; without even the implied warranty of
       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
       GNU General Public License for more details.

       You should have received a copy of the GNU General Public License
       along with this program; if not, write to the Free Software
       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
       MA 02110-1301, USA.

video4fuze is free software, distributed under the GPLv3.

Icons were created by Ben Brooks <benbrooks.co.uk>, and are under a
Creative Commons Attribution-Noncommercial-Share Alike 3.0 License.

This applications uses mencoder, ffmpeg and fuzemux in order to
convert your video files to be seen in you sansa fuze. All of them are open-source but I only include
their win32 binary for commodity reasons.

Thanks to ewelot, Dunny and  earthcrosser  from the sansa forums, for finding the way to convert the videos,
providing me with all necessary information about the .pla playlist format the fuze uses and writing a great crossplatform remuxer for the fuze. Without their findings this app wouldn't exist. Thank you ;)

For any feedback, suggestions, or if you want to contribute with translations (it's very easy!) or coding,
feel free to email me at <ssorgatem@esdebian.og>

If you are using the "universal" distribution of video4fuze, in order for it to work you need on your system:

* Python >=2.5, < 3.0
* PyQt4 >= 4.5 (debian package: python-qt4)
* PIL (Python Imaging Library) (debian package: python-imaging)
* Mencoder
* FFMPEG
* xterm (not needed, but recommended)

To run video4fuze, just type:

    python video4fuze.pyw

    (or run video4fuze.exe if you're on win32 and have downloaded a py2exe'd version, or double click on i
    t on any decent desktop environment)

If you prefer the commandline version, just type:

    python fuze.py INPUTFILE1 INPUTFILE2 ...

    and it will conver every video you throw at it, and put the result in the same folder as the original,
    with suffix "_fuze" and extension ".avi".


Make sure "mencoder", "ffmpeg" and "fuzemux" are in your path (or, in win32, the same folder as the main script).

If you downloaded the source package, fuzemux source is included in it. Just cd to its source directory and type "make" to get it compiled for your system.
