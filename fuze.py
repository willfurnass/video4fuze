#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Class and methods to convert video for the fuze
"""
import os, tempfile, shutil, sys, commands, unicodedata
from subprocess import check_call, call
from PyQt4.QtCore import QT_TR_NOOP,SIGNAL,QObject,QString,QVariant
from vthumb import *

class Fuze( ):
    def __init__(self, GUI = None):
        self.GUI = GUI
        self.CWD = os.getcwd()
####################################################################
        self.mencoderpass1 = "mencoder -ffourcc DX50 -ofps 20 -vf pp=li,expand=:::::224/176,scale=224:176,harddup     -ovc lavc -lavcopts vcodec=mpeg4:vbitrate=683:vmax_b_frames=0:keyint=15:turbo:vpass=1 -srate 44100 -af resample=44100:0:1,format=s16le -oac mp3lame -lameopts cbr:br=128"

        self.mencoderpass2 = "mencoder -ffourcc DX50 -ofps 20 -vf pp=li,expand=:::::224/176,scale=224:176,harddup     -ovc lavc -lavcopts vcodec=mpeg4:vbitrate=683:vmax_b_frames=0:keyint=15:vpass=2 -srate 44100 -af resample=44100:0:1,format=s16le -oac mp3lame -lameopts cbr:br=128"
####################################################################
        if self.GUI != None:
            self.qobject = QObject()
            self.qobject.connect(self.qobject, SIGNAL("stop"),GUI.WAIT)
            self.qobject.connect(self.qobject, SIGNAL("working"),GUI.Status)
            self.qobject.connect(self.qobject, SIGNAL("Exception"),GUI.ErrorDiag)
            self.qobject.connect(self.qobject, SIGNAL("itemDone"),GUI.DelItem)
            self.qobject.connect(self.qobject, SIGNAL("finished"),GUI.getReady)
            self.LoadSettings()
        self.xterm = None
        if os.name == 'nt':
            self.FFMPEG = os.path.join(self.CWD, "ffmpeg.exe")
            self.AMGPrefix = tempfile.gettempdir()
            self.WINE = False
        else:
            self.FFMPEG = "ffmpeg"
            self.WINE = True
            wineprefix = os.environ.get('WINEPREFIX')
            if wineprefix != None:
                self.AMGPrefix = os.path.join(wineprefix,"drive_c")
            else:
                self.AMGPrefix = os.path.join(os.environ.get('HOME'),".wine/drive_c")
            try:
                call(["mkdir","-p",self.AMGPrefix])
            except Exception, e:
                print "Could not create wine C drive because of:"
                print e
                print "It may already exist"
            if os.name == 'posix' and self.GUI != None:
                termloc = commands.getstatusoutput("which xterm")
                if termloc[0] == 0:
                    self.xterm = termloc[1]
                else:
                    print "xterm not found"
                print self.xterm
            else:
                if self.GUI != None:
                    print "No terminal emulator available"

    def LoadSettings(self):
        self.mencoderpass1 = str(self.GUI.settings.value("mencoderpass1", QVariant(self.mencoderpass1)).toString())
        self.mencoderpass2 = str(self.GUI.settings.value("mencoderpass2", QVariant(self.mencoderpass2)).toString())

    def AmgConf(self,input,output):
        AMG = """CLEAR
