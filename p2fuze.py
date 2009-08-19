#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module implements image export features for video4fuze
"""
import os, sys, Image
from PyQt4.QtCore import QT_TR_NOOP,SIGNAL,QObject

class TransFuze():
    """
    Convert input image to a fuze suitable image
    """
    #Do something useful
    def __init__(self, GUI = None):
        self.extlist = (".bmp",".cur",".dcx",".eps", ".fli", ".flc", ".fpx", ".gbr",".gd",".gif", ".ico",".im",".imt",".iptc",".naa",".jpg",".jpeg",".mcidas",".mic",".msp",".pcd",".pcx",".pixar",".png",".ppm",".pgm",".pbm",".psd",".sgi", ".tga",".tiff",".tif",".wal",".xbm",".xpm",".xv")
        self.size = 224, 176
        self.GUI = GUI
        if self.GUI != None:
            self.qobject = QObject()
            self.qobject.connect(self.qobject, SIGNAL("stop"),GUI.WAIT)
            self.qobject.connect(self.qobject, SIGNAL("working"),GUI.Status)
            self.qobject.connect(self.qobject, SIGNAL("Exception"),GUI.ErrorDiag)
            self.qobject.connect(self.qobject, SIGNAL("itemDone"),GUI.DelItem)
            self.qobject.connect(self.qobject, SIGNAL("finished"),GUI.getReady)

    def convert(self,args, FINALPREFIX =  None):
        for argument in args:
            try:
                image = Image.open(argument)
                image.thumbnail(self.size, Image.ANTIALIAS)
                if FINALPREFIX == None:
                    image.save(os.path.splitext(argument)[0] + "_fuze.jpg")
                else:
                    image.save(os.path.join(FINALPREFIX,os.path.splitext(os.path.basename(argument))[0] + "_fuze.jpg"))
            except Exception, e:
                print e
                if self.GUI != None:
                    self.qobject.emit(SIGNAL("Exception"),e)

if __name__ == "__main__":
    if sys.argv[1:] == [] :
        print """Usage:
        python p2fuze.py INPUTIMAGE1 INPUTIMAGE2 ..."""
        exit(1)
    TransFuze().convert(sys.argv[1:])
