# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/ssorgatem/Documents/python/video4fuze/GUI/MainWindow.ui'
#
# Created: Wed Aug 19 21:39:37 2009
#      by: PyQt4 UI code generator 4.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(643, 456)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/blue.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setUnifiedTitleAndToolBarOnMac(True)
        self.centralWidget = QtGui.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.tabWidget = QtGui.QTabWidget(self.centralWidget)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 641, 411))
        self.tabWidget.setObjectName("tabWidget")
        self.Video = QtGui.QWidget()
        self.Video.setObjectName("Video")
        self.label = QtGui.QLabel(self.Video)
        self.label.setGeometry(QtCore.QRect(-50, 50, 281, 271))
        self.label.setPixmap(QtGui.QPixmap(":/icons/black.png"))
        self.label.setScaledContents(True)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.AddButton = QtGui.QPushButton(self.Video)
        self.AddButton.setGeometry(QtCore.QRect(70, 10, 131, 25))
        self.AddButton.setMinimumSize(QtCore.QSize(131, 25))
        self.AddButton.setObjectName("AddButton")
        self.RemoveButton = QtGui.QPushButton(self.Video)
        self.RemoveButton.setGeometry(QtCore.QRect(420, 9, 131, 25))
        self.RemoveButton.setMinimumSize(QtCore.QSize(131, 25))
        self.RemoveButton.setObjectName("RemoveButton")
        self.tableWidget = QtGui.QTableWidget(self.Video)
        self.tableWidget.setGeometry(QtCore.QRect(190, 40, 431, 281))
        self.tableWidget.setAcceptDrops(True)
        self.tableWidget.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.tableWidget.setDragDropMode(QtGui.QAbstractItemView.NoDragDrop)
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        self.tableWidget.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tableWidget.setShowGrid(False)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        self.SelectOutputButton = QtGui.QPushButton(self.Video)
        self.SelectOutputButton.setGeometry(QtCore.QRect(230, 10, 161, 25))
        self.SelectOutputButton.setMinimumSize(QtCore.QSize(131, 25))
        self.SelectOutputButton.setObjectName("SelectOutputButton")
        self.ConvertButton = QtGui.QPushButton(self.Video)
        self.ConvertButton.setGeometry(QtCore.QRect(240, 330, 131, 41))
        self.ConvertButton.setMinimumSize(QtCore.QSize(131, 25))
        self.ConvertButton.setObjectName("ConvertButton")
        self.tabWidget.addTab(self.Video, "")
        self.Image = QtGui.QWidget()
        self.Image.setObjectName("Image")
        self.label_2 = QtGui.QLabel(self.Image)
        self.label_2.setGeometry(QtCore.QRect(-50, 50, 281, 271))
        self.label_2.setPixmap(QtGui.QPixmap(":/icons/red.png"))
        self.label_2.setScaledContents(True)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.AddButton_2 = QtGui.QPushButton(self.Image)
        self.AddButton_2.setGeometry(QtCore.QRect(70, 10, 131, 25))
        self.AddButton_2.setMinimumSize(QtCore.QSize(131, 25))
        self.AddButton_2.setObjectName("AddButton_2")
        self.RemoveButton_2 = QtGui.QPushButton(self.Image)
        self.RemoveButton_2.setGeometry(QtCore.QRect(420, 9, 131, 25))
        self.RemoveButton_2.setMinimumSize(QtCore.QSize(131, 25))
        self.RemoveButton_2.setObjectName("RemoveButton_2")
        self.tableWidget_2 = QtGui.QTableWidget(self.Image)
        self.tableWidget_2.setGeometry(QtCore.QRect(190, 40, 431, 281))
        self.tableWidget_2.setAcceptDrops(True)
        self.tableWidget_2.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.tableWidget_2.setDragDropMode(QtGui.QAbstractItemView.NoDragDrop)
        self.tableWidget_2.setAlternatingRowColors(True)
        self.tableWidget_2.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        self.tableWidget_2.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tableWidget_2.setShowGrid(False)
        self.tableWidget_2.setObjectName("tableWidget_2")
        self.tableWidget_2.setColumnCount(2)
        self.tableWidget_2.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(1, item)
        self.SelectOutputButton_2 = QtGui.QPushButton(self.Image)
        self.SelectOutputButton_2.setGeometry(QtCore.QRect(230, 10, 161, 25))
        self.SelectOutputButton_2.setMinimumSize(QtCore.QSize(131, 25))
        self.SelectOutputButton_2.setObjectName("SelectOutputButton_2")
        self.ConvertButton_2 = QtGui.QPushButton(self.Image)
        self.ConvertButton_2.setGeometry(QtCore.QRect(240, 330, 131, 41))
        self.ConvertButton_2.setMinimumSize(QtCore.QSize(131, 25))
        self.ConvertButton_2.setObjectName("ConvertButton_2")
        self.tabWidget.addTab(self.Image, "")
        MainWindow.setCentralWidget(self.centralWidget)
        self.statusBar = QtGui.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)
        self.menuBar = QtGui.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 643, 22))
        self.menuBar.setObjectName("menuBar")
        self.menuFile = QtGui.QMenu(self.menuBar)
        self.menuFile.setObjectName("menuFile")
        self.menuHelp = QtGui.QMenu(self.menuBar)
        self.menuHelp.setObjectName("menuHelp")
        self.menuAdvanced = QtGui.QMenu(self.menuBar)
        self.menuAdvanced.setObjectName("menuAdvanced")
        MainWindow.setMenuBar(self.menuBar)
        self.actionAdd_file = QtGui.QAction(MainWindow)
        self.actionAdd_file.setObjectName("actionAdd_file")
        self.actionAbout_video4fuze = QtGui.QAction(MainWindow)
        self.actionAbout_video4fuze.setObjectName("actionAbout_video4fuze")
        self.actionAbout_Qt = QtGui.QAction(MainWindow)
        self.actionAbout_Qt.setObjectName("actionAbout_Qt")
        self.actionRemove_selected_files = QtGui.QAction(MainWindow)
        self.actionRemove_selected_files.setObjectName("actionRemove_selected_files")
        self.actionSelect_output_folder = QtGui.QAction(MainWindow)
        self.actionSelect_output_folder.setObjectName("actionSelect_output_folder")
        self.actionPreferences = QtGui.QAction(MainWindow)
        self.actionPreferences.setObjectName("actionPreferences")
        self.menuFile.addAction(self.actionAdd_file)
        self.menuFile.addAction(self.actionRemove_selected_files)
        self.menuFile.addAction(self.actionSelect_output_folder)
        self.menuHelp.addAction(self.actionAbout_video4fuze)
        self.menuHelp.addAction(self.actionAbout_Qt)
        self.menuAdvanced.addAction(self.actionPreferences)
        self.menuBar.addAction(self.menuFile.menuAction())
        self.menuBar.addAction(self.menuAdvanced.menuAction())
        self.menuBar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "video4fuze 0.2", None, QtGui.QApplication.UnicodeUTF8))
        self.AddButton.setText(QtGui.QApplication.translate("MainWindow", "Add files...", None, QtGui.QApplication.UnicodeUTF8))
        self.RemoveButton.setText(QtGui.QApplication.translate("MainWindow", "Remove files", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.horizontalHeaderItem(0).setText(QtGui.QApplication.translate("MainWindow", "Input files", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.horizontalHeaderItem(1).setText(QtGui.QApplication.translate("MainWindow", "Output folder", None, QtGui.QApplication.UnicodeUTF8))
        self.SelectOutputButton.setText(QtGui.QApplication.translate("MainWindow", "Select output folder", None, QtGui.QApplication.UnicodeUTF8))
        self.ConvertButton.setText(QtGui.QApplication.translate("MainWindow", "Convert!", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Video), QtGui.QApplication.translate("MainWindow", "Video", None, QtGui.QApplication.UnicodeUTF8))
        self.AddButton_2.setText(QtGui.QApplication.translate("MainWindow", "Add images...", None, QtGui.QApplication.UnicodeUTF8))
        self.RemoveButton_2.setText(QtGui.QApplication.translate("MainWindow", "Remove files", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget_2.horizontalHeaderItem(0).setText(QtGui.QApplication.translate("MainWindow", "Input files", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget_2.horizontalHeaderItem(1).setText(QtGui.QApplication.translate("MainWindow", "Output folder", None, QtGui.QApplication.UnicodeUTF8))
        self.SelectOutputButton_2.setText(QtGui.QApplication.translate("MainWindow", "Select output folder", None, QtGui.QApplication.UnicodeUTF8))
        self.ConvertButton_2.setText(QtGui.QApplication.translate("MainWindow", "Convert!", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Image), QtGui.QApplication.translate("MainWindow", "Photos", None, QtGui.QApplication.UnicodeUTF8))
        self.menuFile.setTitle(QtGui.QApplication.translate("MainWindow", "File", None, QtGui.QApplication.UnicodeUTF8))
        self.menuHelp.setTitle(QtGui.QApplication.translate("MainWindow", "Help", None, QtGui.QApplication.UnicodeUTF8))
        self.menuAdvanced.setTitle(QtGui.QApplication.translate("MainWindow", "Advanced", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAdd_file.setText(QtGui.QApplication.translate("MainWindow", "Add files...", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAbout_video4fuze.setText(QtGui.QApplication.translate("MainWindow", "About video4fuze", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAbout_Qt.setText(QtGui.QApplication.translate("MainWindow", "About Qt", None, QtGui.QApplication.UnicodeUTF8))
        self.actionRemove_selected_files.setText(QtGui.QApplication.translate("MainWindow", "Remove selected files", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSelect_output_folder.setText(QtGui.QApplication.translate("MainWindow", "Select output folder", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPreferences.setText(QtGui.QApplication.translate("MainWindow", "Preferences", None, QtGui.QApplication.UnicodeUTF8))

import video4fuze_rc

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

