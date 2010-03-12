# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/ssorgatem/Documents/python/video4fuze/GUI/AboutDiag.ui'
#
# Created: Fri Mar 12 19:46:52 2010
#      by: PyQt4 UI code generator 4.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setEnabled(True)
        Dialog.resize(413, 539)
        Dialog.setMaximumSize(QtCore.QSize(413, 539))
        Dialog.setCursor(QtCore.Qt.WhatsThisCursor)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/silver.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)
        self.AboutTabs = QtGui.QTabWidget(Dialog)
        self.AboutTabs.setGeometry(QtCore.QRect(0, 60, 411, 441))
        self.AboutTabs.setCursor(QtCore.Qt.WhatsThisCursor)
        self.AboutTabs.setObjectName("AboutTabs")
        self.ReadmeTab = QtGui.QWidget()
        self.ReadmeTab.setCursor(QtCore.Qt.WhatsThisCursor)
        self.ReadmeTab.setAutoFillBackground(False)
        self.ReadmeTab.setObjectName("ReadmeTab")
        self.ReadmeText = QtGui.QTextBrowser(self.ReadmeTab)
        self.ReadmeText.setGeometry(QtCore.QRect(0, 0, 411, 411))
        self.ReadmeText.setProperty("cursor", QtCore.Qt.WhatsThisCursor)
        self.ReadmeText.setObjectName("ReadmeText")
        self.AboutTabs.addTab(self.ReadmeTab, "")
        self.LicenseTab = QtGui.QWidget()
        self.LicenseTab.setObjectName("LicenseTab")
        self.LicenseText = QtGui.QTextBrowser(self.LicenseTab)
        self.LicenseText.setGeometry(QtCore.QRect(0, 0, 411, 411))
        self.LicenseText.setProperty("cursor", QtCore.Qt.WhatsThisCursor)
        self.LicenseText.setObjectName("LicenseText")
        self.AboutTabs.addTab(self.LicenseTab, "")
        self.okButton = QtGui.QPushButton(Dialog)
        self.okButton.setGeometry(QtCore.QRect(160, 510, 95, 25))
        self.okButton.setCursor(QtCore.Qt.PointingHandCursor)
        self.okButton.setObjectName("okButton")
        self.logo = QtGui.QLabel(Dialog)
        self.logo.setGeometry(QtCore.QRect(290, 10, 61, 61))
        self.logo.setCursor(QtCore.Qt.WhatsThisCursor)
        self.logo.setAutoFillBackground(False)
        self.logo.setPixmap(QtGui.QPixmap(":/icons/black.png"))
        self.logo.setScaledContents(True)
        self.logo.setAlignment(QtCore.Qt.AlignCenter)
        self.logo.setWordWrap(False)
        self.logo.setObjectName("logo")
        self.Appinfo = QtGui.QLabel(Dialog)
        self.Appinfo.setGeometry(QtCore.QRect(30, 10, 221, 41))
        self.Appinfo.setCursor(QtCore.Qt.WhatsThisCursor)
        self.Appinfo.setText("TextLabel")
        self.Appinfo.setAlignment(QtCore.Qt.AlignCenter)
        self.Appinfo.setWordWrap(True)
        self.Appinfo.setObjectName("Appinfo")

        self.retranslateUi(Dialog)
        self.AboutTabs.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "About", None, QtGui.QApplication.UnicodeUTF8))
        self.AboutTabs.setTabText(self.AboutTabs.indexOf(self.ReadmeTab), QtGui.QApplication.translate("Dialog", "Readme", None, QtGui.QApplication.UnicodeUTF8))
        self.AboutTabs.setTabText(self.AboutTabs.indexOf(self.LicenseTab), QtGui.QApplication.translate("Dialog", "License", None, QtGui.QApplication.UnicodeUTF8))
        self.okButton.setText(QtGui.QApplication.translate("Dialog", "Ok", None, QtGui.QApplication.UnicodeUTF8))

import video4fuze_rc

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Dialog = QtGui.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

