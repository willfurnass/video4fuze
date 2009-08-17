#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

if sys.argv[1:] == [] :
    print """Usage:
    python video4fuze.pyw INPUTVIDEO[.avi/.mp4/.asf]
    or, in order to display the GUI:
    python video4fuze.pyw --gui"""
    exit(1)

if "--gui" in sys.argv[1]:
    #TODO:GUI things
    from PyQt4.QtGui import QApplication
    from PyQt4.QtCore import QTranslator, QString, QLocale
    from GUI.MainWindow import MainWindow
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
    import fuze
    fuze.convert(sys.argv[1:])
