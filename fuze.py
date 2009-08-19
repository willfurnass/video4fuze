# -*- coding: utf-8 -*-
"""
Functions to convert video for the fuze
"""
import os, tempfile, shutil, sys, commands
from subprocess import check_call, call


class Fuze():
    def __init__(self):
        self.xterm = None
        if os.name == 'nt':
            self.AMGPrefix = tempfile.gettempdir()
            self.WINE = False
        else:
            self.WINE = True
            wineprefix = os.environ.get('WINEPREFIX')
            if wineprefix != None:
                self.AMGPrefix = os.path.join(wineprefix,"drive_c")
            else:
                self.AMGPrefix = os.path.join(os.environ.get('HOME'),".wine/drive_c")
            if os.name == 'posix':
                termloc = commands.getstatusoutput("which xterm")
                if termloc[0] == 0:
                    self.xterm = termloc[1]
                else:
                    print "xterm not found"
                print self.xterm
            else:
                print "No terminal emulator available"
####################################################################
        size = "224:176"
        fps = "20"
        vbit = "683"        # in kbit/s
        abit = "128"        # in kbit/s
        keyint = "15"
        pass1 = "keyint=" + keyint + ":turbo:vpass=1"
        pass2 = "keyint=" + keyint + ":vpass=2"
#TODO: Ability to change mencoder commandline (with QSettings, presumably)
        self.mencoderpass1 = "mencoder -ofps " + fps + " -vf scale=" + size + ",harddup -ovc lavc -lavcopts vcodec=mpeg4:vbitrate=" + vbit + ":" + pass1 + " -srate 44100 -af resample=44100:0:1 -oac mp3lame -lameopts cbr:br=" + abit

        self.mencoderpass2 = "mencoder -ofps " + fps + " -vf scale=" + size + ",harddup -ovc lavc -lavcopts vcodec=mpeg4:vbitrate=" + vbit + ":" + pass2 + " -srate 44100 -af resample=44100:0:1 -oac mp3lame -lameopts cbr:br=" + abit
####################################################################
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
AVI RIFFAVISIZE 800
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

    def convert(self,args, FINALPREFIX =  None, GUI = None):
        if GUI != None:
            from PyQt4.QtCore import QT_TR_NOOP,SIGNAL,QObject
            self.qobject = QObject()
            self.qobject.connect(self.qobject, SIGNAL("stop"),GUI.WAIT)
            self.qobject.connect(self.qobject, SIGNAL("working"),GUI.Status)
            self.qobject.connect(self.qobject, SIGNAL("Exception"),GUI.ErrorDiag)
            self.qobject.connect(self.qobject, SIGNAL("itemDone"),GUI.DelItem)
            self.qobject.connect(self.qobject, SIGNAL("finished"),GUI.getReady)
            self.qobject.emit(SIGNAL("stop"))
        tempfiles = {}
        for argument in args:
            if os.path.isfile(argument):
                OUTPUT = os.path.join(self.AMGPrefix,os.path.splitext(os.path.basename(argument))[0] + ".temp.avi")
                try:
                    print "Calling mencoder #1"
                    mencoderpass1 = self.mencoderpass1 + " " + argument + " -o " + OUTPUT
                    if GUI != None:
                        self.qobject.emit(SIGNAL("working"),"Using mencoder on " + argument + "...")
                        if self.xterm != None:
                            mencoderpass1 = self.xterm + " -e " + mencoderpass1
                    check_call(mencoderpass1.split(" "))
                except Exception, e:
                    print e
                    if GUI != None:
                        self.qobject.emit(SIGNAL("Exception"),e)
                    continue
                try:
                    print "Calling mencoder #2"
                    mencoderpass2 = self.mencoderpass2 + " " + argument + " -o " + OUTPUT
                    if GUI != None:
                        self.qobject.emit(SIGNAL("working"),"Using mencoder on " + argument + " (pass 2)...")
                        if self.xterm != None:
                            mencoderpass2 = self.xterm + " -e " + mencoderpass2
                    check_call(mencoderpass2.split(" "))
                    tempfiles[OUTPUT] = argument
                except Exception, e:
                    print e
                    if GUI != None:
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
                if GUI != None:
                    self.qobject.emit(SIGNAL("working"),"Calling avi-mux GUI...")
                if self.WINE:
                    print "using wine"
                    OUTPUT =  """C:\\""" + os.path.basename(file)
                    print "Opening file: " + OUTPUT
                    self.AmgConf(OUTPUT,"C:\\final.avi")
                    call(["wine",os.path.join(os.getcwd(),"avimuxgui","AVIMux_GUI.exe"),"C:\\fuze.amg"])
                else:
                    OUTPUT = file
                    self.AmgConf(OUTPUT,os.path.join(self.AMGPrefix,"final.avi"))
                    call([os.path.join(os.getcwd(),"avimuxgui","AVIMux_GUI.exe"),os.path.join(self.AMGPrefix,"fuze.amg")])
            except Exception, e:
                print e
                if GUI != None:
                    self.qobject.emit(SIGNAL("Exception"),e)
                os.remove(os.path.join(self.AMGPrefix,"final.avi"))
                continue
            print "Moving " + os.path.join(self.AMGPrefix,"final.avi") + " to " + FINAL + " and cleaning temporary files"
            try:
                shutil.move(os.path.join(self.AMGPrefix,"final.avi"),FINAL)
                if GUI != None:
                    self.qobject.emit(SIGNAL("itemDone"),tempfiles[file])
                os.remove(file)
                os.remove(os.path.join(self.AMGPrefix,"fuze.amg"))
            except Exception, e:
                print e
                if GUI != None:
                    self.qobject.emit(SIGNAL("Exception"),e)
        if GUI != None:
            self.qobject.emit(SIGNAL("finished"))

if __name__ == "__main__":
    if sys.argv[1:] == [] :
        print """Usage:
        python fuze.py INPUTVIDEO"""
        exit(1)
    Fuze().convert(sys.argv[1:])

