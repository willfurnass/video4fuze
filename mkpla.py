#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#This module is inspired in Dunny's YAPL, and has been possible to write thanks to his help about the
# .pla playlist format.

#Two files: filename.pla and filename.pla.refs
#The former, is empty, the latter contains all the paths, following:
#Internal memory is /mmc:0/
#µSD is /mmc:1/

#Line endings have to be DOS CR+LF

import os

#TODO: playlist creator/editor.

#1 - get fuze's internal and µSD root directories: Let the user tell us them

#2 - Open (create) a playlist, and load it's contents, if any.

#3 - Put there songs, converting paths (maybe path normalisation?)

#4 - Allow reordering and so, this should be a GUI thingcommalist

#5 - Save the file.
