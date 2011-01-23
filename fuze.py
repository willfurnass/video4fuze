#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       (c) 2009-2011 Adrián Cereto Massagué <ssorgatem@gmail.com>
#       (c) 2011 <russs.com@gmail.com>
#
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 3 of the License, or
#       (at your option) any later version.
#
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.
"""
Class and methods to convert video for the fuze
"""
import os, tempfile, shutil, commands, unicodedata, glob, multiprocessing
import info #info is a custom module
from subprocess import check_call, call
from PyQt4.QtCore import QT_TR_NOOP,SIGNAL,QObject,QString,QVariant, QSettings
from vthumb import *
####################################################################
mencoderpass1 = "mencoder -msglevel all=0:statusline=5 -ffourcc DX50 -ofps 20 -vf pp=li,expand=:::::224/176,scale=224:176,harddup     -ovc lavc -lavcopts vcodec=mpeg4:vbitrate=683:vmax_b_frames=0:keyint=15:turbo:vpass=1 -srate 44100 -af resample=44100:0:1,format=s16le -oac mp3lame -lameopts cbr:br=128"

mencoderpass2 = "mencoder -msglevel all=0:statusline=5 -ffourcc DX50 -ofps 20 -vf pp=li,expand=:::::224/176,scale=224:176,harddup     -ovc lavc -lavcopts vcodec=mpeg4:vbitrate=683:vmax_b_frames=0:keyint=15:vpass=2 -srate 44100 -af resample=44100:0:1,format=s16le -oac mp3lame -lameopts cbr:br=128"

mencodersinglepass = "mencoder  -msglevel all=0:statusline=5 -ofps 20 -ovc lavc -lavcopts vcodec=mpeg4:vqscale=3:keyint=15  -vf field,expand=:::::224/176,scale=224:176,harddup -srate 44100 -af resample=44100:0:1,format=s16le -oac mp3lame -lameopts cbr:br=128"
pass2 = False
####################################################################


fuzemuxPrefix = tempfile.gettempdir()
FINALPREFIX = None
if os.name == 'nt':
    FFMPEG = os.path.join(self.CWD, "ffmpeg.exe")
    fuzemux = os.path.join(self.CWD, "fuzemux.exe")
else:
    FFMPEG = "ffmpeg"
    fuzemux = "fuzemux"

xterm = None

if os.name == 'posix':
    termloc = commands.getstatusoutput("which xterm")
    if termloc[0] == 0:
        xterm = termloc[1]

vdict = {
    'pass2': pass2
    ,'mencoderpass1': mencoderpass1
    ,'mencoderpass2': mencoderpass2
    ,'mencodersinglepass':mencodersinglepass
    ,'fuzemuxPrefix':fuzemuxPrefix
    ,'FINALPREFIX':FINALPREFIX
    ,'fuzemux':fuzemux
    ,'FFMPEG':FFMPEG
    ,'xterm':xterm
         }


class Fuze():
    """
    This class implements a convert() method used to convert video files for the fuze.
    """
    def __init__(self, GUI = None):
        self.pool = multiprocessing.Pool()
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

        if os.name != 'posix' or not self.GUI:
            global xterm
            xterm = None

    def LoadSettings(self):
        """
        Loads video4fuze's settings for this instance
        """
        global mencoderpass1
        global mencoderpass2
        global mencodersinglepass
        global pass2
        self.Settings = QSettings(QSettings.IniFormat, QSettings.UserScope, info.ORGNAME, info.NAME)
        mencoderpass1 = unicode(self.Settings.value("mencoderpass1", QVariant(mencoderpass1)).toString())
        mencoderpass2 = unicode(self.Settings.value("mencoderpass2", QVariant(mencoderpass2)).toString())
        mencodersinglepass = unicode(self.Settings.value("mencodersinglepass",QVariant(mencodersinglepass)).toString())
        pass2 = self.Settings.value("2pass",QVariant(pass2)).toBool()
        print "Current settings:"
        print
        if pass2:
            print "Two-pass conversion;"
            print "Pass 1: ",  mencoderpass1
            print "Pass 2: ",  mencoderpass2
        else:
            print "Single-pass conversion;"
            print "Options used: ",  mencodersinglepass

    def convert(self,args, dest =  None):
        """
        This method converts any video file passed as argument to a file suitable for the sansa fuze.
        """
        vdict['FINALPREFIX'] = dest
        if self.GUI:
            self.qobject.emit(SIGNAL("stop"),self.GUI.Video)
            self.qobject.emit(SIGNAL("working"),"Converting files...")
        os.chdir(vdict['fuzemuxPrefix'])

        argslist = []
        for arg in args:
            if os.path.isfile(arg):
                argslist.append((arg, vdict))
            elif os.path.isdir(arg):
                if not os.path.isdir(arg + '/VIDEO_TS') and not os.path.isdir(arg + '/BDMV/STREAM'):
                    glob_file =  arg + '/*.??*'
                    for file in glob.glob(glob_file):
                        argslist.append((file, vdict))
                else:
                    argslist.append((arg, vdict))
            else:
                print arg,': file not found'
        #print [a[0] for a in argslist]

        for file, error in self.pool.map(_convert_process, argslist):
            if error:
                self.qobject.emit(SIGNAL("Exception"),unicode(error))
                print file, 'could not be converted succesfully'
            if self.GUI:
                self.qobject.emit(SIGNAL("itemDone"),file)
        os.chdir(self.CWD)
        if self.GUI:
            self.qobject.emit(SIGNAL("finished"),self.GUI.Video)
            print "Finished!"

