# -*- coding: utf-8 -*-

"""
Module implementing PreferencesDialog.
"""

from PyQt4.QtGui import QDialog
from PyQt4.QtCore import QSettings, QVariant,SIGNAL,  QCoreApplication
import fuze, p2fuze

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
        self.Settings = QSettings(QSettings.IniFormat, QSettings.UserScope, QCoreApplication.organizationName(), QCoreApplication.applicationName())
        self.loadSettings(self.Pass2Check.isChecked())
        self.connect(self.DefaultsButton, SIGNAL("clicked()"),self.on_DefaultsButton_clicked)
        self.connect(self.okButton, SIGNAL("clicked()"),self.on_okButton_clicked)
        self.connect(self.Pass2Check, SIGNAL("toggled(bool)"), self.loadSettings)
        self.Pass2Check.setChecked(self.Settings.value("2pass",QVariant("False")).toBool())
            

    def loadSettings(self, pass2):
        if pass2:
            print "loading settings for 2 passes"
            print pass2
            self.mencoderpass1Edit.setPlainText(self.Settings.value("mencoderpass1",QVariant(fuze.mencoderpass1)).toString())
            self.mencoderpass2Edit.setPlainText(self.Settings.value("mencoderpass2",QVariant(fuze.mencoderpass2)).toString())
        else:
            print "loading settings for single pass"
            self.mencoderpass1Edit.setPlainText(self.Settings.value("mencodersinglepass",QVariant(fuze.mencodersinglepass)).toString())
        self.Wiline.setText(self.Settings.value("imagew",QVariant(str(p2fuze.defaultsize[0]))).toString())
        self.Heline.setText(self.Settings.value("imageh",QVariant(str(p2fuze.defaultsize[1]))).toString())

    def on_DefaultsButton_clicked(self):
        """
        Restore defaults from fuze.py
        """
        if self.Pass2Check.isChecked():
            self.mencoderpass1Edit.setPlainText(fuze.mencoderpass1)
            self.mencoderpass2Edit.setPlainText(fuze.mencoderpass2)
        else:
            self.mencoderpass1Edit.setPlainText(fuze.mencodersinglepass)
        self.Wiline.setText(str(p2fuze.defaultsize[0]))
        self.Heline.setText(str(p2fuze.defaultsize[1]))

    def on_okButton_clicked(self):
        """
        Apply the changes
        """
        if self.Pass2Check.isChecked():
            self.Settings.setValue("mencoderpass1", QVariant(self.mencoderpass1Edit.toPlainText()))
            self.Settings.setValue("mencoderpass2", QVariant(self.mencoderpass2Edit.toPlainText()))
        else:
            self.Settings.setValue("mencodersinglepass", QVariant(self.mencoderpass1Edit.toPlainText()))
        self.Settings.setValue("imagew",QVariant(str(self.Wiline.text())))
        self.Settings.setValue("imageh",QVariant(str(self.Heline.text())))
        self.Settings.setValue("2pass",self.Pass2Check.isChecked())
