# -*- coding: utf-8 -*-

"""
Module implementing PreferencesDialog.
"""

from PyQt4.QtGui import QDialog
from PyQt4.QtCore import pyqtSignature, QSettings, QVariant
import fuze

from Ui_Preferences import Ui_PreferencesDialog

class PreferencesDialog(QDialog, Ui_PreferencesDialog):
    """
    video4fuze preferences dialog
    """
    def __init__(self, parent = None):
        """
        Constructor
        """
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.default = fuze.Fuze()
        self.mencoderpass1Edit.setPlainText(QSettings().value("mencoderpass1",QVariant(self.default.mencoderpass1)).toString())
        self.mencoderpass2Edit.setPlainText(QSettings().value("mencoderpass2",QVariant(self.default.mencoderpass2)).toString())

    @pyqtSignature("")
    def on_DefaultsButton_clicked(self):
        """
        Restore defaults from fuze.py
        """
        self.mencoderpass1Edit.setPlainText(self.default.mencoderpass1)
        self.mencoderpass2Edit.setPlainText(self.default.mencoderpass2)

    @pyqtSignature("")
    def on_okButton_clicked(self):
        """
        Apply the changes
        """
        QSettings().setValue("mencoderpass1", QVariant(self.mencoderpass1Edit.toPlainText()))
        QSettings().setValue("mencoderpass2", QVariant(self.mencoderpass2Edit.toPlainText()))
