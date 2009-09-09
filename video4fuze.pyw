#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from PyQt4.QtGui import QApplication
from PyQt4.QtCore import QTranslator, QString, QLocale
from GUI.MainWindow import MainWindow

#FIXME: Win32 UTF-8 issue.

if __name__ == "__main__":
    translator = QTranslator()
    translator.load(QString("translations/v4f_%1").arg(QLocale.system().name()))
    qttranslator = QTranslator()
    qttranslator.load(QString("qt_%1").arg(QLocale.system().name()))
    Vapp = QApplication(sys.argv)
    Vapp.setOrganizationName("ssorgatem productions")
    Vapp.setApplicationName("video4fuze 0.3")
    Vapp.installTranslator(translator)
    Vapp.installTranslator(qttranslator)
    VentanaP = MainWindow()
    VentanaP.show()
    sys.exit(Vapp.exec_())
