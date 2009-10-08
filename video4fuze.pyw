#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       Copyright 2009 Adrián Cereto Massagué <ssorgatem@esdebian.org>
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

#TODO: Fix songs drag'n'dropping
#FIXME: mencoder default settings suck
#FIXME: mencoder calling algorithm

settingsVERSION = "0.5"

import sys
from PyQt4.QtGui import QApplication
from PyQt4.QtCore import QTranslator, QString, QLocale
from GUI.MainWindow import MainWindow

def main():
    translator = QTranslator()
    translator.load(QString("translations/v4f_%1").arg(QLocale.system().name()))
    qttranslator = QTranslator()
    qttranslator.load(QString("qt_%1").arg(QLocale.system().name()))
    Vapp = QApplication(sys.argv)
    Vapp.setOrganizationName("ssorgatem productions")
    Vapp.setApplicationName("video4fuze " + settingsVERSION)
    Vapp.installTranslator(translator)
    Vapp.installTranslator(qttranslator)
    VentanaP = MainWindow()
    VentanaP.show()
    sys.exit(Vapp.exec_())

if __name__ == "__main__":
    main()
