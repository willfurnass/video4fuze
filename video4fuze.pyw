#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, os, tempfile, shutil
from subprocess import call

if sys.argv[1:] == [] :
    print """Usage:
    python video4fuze.pyw INPUTVIDEO[.avi/.mp4/.asf]
    or, in order to display the GUI:
    python video4fuze.pyw --gui"""
    exit(1)
#extlist = [".avi",".mp4",".asf"]
if os.name == 'nt':
    AMGPrefix = tempfile.gettempdir()
    WINE = False
else:
    WINE = True
    wineprefix = os.environ.get('WINEPREFIX')
    if wineprefix != None:
        AMGPrefix = os.path.join(wineprefix,"drive_c")
    else:
        AMGPrefix = os.path.join(os.environ.get('HOME'),".wine/drive_c")

def AmgConf(input,output):
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
LOAD /tmp/test.avi
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
    open(os.path.join(AMGPrefix,"fuze.amg"), "w").write(AMG)

def convert(args, FINAL =  None):
    size = "224:176"
    fps = "20"
    vbit = "683"        # in kbit/s
    abit = "128"        # in kbit/s
    keyint = "15"

    tempavi = os.path.join(tempfile.gettempdir(),"ffmpeg.avi") #Just in case we need to use ffmpeg and i have to revert it's dropping

    pass1 = "keyint=" + keyint + ":turbo:vpass=1"
    pass2 = "keyint=" + keyint + ":vpass=2"

    for argument in args:
        if os.path.isfile(argument):
            OUTPUT = os.path.join(AMGPrefix,"temp.avi")
            if FINAL == None:
                FINAL = os.path.splitext(argument)[0] + ".fuze.avi"
#            if os.path.splitext(argument)[1].lower() not in extlist: #mencoder seems just to be happy with everything you throw to it.
#                print "Input video needs to be in a suitable format. Suitable formats are:"
#                print extlist
#                exit(1)
#            print "Calling ffmpeg"
#            try:
#                call(["ffmpeg","-i",argument,"-vcodec","libxvid","-r",fps,"-b","1000k","-acodec","copy","-y",tempavi])
#            except Exception, e:
#                print e
#                continue #Problems dropping last part of the videos
            tempavi = argument
            try:
                print "Calling mencoder #1"
                call(["mencoder","-ofps",fps,"-vf","scale=" + size + ",harddup","-ovc","lavc","-lavcopts","vcodec=mpeg4:vbitrate=" + vbit + ":" + pass1,"-srate","44100","-af","resample=44100:0:1","-oac","mp3lame","-lameopts","cbr:br=" + abit,tempavi,"-o",OUTPUT])
            except Exception, e:
                print e
                continue
            try:
                print "Calling mencoder #2"
                call(["mencoder","-ofps",fps,"-vf","scale=" + size + ",harddup","-ovc","lavc","-lavcopts","vcodec=mpeg4:vbitrate=" + vbit + ":" + pass2,"-srate","44100","-af","resample=44100:0:1","-oac","mp3lame","-lameopts","cbr:br=" + abit,tempavi,"-o",OUTPUT])
            except Exception, e:
                print e
                continue
            try:
                print "Calling avi-mux GUI"
                if WINE:
                    print "using wine"
                    OUTPUT =  """C:\\temp.avi"""
                    AmgConf(OUTPUT,"C:\\final.avi")
                    call(["wine",os.path.join(os.getcwd(),"avimuxgui","AVIMux_GUI.exe"),"C:\\fuze.amg"])
                else:
                    AmgConf(OUTPUT,os.path.join(AMGPrefix,"final.avi"))
                    call([os.path.join(os.getcwd(),"avimuxgui","AVIMux_GUI.exe"),os.path.join(AMGPrefix,"fuze.amg")])
            except Exception, e:
                print e
                continue
#            os.remove(tempavi)
            shutil.move(os.path.join(AMGPrefix,"final.avi"),FINAL)
            os.remove(os.path.join(AMGPrefix,"temp.avi"))
            os.remove(os.path.join(AMGPrefix,"fuze.amg"))
        else:
            print "\'" + argument + "\'" + ": file not found"

if "--gui" in sys.argv[1]:
    #TODO:GUI things
    from GUI import MainWindow
    GUI = True
    print "Still In Development"
    translator = QTranslator()
    translator.load(QString("translations/v4f_%1").arg(QLocale.system().name()))
    qttranslator = QTranslator()
    qttranslator.load(QString("qt_%1").arg(QLocale.system().name()))
    Vapp = QApplication(sys.argv)
    Vapp.installTranslator(translator)
    Vapp.installTranslator(qttranslator)
    VentanaP = MainWindow()
    VentanaP.show()
    sys.exit(Vapp.exec_())
else:
    GUI = False
    convert(sys.argv[1:])
