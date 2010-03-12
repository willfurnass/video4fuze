# -*- coding: utf-8 -*-
"""
Module implementing MainWindow. Playlist edition capabilities are inspired by Dunny's YAPL, and had been possible to write thanks to his help about the
# .pla playlist format.
"""
import os, fuze, p2fuze
from PyQt4.QtGui import QMainWindow,QFileDialog,QMessageBox, QLabel, QTableWidgetItem, QListWidgetItem, QIcon
from PyQt4.QtCore import QString,QT_TR_NOOP,SIGNAL,QObject,Qt,QSettings,QVariant, QSize, QCoreApplication
from threading import Thread
from Ui_MainWindow import Ui_MainWindow
from v4fPreferences import PreferencesDialog

class MainWindow(QMainWindow, Ui_MainWindow):
    """
    video4fuze's main window, implementing too playlist management logic
    """
    def __init__(self, v4fhome, parent = None):
        """
        Constructor
        """
        QMainWindow.__init__(self, parent) #Use QMainWindow.__init___
        self.setupUi(self) #setup the ui...
        #IMPORTANT: the line "QtCore.QMetaObject.connectSlotsByName(MainWindow)" in UI_MainWindow.py MUST be commented.
        self.v4fhome = v4fhome #Where are we?
        self.settings = QSettings(QSettings.IniFormat, QSettings.UserScope, QCoreApplication.organizationName(), QCoreApplication.applicationName()) #Instantiate QSettings, using ini format always
        self.Fuze = fuze.Fuze(self) #Instantiate the Fuze class.
        self.resis = p2fuze.TransFuze(self) #AnotherTestPlugin her useful class.
        if os.name != 'nt': #If you are lucky and don't run that OS...
            self.mediaroot = "/media" #this is a very probable directory to start from to look for the fuze.
        else:
            self.mediaroot = os.path.join(os.path.expanduser("~"), "Desktop") #Otherwise, here we have the classical desktop...
        self.playlistname = self.mediaroot #Apply that for playlists too
        try:
            self.tableWidget.horizontalHeader().setResizeMode(3) #Try to fix size of tableWidgets
            self.tableWidget_2.horizontalHeader().setResizeMode(3)
        except:
            print "Your version of PyQt4 seems a bit out of date. This may lead to problems. But may not :)" #Most probable. The fact is that it doesn't work in PySide and older PyQt4.
        self.output = toPython(self.settings.value("outputdir",QVariant(os.path.expanduser("~"))).toString()) #Where to output things.
        self.setWindowTitle(QCoreApplication.applicationName()+" "+QCoreApplication.applicationVersion())
        self.connect(self.actionAbout_Qt, SIGNAL("triggered()"),self.on_actionAbout_Qt_triggered)
        self.connect(self.RemoveButton, SIGNAL("clicked()"),self.on_RemoveButton_clicked)
        self.connect(self.RemoveButton_2, SIGNAL("clicked()"),self.on_RemoveButton_2_clicked)
        self.connect(self.RemoveButton_3, SIGNAL("clicked()"),self.on_RemoveButton_3_clicked)
        self.connect(self.ConvertButton, SIGNAL("clicked()"),self.on_ConvertButton_clicked)
        self.connect(self.ConvertButton_2, SIGNAL("clicked()"),self.on_ConvertButton_2_clicked)
        self.connect(self.actionPreferences, SIGNAL("triggered()"),self.on_actionPreferences_triggered)
        self.connect(self.actionAbout_video4fuze, SIGNAL("triggered()"),self.on_actionAbout_video4fuze_triggered)
        self.connect(self.AddButton, SIGNAL("clicked()"),self.on_AddButton_clicked)
        self.connect(self.AddButton_2, SIGNAL("clicked()"),self.on_AddButton_2_clicked)
        self.connect(self.SelectOutputButton, SIGNAL("clicked()"),self.on_SelectOutputButton_clicked)
        self.connect(self.SelectOutputButton_2, SIGNAL("clicked()"),self.on_SelectOutputButton_2_clicked)
        self.connect(self.SavePlaylist, SIGNAL("clicked()"),self.on_SavePlaylist_clicked)
        self.connect(self.SongsFromSD, SIGNAL("clicked()"),self.on_SongsFromSD_clicked)
        self.connect(self.SongsFromFuze, SIGNAL("clicked()"),self.on_SongsFromFuze_clicked)
        self.connect(self.OpenPlaylist, SIGNAL("clicked()"),self.on_OpenPlaylist_clicked)
        self.connect(self.ToggleSort, SIGNAL("clicked()"),self.on_ToggleSort_clicked)


    def fuzePath(self,prefix): #TODO: Tags display & sorting
        """
        Translates paths to fuze's .pla format, and loads them in the UI
        """
        if os.name == 'nt':
            prefix = prefix + "/"#Add this prefix in case of redmond's semi-operating system....
        Songs = QFileDialog.getOpenFileNames(\
            None,
            self.trUtf8("Select songs to add to the playlist"),
            self.settings.value("lastsongdir",QVariant(self.mediaroot)).toString(),
            self.trUtf8("*.ogg *.OGG *.mp3 *.MP3 *.wma *.WMA *.flac *.FLAC"),
            None) # A QFileDialog for picking songs
        if not Songs.isEmpty(): #Do nothing if nothing was picked
            try:
                self.settings.setValue(
                    "lastsongdir",
                    QVariant(os.path.split(toPython(Songs[0]))[0])
                    )#Store the last dir from where songs were picked. Thats for commodity.
            except Exception, e:
                print e
                print Songs
        for song in Songs: #Iterate selected songs and render them.
            unicodesong = toPython(song)
            cover = os.path.join(os.path.split(unicodesong)[0], "folder.jpg")
            tostrip = mountpoint(unicodesong)
            song.replace(tostrip, prefix)
            song.replace("\\","/")
            listItem = QListWidgetItem(song)
            if os.path.isfile(cover):
                listItem.setIcon(QIcon(cover))
            else:
                print cover + " not found"
            self.playlistWidget.addItem(listItem)

