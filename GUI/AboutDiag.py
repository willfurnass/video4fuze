# -*- coding: utf-8 -*-

"""
Module implementing About Dialog.
"""

from PyQt4.QtGui import QDialog
from PyQt4.QtCore import QCoreApplication

from Ui_AboutDiag import Ui_Dialog

class Dialog(QDialog, Ui_Dialog):
    """
    Class documentation goes here.
    """
    def __init__(self, parent = None):
        """
        Constructor
        """
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.Appinfo.setText(QCoreApplication.applicationName())
        self.connect(self.okButton, SIGNAL("clicked()"),self.on_okButton_clicked)

    def on_okButton_clicked(self):
        # TODO: not implemented yet
        #raise NotImplementedError
        print "it works!"
