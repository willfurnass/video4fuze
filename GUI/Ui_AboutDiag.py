# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/ssorgatem/Documents/python/video4fuze/GUI/AboutDiag.ui'
#
# Created: Sun Jan 23 02:30:17 2011
#      by: PyQt4 UI code generator 4.7.3
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
        Dialog.setLocale(QtCore.QLocale(QtCore.QLocale.C, QtCore.QLocale.AnyCountry))
        self.verticalLayout = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.Appinfo = QtGui.QLabel(Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Appinfo.sizePolicy().hasHeightForWidth())
        self.Appinfo.setSizePolicy(sizePolicy)
        self.Appinfo.setCursor(QtCore.Qt.ArrowCursor)
        self.Appinfo.setToolTip("")
        self.Appinfo.setText("<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'DejaVu Sans\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:20pt; font-weight:600;\">Info</span></p></body></html>")
        self.Appinfo.setTextFormat(QtCore.Qt.RichText)
        self.Appinfo.setAlignment(QtCore.Qt.AlignCenter)
        self.Appinfo.setWordWrap(True)
        self.Appinfo.setObjectName("Appinfo")
        self.horizontalLayout.addWidget(self.Appinfo)
        self.label = QtGui.QLabel(Dialog)
        font = QtGui.QFont()
        font.setWeight(75)
        font.setItalic(False)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setAutoFillBackground(False)
        self.label.setFrameShape(QtGui.QFrame.StyledPanel)
        self.label.setFrameShadow(QtGui.QFrame.Raised)
        self.label.setLineWidth(2)
        self.label.setTextFormat(QtCore.Qt.RichText)
        self.label.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByKeyboard|QtCore.Qt.LinksAccessibleByMouse)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.gridLayout_2 = QtGui.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        spacerItem = QtGui.QSpacerItem(0, 0, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 0, 0, 1, 1)
        self.logo = QtGui.QLabel(Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.logo.sizePolicy().hasHeightForWidth())
        self.logo.setSizePolicy(sizePolicy)
        self.logo.setMaximumSize(QtCore.QSize(35, 52))
        self.logo.setCursor(QtCore.Qt.ArrowCursor)
        self.logo.setAutoFillBackground(False)
        self.logo.setLocale(QtCore.QLocale(QtCore.QLocale.C, QtCore.QLocale.AnyCountry))
        self.logo.setText("")
        self.logo.setPixmap(QtGui.QPixmap(":/icons/black.png"))
        self.logo.setScaledContents(True)
        self.logo.setAlignment(QtCore.Qt.AlignCenter)
        self.logo.setWordWrap(False)
        self.logo.setObjectName("logo")
        self.gridLayout_2.addWidget(self.logo, 0, 1, 1, 1)
        self.horizontalLayout.addLayout(self.gridLayout_2)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.AboutTabs = QtGui.QTabWidget(Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.AboutTabs.sizePolicy().hasHeightForWidth())
        self.AboutTabs.setSizePolicy(sizePolicy)
        self.AboutTabs.setCursor(QtCore.Qt.WhatsThisCursor)
        self.AboutTabs.setObjectName("AboutTabs")
        self.ReadmeTab = QtGui.QWidget()
        self.ReadmeTab.setCursor(QtCore.Qt.WhatsThisCursor)
        self.ReadmeTab.setAutoFillBackground(False)
        self.ReadmeTab.setObjectName("ReadmeTab")
        self.gridLayout = QtGui.QGridLayout(self.ReadmeTab)
        self.gridLayout.setObjectName("gridLayout")
        self.ReadmeText = QtGui.QTextBrowser(self.ReadmeTab)
        self.ReadmeText.setProperty("cursor", QtCore.Qt.WhatsThisCursor)
        self.ReadmeText.setObjectName("ReadmeText")
        self.gridLayout.addWidget(self.ReadmeText, 0, 0, 1, 1)
        self.AboutTabs.addTab(self.ReadmeTab, "")
        self.LicenseTab = QtGui.QWidget()
        self.LicenseTab.setObjectName("LicenseTab")
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.LicenseTab)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.LicenseText = QtGui.QTextBrowser(self.LicenseTab)
        self.LicenseText.setProperty("cursor", QtCore.Qt.WhatsThisCursor)
        self.LicenseText.setObjectName("LicenseText")
        self.horizontalLayout_3.addWidget(self.LicenseText)
        self.AboutTabs.addTab(self.LicenseTab, "")
        self.verticalLayout.addWidget(self.AboutTabs)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem1 = QtGui.QSpacerItem(28, 17, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.okButton = QtGui.QPushButton(Dialog)
        self.okButton.setCursor(QtCore.Qt.PointingHandCursor)
        self.okButton.setObjectName("okButton")
        self.horizontalLayout_2.addWidget(self.okButton)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(Dialog)
        self.AboutTabs.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "About", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'DejaVu Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><a href=\"https://www.paypal.com/cgi-bin/webscr?cmd=_donations&amp;business=ZDFRGDZPUUJZ4&amp;lc=EN&amp;item_name=video4fuze&amp;currency_code=EUR&amp;bn=PP%2dDonationsBF%3abtn_donate_LG%2egif%3aNonHosted\"><span style=\" font-size:9pt; text-decoration: underline; color:#0057ae;\">Donate</span></a></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
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

