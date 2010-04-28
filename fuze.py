#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Class and methods to convert video for the fuze
"""
import os, tempfile, shutil, sys, commands, unicodedata
import info
from subprocess import check_call, call
from PyQt4.QtCore import QT_TR_NOOP,SIGNAL,QObject,QString,QVariant, QSettings
from vthumb import *
####################################################################
mencoderpass1 = "mencoder -msglevel all=0:statusline=5 -ffourcc DX50 -ofps 20 -vf pp=li,expand=:::::224/176,scale=224:176,harddup     -ovc lavc -lavcopts vcodec=mpeg4:vbitrate=683:vmax_b_frames=0:keyint=15:turbo:vpass=1 -srate 44100 -af resample=44100:0:1,format=s16le -oac mp3lame -lameopts cbr:br=128"

mencoderpass2 = "mencoder -msglevel all=0:statusline=5 -ffourcc DX50 -ofps 20 -vf pp=li,expand=:::::224/176,scale=224:176,harddup     -ovc lavc -lavcopts vcodec=mpeg4:vbitrate=683:vmax_b_frames=0:keyint=15:vpass=2 -srate 44100 -af resample=44100:0:1,format=s16le -oac mp3lame -lameopts cbr:br=128"

mencodersinglepass = "mencoder  -msglevel all=0:statusline=5 -ofps 20 -ovc lavc -lavcopts vcodec=mpeg4:vqscale=3:keyint=15  -vf field,expand=:::::224/176,scale=224:176,harddup -srate 44100 -af resample=44100:0:1,format=s16le -oac mp3lame -lameopts cbr:br=128"
pass2 = False
####################################################################
class Fuze():
    """
    This class implements a convert() method used to convert video files for the fuze.
    """
    def __init__(self, GUI = None):
        self.GUI = GUI
        self.CWD = os.getcwd()
        self.qobject = QObject()
        if self.GUI:
            self.qobject.connect(self.qobject, SIGNAL("stop"),GUI.WAIT)
            self.qobject.connect(self.qobject, SIGNAL("working"),GUI.Status)
            self.qobject.connect(self.qobject, SIGNAL("Exception"),GUI.ErrorDiag)
            self.qobject.connect(self.qobject, SIGNAL("itemDone"),GUI.DelItem)
            self.qobject.connect(self.qobject, SIGNAL("finished"),GUI.getReady)
        self.LoadSettings()
        self.xterm = None
        self.fuzemuxPrefix = tempfile.gettempdir()
        if os.name == 'nt':
            self.FFMPEG = os.path.join(self.CWD, "ffmpeg.exe")
            self.mencoderpass1 = self.mencoderpass1.replace("mencoder",os.path.join(self.CWD, "mencoder.exe"))
            self.mencoderpass2 = self.mencoderpass2.replace("mencoder",os.path.join(self.CWD, "mencoder.exe"))
            self.fuzemux = os.path.join(self.CWD, "fuzemux.exe")
        else:
            self.FFMPEG = "ffmpeg"
            self.fuzemux = "fuzemux"
            if os.name == 'posix' and self.GUI != None:
                termloc = commands.getstatusoutput("which xterm")
                if termloc[0] == 0:
                    self.xterm = termloc[1]
                else:
                    print "xterm not found"
            else:
                if self.GUI != None:
                    print "No terminal emulator available"

    def LoadSettings(self):
        """
        Loads video4fuze's settings for this instance
        """
        self.Settings = QSettings(info.ORGNAME, info.NAME)
        self.mencoderpass1 = unicode(self.Settings.value("mencoderpass1", QVariant(mencoderpass1)).toString())
        self.mencoderpass2 = unicode(self.Settings.value("mencoderpass2", QVariant(mencoderpass2)).toString())
        self.mencodersinglepass = unicode(self.Settings.value("mencodersinglepass",QVariant(mencodersinglepass)).toString())
        self.pass2 = self.Settings.value("2pass",QVariant(pass2)).toBool()
        print "Current settings:"
        print
        print self.pass2
        if self.pass2:
            print "Two-pass conversion;"
            print "Pass 1: ",  self.mencoderpass1
            print "Pass 2: ",  self.mencoderpass2
        else:
            print "Single-pass conversion;"
            print "Options used: ",  self.mencodersinglepass

    def convert(self,args, FINALPREFIX =  None):
        """
        This method converts any video file passed as argument to a file suitable for the sansa fuze.
        """
        os.chdir(self.fuzemuxPrefix)
        if self.GUI:
	  self.qobject.emit(SIGNAL("stop"),self.GUI.Video)
        for argument in args:
#################################mencoder pass 1###################
            if os.path.isfile(argument):
                if os.name == 'nt':
                    OUTPUT = os.path.join(self.fuzemuxPrefix,os.path.splitext(os.path.basename(argument))[0] + ".temp.avi")
                else:
                    OUTPUT = unicodedata.normalize('NFKD',os.path.join(self.fuzemuxPrefix.decode('utf-8'),os.path.splitext(os.path.basename(argument))[0] + ".temp.avi")).encode("ascii", "ignore")
                try:
                    if self.pass2:
                        print "Calling mencoder #1"
                    else:
                        print "Calling a single pass of mencoder"
                    if self.pass2:
                        mencoderpass1 = unicode(self.mencoderpass1)
                    else:
                        mencoderpass1 = self.mencodersinglepass
                    self.qobject.emit(SIGNAL("working"),"Using mencoder on " + argument + "...")
                    if self.xterm != None:
                        mencoderpass1 = self.xterm + " -e " + mencoderpass1
                    mencoderpass1 = mencoderpass1.split()
                    mencoderpass1.append(argument)
                    mencoderpass1.append("-o")
                    mencoderpass1.append(OUTPUT)
                    print "\nExecuting", mencoderpass1, "\n"
                    check_call(mencoderpass1)
                except Exception, e:
                    print e
                    self.qobject.emit(SIGNAL("Exception"),e)
                    continue
#####################mencoder pass 2#############################
                if self.pass2:
                    try:
                        print "Calling mencoder #2"
                        mencoderpass2 = str(self.mencoderpass2)
                        self.qobject.emit(SIGNAL("working"),"Using mencoder on " + argument + " (pass 2)...")
                        if self.xterm != None:
                            mencoderpass2 = self.xterm + " -e " + mencoderpass2
                        mencoderpass2 = mencoderpass2.split()
                        mencoderpass2.append(argument)
                        mencoderpass2.append("-o")
                        mencoderpass2.append(OUTPUT)
                        check_call(mencoderpass2)
                    except Exception, e:
                        print e
                        self.qobject.emit(SIGNAL("Exception"),e)
                        continue
########################################################
            else:
                print "\'" + argument + "\'" + ": file not found"
            if FINALPREFIX == None:
                FINAL = os.path.splitext(argument)[0] + "_fuze.avi"
            else:
                FINAL = os.path.join(FINALPREFIX,os.path.splitext(os.path.basename(argument))[0]) + "_fuze.avi"
            try:
                fuzemux = self.fuzemux
                fuzemux_temp = os.path.splitext(OUTPUT)[0] + "_fuzemuxed.avi"
                self.qobject.emit(SIGNAL("working"),"Using " + fuzemux)
                if self.xterm != None:
                    fuzemux = self.xterm + " -e " + fuzemux
                fuzemux=fuzemux.split()
                fuzemux.append(OUTPUT)
                fuzemux.append(fuzemux_temp)
                print "Calling fuzemux"
                check_call(fuzemux)
            except Exception, e:
                print e
                self.qobject.emit(SIGNAL("Exception"),e)
                os.remove(fuzemux_temp)
                continue
            print "Moving " + fuzemux_temp+ " to " + FINAL + " and cleaning temporary files"
            print FINAL
            try:
                try:
                    self.qobject.emit(SIGNAL("working"),"Creating video thumbnail")
                    print "Creating video thumbnail"
                    os.chdir(os.path.split(FINAL)[0])
                    find_thumb(fuzemux_temp, os.path.splitext(os.path.basename(FINAL))[0], 100, [], True, False, self.FFMPEG)
                except Exception, e:
                    print e
                    raise e
                    self.qobject.emit(SIGNAL("Exception"),e)
                shutil.move(fuzemux_temp,FINAL)
                os.chdir(self.CWD)
                os.chdir(self.CWD)
                self.qobject.emit(SIGNAL("itemDone"),argument)
                os.remove(OUTPUT)
            except Exception, e:
                print e
                print  "Ooops not moving final video"
                self.qobject.emit(SIGNAL("Exception"),e)
	if self.GUI:
	  self.qobject.emit(SIGNAL("finished"),self.GUI.Video)

if __name__ == "__main__":
    if sys.argv[1:] == [] :
        print """Usage:
        python fuze.py INPUTVIDEO1 INPUTVIDEO2 ..."""
        exit(1)
    Fuze().convert(sys.argv[1:])