def _convert_process(argumentlist):
    """
    """
    argument, vdict = os.path.abspath(argumentlist[0]), argumentlist[1]

    if vdict['FINALPREFIX'] == None:
        FINAL = os.path.splitext(argument)[0] + "_fuze.avi"
    else:
        FINAL = os.path.join(vdict['FINALPREFIX'],os.path.splitext(os.path.basename(argument))[0]) + "_fuze.avi"
    if os.path.isfile(FINAL) and os.path.getmtime(FINAL) >= os.path.getmtime(argument):
        print 'Skipping existing', FINAL
        return argument, 'File %s already exists' % argument
    print "Creating", FINAL
    valid_file_set = False
    srcfiles = [argument]

    glob_file = None
    if os.path.isdir(argument):
        if os.path.isdir(argument + '/VIDEO_TS'):
            #print "DVD directory specified"
            glob_file = argument + '/VIDEO_TS/*.vob'
        elif os.path.isdir(argument + '/BDMV/STREAM'):
            #Blu-ray directory specified
            glob_file = argument + '/BDMV/STREAM/*.m2ts'
    if glob_file:
        glob_files = glob.glob(glob_file)
        if glob_files:
            srcfiles = glob_files
            srcfiles.sort()
            valid_file_set = True

#################################mencoder pass 1###################
    if valid_file_set or os.path.isfile(argument):
        if os.name == 'nt':
            OUTPUT = os.path.join(vdict['fuzemuxPrefix'],os.path.splitext(os.path.basename(argument))[0] + ".temp.avi")
        else:
            OUTPUT = unicodedata.normalize('NFKD',os.path.join(vdict['fuzemuxPrefix'].decode('utf-8'),os.path.splitext(os.path.basename(argument))[0] + ".temp.avi")).encode("ascii", "ignore")
        print "Output =", OUTPUT
        try:
            if pass2:
                print "Calling mencoder #1"
                mencoderpass1 = unicode(vdict['mencoderpass1'])
            else:
                print "Calling a single pass of mencoder"
                mencoderpass1 = vdict['mencodersinglepass']
            #self.qobject.emit(SIGNAL("working"),"Using mencoder on " + argument + "...")
            if vdict['xterm']:
                mencoderpass1 = vdict['xterm'] + " -e " + mencoderpass1
            mencoderpass1 = mencoderpass1.split()
            for src in srcfiles:
                mencoderpass1.append(src)
            mencoderpass1.append("-o")
            mencoderpass1.append(OUTPUT)
            print "\n", mencoderpass1, "\n"
            check_call(mencoderpass1)
        except Exception, e:
            print e
            return argument, e
            #self.qobject.emit(SIGNAL("Exception"),e)