#############################################################
#Slot functions which should only be called by SIGNALs and not directly:

    def ErrorDiag(self, error = QT_TR_NOOP("Unknown error")):
            """
            A useful function to add easy error reporting to any other place of the code.
            """
            print error
            QMessageBox.critical(None,
                self.trUtf8("Error"),
                self.trUtf8("""An error has ocurred:""") +" " + unicode(error),
                QMessageBox.StandardButtons(\
                QMessageBox.Ok),
                QMessageBox.Ok)

    def getReady(self, tab):
        """
        Set the UI ready again. We are done of the hard work ;). Or we failed miserably at it. Well, not so miserably, since we've recovered.
        """
        tab.setEnabled(True)
        self.statusBar.showMessage(self.trUtf8("Done"))

    def DelItem(self, itemText, image = False):
        """
        Clean items and/or objects from the different tabs. This function is intended to be a slot to connect with signals on other threads.
        """
        if image:
            row = 0
            while row < self.tableWidget_2.rowCount():
                if itemText == toPython(self.tableWidget_2.item(row,0).text()):
                    self.tableWidget_2.removeRow(row)
                    break
                row += 1
        else:
            row = 0
            while row < self.tableWidget.rowCount():
                if itemText == toPython(self.tableWidget.item(row,0).text()):
                    self.tableWidget.removeRow(row)
                    break
                row += 1

    def Status(self,status):
        """
        Report what are we currently doing in the statusbar. This function is also intended to be a slot, so it shouldn't be called directly.
        """
        self.statusBar.showMessage(status)

    def WAIT(self, tab):
        """
        Disable working tab. We don't want the user to mess up with useless buttons there.
        """
        tab.setEnabled(False)

    def SelectOutput(self):
        """
        Select destination of converted files. Preferably the VIDEOS folder in you fuze.
        """
        output = QFileDialog.getExistingDirectory(\
            None,
            self.trUtf8("Select output directory"),
            os.path.expanduser("~"),
            QFileDialog.Options(QFileDialog.ShowDirsOnly))
        if output != None:
            self.output = toPython(output)
            self.settings.setValue("outputdir",QVariant(self.output))
        row = 0
        while row < self.tableWidget.rowCount():
            self.tableWidget.item(row,1).setText(self.output)
            row += 1
        row = 0
        while row < self.tableWidget_2.rowCount():
            self.tableWidget_2.item(row,1).setText(self.output)
            row += 1

    def on_RemoveButton_clicked(self):
        """
        Removes files to convert
        """
        remlist = []
        for item in self.tableWidget.selectedItems():
            try:
                if item.column() == 0:
                    self.tableWidget.removeRow(self.tableWidget.row(item))
            except:
                print "Weird things happening between python and c++"

    def on_RemoveButton_2_clicked(self):
        """
        Removes files to convert
        """
        remlist = []
        for item in self.tableWidget_2.selectedItems():
            try:
                if item.column() == 0:
                    self.tableWidget_2.removeRow(self.tableWidget_2.row(item))
            except:
                print "Weird things happening between python and c++"

    def on_ConvertButton_clicked(self):
        """
        Starts conversion
        """
        args = [] #Initialization of some variables, just in case.
        row = 0
        while row < self.tableWidget.rowCount():
            args.append(toPython(self.tableWidget.item(row,0).text()))
            row += 1
        Conversion = Converter(args, self, self.output)
        Conversion.start()

    def on_ConvertButton_2_clicked(self):
        """
        Starts image conversion & resizing
        """
        args = []
        row = 0
        while row < self.tableWidget_2.rowCount():
            args.append(toPython(self.tableWidget_2.item(row,0).text()))
            row += 1
        Resize = Resizer(args, self, self.output)
        Resize.start()

    def on_AddButton_clicked(self):
        """
        Now it's time to add those files we were avoiding to emiting extra signals, right? xD
        """
        files = QFileDialog.getOpenFileNames(\
            None,
            self.trUtf8("Select files to add to the convert queue"),
            self.settings.value("lastdir",QVariant(os.path.expanduser("~"))).toString(),
            QString(),
            None) # A cute QFileDialog asks the user for the files to convert, for both videos and images.
        if not files.isEmpty(): #If nothing, do nothing.
            try:
                self.settings.setValue("lastdir", QVariant(os.path.split(toPython(files[0]))[0]))
                #Remembering last used dir comes always in handy.
            except:
                print files #Debugging stuff...
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

    def on_AddButton_2_clicked(self):
        """
        Now it's time to add those files we were avoiding to emiting extra signals, right? xD
        """
        files = QFileDialog.getOpenFileNames(\
            None,
            self.trUtf8("Select files to add to the convert queue"),
            self.settings.value("lastdir",QVariant(os.path.expanduser("~"))).toString(),
            QString(),
            None) # A cute QFileDialog asks the user for the files to convert, for both videos and images.
        if not files.isEmpty(): #If nothing, do nothing.
            try:
                self.settings.setValue("lastdir", QVariant(os.path.split(toPython(files[0]))[0]))
                #Remembering last used dir comes always in handy.
            except:
                print files #Debugging stuff...
        for file in files:
            currentrow = self.tableWidget_2.rowCount()
            self.tableWidget_2.insertRow(currentrow)
            filewidget = QTableWidgetItem()
            filewidget.setText(file)
            try:
                filewidget.setIcon(QIcon(file))
            except:
                print "Could not load a thumbnail of the album art"
            outputitem = QTableWidgetItem()
            outputitem.setText(self.output)
            self.tableWidget_2.setItem(currentrow,0,filewidget)
            self.tableWidget_2.setItem(currentrow,1,outputitem)
            self.tableWidget_2.resizeColumnsToContents()

    def on_SelectOutputButton_clicked(self):
        """
        Pass to actionSelect_output_folder_triggered
        """
        self.SelectOutput()

    def on_SelectOutputButton_2_clicked(self):
        """
        Pass to actionSelect_output_folder_triggered
        """
        self.SelectOutput()

    def on_actionAbout_video4fuze_triggered(self):
        """
        Show a popup with info about video4fuze. I should really improve it...
        """
        QMessageBox.about(None,
            self.trUtf8("About")+" "+QCoreApplication.applicationName()+" "+QCoreApplication.applicationVersion(),
            self.trUtf8("""This applications uses mencoder and fuzemux in order to convert your video files to be seen in you sansa fuze.

Thanks to ewelot and  earthcrosser  from the sansa forums for finding the way to convert the videos, without their findings this app wouldn't exist."""))
    #TODO: Maybe with a text widget loading the README.txt it could be more practical and mainteinable.

    def on_actionAbout_Qt_triggered(self):
        QMessageBox.aboutQt(None,
            self.trUtf8(""))

    def on_actionPreferences_triggered(self):
        prefs = PreferencesDialog()
        prefs.exec_()

    def on_SavePlaylist_clicked(self):
        """
        Write the playlist to a file..
        """
        self.playlistname = toPython(QFileDialog.getSaveFileName(\
            None,
            self.trUtf8("Save your playlist"),
            self.playlistname,
            self.trUtf8("*.pla"),
            None))

        if self.playlistname != "":
            if os.path.splitext(toPython(self.playlistname))[1] != ".pla":
                self.playlistname = self.playlistname + ".pla"
            Playlist = QString("")
            if os.name == 'nt':
                newline = "\n"
            else:
                newline = "\r\n"
            row = 0
            while row < self.playlistWidget.count():
                Playlist = Playlist + self.playlistWidget.item(row).text() + QString(newline)
                row += 1
            PLA = open(self.playlistname, "wb")
            PLA.close()
            REFS = open(self.playlistname + ".refs", "w")
            REFS.write(Playlist)
            REFS.close

    def on_SongsFromSD_clicked(self):
        """
        Add µSD songs to playlist.
        """
        self.fuzePath("/mmc:1:")

    def on_SongsFromFuze_clicked(self):
        """
        Get songs from the fuze
        """
        self.fuzePath("/mmc:0:")

    def on_RemoveButton_3_clicked(self):
        """
        Removes files to convert
        """
        remlist = []
        for item in self.playlistWidget.selectedItems():
            self.playlistWidget.takeItem(self.playlistWidget.row(item))

    def on_OpenPlaylist_clicked(self):
        """
        Load and parse a .pla.refs file
        """
        self.playlistname = toPython(QFileDialog.getOpenFileName(\
            None,
            self.trUtf8("Select playlist to edit"),
            self.playlistname,
            self.trUtf8("*.pla"),
            None))
        if self.playlistname:
            unicodeplaylist = toPython(self.playlistname)
            prefix = mountpoint(unicodeplaylist)
            if os.name == 'nt':
                prefix = prefix + "\\"
            PL = open(self.playlistname + ".refs", "r")
            self.playlistWidget.clear()
            for song in PL.readlines():
                song = toPython(QString(song))
                song = song.strip()
                pcsong = prefix + song[7:]
                cover = os.path.join(os.path.split(pcsong)[0], "folder.jpg")
                listItem = QListWidgetItem(song)
                if os.path.isfile(cover):
                    listItem.setIcon(QIcon(cover))
                    print "Loading " + cover
                else:
                    print "Album art'" + cover +" not found"
                self.playlistWidget.addItem(listItem)
            PL.close()

    def on_ToggleSort_clicked(self):
        """
        Sort playlist
        """
        self.playlistWidget.sortItems()

#Here come two _very_ ugly threaded worker classes
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

def mountpoint(dir):
    """
    Function to determine the mountpoint of a given dir
    """
    if (os.path.ismount(dir) or len(dir) == 0):
        return dir
    else:
        return mountpoint(os.path.split(dir)[0])

def toPython(string):
    """
    Little helper function to workaround MS Windows unicode support
    """
    qstring = QString(string)
    if os.name == 'nt':
        return str(qstring.toAscii())
    else:
        return unicode(qstring)
