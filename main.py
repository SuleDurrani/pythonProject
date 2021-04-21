import os
import subprocess
import sys

from functools import partial
import ast
from datetime import date
import git
import requests
import yaml
from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtCore import QSize, pyqtSlot
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import QWidget, QApplication, QMessageBox, QDesktopWidget, QTableWidget, \
    QTableWidgetItem, QVBoxLayout, QPushButton, QLabel, QGridLayout, QTextEdit, QHeaderView, QLineEdit, QMenuBar, \
    QTextBrowser, QAction, QAbstractItemView
from bs4 import BeautifulSoup
from natsort import natsorted



liOpt = []  # initialize variables for the recommended, the minimum and the optional
liRec = []  # properties, based on marginality
liMin = []
liUns = []

liRecTest = False
liMinTest = False
liOptTest = False

buttonList = []
buttonList2 = []
btnCounter = 0
btnIndex = 0
btnIndex2 = 0
exampleList = []


class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'Pick a profile to Edit'
        self.left = 10
        self.top = 10
        self.width = 600
        self.height = 700
        self.i = 0
        self.initUI()

    def initUI(self):
        #print("hello")
        # app = QApplication(sys.argv)
        cwd = os.getcwd()
        cwd = cwd + "\\BioschemasGitClone"
        try:
            mkd = os.mkdir(cwd)
        except OSError as error:
            print(error)
        try:
            git.Git(cwd).clone("https://github.com/BioSchemas/bioschemas.github.io.git")
        except:
            print("You have already cloned the repo, there is no need to do it again.")

        global printProfiles
        printProfiles = os.listdir(cwd + "/bioschemas.github.io/_profiles")
        global firstChange
        firstChange = False

        # for elim in printProfiles:
        #   print(elim)
        self.setWindowTitle(self.title)
        # self.setGeometry(self.left, self.top, self.width, self.height)
        self.setFixedSize(self.width, self.height)
        self.layout = QVBoxLayout()
        self.center()
        self.createTable2()
        ##for i in range(50):
        ##  button = QPushButton(str(i), self)
        ##button.setToolTip('This is an example button')
        ###button.move(50, 70)
        ##self.layout.addWidget(button)
        # button.clicked.connect(self.on_click)
        lab = QLabel()
        lab.setContentsMargins(10, 10, 10, 10)
        lab.setText("This is where you can pick the specific profile that you want to edit. You can do this simply "
                    "by clicking that particular profile name. This will open that profile in a new window with all "
                    "of the appropriate properties, at which point you can click on any property to change any aspect "
                    "of it.")
        lab.setWordWrap(True)
        self.layout.addWidget(lab)
        self.layout.addWidget(self.tableWidget)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def createTable2(self):
        self.tableWidget = QTableWidget()
        self.tableWidget.horizontalHeader().hide()
        self.tableWidget.verticalHeader().hide()

        # Row count

        h = len(printProfiles)

        self.tableWidget.setRowCount(h)

        # Column count
        self.tableWidget.setColumnCount(1)
        self.tableWidget.setColumnWidth(0, 500)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.tableWidget.verticalScrollBar().setSingleStep(20)
        for i in range(h):
            btn = QPushButton()
            currentButton = printProfiles[i]
            btn.setText(str(currentButton))
            self.i = i
            btn.clicked.connect(partial(self.on_click, i))
            self.tableWidget.setCellWidget(i, 0, btn)

    @pyqtSlot()
    def on_click(self, i):
        #print(str(i) + " iaewhdoiuhwaoiudhwa")
        profile = str(printProfiles[i])
        printFiles = os.listdir(
            "BioschemasGitClone/bioschemas.github.io/_profiles/" + profile)

        global highest
        highest = 0
        newest = ""
        for elim in printFiles:
            m = elim.split("-", 1)
            x = str(m[0])
            x = x[2:]
            x = int(x)
            if x > highest:
                highest = x
                newest = elim  # get the newest change to the profile

        global startingHighest
        startingHighest = highest

        #print(profile + "/" + newest)
        global profileNewest
        profileNewest = str(profile + "/" + newest)

        self.j = E()
        self.j.show()
        self.close()


