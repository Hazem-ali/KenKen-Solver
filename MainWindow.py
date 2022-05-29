# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:\Hazem\Coding\KenKen GUI\Ui Files\KenKen_Main.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from typing import List, Tuple, Optional, Dict
from PyQt5 import QtCore, QtGui, QtWidgets
import qdarkstyle as theme
from board import Board
from kenken import generate, solve
import helpers

# Theme Constants
Light, Dark = "Light", "Dark"


# TODO if you want constant color list for board, create random colors when generate button is clicked

class Ui_MainWindow(object):
    def __init__(
            self: object) -> None:
        self.guiTheme = Light
        self.Board: object = None
        self.cellAssignments = None
        self.colors = list()  # generated colors for the board

    def StatusBar_Message(self, color, message):
        if self.guiTheme == Light:
            self.statusBar.setStyleSheet("color : " + color)
        else:
            self.statusBar.setStyleSheet("color : white")
        self.statusBar.showMessage(message, 5000)
        return

    def GUI_Color(self, color):
        self.guiTheme = color
        Change_Theme(color)
        self.StatusBar_Message("blue", color + " Mode Applied")
        return

    def ErrorDialog(self, error_message):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Critical)
        msg.setText('Error' + ' '*60)
        msg.setInformativeText(error_message)
        msg.setWindowTitle("Error")
        msg.exec_()
        return

    def InfoDialog(self, message):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.setText('Info' + ' '*60)
        msg.setInformativeText(message)
        msg.setWindowTitle("Info")
        msg.exec_()
        return

    def GenerateButtonHandler(
            self: object,
            nrows: int = 3) -> None:
        """
        Generate a new board with the given number of blocks

        :param nrows: rows of the square board
        :return: None
        """

        try:
            nrows = int(self.BoardSizeInput.text())
        except:
            self.ErrorDialog("Please enter a valid board size")
            return


        self.Generate_Board(number_of_blocks=nrows)

    def Generate_Board(
            self: object,
            number_of_blocks: int = 3,
            block_size: int = 80):
        # self.Board = Board(self.BoardSizeInput.value())

        _, cellAssignments = generate(number_of_blocks)

        self.Board = Board(number_of_blocks=number_of_blocks,
                           block_size=block_size)
        # genrate the board
        # generate the laws for the board (m3rof y3ny)
        laws = "\n".join(cel.__str__() for cel in cellAssignments)

        # * wrapper function to get cage values and cage cells
        laws = helpers.Create_Law_Positions(laws)
        # {((1, 1), (1, 2)): '11 +',...}

        self.Board.setColors(helpers.Generate_Random_Colors(len(laws)))

        self.Board.setLaws(laws)
        # self.Board.setData([
        # 4x4 board

        # ((0, 0), (0, 255, 150), "1"),
        # ((1, 0), (150, 255, 150), "4"),
        # ((2, 0), (0, 18, 150), "7"),
        # ((3, 0), (158, 255, 12), "7"),
        # ((0, 1), (255, 0, 150), "2"),
        # ((1, 1), (0, 255, 150), "M"),
        # ((2, 1), (0, 255, 150), "O"),
        # ((3, 1), (0, 255, 150), "O"),
        # ((0, 2), (0, 255, 150), "F"),
        # ((1, 2), (255, 255, 150), "T"),
        # ((2, 2), (0, 255, 150), "Y"),
        # ((3, 2), (0, 255, 150), "Y"),
        # ((0, 3), (0, 255, 150), "K"),
        # ((1, 3), (0, 255, 150), "N"),
        # ((2, 3), (0, 255, 150), "K"),
        # ((3, 3), (0, 255, 0), "N"),

        # 3x3 board
        # ((0, 0), (12, 0, 150), "X"),
        # ((1, 0), (150, 255, 150), ''),
        # ((2, 0), (0, 18, 150), ""),
        # ((3, 0), (158, 255, 12), ""),
        # ((0, 1), (255, 0, 150), "2"),
        # ((1, 1), (0, 255, 150), "a"),
        # ((2, 1), (0, 255, 150), "a"),
        # ((3, 1), (0, 255, 150), "O"),
        # ((0, 2), (0, 255, 150), "F"),
        # ((1, 2), (255, 255, 150), "T"),
        # ((2, 2), (0, 255, 150), "2"),
        # ((3, 2), (0, 255, 150), "q"),
        # ])

        self.cellAssignments = cellAssignments
        # dsiplay
        self.Board.display()

    def SolveButtonHandler(
            self: object) -> None:
        # self.Generate_Board(number_of_blocks=board_size)
        algo = ''
        algorithms = ["Backtracking", "Forward Checking", "Arc Consistency"]

        algo = self.AlgorithmComboBox.currentText()

        # Error handling: invalid algorithm
        if algo not in algorithms:
            self.ErrorDialog("Please select an algorithm to solve the puzzle")
            return
        # Error handling: no board generated
        if self.cellAssignments is None:
            self.ErrorDialog("Please generate a board first")
            return

        # SOLVE THE BOARD
        self.solveBoard(algo)

    def solveBoard(
            self: object,
            algo: str):
        # laws = self.Board.getLaws()
        # solve from repo
        size = self.Board.number_of_blocks
        solver = solve(
            size=size, cellAssignments=self.cellAssignments, algorithm=algo)

        # solver = eval('''{((1,1),(1,2)):(5,6),((3,1),(2,1)):(3,6),((3,2),(2,2)):(4,1)\
        #     ,((4,1),(4,2)):(4,5),((6,1),(6,2),(6,3),(5,1)): (2,3,1,1),((5,3),(5,2)):(6,2)\
        #     ,((2,3),(2,4),(1,3),(1,4)):(5,4,4,3),((3,3),(4,3)):(2,3),((5,4),(6,4)):(5,6)\
        #     ,((2,5),(1,5)):(3,2),((3,4),(3,5)):(1,6),((4,4),(4,5),(5,5)):(2,1,4),\
        #     ((1,6),(2,6),(3,6)):(1,2,5),((4,6),(5,6)):(6,3),((6,6),(6,5)):(4,5)}''')

        # wrapper function to get cage values and cage cells
        cells = helpers.Convert_Cages(solver)
        self.Board.setData(cells)
        self.Board.display()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 620)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(800, 620))
        MainWindow.setMaximumSize(QtCore.QSize(800, 620))
        font = QtGui.QFont()
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        MainWindow.setFont(font)
        MainWindow.setAcceptDrops(False)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(
            "d:\\Hazem\\Coding\\KenKen GUI\\Ui Files\\../static/moftyIcon.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        self.verticalLayout_2.addItem(spacerItem)
        self.Title = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Felix Titling")
        font.setPointSize(23)
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(75)
        font.setStrikeOut(False)
        self.Title.setFont(font)
        self.Title.setAutoFillBackground(False)
        self.Title.setAlignment(QtCore.Qt.AlignCenter)
        self.Title.setObjectName("Title")
        self.verticalLayout_2.addWidget(self.Title)
        spacerItem1 = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        self.verticalLayout_2.addItem(spacerItem1)
        self.frame_2 = QtWidgets.QFrame(self.centralwidget)
        self.frame_2.setFrameShape(QtWidgets.QFrame.NoFrame)

        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame_2)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem2 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.BoardSizeLabel = QtWidgets.QLabel(self.frame_2)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        self.BoardSizeLabel.setFont(font)
        self.BoardSizeLabel.setObjectName("BoardSizeLabel")
        self.horizontalLayout_2.addWidget(self.BoardSizeLabel)
        self.BoardSizeInput = QtWidgets.QSpinBox(self.frame_2)
        self.BoardSizeInput.setMinimumSize(QtCore.QSize(200, 0))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        self.BoardSizeInput.setFont(font)
        self.BoardSizeInput.setMinimum(1)
        self.BoardSizeInput.setObjectName("BoardSizeInput")
        self.horizontalLayout_2.addWidget(self.BoardSizeInput)
        self.GenerateButton = QtWidgets.QPushButton(
            self.frame_2, clicked=lambda: self.GenerateButtonHandler())
        self.GenerateButton.setMinimumSize(QtCore.QSize(100, 0))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        self.GenerateButton.setFont(font)
        self.GenerateButton.setObjectName("GenerateButton")
        self.horizontalLayout_2.addWidget(self.GenerateButton)
        spacerItem3 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem3)
        self.verticalLayout_2.addWidget(self.frame_2)

        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setLineWidth(0)
        self.frame.setObjectName("frame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem4 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem4)
        self.AlgorithmComboBox = QtWidgets.QComboBox(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.AlgorithmComboBox.sizePolicy().hasHeightForWidth())
        self.AlgorithmComboBox.setSizePolicy(sizePolicy)
        self.AlgorithmComboBox.setMinimumSize(QtCore.QSize(250, 0))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        self.AlgorithmComboBox.setFont(font)
        self.AlgorithmComboBox.setObjectName("AlgorithmComboBox")
        self.AlgorithmComboBox.addItem("")
        self.AlgorithmComboBox.addItem("")
        self.AlgorithmComboBox.addItem("")
        self.AlgorithmComboBox.addItem("")
        self.horizontalLayout.addWidget(self.AlgorithmComboBox)
        self.SolveButton = QtWidgets.QPushButton(
            self.frame, clicked=lambda: self.SolveButtonHandler())
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.SolveButton.sizePolicy().hasHeightForWidth())
        self.SolveButton.setSizePolicy(sizePolicy)
        self.SolveButton.setMinimumSize(QtCore.QSize(100, 0))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        self.SolveButton.setFont(font)
        self.SolveButton.setObjectName("SolveButton")
        self.horizontalLayout.addWidget(self.SolveButton)
        spacerItem5 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem5)
        self.verticalLayout_2.addWidget(self.frame)

        spacerItem7 = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem7)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        self.menuOpen = QtWidgets.QMenu(self.menubar)
        self.menuOpen.setObjectName("menuOpen")
        self.menuTheme = QtWidgets.QMenu(self.menubar)
        self.menuTheme.setObjectName("menuTheme")
        MainWindow.setMenuBar(self.menubar)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        font = QtGui.QFont()
        font.setBold(True)
        font.setUnderline(False)
        font.setWeight(75)
        font.setStrikeOut(False)
        self.statusBar.setFont(font)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)
        self.actionOpen_Snippet_File = QtWidgets.QAction(MainWindow)
        self.actionOpen_Snippet_File.setObjectName("actionOpen_Snippet_File")
        self.actionSave_As = QtWidgets.QAction(MainWindow)
        self.actionSave_As.setObjectName("actionSave_As")
        self.actionClose = QtWidgets.QAction(MainWindow)
        self.actionClose.setObjectName("actionClose")
        self.actionLight = QtWidgets.QAction(MainWindow)
        self.actionLight.setCheckable(False)
        self.actionLight.setChecked(False)
        self.actionLight.setObjectName("actionLight")
        self.actionLight.triggered.connect(lambda: self.GUI_Color(Light))
        self.actionDark = QtWidgets.QAction(MainWindow)
        self.actionDark.setCheckable(False)
        self.actionDark.setChecked(False)
        self.actionDark.setObjectName("actionDark")
        self.actionDark.triggered.connect(lambda: self.GUI_Color(Dark))

        self.actionCompress_Current_XML = QtWidgets.QAction(MainWindow)
        self.actionCompress_Current_XML.setObjectName(
            "actionCompress_Current_XML")
        self.actionDecompress_a_File = QtWidgets.QAction(MainWindow)
        self.actionDecompress_a_File.setObjectName("actionDecompress_a_File")
        self.actionOpen_Tokens_File = QtWidgets.QAction(MainWindow)
        self.actionOpen_Tokens_File.setObjectName("actionOpen_Tokens_File")
        self.menuOpen.addAction(self.actionClose)
        self.menuTheme.addAction(self.actionLight)
        self.menuTheme.addAction(self.actionDark)
        self.menubar.addAction(self.menuOpen.menuAction())
        self.menubar.addAction(self.menuTheme.menuAction())

        self.retranslateUi(MainWindow)
        self.AlgorithmComboBox.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Kenken"))
        self.Title.setText(_translate("MainWindow", "KenKen Solver"))
        self.BoardSizeLabel.setText(
            _translate("MainWindow", "Enter board size"))
        self.BoardSizeInput.setSpecialValueText(
            _translate("MainWindow", "eg. 3 for a 3x3"))
        self.GenerateButton.setText(_translate("MainWindow", "Generate"))
        self.AlgorithmComboBox.setCurrentText(_translate(
            "MainWindow", "Choose algorithm for solver"))
        self.AlgorithmComboBox.setItemText(0, _translate(
            "MainWindow", "Choose algorithm for solver"))
        self.AlgorithmComboBox.setItemText(
            1, _translate("MainWindow", "Backtracking"))
        self.AlgorithmComboBox.setItemText(
            2, _translate("MainWindow", "Forward Checking"))
        self.AlgorithmComboBox.setItemText(
            3, _translate("MainWindow", "Arc Consistency"))
        self.SolveButton.setText(_translate("MainWindow", "Solve"))
        self.menuOpen.setTitle(_translate("MainWindow", "File"))
        self.menuTheme.setTitle(_translate("MainWindow", "Theme"))
        self.actionOpen_Snippet_File.setText(
            _translate("MainWindow", "Open Snippet File"))
        self.actionSave_As.setText(_translate("MainWindow", "Save As"))
        self.actionClose.setText(_translate("MainWindow", "Close"))
        self.actionLight.setText(_translate("MainWindow", "Light"))
        self.actionDark.setText(_translate("MainWindow", "Dark"))
        self.actionCompress_Current_XML.setText(
            _translate("MainWindow", "Compress Current XML..."))
        self.actionDecompress_a_File.setText(
            _translate("MainWindow", "Decompress a File..."))
        self.actionOpen_Tokens_File.setText(
            _translate("MainWindow", "Open Tokens File"))


def Change_Theme(color):

    # Change GUI Theme
    # get the QApplication instance,  or crash if not set
    app = QtWidgets.QApplication.instance()
    if app is None:
        raise RuntimeError("No Qt Application found.")

    if color == Dark:
        app.setStyleSheet(theme.load_stylesheet(palette=theme.DarkPalette))
    elif color == Light:
        app.setStyleSheet(theme.load_stylesheet(palette=theme.LightPalette))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    try:
        app.setStyleSheet(theme.load_stylesheet(palette=theme.DarkPalette))
    except:
        pass
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
