# -*- coding: utf-8 -*-

"""
Module implementing MainWindow.
"""
import os, fuze
from PyQt4.QtGui import QMainWindow,QFileDialog,QMessageBox, QLabel, QTableWidgetItem
from PyQt4.QtCore import pyqtSignature,QString,QT_TR_NOOP,SIGNAL,QObject,Qt
from threading import Thread
from Ui_MainWindow import Ui_MainWindow

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
        self.Fuze = fuze.Fuze()
        try:
            self.tableWidget.horizontalHeader().setResizeMode(3)
        except:
            print "Your version of PyQt4 seems a bit out of date. This may lead to problems. And may not :)"
        self.output = os.path.expanduser("~")

    def ErrorDiag(self, error = QT_TR_NOOP("Unknown error")):
            print error
            QMessageBox.critical(None,
                self.trUtf8("Error"),
                self.trUtf8("""An error has ocurred:""") +" " + str(error),
                QMessageBox.StandardButtons(\
                QMessageBox.Ok),
                QMessageBox.Ok)

    def getReady(self):
        self.setEnabled(True)
        self.setCursor(Qt.ArrowCursor)
        self.unsetCursor()
        self.statusBar.showMessage(self.trUtf8("Done"))

    def DelItem(self, itemText):
        """
        Clean the ui
        """
        row = 0
        while row < self.tableWidget.rowCount():
            if itemText == str(self.tableWidget.item(row,0).text()):
                self.tableWidget.removeRow(row)
                break
            row += 1

    def Status(self,status):
        self.statusBar.showMessage(status)

    def WAIT(self):
        self.setCursor(Qt.WaitCursor)
        self.setEnabled(False)

    @pyqtSignature("QPoint")
    def on_tableWidget_customContextMenuRequested(self, pos):
        """
        Slot documentation goes here.
        """
        # TODO: on_tableWidget_customContextMenuRequested
        raise NotImplementedError

    @pyqtSignature("")
    def on_RemoveButton_clicked(self):
        self. actionRemove_selected_files.emit(SIGNAL("triggered()"))

    @pyqtSignature("")
    def on_ConvertButton_clicked(self):
        """
        Starts conversion
        """
        args = []
        row = 0
        while row < self.tableWidget.rowCount():
            args.append(str(self.tableWidget.item(row,0).text()))
            row += 1
        Conversion = Converter(args, self, self.output)
        Conversion.start()

    @pyqtSignature("")
    def on_AddButton_clicked(self):
        self. actionAdd_file.emit(SIGNAL("triggered()"))

    @pyqtSignature("")
    def on_SelectOutputButton_clicked(self):
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
        for file in files:
            print file
            currentrow = self.tableWidget.rowCount() #+ 1
            #self.tableWidget.setRowCount(currentrow)
            self.tableWidget.insertRow(currentrow)

            filewidget = QTableWidgetItem()
            filewidget.setText(file)
            outputitem = QTableWidgetItem()
            outputitem.setText(self.output)
            self.tableWidget.setItem(currentrow,0,filewidget)
            self.tableWidget.setItem(currentrow,1,outputitem)

            print filewidget.text()
        self.tableWidget.resizeColumnsToContents()

        #raise NotImplementedError

    @pyqtSignature("")
    def on_actionAbout_video4fuze_triggered(self):
        """
        Slot documentation goes here.
        """
        QMessageBox.about(None,
            self.trUtf8("Abut video4fuze"),
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
        for item in self.tableWidget.selectedItems():
            if item.column() == 0:
                remlist.append(item)
        for item in remlist:
            self.tableWidget.removeRow(self.tableWidget.row(item))

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
            self.output = str(output)
        row = 0
        while row < self.tableWidget.rowCount():
            self.tableWidget.item(row,1).setText(self.output)
            row += 1

class Converter(Thread):
    """
    Doing the job in a different thread is always good.
    """
    def __init__(self,args,GUI,FINALPREFIX=None):
        Thread.__init__(self)
        self.args = args
        self.FINALPREFIX = FINALPREFIX
        self.GUI = GUI
    def run(self):
        self.GUI.Fuze.convert(self.args, self.FINALPREFIX, self.GUI)
