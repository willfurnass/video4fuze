# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/ssorgatem/Documents/python/video4fuze/GUI/Preferences.ui'
#
# Created: Wed Aug 19 13:05:56 2009
#      by: PyQt4 UI code generator 4.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_PreferencesDialog(object):
    def setupUi(self, PreferencesDialog):
        PreferencesDialog.setObjectName("PreferencesDialog")
        PreferencesDialog.resize(493, 415)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/blue.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        PreferencesDialog.setWindowIcon(icon)
        self.layoutWidget = QtGui.QWidget(PreferencesDialog)
        self.layoutWidget.setGeometry(QtCore.QRect(120, 370, 351, 33))
        self.layoutWidget.setObjectName("layoutWidget")
        self.hboxlayout = QtGui.QHBoxLayout(self.layoutWidget)
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setObjectName("hboxlayout")
        spacerItem = QtGui.QSpacerItem(131, 31, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem)
        self.DefaultsButton = QtGui.QPushButton(self.layoutWidget)
        self.DefaultsButton.setObjectName("DefaultsButton")
        self.hboxlayout.addWidget(self.DefaultsButton)
        self.okButton = QtGui.QPushButton(self.layoutWidget)
        self.okButton.setObjectName("okButton")
        self.hboxlayout.addWidget(self.okButton)
        self.cancelButton = QtGui.QPushButton(self.layoutWidget)
        self.cancelButton.setDefault(True)
        self.cancelButton.setFlat(False)
        self.cancelButton.setObjectName("cancelButton")
        self.hboxlayout.addWidget(self.cancelButton)
        self.mencoderpass1Edit = QtGui.QPlainTextEdit(PreferencesDialog)
        self.mencoderpass1Edit.setGeometry(QtCore.QRect(50, 150, 401, 71))
        self.mencoderpass1Edit.setObjectName("mencoderpass1Edit")
        self.mencoderpass2Edit = QtGui.QPlainTextEdit(PreferencesDialog)
        self.mencoderpass2Edit.setGeometry(QtCore.QRect(50, 270, 401, 71))
        self.mencoderpass2Edit.setObjectName("mencoderpass2Edit")
        self.label = QtGui.QLabel(PreferencesDialog)
        self.label.setGeometry(QtCore.QRect(50, 130, 401, 16))
        self.label.setObjectName("label")
        self.label_2 = QtGui.QLabel(PreferencesDialog)
        self.label_2.setGeometry(QtCore.QRect(50, 250, 401, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtGui.QLabel(PreferencesDialog)
        self.label_3.setGeometry(QtCore.QRect(50, 30, 391, 81))
        self.label_3.setScaledContents(False)
        self.label_3.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_3.setWordWrap(True)
        self.label_3.setObjectName("label_3")

        self.retranslateUi(PreferencesDialog)
        QtCore.QObject.connect(self.okButton, QtCore.SIGNAL("clicked()"), PreferencesDialog.accept)
        QtCore.QObject.connect(self.cancelButton, QtCore.SIGNAL("clicked()"), PreferencesDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(PreferencesDialog)

    def retranslateUi(self, PreferencesDialog):
        PreferencesDialog.setWindowTitle(QtGui.QApplication.translate("PreferencesDialog", "video4fuze preferences", None, QtGui.QApplication.UnicodeUTF8))
        self.DefaultsButton.setText(QtGui.QApplication.translate("PreferencesDialog", "Defaults", None, QtGui.QApplication.UnicodeUTF8))
        self.okButton.setText(QtGui.QApplication.translate("PreferencesDialog", "&OK", None, QtGui.QApplication.UnicodeUTF8))
        self.cancelButton.setText(QtGui.QApplication.translate("PreferencesDialog", "&Cancel", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("PreferencesDialog", "Mencoder pass 1 command line:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("PreferencesDialog", "Mencoder pass 2 command line:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("PreferencesDialog", "Warning: invalid command line arguments for mencoder may cause video4fuze to crash.\n"
"These settings will be remembered, so if you only want them for just this conversion, remember to revert them to defaults or setting them as you wish.", None, QtGui.QApplication.UnicodeUTF8))

import video4fuze_rc

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    PreferencesDialog = QtGui.QDialog()
    ui = Ui_PreferencesDialog()
    ui.setupUi(PreferencesDialog)
    PreferencesDialog.show()
    sys.exit(app.exec_())