LOAD """ + input +"""
LANGUAGE English
SET OPTION CLOSEAPP 1
SET OPTION DONEDLG 0
SET INPUT OPTIONS
WITH SET OPTION
UNBUFFERED 1
OVERLAPPED 1
ADD_IMMED 0
AVI FORCE MP3VBR 0
END WITH
WITH SET OPTION
FILEORDER 1 0
ADD_IMMED 1
USE CACHE 1
AVI FORCE MP3VBR 0
MP3 VERIFY CBR ASK
MP3 VERIFY RESDLG 0
M2F2 CRC 1
AVI FIXDX50 1
AVI IGNLCHUNKS OFF
AVI TRY2FIXLCHUNKS 0
WITH CHAPTERS
IMPORT 1
FROMFILENAMES 0
END WITH
END WITH
DESELECT FILE 0
SELECT FILE 1
ADD MMSOURCE
DESELECT FILE 0
SET OUTPUT OPTIONS
WITH SET OPTION
UNBUFFERED 1
THREAD 1
LOGFILE 0
STDOUTPUTFMT AVI
END WITH
DESELECT AUDIO 0
SELECT AUDIO 1
WITH SET OPTION
STREAMORDER 2 0 1
VIDEO NAMEEX 1 *
VIDEO DEFAULT 1 1
AUDIO NAMEEX 1 *
AUDIO DEFAULT 1 1
END WITH
DESELECT SUBTITLE 0
WITH SET OPTION
NO AUDIO 0
ALL AUDIO 1
NO SUBTITLES 0
ALL SUBTITLES 1
OPENDML 1
LEGACY 0
RECLISTS 0
FRAMES 0
PRELOAD 0
MP3 CBR FRAMEMODE 0
MAXFILESIZE OFF
AVI AC3FPC 2
AVI MP3FPC 1
AVI DTSFPC 2
AVI ADDJUNKBEFOREHEADERS 0
OGG PAGESIZE 65025
AVI RIFFAVISIZE 999
AVI HAALIMODE 0
OVERLAPPED 0
MAXFILESIZE 2030
MAXFILES OFF
NUMBERING OFF
NUMBERING $Name ($Nbr)
AUDIO INTERLEAVE 2 FR
SPLIT POINTS OFF
STDIDX 4000 FRAMES
PRLAC BYTE
TITLE boladedracz
END WITH
WITH SET OPTION MKV
LACE 3
LACESIZE general 1 500
LACESIZE mp3 1 500
LACESIZE ac3 1 200
LACESIZE dts 1 100
LACESIZE aac 1 200
LACESIZE vorbis 1 50
CLUSTERSIZE 512
CLUSTERTIME 30000
CLUSTERINDEX 0
HARDLINKING 0
NONCLUSTERINDEXMODE 1
HEADERSIZE 0
HEADERSTRIPPING 0
USE_A_AAC 0
PREVCLUSTERSIZE 1
CLUSTERPOSITION 1
LIMIT1STCLUSTER 1
DISPWH 1
CUES 1
CUES VIDEO 1
CUES AUDIO 1
CUES SUBS 1
CUES AUTOSIZE 1
CUES MINIMUMINTERVAL 2000
CUES SIZERATIO 20
CUES TARGETSIZERATIO 980
CUES WRITEBLOCKNUMBER 1
CUES AUDIO ONLY_AUDIO_ONLY 0
TIMECODESCALE MKA 10000
TIMECODESCALE MKV 500000
FORCE_V1 1
FORCE_V2 0
FLOAT_WIDTH 32
RANDOMIZE_ORDER 1
2ND_COPY_OF_TRACKS 1
END WITH
START """ + output + """
"""
        amgfile = open(os.path.join(self.AMGPrefix,"fuze.amg"), "w")
        amgfile.write(AMG)
        amgfile.close()

    def runmencoder(self, mencoderpassn, argument, OUTPUT):
        mencoderpass = str(mencoderpassn)
        mencoderpass = mencoderpass.split()
        if os.name == 'nt':
            mencoderpass[0] = os.path.join(self.CWD, "mencoder.exe")
        if self.GUI != None:
            self.qobject.emit(SIGNAL("working"),"Using mencoder on " + argument + "...")
            if self.xterm != None:
                mencoderpass = [self.xterm,"-e "] + mencoderpass
        mencoderpass = mencoderpass + [argument,"-o",OUTPUT]
        check_call(mencoderpass)

    def convert(self,args, FINALPREFIX =  None):
        os.chdir(self.AMGPrefix)
        tempfiles = {}
        if self.GUI != None:
            self.qobject.emit(SIGNAL("stop"),self.GUI.Video)
        for argument in args:
            if os.path.isfile(argument):
                if os.name == 'nt':
                    OUTPUT = os.path.join(self.AMGPrefix,os.path.splitext(os.path.basename(argument))[0] + ".temp.avi")#.encode("ascii", "ignore")
                else:
                    OUTPUT = unicodedata.normalize('NFKD',os.path.join(self.AMGPrefix,os.path.splitext(os.path.basename(argument))[0] + ".temp.avi")).encode("ascii", "ignore")
                try:
                    print "Calling mencoder #1"
                    self.runmencoder(self.mencoderpass1, argument, OUTPUT)
                except Exception, e:
                    print e
                    if self.GUI != None:
                        self.qobject.emit(SIGNAL("Exception"),e)
                    continue
                try:
                    print "Calling mencoder #2"
                    self.runmencoder(self.mencoderpass2, argument, OUTPUT)
                    tempfiles[OUTPUT] = argument
                except Exception, e:
                    print e
                    if self.GUI != None:
                        self.qobject.emit(SIGNAL("Exception"),e)
                    continue
            else:
                print "\'" + argument + "\'" + ": file not found"

        print "temporary files are: "
        print tempfiles

        for file in tempfiles.keys():
            if FINALPREFIX == None:
                FINAL = os.path.splitext(tempfiles[file])[0] + "_fuze.avi"
            else:
                FINAL = os.path.join(FINALPREFIX,os.path.splitext(os.path.basename(tempfiles[file]))[0]) + "_fuze.avi"
            try:
                print "Calling avi-mux GUI"
                if self.GUI != None:
                    self.qobject.emit(SIGNAL("working"),"Calling avi-mux GUI...")
                if self.WINE:
                    print "using wine"
                    OUTPUT =  """C:\\""" + os.path.basename(file)#.encode("ascii", "ignore")
                    print "Opening file: " + OUTPUT
                    self.AmgConf(OUTPUT,"C:\\final.avi")
                    wineprefix = os.environ.get('WINEPREFIX')
                    if wineprefix != None:
                       amgexe = os.path.join(wineprefix,"drive_c","avimuxgui","AVIMux_GUI.exe")
                    else:
                       amgexe = os.path.join(os.environ.get('HOME'),".wine","drive_c","avimuxgui","AVIMux_GUI.exe")
                    if os.path.isfile(amgexe):
                        call(["wine",amgexe,"C:\\fuze.amg"])
                    else:
                        call(["wine",os.path.join(self.CWD,"avimuxgui","AVIMux_GUI.exe"),"C:\\fuze.amg"])
                else:
                    OUTPUT = file#.encode("ascii", "ignore")
                    self.AmgConf(OUTPUT,os.path.join(self.AMGPrefix,"final.avi"))
                    call([os.path.join(self.CWD,"avimuxgui","AVIMux_GUI.exe"),os.path.join(self.AMGPrefix,"fuze.amg")])
            except Exception, e:
                print e
                if self.GUI != None:
                    self.qobject.emit(SIGNAL("Exception"),e)
                os.remove(os.path.join(self.AMGPrefix,"final.avi"))
                continue
            print "Moving " + os.path.join(self.AMGPrefix,"final.avi") + " to " + FINAL + " and cleaning temporary files"
            print FINAL
            try:
                try:
                    if self.GUI != None:
                        self.qobject.emit(SIGNAL("working"),"Creating video thumbnail")
                    print "Creating video thumbnail"
                    os.chdir(os.path.split(FINAL)[0])
                    find_thumb(os.path.join(self.AMGPrefix,"final.avi"), os.path.splitext(os.path.basename(FINAL))[0], 100, [], True, False, self.FFMPEG)
                except Exception, e:
                    print e
                    raise e
                    if self.GUI != None:
                        self.qobject.emit(SIGNAL("Exception"),e)
                shutil.move(os.path.join(self.AMGPrefix,"final.avi"),FINAL)
                os.chdir(self.CWD)
                os.chdir(self.CWD)
                if self.GUI != None:
                    self.qobject.emit(SIGNAL("itemDone"),tempfiles[file])
                os.remove(file)
                os.remove(os.path.join(self.AMGPrefix,"fuze.amg"))
            except Exception, e:
                print e
                print  "Ooops not moving final video"
                if self.GUI != None:
                    self.qobject.emit(SIGNAL("Exception"),e)
        if self.GUI != None:
            self.qobject.emit(SIGNAL("finished"),self.GUI.Video)

if __name__ == "__main__":
    if sys.argv[1:] == [] :
        print """Usage:
        python fuze.py INPUTVIDEO1 INPUTVIDEO2 ..."""
        exit(1)
    Fuze().convert(sys.argv[1:])

