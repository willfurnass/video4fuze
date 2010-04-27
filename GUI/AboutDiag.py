# -*- coding: utf-8 -*-

"""
Module implementing About Dialog.
"""

from PyQt4.QtGui import QDialog
from PyQt4.QtCore import QCoreApplication, SIGNAL, QString

from Ui_AboutDiag import Ui_Dialog

class AboutV4F(QDialog, Ui_Dialog):
    """
    V4F about dialog
    """
    def __init__(self, parent = None):
        """
        Constructor
        """
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.Appinfo.setText(QCoreApplication.applicationName()+" "+QCoreApplication.applicationVersion())
        try:
            READMEfile = open("README.txt","rb")
            README = QString(READMEfile.read())
            READMEfile.close()
        except Exception, e:
            README = unicode(e)
        try:
            LICENSEfile = open("LICENSE.html","rb")
            LICENSE= LICENSEfile.read()
            LICENSEfile.close()
        except Exception, e:
            LICENSE = unicode(e)
        self.ReadmeText.setText(README)
        self.LicenseText.setText(LICENSE)
        self.connect(self.okButton, SIGNAL("clicked()"), self.accept)