#####################mencoder pass 2#############################
        if vdict['pass2']:
            try:
                print "Calling mencoder #2"
                mencoderpass2 = unicode(vdict['mencoderpass2'])
                #self.qobject.emit(SIGNAL("working"),"Using mencoder on " + argument + " (pass 2)...")
                if vdict['xterm']:
                    mencoderpass2 = vdict['xterm'] + " -e " + mencoderpass2
                mencoderpass2 = mencoderpass2.split()
                mencoderpass2.append(argument)
                mencoderpass2.append("-o")
                mencoderpass2.append(OUTPUT)
                check_call(mencoderpass2)
            except Exception, e:
                print e
                return argument, e
                #self.qobject.emit(SIGNAL("Exception"),e)
########################################################

        try:
            fuzemux_temp = os.path.splitext(OUTPUT)[0] + "_fuzemuxed.avi"
            #self.qobject.emit(SIGNAL("working"),"Using " + fuzemux)
            if vdict['xterm']:
                vdict['fuzemux'] = vdict['xterm'] + " -e " + vdict['fuzemux']
            fuzemux=vdict['fuzemux'].split()
            fuzemux.append(OUTPUT)
            fuzemux.append(fuzemux_temp)
            print "Calling fuzemux", fuzemux
            check_call(fuzemux)
        except Exception, e:
            print e
            #self.qobject.emit(SIGNAL("Exception"),e)
            os.remove(fuzemux_temp)
            return argument, e

        print "Moving " + fuzemux_temp+ " to " + FINAL + " and cleaning temporary files"
        print FINAL
        try:
            try:
                destthumb = os.path.splitext(FINAL)[0] + '.thm'
                havethumb = find_thumb_from_image(argument, destthumb)

                if not havethumb:
                    #self.qobject.emit(SIGNAL("working"),"Creating video thumbnail")
                    print "Creating video thumbnail"
                    os.chdir(os.path.split(FINAL)[0])
                    find_thumb(fuzemux_temp, destthumb, 100, [], True, False, vdict['FFMPEG'])
            except Exception, e:
                print e
                return argument,e
                #self.qobject.emit(SIGNAL("Exception"),e)
            shutil.move(fuzemux_temp,FINAL)
            #self.qobject.emit(SIGNAL("itemDone"),argument)
            os.remove(OUTPUT)
        except Exception, e:
            print e
            print  "Ooops not moving final video"
            return argument, e
            #self.qobject.emit(SIGNAL("Exception"),e)
    else:
        error = "\'" + argument + "\'" + ": file not found"
        #self.qobject.emit(SIGNAL("Exception"),error)
        print error
        return argument, error

    print
    return argument, 0


def process_dir (src, dir = '', dest = './', fuze = None ):
    """
    Converts recursively all files in a directory and its subdirectories
    """
    if not fuze:
        fuze = Fuze()
    sdir = os.path.join(src, dir)
    if os.path.isdir(sdir + '/VIDEO_TS') or os.path.isdir(sdir + '/BDMV/STREAM'):
        fuze.convert([sdir], dest)
    else:
        ddir = os.path.join(dest, dir)
        if not os.path.exists(ddir):
            os.mkdir(ddir)
        sglob = glob.glob (os.path.join(sdir, '*'))
        for file in sglob:
            if os.path.isdir(file):
                try:
                    process_dir(sdir, os.path.split(file)[1], ddir, fuze)
                except Exception, e:
                    print unicode(e)


if __name__ == "__main__":
    from optparse import OptionParser

    multiprocessing.freeze_support()

    parser = OptionParser()
    parser.usage = """%prog [options] INPUT
    INPUT may be a list of files and directories"""
    parser.add_option("-o","--outputdir", dest="outputdir", help="save the converted files to OUTPUTDIR", metavar="OUTPUTDIR")
    parser.add_option('-r', '--recursive', action="store_true", dest="recursive", help = 'Convert files recursively in directories and all their subdirectories.')
    options, args = parser.parse_args()

    if options.outputdir:
        if not os.path.isdir(options.outputdir):
            print options.outputdir,  "is not a directory!"
            print "Aborting..."
            exit(1)
        print "Output directory:", options.outputdir
    else:
        print "Output directory: same as source"

    fuze = Fuze()

    if options.recursive:
        print 'Converting all files in', args
        dirs = [argument for argument in args if os.path.isdir(argument)]
        args = [file for file in args if file not in dirs]
        for dir in dirs:
            process_dir(src=dir,dest=options.outputdir, fuze = fuze)
    else:
        print "Files to convert:", args

    Fuze().convert(args,options.outputdir)