class E(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        self.resize(1920, 900)  # set initial size of the window
        self.center()  # center the window
        # self.setStyleSheet("background-color: white;")

        self.setStyleSheet("background-color: rgb(240, 240, 240)")
        self.menubar = QMenuBar()
        self.menubar.setFont((QFont("Ariel", 10)))
        self.menubar.setStyleSheet(
            """
            QMenuBar {
                background: #0b794b
            }
            QMenuBar::item {
                color: rgb(255,255,255);
                font-size: 36px
            }
            QMenuBar::item:selected { 
                color: rgb(0, 0, 0);
                background-color: #519f7f
            }
            QMenu {
                background: #519f7f
            }

            """)
        #actionFile = self.menubar.addMenu("File")
        #actionFile.addAction("New")
        #actionFile.addAction("Open")
        #actionFile.addAction("Save")

        #self.menubar.addAction("Switch Profile")

        openFile = QAction("Open Externally", self)
        self.menubar.addAction(openFile)
        openFile.triggered.connect(self.onClickOpenNotepad)

        #action1 = QtWidgets.QWidgetAction(self)
        #self.label1 = QtWidgets.QLabel("Action1")
        #action1.setDefaultWidget(self.label1)
        #action1.setText('Action1')
        #self.menubar.addAction(action1)

        # menubar.setStyleSheet("QMenuBar::item {background: rgb(170,200,200)}")

        self.setWindowTitle('Profile Editing Application- Currently Editing: ' + profileNewest)  # set the title of the window

        self.creatingTable()  # create the table that will store the property data
        l1 = QLabel()

        l1.setText(
            "This is an application to edit the properties of Bioschemas profiles. <br><br><font color='green'>Green</font> properties/types are "
            "proposed by Bioschemas, or indicate proposed changes by Bioschemas to Schema.org <br><font color='red'>Red</font> properties/"
            "types exist in the core of Schema.org <br><font color='blue'>Blue</font> properties/types exist in the pending area of Schema.org"
            "<br>Black properties/types are reused from external vocabularies/ontologies")
        l1.setFont((QFont("Ariel", 10)))
        # l1.setStyleSheet("background-color: rgb(220, 220, 220)")
        createNewProperty = QPushButton("Create New Property")
        createNewProperty.setStyleSheet("font: bold;")
        createNewProperty.clicked.connect(self.clickNewPropertyButton)
        createNewProperty.setMaximumWidth(300)

        showAllExamples = QPushButton("Show All Examples")
        showAllExamples.setStyleSheet("font: bold;")
        showAllExamples.clicked.connect(self.clickShowAllExamples)
        showAllExamples.setMaximumWidth(300)

        self.searchbar = QLineEdit()
        self.searchbar.setPlaceholderText("Search Properties")
        self.searchbar.setMaximumWidth(300)
        self.searchbar.textChanged.connect(self.update_display)
        self.searchbar.setStyleSheet("background-color: white; border: 1px solid black")
        self.searchbar.setToolTip("This will let you search through the loaded properties.")

        self.layout = QVBoxLayout()  # this sets the layout to be aligned vertically
        l2 = QVBoxLayout()
        l2.setContentsMargins(10, 0, 0, 0)
        self.layout.addWidget(self.menubar)
        l2.addWidget(l1)
        l2.addWidget(createNewProperty)
        l2.addWidget(showAllExamples)
        l2.addWidget(self.searchbar)
        self.layout.addLayout(l2)
        self.layout.addWidget(self.tableWidget)  # add the widgets to the layout
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(self.layout)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def creatingTable(self):
        self.tableWidget = QTableWidget()

        #print("hiawdawde")
        data = importYaml()  # get the initial data from the file and set it to a variable

        b = data['mapping'][0]
        rowNames = []
        for elim in b:
            rowNames.append(elim)
        # print(rowNames)
        h = len(data['mapping']) + 4  # this is used to set the height and width of
        # the table to the amount of entries in the file, adjusted for the marginality
        w = len(rowNames)

        self.tableWidget.setRowCount(h)
        self.tableWidget.setColumnCount(w)
        self.tableWidget.setHorizontalHeaderLabels(rowNames)
        for c in range(w):
            self.tableWidget.setColumnWidth(c, 150)
            if c == 0 or c == 1 or c == 8:
                self.tableWidget.setColumnWidth(c, 300)
            if c == 2:
                self.tableWidget.setColumnWidth(c, 500)

        liRec.append(["Marginality: Recommended", "", "", "", "", "", "", "", "", "", ""])
        liMin.append(["Marginality: Minimum", "", "", "", "", "", "", "", "", "", ""])
        liOpt.append(["Marginality: Optional", "", "", "", "", "", "", "", "", "", ""])
        liUns.append(["Marginality: Unspecified", "", "", "", "", "", "", "", "", "", ""])

        for rows in range(len(data['mapping'])):
            res = findYamlValue(data, rows, rowNames)
            sorter(res)

        liTot = liMin + liRec + liOpt + liUns

        if len(liRec) == 1:
            for c in range(len(liTot)):
                if liTot[c][0] == "Marginality: Recommended":
                    self.tableWidget.hideRow(c)

        font = QFont()
        font.setBold(True)
        font.setPointSize(10)

        fon = "Schema: \n"
        # fon.setFont(font)
        for c in range(len(liTot)):
            exampleList.append(liTot[c][9])
            if liTot[c][0] != "Marginality: Recommended":
                if liTot[c][0] != "Marginality: Minimum":
                    if liTot[c][0] != "Marginality: Optional":
                        if liTot[c][0] != "Marginality: Unspecified":
                            liTot[c][2] = "<b>Schema:</b> <br>" + liTot[c][2]
                            if liTot[c][5] != "":
                                liTot[c][2] = liTot[c][2] + "<br><br><b>Bioschemas:</b><br>" + liTot[c][5]

        URL = 'https://schema.org/docs/full.html'
        page = requests.get(URL)
        final = []
        soup = BeautifulSoup(page.content, 'html.parser')
        results = soup.find(id='mainContent')
        q = results.find_all('a')
        for elim in q:
            stringSchema = str(elim)
            frontCheck = stringSchema.split('href="/')
            for g in frontCheck:
                i = g.split('"')[0]
                if i != "<td class=":
                    final.append(i)

        final = list(dict.fromkeys(final))

        for c in range(len(liTot)):
            x = liTot[c][1]
            t = ""
            for s in x:
                if s == ",":
                    t = t + "\n"
                elif s != "[":
                    if s != "]":
                        if s != "'":
                            if s != " ":
                                t = t + s
            # liTot[c][1] = t  # i know this is really ugly, but the input is a string that looks like a list, so
            # had to cut off all the extra bits
            expectedList = t.split('\n')
            colouredList = ""
            for elLength in range(len(expectedList)):
                for schemaList in range(len(final)):
                    if expectedList[elLength] == final[schemaList]:
                        expectedList[elLength] = "<a href=\"https://schema.org/" + expectedList[
                            elLength] + "\" style=\"color:red\">" + expectedList[elLength] + "<br></a>"

                if liTot[c][0] != "Marginality: Recommended":
                    if liTot[c][0] != "Marginality: Minimum":
                        if liTot[c][0] != "Marginality: Optional":
                            if liTot[c][0] != "Marginality: Unspecified":
                                if "color:red" not in expectedList[elLength]:
                                    expectedList[elLength] = "<a href=\"https://bioschemas.org/" + expectedList[
                                        elLength] + "\" style=\"color:green\">" + expectedList[elLength] + "<br></a>"

                colouredList = colouredList + expectedList[elLength]
            liTot[c][1] = colouredList

        for rows in range(len(liTot)):
            for x in range(w):
                self.tableWidget.setItem(rows, x, QTableWidgetItem(liTot[rows][x]))

        profileName = data['name']
        for rows in range(len(liTot)):
            for x in range(w - 1):
                textEdit = QTextBrowser()
                textEdit.setFont(QFont("Ariel", 9))
                textEdit.setStyleSheet("background-color: white; border: white")
                textEdit.setText(str(liTot[rows][x]))
                textEdit.setOpenExternalLinks(True)

                if str(liTot[rows][0]) != "Marginality: Minimum" and str(liTot[rows][0]) != "Marginality: Recommended" \
                        and str(liTot[rows][0]) != "Marginality: Optional" and str(
                    liTot[rows][0]) != "Marginality: Unspecified":
                    if x == 0:
                        textEdit.setStyleSheet("background-color: rgb(180, 180, 180); border: 2px solid white;")
                        if str(liTot[rows][3]) == "bioschemas":
                            textEdit.setText("<a href=\"https://bioschemas.org/profiles/" + str(
                                profileName) + "\" style=\"color:green\"><b>" + str(liTot[rows][x]) + "</b></a>")
                        if str(liTot[rows][3]) == "":
                            textEdit.setText("<a href=\"https://schema.org/" + str(
                                liTot[rows][x]) + "\" style=\"color:red\"><b>" + str(liTot[rows][x]) + "</b></a>")

                else:
                    textEdit.setText("<b>" + str(liTot[rows][x]) + "</b>")

                self.tableWidget.setCellWidget(rows, x, textEdit)

                if str(liTot[rows][0]) == "Marginality: Minimum" or str(liTot[rows][0]) == "Marginality: Recommended" \
                        or str(liTot[rows][0]) == "Marginality: Optional" or str(
                    liTot[rows][0]) == "Marginality: Unspecified":
                    textEdit.setStyleSheet("background-color: rgb(180, 180, 180); border: none")

        for i in range(h):
            self.tableWidget.item(i, 0).setFont(font)
        self.tableWidget.setShowGrid(False)
        self.tableWidget.setFocusPolicy(QtCore.Qt.NoFocus)

        self.tableWidget.setWordWrap(True)
        self.tableWidget.setFont(QFont("Ariel", 9))
        self.tableWidget.insertColumn(w)
        for col in range(h):
            self.tableWidget.setItem(col, w, QTableWidgetItem(""))  # all columns have to have some value to be coloured
            self.tableWidget.item(col, w).setBackground(QtGui.QColor(180, 180, 180))

        rowNames.append("Edit Property")
        self.tableWidget.setHorizontalHeaderLabels(rowNames)
        for x in range(len(liTot)):
            if liTot[x][0] != "Marginality: Recommended":
                if liTot[x][0] != "Marginality: Minimum":
                    if liTot[x][0] != "Marginality: Optional":
                        if liTot[x][0] != "Marginality: Unspecified":
                            eachButton = self.tableButton()
                            eachButton.setGeometry(200, 150, 100, 40)
                            eachButton.setIcon(QIcon('edit_button.png'))
                            eachButton.setIconSize(QSize(60, 60))
                            eachButton.setStyleSheet('QPushButton {background-color: #FFFFFF; border:  none}')

                            self.tableWidget.setCellWidget(x, w, eachButton)
                            buttonList.append(eachButton)
                            eachButton.clicked.connect(self.click)

        for x in range(len(liTot)):
            if liTot[x][0] != "Marginality: Recommended":
                if liTot[x][0] != "Marginality: Minimum":
                    if liTot[x][0] != "Marginality: Optional":
                        if liTot[x][0] != "Marginality: Unspecified":
                            eachExampleButton = self.tableExampleButton()
                            # eachExampleButton.setGeometry(200, 150, 100, 40)
                            eachExampleButton.setIcon(QIcon('example_icon.png'))
                            eachExampleButton.setIconSize(QSize(60, 60))
                            eachExampleButton.setStyleSheet('QPushButton {background-color: #FFFFFF; border:  none}')

                            self.tableWidget.setCellWidget(x, w - 1, eachExampleButton)
                            buttonList2.append(eachExampleButton)
                            eachExampleButton.clicked.connect(self.clickExample)
        self.show()

        for c in range(h):
            self.tableWidget.setRowHeight(c, 250)
            self.tableWidget.item(c, 0).setBackground(QtGui.QColor(200, 200, 200))

            if liTot[c][3] == "":
                self.tableWidget.item(c, 0).setForeground(QtGui.QColor(100, 0, 0))
            elif liTot[c][3] == "bioschemas":
                self.tableWidget.item(c, 0).setForeground(QtGui.QColor(0, 100, 0))
            else:
                self.tableWidget.item(c, 0).setForeground(QtGui.QColor(0, 0, 100))

            if liTot[c][0] == "Marginality: Recommended" or liTot[c][0] == "Marginality: Minimum" or liTot[c][
                0] == "Marginality: Optional" or liTot[c][0] == "Marginality: Unspecified":
                self.tableWidget.setRowHeight(c, 50)
                self.tableWidget.item(c, 0).setForeground(QtGui.QColor(0, 0, 0))
                for s in range(w):
                    self.tableWidget.item(c, s).setBackground(QtGui.QColor(180, 180, 180))

        self.tableWidget.hideColumn(3)
        self.tableWidget.hideColumn(4)
        self.tableWidget.hideColumn(5)
        if w == 10:
            self.tableWidget.hideColumn(6)
        else:
            self.tableWidget.hideColumn(7)  # to deal with when there are 10/11 columns

        # self.tableWidget.setStyleSheet('QTableWidget::item {border-bottom: 1px solid blue;}')
        self.tableWidget.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.tableWidget.verticalScrollBar().setSingleStep(20)
        self.tableWidget.setStyleSheet("::section{Background-color:rgb(160,160,160);border-radius:1px;}")
        self.tableWidget.verticalScrollBar().setStyleSheet('background:rgb(160,160,160)')
        self.tableWidget.horizontalScrollBar().setStyleSheet('background:rgb(160,160,160)')
        self.tableWidget.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.horizontalHeader().setFont(font)

        self.tableWidget.horizontalHeaderItem(0).setToolTip("This column is for listing the property name.")
        self.tableWidget.horizontalHeaderItem(1).setToolTip("This column is for listing expected type of the property.")
        self.tableWidget.horizontalHeaderItem(2).setToolTip(
            "This column is for the description, as well as\nthe bioschemas description of the property.")
        self.tableWidget.horizontalHeaderItem(7).setToolTip(
            "This column is for listing the cardinality of the property.")
        self.tableWidget.horizontalHeaderItem(8).setToolTip("This column is for listing the controlled vocabulary.")
        self.tableWidget.horizontalHeaderItem(9).setToolTip("This column is for listing the examples of the property.")
        self.tableWidget.horizontalHeaderItem(10).setToolTip("This column is for the edit buttons.")

        self.tableWidget.verticalHeader().hide()

        for c in range(h):
            if len(liMin) == 1:
                if self.tableWidget.item(c, 0).text() == "Marginality: Minimum":
                    self.tableWidget.hideRow(c)
            if len(liRec) == 1:
                if self.tableWidget.item(c, 0).text() == "Marginality: Recommended":
                    self.tableWidget.hideRow(c)
            if len(liOpt) == 1:
                if self.tableWidget.item(c, 0).text() == "Marginality: Optional":
                    self.tableWidget.hideRow(c)
            if len(liUns) == 1:
                if self.tableWidget.item(c, 0).text() == "Marginality: Unspecified":
                    self.tableWidget.hideRow(c)

            # if str(self.tableWidget.item(c, 0).background().color().getRgb()) == "(180, 180, 180, 255)":
            # print("yancy")

    def tableButton(self):
        btn = QPushButton("")
        return btn

    def tableExampleButton(self):
        btn = QPushButton("")
        return btn

    def click(self):
        btn = self.tableWidget.focusWidget()
        index = self.tableWidget.indexAt(btn.pos())
        global btnIndex
        btnIndex = index.row()
        self.d = Second()
        self.d.show()

    def clickExample(self):
        btn2 = self.tableWidget.focusWidget()
        index2 = self.tableWidget.indexAt(btn2.pos())
        global btnIndex2
        btnIndex2 = index2.row()
        self.sw = ExampleButtons()
        self.sw.show()

    def clickNewPropertyButton(self):
        global btnIndex
        btnIndex = 0
        self.d = Second()
        self.d.show()

    def clickShowAllExamples(self):
        global btnIndex2
        btnIndex2 = 0
        self.full = ExampleButtons()
        self.full.show()

    def onClickOpenNotepad(self):
        global profileNewest
        p = profileNewest
        #print(p)
        subprocess.call(['notepad.exe', 'BioschemasGitClone/bioschemas.github.io/_profiles/' + p])


    def update_display(self, text):
        data = importYaml()  # get the initial data from the file and set it to a variable
        b = data['mapping'][0]
        h = len(data['mapping']) + 4
        x = self.tableWidget.item(1, 0).text()
        for row in range(h):
            if text.lower() in self.tableWidget.item(row, 0).text().lower() or self.tableWidget.item(row, 0).text() == \
                    "Marginality: Recommended" or self.tableWidget.item(row, 0).text() == "Marginality: Minimum" \
                    or self.tableWidget.item(row, 0).text() == "Marginality: Optional" or \
                    self.tableWidget.item(row, 0).text() == "Marginality: Unspecified":

                self.tableWidget.showRow(row)
            else:
                self.tableWidget.hideRow(row)

    def passed(self):
        return btnIndex

    def closeEvent(self, event):
        global startingHighest
        #print(startingHighest)
        c = startingHighest

        global profileNewest
        f = profileNewest
        location = f.split("/", 1)
        profile = location[0]
        p = os.listdir('BioschemasGitClone/bioschemas.github.io/_profiles/' + profile)
        #print(p)

        h = 0
        newest = ""
        allVersionList = []
        for elim in p:
            m = elim.split("-", 1)
            x = str(m[0])
            x = x[2:]
            x = int(x)
            allVersionList.append(x)
            if x > h:
                h = x
                newest = elim

        lenDirectory = h
        #print(lenDirectory)
        x = natsorted(p)  # little function i found that will sort the list in a natural way, similar to windows file explorer
        #print(x)
        t = sorted(allVersionList)
        #print(t)
        #print("000")
        #print("oahwdh8o" + str(startingHighest))
        index = t.index(int(startingHighest))
        #print(index)
        count = 0
        for i in range(len(t)):
            #print("c=" + str(count))
            if i > index:
                #print("i= " + str(i))
                #print("nlent" + str(len(t)))
                if i != len(t) - 1:
                    #print(("llllll " + str(len(allVersionList))))
                    os.remove('BioschemasGitClone/bioschemas.github.io/_profiles/' + profile + '/' + x[i])
            count = count + 1

        currentVersion = startingHighest + 1

        today = date.today()
        dateToday = today.strftime("%Y_%m_%d")

        p = os.listdir('BioschemasGitClone/bioschemas.github.io/_profiles/' + profile)  # get the new length of the directory
        fileToRename = '/0.' + str(currentVersion) + '-DRAFT-' + dateToday + '.html'
        # print("\n" + p[-1])
        if t[-1] != startingHighest:
            os.rename('BioschemasGitClone/bioschemas.github.io/_profiles/' + profile + '/' + x[-1], 'BioschemasGitClone/bioschemas.github.io/_profiles/' + profile + '/' + fileToRename)



class Second(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        l1 = QLabel()
        l1.setText(
            "This is the area where you can edit a selected property or create a new one.\nJust type in the boxes to change them, "
            "and hit save when you are done. Then close the application.\nWhen you click save the changes will be saved to a new file.\n\n"
            "[PLEASE NOTE] \nFor expected type, make sure the whole entry is in square brackets and put a comma between each entity (example: ['URL', 'Name']).")
        l1.setFont((QFont("Ariel", 10)))
        boxList = []
        self.createTable2(boxList)
        self.saveButton()
        self.button.clicked.connect(partial(clickSave, boxList, l1))

        self.layoutH = QGridLayout()

        # self.layout2 = QVBoxLayout()  # this sets the layout to be aligned vertically
        self.layoutH.addWidget(l1, 0, 0)
        self.layoutH.addWidget(self.button, 0, 1, 2, 1)
        # self.layout2.addWidget(self.layoutH)
        self.layoutH.addWidget(self.tableWidget2, 2, 0, 1, 2)
        self.setLayout(self.layoutH)
        self.resize(1280, 720)  # set initial size of the window
        self.setWindowTitle('Property Editor')

    def saveButton(self):
        self.button = QPushButton('', self)
        self.button.setIcon(QIcon('save.png'))
        self.button.setStyleSheet('QPushButton {background-color:#FFFFFF;}')
        self.button.setMaximumWidth(100)
        self.button.setIconSize(QSize(50, 50))

        self.button.move(50000, 50000)  # for some reason it spawns two buttons, so i just set the second to be off page

    def createTable2(self, boxList):
        data2 = importYaml()
        b = data2['mapping'][0]
        rowNames = []
        for elim in b:
            rowNames.append(elim)
        h = len(rowNames)
        w = 1
        self.tableWidget2 = QTableWidget()
        self.tableWidget2.setRowCount(h)
        self.tableWidget2.setColumnCount(w)
        self.tableWidget2.setVerticalHeaderLabels(rowNames)
        self.tableWidget2.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # self.tableWidget2.setMaximumWidth(900)

        row = getInd()
        liOpt2 = []
        liRec2 = []
        liMin2 = []
        liUns2 = []
        liRec2.append(["Marginality: Recommended", "", "", "", "", "", "", "", "", ""])
        liMin2.append(["Marginality: Minimum", "", "", "", "", "", "", "", "", ""])
        liOpt2.append(["Marginality: Optional", "", "", "", "", "", "", "", "", ""])
        liUns2.append(["Marginality: Unspecified", "", "", "", "", "", "", "", "", ""])

        for rows in range(len(data2['mapping'])):
            res2 = findYamlValue(data2, rows, rowNames)
            sorter2(res2, liMin2, liOpt2, liRec2, liUns2)
        liTot2 = liMin2 + liRec2 + liOpt2 + liUns2

        res2 = liTot2[row]

        for x in range(h):
            textEdit = QTextEdit()
            textEdit.setText('')
            textEdit.setFont(QFont("Ariel", 9))
            if row != 0:
                textEdit.setText(res2[x])
            else:
                textEdit.setText('')
            boxList.append(textEdit)
            self.tableWidget2.setCellWidget(x, 0, textEdit)
            self.tableWidget2.setRowHeight(x, 200)
        # w = self.textEdit.toPlainText()
        # w.toPlainText()
        # print(str(s))

        # self.tableWidget2.setCellWidget(0, 0, self.textEdit)

        self.tableWidget2.setColumnWidth(0, 400)
        self.tableWidget2.setColumnWidth(1, 900)
        self.tableWidget2.verticalHeader().setFont(QFont("Ariel", 10))
        self.tableWidget2.horizontalHeader().hide()
        self.tableWidget2.setStyleSheet("::section{Background-color:rgb(160,160,160);border-radius:1px;}")
        self.tableWidget2.verticalScrollBar().setStyleSheet('background:rgb(160,160,160)')
        self.tableWidget2.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.tableWidget2.verticalScrollBar().setSingleStep(20)

        self.show()

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message',
                                     "Are you sure you want to quit? Any unsaved changes will not be kept",
                                     QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:

            event.accept()
        else:
            event.ignore()
            # add a pop up box that will prompt the user if they hit the quit button


def getInd():
    global btnIndex
    x = btnIndex
    return x


def clickSave(boxList, l1):
    #print("1123454311")
    global profileNewest
    f = profileNewest
    location = f.split("/", 1)
    profile = location[0]

    printFiles = os.listdir(
        "BioschemasGitClone/bioschemas.github.io/_profiles/" + profile)

    highest = 0
    newest = ""
    for elim in printFiles:
        m = elim.split("-", 1)
        x = str(m[0])
        x = x[2:]
        x = int(x)
        if x > highest:
            highest = x
            newest = elim  # get the newest change to the profile

    #print(profile + "/" + newest)
    profileNewest = str(profile + "/" + newest)

    data2 = importYaml()
    # pList = ["property", "expected_types", "description", "type", "type_url", "bsc_description", "equivalentProperty",                              # grab from the actual data instead
    #       "marginality", "cardinality", "controlled_vocab", "example"]
    b = data2['mapping'][0]
    pList = []
    for elim in b:
        pList.append(elim)

    q = getLiTot()

    row = getInd()
    try:
        for d in range(len(data2['mapping'])):
            if data2['mapping'][d]['property'] == q[row][0]:
                for i in range(len(pList)):
                    w = boxList[i]
                    x1 = str(w.toPlainText())
                    data2['mapping'][d][pList[i]] = x1
                    if i == 1:
                        x1 = ast.literal_eval(x1)  # this beforehand is a list that looks like a string, this small function converts it nicely to a list for me
                        data2['mapping'][d][pList[i]] = x1
    except:
        print("something went wrong")
    try:
        if row == 0:
            for i in range(len(pList)):
                w = boxList[i]
                x2 = str(w.toPlainText())
                #print(d)
                data2['mapping'][d][pList[i]] = x2
                if i == 1:
                    x2 = ast.literal_eval(x2)  # this beforehand is a list that looks like a string, this small function converts it nicely to a list for me
                    data2['mapping'][d][pList[i]] = x2
        l1.setText(
            "This is the area where you can edit a selected property or create a new one.\nJust type in the boxes to change them, "
            "and hit save when you are done. Then close the application.\nWhen you click save the changes will be saved to a new file."
            "\n\n[PLEASE NOTE] \nFor expected type, make sure the whole entry is in square brackets and put a comma between each entity (example: ['URL', 'Name'])."
            "\n\nTHAT SAVE WAS MADE CORRECTLY!!\n")
    except:
        print("that was the wrong data that you typed")
        l1.setText("Sorry, you entered the incorrect format for the YAML, please try again!")

    s = "\n---\n"
    foundHTML = False

    currentVersion = highest
    currentVersion = currentVersion + 1

    today = date.today()
    dateToday = today.strftime("%Y_%m_%d")
    f = profileNewest

    fileToOpen = 'BioschemasGitClone/bioschemas.github.io/_profiles/' + location[0] + '/0.' + str(currentVersion) + '-DRAFT-' + dateToday + '.html'
    with open('0.11-RELEASE.html', 'r') as f:
        for line in f:
            if '<!DOCTYPE HTML>' in line:
                foundHTML = True
            if foundHTML:
                s = s + line
    #data2.encode(encoding='utf-16')
    # open(fileToOpen, "w").close()  # make sure the file is empty
    with open(fileToOpen, 'a') as file:
        file.write("---\n")
        documents = yaml.dump(data2, file, default_flow_style=False, sort_keys=False)
        file.write(s)


class ExampleButtons(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()
        self.btnIndex2 = btnIndex2

    def initUI(self):
        self.setWindowTitle('Single Example Viewer')
        self.setMinimumWidth(500)
        self.setMinimumHeight(500)
        self.center()

        myFont = QtGui.QFont()
        myFont.setBold(True)
        ku = self.getInd2()
        if ku == 0:
            self.setWindowTitle('All Example Viewer')
        exampleValue = self.getExampleValue(ku)
        l1 = QTextEdit()
        l1.setText(str(exampleValue))

        self.layout = QVBoxLayout()  # this sets the layout to be aligned vertically
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(l1)

        # self.setFixedSize(self.layout.sizeHint())
        self.setLayout(self.layout)

    def getInd2(self):
        global btnIndex2
        x = btnIndex2
        return x

    def getExampleValue(self, ku):

        data3 = importYaml()
        b = data3['mapping'][0]
        rowNames2 = []
        for elim in b:
            rowNames2.append(elim)
        liOpt3 = []
        liRec3 = []
        liMin3 = []
        liUns3 = []
        liRec3.append(["Marginality: Recommended", "", "", "", "", "", "", "", "", ""])
        liMin3.append(["Marginality: Minimum", "", "", "", "", "", "", "", "", ""])
        liOpt3.append(["Marginality: Optional", "", "", "", "", "", "", "", "", ""])
        liUns3.append(["Marginality: Unspecified", "", "", "", "", "", "", "", "", ""])
        for rows in range(len(data3['mapping'])):
            res3 = findYamlValue(data3, rows, rowNames2)
            sorter2(res3, liMin3, liOpt3, liRec3, liUns3)
        liTot2 = liMin3 + liRec3 + liOpt3 + liUns3

        if ku == 0:
            listExample = ""
            for rows in range(len(data3['mapping'])):
                if liTot2[rows][0] == "Marginality: Recommended" or liTot2[rows][0] == "Marginality: Minimum" or \
                        liTot2[rows][0] == "Marginality: Optional" or liTot2[rows][0] == "Marginality: Unspecified":
                    pass
                else:
                    listExample = listExample + "//---------------------\nProperty: \n" + liTot2[rows][
                        0] + "\n\nExample: \n" + str(liTot2[rows][9]) + "\n\n"
            return listExample

        return "Property: \n" + liTot2[ku][0] + "\n\nExample: \n" + liTot2[ku][9]

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

class StartWarning(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setGeometry(200, 200, 200, 220)
        layout = QVBoxLayout()
        label = QLabel("The application has to download the whole Bioschemas Github, so this may take a few moments. This window will disappear after a few seconds.")
        label.setWordWrap(True)
        label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(label)
        self.setLayout(layout)
        self.center()
        self.show()
        # threaded1()
        QtCore.QTimer.singleShot(8000, self.close)
        QtCore.QTimer.singleShot(200, openApp)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


def getLiTot():
    data2 = importYaml()
    b = data2['mapping'][0]
    rowNames = []
    for elim in b:
        rowNames.append(elim)

    liOpt2 = []
    liRec2 = []
    liMin2 = []
    liUns2 = []
    liRec2.append(["Marginality: Recommended", "", "", "", "", "", "", "", "", ""])
    liMin2.append(["Marginality: Minimum", "", "", "", "", "", "", "", "", ""])
    liOpt2.append(["Marginality: Optional", "", "", "", "", "", "", "", "", ""])
    liUns2.append(["Marginality: Unspecified", "", "", "", "", "", "", "", "", ""])

    for rows in range(len(data2['mapping'])):
        res2 = findYamlValue(data2, rows, rowNames)
        sorter2(res2, liMin2, liOpt2, liRec2, liUns2)
    liTot2 = liMin2 + liRec2 + liOpt2 + liUns2
    return liTot2


def sorter(res):
    if res[6] == "Optional" or res[7] == "Optional":
        liOpt.append(res)
    elif res[6] == "Recommended" or res[7] == "Recommended":
        liRec.append(res)
    elif res[6] == "Minimum" or res[7] == "Minimum":
        liMin.append(res)
    elif res[6] == "Unspecified" or res[7] == "Unspecified":
        liUns.append(res)


def sorter2(res2, liMin2, liOpt2, liRec2, liUns2):
    if res2[6] == "Optional" or res2[7] == "Optional":
        liOpt2.append(res2)
    elif res2[6] == "Recommended" or res2[7] == "Recommended":
        liRec2.append(res2)
    elif res2[6] == "Minimum" or res2[7] == "Minimum":
        liMin2.append(res2)
    elif res2[6] == "Unspecified" or res2[7] == "Unspecified":
        liUns2.append(res2)


def alignText(text):
    counter = 0
    counter2 = 0
    newText = ""
    m = False
    for q in text:
        if counter % 30 == 0 and counter != 0:
            m = True

        if text[counter] == " " and m is True:
            newText = newText + "\n"
            m = False
            counter2 = 0

        if counter2 == 35:
            newText = newText + "\n"
            counter2 = 0

        newText = newText + q
        counter = counter + 1
        counter2 = counter2 + 1
    newText = newText.replace("\n ", "\n")
    return newText


def importYaml():
    with open('BioschemasGitClone/bioschemas.github.io/_profiles/' + profileNewest, encoding='utf-8') as f:
        # needs to be forced to utf-8 because if not python will not parse the characters correctly (yaml default is utf-16), probably resulting in a crash
        t = yaml.safe_load_all(f)
        data = list(t)
        return data[0]


def findYamlValue(data, row, rowNames):
    dataList = []
    pList = rowNames
    key = data['mapping'][row]
    # print(key["property"])
    # for value in key:
    # print(value + ":")
    # print(key[value])
    # print(key["property"])
    for l in range(len(pList)):
        dataList.append(str(key[pList[l]]))
    return dataList


def openApp():
    ex = App()
    # sys.exit(app.exec_())


def main():
    # importYaml()
    app = QApplication(sys.argv)
    window = StartWarning()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
