#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module implements image export features for video4fuze
"""
import os, sys, Image
from PyQt4.QtCore import QT_TR_NOOP,SIGNAL,QObject, QSettings, QVariant

defaultsize = 224, 176

class TransFuze():
    """
    Convert input image to a fuze-suitable image
    """
    #Do something useful
    def __init__(self, GUI = None):
        self.size = [int(QSettings().value("imagew",QVariant(defaultsize[0])).toInt()[0]), int(QSettings().value("imageh",QVariant(defaultsize[1])).toInt()[0])]
        self.size = defaultsize
        self.GUI = GUI
        self.tab = GUI.Image
        if self.GUI != None:
            self.qobject = QObject()
            self.qobject.connect(self.qobject, SIGNAL("stop"),GUI.WAIT)
            self.qobject.connect(self.qobject, SIGNAL("working"),GUI.Status)
            self.qobject.connect(self.qobject, SIGNAL("Exception"),GUI.ErrorDiag)
            self.qobject.connect(self.qobject, SIGNAL("itemDone"),GUI.DelItem)
            self.qobject.connect(self.qobject, SIGNAL("finished"),GUI.getReady)

    def convert(self,args, FINALPREFIX =  None):
        """
        This method converts the passed files to jpg viewable in the fuze.
        """
        self.qobject.emit(SIGNAL("stop"),self.tab)
        for argument in args:
            try:
                self.qobject.emit(SIGNAL("working"),"Converting " + argument + "...")
                image = Image.open(argument)
                image.thumbnail(self.size, Image.ANTIALIAS)
                if FINALPREFIX == None:
                    image.save(os.path.splitext(argument)[0] + "_fuze.jpg")
                else:
                    image.save(os.path.join(FINALPREFIX,os.path.splitext(os.path.basename(argument))[0] + "_fuze.jpg"))
                self.qobject.emit(SIGNAL("itemDone"), argument, True)
            except Exception, e:
                print e
                self.qobject.emit(SIGNAL("Exception"),e)
        self.qobject.emit(SIGNAL("finished"),self.tab)


if __name__ == "__main__":
    if sys.argv[1:] == [] :
        print """Usage:
        python p2fuze.py INPUTIMAGE1 INPUTIMAGE2 ..."""
        exit(1)
    TransFuze().convert(sys.argv[1:])
