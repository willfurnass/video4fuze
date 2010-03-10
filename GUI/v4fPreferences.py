# -*- coding: utf-8 -*-

"""
Module implementing PreferencesDialog.
"""

from PyQt4.QtGui import QDialog
from PyQt4.QtCore import QSettings, QVariant,SIGNAL
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
        self.connect(self.DefaultsButton, SIGNAL("clicked()"),self.on_DefaultsButton_clicked)
        self.connect(self.okButton, SIGNAL("clicked()"),self.on_okButton_clicked)

    def on_DefaultsButton_clicked(self):
        """
        Restore defaults from fuze.py
        """
        self.mencoderpass1Edit.setPlainText(self.default.mencoderpass1)
        self.mencoderpass2Edit.setPlainText(self.default.mencoderpass2)

    def on_okButton_clicked(self):
        """
        Apply the changes
        """
        QSettings().setValue("mencoderpass1", QVariant(self.mencoderpass1Edit.toPlainText()))
        QSettings().setValue("mencoderpass2", QVariant(self.mencoderpass2Edit.toPlainText()))
