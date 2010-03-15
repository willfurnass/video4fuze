#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Video Thumbnail Extractor
#
# Requirements:
# PIL 1.1.6 or later: http://www.pythonware.com/products/pil/index.htm
# FFMPEG: http://ffmpeg.mplayerhq.hu/download.html
#
# @author Vadim Zaliva <lord@crocodile.org>
#
# Adapted for video4fuze by Adrián Cereto <ssorgatem@esdebian.org>
#
# ----------------------------------------------------------------------
# LICENSE:
#
# Video Thumbnail Extractor
# Copyright (C) 2006  Vadim Zaliva
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#
"""
This module implements video thumbnail creation using ffmpeg
"""

import Image
import sys, os, time, math, shutil, string, tempfile
import getopt
from subprocess import check_call

NFRAMES=100
#FFMPEG="ffmpeg"
TMPDIR=tempfile.gettempdir()
THUMB_SIZE = 224, 176

def frame_rmse(hist, median):
    res = 0.0
    n = len(median)
    for j in range(n):
        err=median[j]-float(hist[j]);
        res+=(err*err)/n;
    return math.sqrt(res);

def img_hist(im):
    return im.histogram()

def copy_thumb(src, dst, thumb):
    if thumb:
        im = Image.open(src)
        im.thumbnail(THUMB_SIZE, Image.ANTIALIAS)
        im.save(dst, "JPEG")
    else:
        shutil.copyfile(src, dst)

def find_thumb(infile, outfile, nframes, alsosave, verbose, thumb, FFMPEG = "ffmpeg"):
    if verbose:
        infile = '\"' + infile + '\"'
        print "Processing %s" % infile
        print "Extracting frames"
    framemask = "frame" + str(time.time()) + ".%d.jpg"
    cmd = "%s -y -vframes %d -i %s %s" % (FFMPEG, nframes, infile, framemask)
    if not verbose:
        cmd = cmd + " -v -1" #> /dev/null 2>&1"
    if os.system(cmd) != 0:
        print "Error invoking ffmpeg"
        return 10

    if verbose:
        print "Analyzing frames"
    hist=[]
    for i in range(1,nframes+1):
        fname = framemask % i
        if not os.path.exists(fname):
            break
        if verbose:
            print "\tProcessin frame %d" % i
        im = Image.open(fname).convert("RGB")
        if not im or im.mode == None:
            print "Error reading frame %d" % i
            return 20
        hist.append(img_hist(im))
        if i in alsosave:
            thumbfname = outfile + "."+str(i)+".thm"
            if thumb:
                im.thumbnail(THUMB_SIZE, Image.ANTIALIAS)
                im.save(thumbfname, "JPEG")
            else:
                shutil.copyfile(fname, thumbfname)

    if verbose:
        print "Calculating averages"
    n=len(hist)
    avg=[]
    for c in range(len(hist[0])):
        ac = 0.0
        for i in range(n):
            ac = ac + (float(hist[i][c])/n)
        avg.append(ac)

    minn = -1
    minRMSE = -1
    for i in range(1,n+1):
        rmse = frame_rmse(hist[i-1], avg);
        if minn==-1 or rmse<minRMSE:
            minn = i
            minRMSE = rmse
        #print "Frame %d RMSE %f" % (i, rmse)
    if verbose:
        print "BEST Frame: %d" % minn

    rc = 0
    try:
        # Copy best
        copy_thumb(framemask % (minn), outfile + ".thm", thumb)
    except:
        print "Error copying thumb file"
        rc = 100

    if verbose:
        print "Removing temp files"
    for i in range(1,n+1):
        fname = framemask % i
        os.unlink(fname)
    return rc
