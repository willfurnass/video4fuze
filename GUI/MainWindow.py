# -*- coding: utf-8 -*-

"""
Module implementing MainWindow.
"""
import os, fuze, p2fuze
from PyQt4.QtGui import QMainWindow,QFileDialog,QMessageBox, QLabel, QTableWidgetItem
from PyQt4.QtCore import pyqtSignature,QString,QT_TR_NOOP,SIGNAL,QObject,Qt,QSettings,QVariant
from threading import Thread
from Ui_MainWindow import Ui_MainWindow
from v4fPreferences import PreferencesDialog

class MainWindow(QMainWindow, Ui_MainWindow):
    """
    Class documentation goes here.
    """
    def __init__(self, parent = None):
        """
        Constructor
        """
        QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.settings = QSettings()
        self.Fuze = fuze.Fuze(self)
        self.resis = p2fuze.TransFuze(self)
        try:
            self.tableWidget.horizontalHeader().setResizeMode(3)
            self.tableWidget_2.horizontalHeader().setResizeMode(3)
        except:
            print "Your version of PyQt4 seems a bit out of date. This may lead to problems. And may not :)"
        self.output = unicode(self.settings.value("outputdir",QVariant(os.path.expanduser("~"))).toString())

    def ErrorDiag(self, error = QT_TR_NOOP("Unknown error")):
            print error
            QMessageBox.critical(None,
                self.trUtf8("Error"),
                self.trUtf8("""An error has ocurred:""") +" " + str(error),
                QMessageBox.StandardButtons(\
                QMessageBox.Ok),
                QMessageBox.Ok)

    def getReady(self, tab):
        tab.setEnabled(True)
        self.statusBar.showMessage(self.trUtf8("Done"))

    def DelItem(self, itemText, image = False):
        """
        Clean the ui
        """
        if image:
            row = 0
            while row < self.tableWidget_2.rowCount():
                if itemText == unicode(self.tableWidget_2.item(row,0).text(), "utf-8"):
                    self.tableWidget_2.removeRow(row)
                    break
                row += 1
        else:
            row = 0
            while row < self.tableWidget.rowCount():
                if itemText == unicode(self.tableWidget.item(row,0).text(), "utf-8"):
                    self.tableWidget.removeRow(row)
                    break
                row += 1

    def Status(self,status):
        self.statusBar.showMessage(status)

    def WAIT(self, tab):
        tab.setEnabled(False)

    @pyqtSignature("QPoint")
    def on_tableWidget_customContextMenuRequested(self, pos):
        """
        Slot documentation goes here.
        """
        # TODO: on_tableWidget_customContextMenuRequested

    @pyqtSignature("")
    def on_RemoveButton_clicked(self):
        self. actionRemove_selected_files.emit(SIGNAL("triggered()"))

    @pyqtSignature("")
    def on_RemoveButton_2_clicked(self):
        self. actionRemove_selected_files.emit(SIGNAL("triggered()"))

    @pyqtSignature("")
    def on_ConvertButton_clicked(self):
        """
        Starts conversion
        """
        args = []
        row = 0
        while row < self.tableWidget.rowCount():
            args.append(str(self.tableWidget.item(row,0).text().toUtf8()))
            row += 1
        Conversion = Converter(args, self, self.output)
        Conversion.start()

    @pyqtSignature("")
    def on_ConvertButton_2_clicked(self):
        """
        Starts image conversion & resizing
        """
        args = []
        row = 0
        while row < self.tableWidget_2.rowCount():
            args.append(unicode(self.tableWidget_2.item(row,0).text().toUtf8()))
            row += 1
        Resize = Resizer(args, self, self.output)
        Resize.start()

    @pyqtSignature("")
    def on_AddButton_clicked(self):
        self. actionAdd_file.emit(SIGNAL("triggered()"))

    @pyqtSignature("")
    def on_AddButton_2_clicked(self):
        self. actionAdd_file.emit(SIGNAL("triggered()"))

    @pyqtSignature("")
    def on_SelectOutputButton_clicked(self):
        self. actionSelect_output_folder.emit(SIGNAL("triggered()"))

    @pyqtSignature("")
    def on_SelectOutputButton_2_clicked(self):
        self. actionSelect_output_folder.emit(SIGNAL("triggered()"))


    @pyqtSignature("")
    def on_actionAdd_file_triggered(self):
        """
        Adding files.
        """
        files = QFileDialog.getOpenFileNames(\
            None,
            self.trUtf8("Select files to add to the convert queue"),
            os.path.expanduser("~"),
            QString(),
            None)
        if self.tabWidget.currentIndex() == 0:
            for file in files:
                currentrow = self.tableWidget.rowCount()
                self.tableWidget.insertRow(currentrow)
                filewidget = QTableWidgetItem()
                filewidget.setText(file)
                outputitem = QTableWidgetItem()
                outputitem.setText(self.output)
                self.tableWidget.setItem(currentrow,0,filewidget)
                self.tableWidget.setItem(currentrow,1,outputitem)
                self.tableWidget.resizeColumnsToContents()

        elif self.tabWidget.currentIndex() == 1:
            for file in files:
                currentrow = self.tableWidget_2.rowCount()
                self.tableWidget_2.insertRow(currentrow)
                filewidget = QTableWidgetItem()
                filewidget.setText(file)
                outputitem = QTableWidgetItem()
                outputitem.setText(self.output)
                self.tableWidget_2.setItem(currentrow,0,filewidget)
                self.tableWidget_2.setItem(currentrow,1,outputitem)
                self.tableWidget_2.resizeColumnsToContents()

    @pyqtSignature("")
    def on_actionAbout_video4fuze_triggered(self):
        """
        Slot documentation goes here.
        """
        QMessageBox.about(None,
            self.trUtf8("About video4fuze 0.2"),
            self.trUtf8("""This applications uses mencoder and avi-mux GUI (under wine where necessary) in order to convert your video files to be seen in you sansa fuze.

Thanks to ewelot from the sansa forums for finding the way to convert the videos, without his findings this app wouldn't exist."""))

        # TODO: on_actionAbout_video4fuze_triggered


    @pyqtSignature("")
    def on_actionAbout_Qt_triggered(self):
        QMessageBox.aboutQt(None,
            self.trUtf8(""))

    @pyqtSignature("")
    def on_actionRemove_selected_files_triggered(self):
        """
        Removes files to convert
        """
        remlist = []
        if self.tabWidget.currentIndex() == 0:
            for item in self.tableWidget.selectedItems():
                if item.column() == 0:
                    remlist.append(item)
            for item in remlist:
                self.tableWidget.removeRow(self.tableWidget.row(item))
        elif self.tabWidget.currentIndex() == 1:
            for item in self.tableWidget_2.selectedItems():
                if item.column() == 0:
                    remlist.append(item)
            for item in remlist:
                self.tableWidget_2.removeRow(self.tableWidget_2.row(item))

    @pyqtSignature("")
    def on_actionSelect_output_folder_triggered(self):
        """
        Select destination of converted files. Preferably the VIDEOS folder in you fuze.
        """
        output = QFileDialog.getExistingDirectory(\
            None,
            self.trUtf8("Select output directory"),
            os.path.expanduser("~"),
            QFileDialog.Options(QFileDialog.ShowDirsOnly))
        if output != None:
            self.output = unicode(output)
            self.settings.setValue("outputdir",QVariant(self.output))
        row = 0
        while row < self.tableWidget.rowCount():
            self.tableWidget.item(row,1).setText(self.output)
            row += 1
        row = 0
        while row < self.tableWidget_2.rowCount():
            self.tableWidget_2.item(row,1).setText(self.output)
            row += 1

    @pyqtSignature("")
    def on_actionPreferences_triggered(self):
        prefs = PreferencesDialog()
        prefs.exec_()

class Converter(Thread):
    """
    Doing the job in a different thread is always good.
    """
    def __init__(self,args, parent, FINALPREFIX=None):
        Thread.__init__(self)
        self.args = args
        self.FINALPREFIX = FINALPREFIX
        self.parent = parent
    def run(self):
        self.parent.Fuze.LoadSettings()
        self.parent.Fuze.convert(self.args, self.FINALPREFIX)

class Resizer(Thread):
    """
    Doing the job in a different thread is always good.
    """
    def __init__(self,args, parent, FINALPREFIX=None):
        Thread.__init__(self)
        self.args = args
        self.FINALPREFIX = FINALPREFIX
        self.parent = parent
    def run(self):
        self.parent.resis.convert(self.args, self.FINALPREFIX)
