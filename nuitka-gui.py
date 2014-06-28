#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# PEP8:OK, LINT:OK, PY3:OK


#     Copyright 2013, Kay Hayen, mailto:kay.hayen@gmail.com
#
#     Part of "Nuitka", an optimizing Python compiler that is compatible and
#     integrates with CPython, but also works on its own.
#
#     Licensed under the Apache License, Version 2.0 (the "License");
#     you may not use this file except in compliance with the License.
#     You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#     Unless required by applicable law or agreed to in writing, software
#     distributed under the License is distributed on an "AS IS" BASIS,
#     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#     See the License for the specific language governing permissions and
#     limitations under the License.


# metadata
' Nuitka-GUI '
__version__ = ' 0.5.2 '
__license__ = ' Apache '
__author__ = ' juancarlospaco '
__email__ = ' juancarlospaco@gmail.com '
__url__ = 'http://nuitka.net'
__date__ = '2014/05'
__prj__ = 'nuitka_gui'
__docformat__ = 'html'


# imports
import sys
from getopt import getopt
from os import path
from random import randint
from subprocess import call, check_output
from webbrowser import open_new_tab

from PyQt4.QtCore import QDir, QProcess, QSize, Qt
from PyQt4.QtGui import (QAction, QApplication, QColor, QComboBox, QCompleter,
                         QCursor, QDialogButtonBox, QDirModel, QDockWidget,
                         QFileDialog, QFont, QGridLayout, QGroupBox, QIcon,
                         QLabel, QLineEdit, QMainWindow, QMessageBox, QPainter,
                         QPalette, QPen, QPixmap, QPushButton, QSizePolicy,
                         QSlider, QTextOption, QToolBar, QToolButton,
                         QVBoxLayout, QWidget)

try:
    from PyKDE4.kdeui import KTextEdit as QTextEdit
except ImportError:
    from PyQt4.QtGui import QTextEdit  # lint:ok


# constants
DEBUG, A11Y = True, False
OPEN = 'chrt -i 0 xdg-open ' if sys.platform.startswith('linux') else 'start '
OPEN = 'open ' if sys.platform.startswith('darwin') else OPEN
IS_WIN = sys.platform.startswith('win')
NUITKA = 'nuitka' if not IS_WIN else r'"C:\Python27\Scripts\nuitka"'


###############################################################################


class MyMainWindow(QMainWindow):
    ' Main Window '
    def __init__(self, parent=None):
        ' Initialize QWidget inside MyMainWindow '
        super(MyMainWindow, self).__init__(parent)
        self.statusBar().showMessage(__doc__.title())
        self.setWindowTitle(__doc__)
        self.setMinimumSize(600, 800)
        self.setMaximumSize(2048, 1024)
        self.resize(1024, 800)
        self.setWindowIcon(QIcon.fromTheme("face-monkey"))
        if not A11Y:
            self.setStyleSheet('''QWidget{color:#fff;font-family:Oxygen}
            QWidget:item:hover, QWidget:item:selected {
                background-color: cyan; color: #000
            }
            QWidget:disabled { color: #404040; background-color: #323232 }
            QWidget:focus { border: 1px solid cyan }
            QPushButton {
                background-color: gray;
                padding: 3px; border: 1px solid gray; border-radius: 9px;
                margin: 0;font-size: 12px;
                padding-left: 5px; padding-right: 5px
            }
            QLineEdit, QTextEdit {
                background-color: #4a4a4a; border: 1px solid gray;
                border-radius: 0; font-size: 12px;
            }
            QPushButton:pressed { background-color: #323232 }
            QComboBox {
                background-color: #4a4a4a; padding-left: 9px;
                border: 1px solid gray; border-radius: 5px;
            }
            QComboBox:pressed { background-color: gray }
            QComboBox QAbstractItemView, QMenu {
                border: 1px solid #4a4a4a; background:grey;
                selection-background-color: cyan;
                selection-color: #000;
            }
            QSlider {
                padding: 3px; font-size: 8px; padding-left: 2px;
                padding-right: 2px; border: 5px solid #1e1e1e
            }
            QSlider::sub-page:vertical {
                background-color: QLinearGradient(spread:pad, x1:0, y1:0, x2:1,
                    y2:0.27, stop:0 rgba(255, 0, 0, 255),
                    stop:1 rgba(50, 0, 0, 200));
                border: 4px solid #1e1e1e; border-radius: 5px
            }
            QSlider::add-page:vertical {
                background-color: QLinearGradient(spread:pad, x1:0, y1:0, x2:1,
                    y2:0.27, stop:0 rgba(0, 255, 0, 255),
                    stop:1 rgba(0, 99, 0, 255));
                border: 4px solid #1e1e1e; border-radius: 5px;
            }
            QSlider::handle:vertical {
                background-color: QLinearGradient(spread:pad, x1:0, y1:0, x2:1,
                    y2:0.273, stop:0 rgba(0, 0, 0, 255), stop:1 gray);
                height: 5px; border: 1px dotted #fff; text-align: center;
                border-top-left-radius: 2px; border-bottom-left-radius: 2px;
                border-top-right-radius: 2px; border-bottom-right-radius 2px;
                margin-left: 2px; margin-right: 2px;
            }
            QSlider::handle:vertical:hover { border: 1px solid cyan }
            QSlider::sub-page:vertical:disabled {
                background: #bbb; border-color: #999;
            }
            QSlider::add-page:vertical:disabled {
                background: #eee; border-color: #999;
            }
            QSlider::handle:vertical:disabled {
                background: #eee; border: 1px solid #aaa; border-radius: 4px;
            }
            QToolBar, QStatusBar, QDockWidget::title{background-color:#323232;}
            QToolBar::handle,
            QToolBar::handle:vertical, QToolBar::handle:horizontal {
                border: 1px solid gray; border-radius: 9px; width: 19px;
                height: 19px; margin: 0.5px
            }
            QGroupBox {
                border: 1px solid gray; border-radius: 9px; padding-top: 9px;
            }
            QStatusBar, QToolBar::separator:horizontal,
            QToolBar::separator:vertical {color:gray}
            QScrollBar:vertical{
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0,
                    stop: 0 #212121,stop: 1.0 #323232);
                width: 10px;
            }
            QScrollBar:horizontal{
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #212121,stop: 1.0 #323232);
                height: 10px;
            }
            QScrollBar::handle:vertical{
                padding: 2px;
                min-height: 50px;
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0,
                    stop: 0 #585858,stop: 1.0 #404040);
                border-radius: 5px;
                border: 1px solid #191919;
            }
            QScrollBar::handle:horizontal{
                padding: 2px;
                min-width: 50px;
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #585858,stop: 1.0 #404040);
                border-radius: 5px;
                border: 1px solid #191919;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical,
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical,
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal,
            QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
                background: none; border: none;
            }
            QDockWidget::close-button, QDockWidget::float-button {
                border: 1px solid gray;
                border-radius: 3px;
                background: darkgray;
            }''')

        self.process = QProcess()
        self.process.readyReadStandardOutput.connect(self.read_output)
        self.process.readyReadStandardError.connect(self.read_errors)
        self.process.finished.connect(self._process_finished)
        self.process.error.connect(self._process_finished)

        self.group0, self.group1 = QGroupBox("Options"), QGroupBox("Paths")
        self.group2 = QGroupBox("Nodes")
        self.group3 = QGroupBox("Python Code")
        self.group4, self.group5 = QGroupBox("Logs"), QGroupBox("Backend")
        g0grid, g1vlay = QGridLayout(self.group0), QVBoxLayout(self.group1)
        g5vlay = QVBoxLayout(self.group5)

        self.treeview_nodes, self.textedit_source = QTextEdit(), QTextEdit()
        self.dock1, self.dock2 = QDockWidget(), QDockWidget()
        self.output, self.dock3 = QTextEdit(), QDockWidget()
        self.treeview_nodes.setAutoFormatting(QTextEdit.AutoAll)
        self.treeview_nodes.setWordWrapMode(QTextOption.NoWrap)
        self.dock1.setWidget(self.treeview_nodes)
        self.dock2.setWidget(self.textedit_source)
        self.dock3.setWidget(self.output)
        self.dock1.setWindowTitle("Tree")
        self.dock2.setWindowTitle("Sources")
        self.dock3.setWindowTitle("STDOutput")
        featur = QDockWidget.DockWidgetMovable | QDockWidget.DockWidgetFloatable
        self.dock1.setFeatures(featur)
        self.dock2.setFeatures(featur)
        self.dock3.setFeatures(featur)
        QVBoxLayout(self.group2).addWidget(self.dock1)
        QVBoxLayout(self.group3).addWidget(self.dock2)
        QVBoxLayout(self.group4).addWidget(self.dock3)
        self.slider1, self.slider2 = QSlider(), QSlider()
        g0grid.addWidget(self.slider1, 0, 0)
        g0grid.addWidget(QLabel('Use Debug'), 0, 1)
        self.slider2.setValue(1)
        g0grid.addWidget(self.slider2, 1, 0)
        g0grid.addWidget(QLabel('Use verbose'), 1, 1)

        self.slider3, self.slider4 = QSlider(), QSlider()
        self.slider3.setValue(1)
        g0grid.addWidget(self.slider3, 2, 0)
        g0grid.addWidget(QLabel('Show compiling progress'), 2, 1)
        self.slider4.setValue(1)
        g0grid.addWidget(self.slider4, 3, 0)
        g0grid.addWidget(QLabel('Show Scons building debug'), 3, 1)

        self.slider5, self.slider6 = QSlider(), QSlider()
        g0grid.addWidget(self.slider5, 4, 0)
        g0grid.addWidget(QLabel('Keep debug unstriped binary'), 4, 1)
        g0grid.addWidget(self.slider6, 5, 0)
        g0grid.addWidget(QLabel('Traced execution outputs'), 5, 1)

        self.slider7, self.slider8 = QSlider(), QSlider()
        self.slider7.setValue(1)
        g0grid.addWidget(self.slider7, 6, 0)
        g0grid.addWidget(QLabel('Remove the build folder'), 6, 1)
        g0grid.addWidget(self.slider8, 7, 0)
        g0grid.addWidget(QLabel('No Python Optimizations'), 7, 1)

        self.slider9, self.slider10 = QSlider(), QSlider()
        g0grid.addWidget(self.slider9, 8, 0)
        g0grid.addWidget(QLabel('No Statements line numbers'), 8, 1)
        g0grid.addWidget(self.slider10, 9, 0)
        g0grid.addWidget(QLabel('Execute the output binary'), 9, 1)

        self.slider11, self.slider12 = QSlider(), QSlider()
        g0grid.addWidget(self.slider11, 10, 0)
        g0grid.addWidget(QLabel('Warning detected implicit exceptions'), 10, 1)
        g0grid.addWidget(self.slider12, 11, 0)
        g0grid.addWidget(QLabel('Keep the PYTHONPATH, do not Reset it'), 11, 1)

        self.slider13 = QSlider()
        g0grid.addWidget(self.slider13, 12, 0)
        g0grid.addWidget(QLabel('Enhance compile, CPython incompatible'), 12, 1)

        self.slider1a, self.slider2a = QSlider(), QSlider()
        g0grid.addWidget(self.slider1a, 0, 2)
        g0grid.addWidget(QLabel('Descendent Recursive Compile'), 0, 3)
        self.slider2a.setValue(1)
        g0grid.addWidget(self.slider2a, 1, 2)
        g0grid.addWidget(QLabel('Force non recursive compile'), 1, 3)

        self.slider3a, self.slider4a = QSlider(), QSlider()
        g0grid.addWidget(self.slider3a, 2, 2)
        g0grid.addWidget(QLabel('STD Lib Recursive Compile'), 2, 3)
        g0grid.addWidget(self.slider4a, 3, 2)
        g0grid.addWidget(QLabel('Enforce the use of Clang'), 3, 3)

        self.slider5a, self.slider6a = QSlider(), QSlider()
        self.slider5a.setValue(1)
        g0grid.addWidget(self.slider5a, 4, 2)
        g0grid.addWidget(QLabel('Use G++ link time optimizations'), 4, 3)
        g0grid.addWidget(self.slider6a, 5, 2)
        g0grid.addWidget(QLabel('Disable the console window'), 5, 3)

        self.slider7a, self.slider8a = QSlider(), QSlider()
        g0grid.addWidget(self.slider7a, 6, 2)
        g0grid.addWidget(QLabel('Force compile for MS Windows'), 6, 3)
        g0grid.addWidget(self.slider8a, 7, 2)
        g0grid.addWidget(QLabel('Use Python Debug versions'), 7, 3)

        self.slider9a, self.slider10a = QSlider(), QSlider()
        self.slider9a.setValue(1)
        g0grid.addWidget(self.slider9a, 8, 2)
        g0grid.addWidget(QLabel('Create standalone executable'), 8, 3)
        g0grid.addWidget(self.slider10a, 9, 2)
        g0grid.addWidget(QLabel('Enable Standalone mode build'), 9, 3)

        self.slider11a, self.slider12a = QSlider(), QSlider()
        g0grid.addWidget(self.slider11a, 10, 2)
        g0grid.addWidget(QLabel('Make module executable instead of app'), 10, 3)
        g0grid.addWidget(self.slider12a, 11, 2)
        g0grid.addWidget(QLabel('No froze module of stdlib as bytecode'), 11, 3)

        self.slider13a = QSlider()
        g0grid.addWidget(self.slider13a, 12, 2)
        g0grid.addWidget(QLabel('Force use of MinGW on MS Windows'), 12, 3)

        for each_widget in (
            self.slider1, self.slider2, self.slider3, self.slider4,
            self.slider5, self.slider6, self.slider7, self.slider8,
            self.slider9, self.slider10, self.slider11, self.slider12,
            self.slider13, self.slider1a, self.slider2a, self.slider3a,
            self.slider4a, self.slider5a, self.slider6a, self.slider7a,
            self.slider8a, self.slider9a, self.slider10a, self.slider11a,
                self.slider12a, self.slider13a):
            each_widget.setRange(0, 1)
            each_widget.setCursor(QCursor(Qt.OpenHandCursor))
            each_widget.setTickInterval(1)
            each_widget.TickPosition(QSlider.TicksBothSides)

        self.combo1 = QComboBox()
        self.combo1.addItems(('2.7', '2.6', '3.2', '3.3'))
        g5vlay.addWidget(QLabel('Python Version'))
        g5vlay.addWidget(self.combo1)
        self.combo2 = QComboBox()
        self.combo2.addItems(('Default', 'Low', 'High'))
        g5vlay.addWidget(QLabel('CPU priority'))
        g5vlay.addWidget(self.combo2)
        self.combo3 = QComboBox()
        self.combo3.addItems(('1', '2', '3', '4', '5', '6', '7', '8', '9'))
        g5vlay.addWidget(QLabel('MultiProcessing Workers'))
        g5vlay.addWidget(self.combo3)

        self.outdir = QLineEdit()
        self.outdir.setStyleSheet("QLineEdit{margin-left:25px}")
        self.clearButton = QToolButton(self.outdir)
        self.clearButton.setIcon(QIcon.fromTheme("edit-clear"))
        self.clearButton.setIconSize(QSize(25, 25))
        self.clearButton.setStyleSheet("QToolButton{border:none}")
        self.clearButton.hide()
        self.clearButton.clicked.connect(self.outdir.clear)
        self.outdir.textChanged.connect(
            lambda: self.clearButton.setVisible(True))
        self.clearButton.clicked.connect(
            lambda: self.clearButton.setVisible(False))
        self.outdir.setPlaceholderText('Output Directory')
        if path.isfile('.nuitka-output-dir.txt'):
            self.outdir.setText(open('.nuitka-output-dir.txt', 'r').read())
        else:
            self.outdir.setText(path.expanduser("~"))
        self.completer, self.dirs = QCompleter(self), QDirModel(self)
        self.dirs.setFilter(QDir.Dirs | QDir.NoDotAndDotDot)
        self.completer.setModel(self.dirs)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.completer.setCompletionMode(QCompleter.PopupCompletion)
        self.completer.popup().setStyleSheet(
            """border:1px solid #4a4a4a;background:grey;
            selection-background-color:cyan;selection-color:#000""")
        self.completer.popup().setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.outdir.setCompleter(self.completer)

        self.btn1 = QPushButton(QIcon.fromTheme("document-open"),
                                'Open' if IS_WIN else '')
        self.btn1.clicked.connect(
            lambda: open('.nuitka-output-dir.txt', 'w').write(str(
                QFileDialog.getExistingDirectory(None, 'Open Output Directory',
                                                 path.expanduser("~")))))
        self.btn1.released.connect(lambda: self.outdir.setText(
            open('.nuitka-output-dir.txt', 'r').read()))
        g1vlay.addWidget(QLabel('Output Directory'))
        g1vlay.addWidget(self.outdir)
        g1vlay.addWidget(self.btn1)

        self.target = QLineEdit()
        self.target.setStyleSheet("QLineEdit{margin-left:25px}")
        self.clearButton2 = QToolButton(self.target)
        self.clearButton2.setIcon(QIcon.fromTheme("edit-clear"))
        self.clearButton2.setIconSize(QSize(25, 25))
        self.clearButton2.setStyleSheet("QToolButton{border:none}")
        self.clearButton2.hide()
        self.clearButton2.clicked.connect(self.target.clear)
        self.target.textChanged.connect(
            lambda: self.clearButton2.setVisible(True))
        self.clearButton2.clicked.connect(
            lambda: self.clearButton2.setVisible(False))
        self.target.setPlaceholderText('Target Python App to Binary Compile')
        self.target.setCompleter(self.completer)
        self.btn2 = QPushButton(QIcon.fromTheme("document-open"),
                                'Open' if IS_WIN else '')
        self.btn2.clicked.connect(lambda: self.target.setText(str(
            QFileDialog.getOpenFileName(
                None, "Open", path.expanduser("~"),
                ';;'.join(['{}(*.{})'.format(e.upper(), e)
                           for e in ('py', 'pyw', '*')])))))
        g1vlay.addWidget(QLabel('Input File'))
        g1vlay.addWidget(self.target)
        g1vlay.addWidget(self.btn2)

        self.icon, self.icon_label = QLineEdit(), QLabel('Icon File')
        self.icon.setStyleSheet("QLineEdit{margin-left:25px}")
        self.clearButton3 = QToolButton(self.icon)
        self.clearButton3.setIcon(QIcon.fromTheme("edit-clear"))
        self.clearButton3.setIconSize(QSize(25, 25))
        self.clearButton3.setStyleSheet("QToolButton{border:none}")
        self.clearButton3.hide()
        self.clearButton3.clicked.connect(self.icon.clear)
        self.icon.textChanged.connect(
            lambda: self.clearButton3.setVisible(True))
        self.clearButton3.clicked.connect(
            lambda: self.clearButton3.setVisible(False))
        self.icon.setPlaceholderText('Path to Icon file for your App')
        self.icon.setCompleter(self.completer)
        self.btn3 = QPushButton(QIcon.fromTheme("document-open"),
                                'Open' if IS_WIN else '')
        self.btn3.clicked.connect(lambda: self.icon.setText(str(
            QFileDialog.getOpenFileName(
                None, "Open", path.expanduser("~"),
                ';;'.join(['{}(*.{})'.format(e.upper(), e)
                           for e in ('ico', 'png', 'bmp', 'svg', '*')])))))
        g1vlay.addWidget(self.icon_label)
        g1vlay.addWidget(self.icon)
        g1vlay.addWidget(self.btn3)

        # Menu Bar inicialization and detail definitions
        menu_salir = QAction(QIcon.fromTheme("application-exit"), 'Quit', self)
        menu_salir.setStatusTip('Quit')
        menu_salir.triggered.connect(exit)
        menu_minimize = QAction(QIcon.fromTheme("go-down"), 'Minimize', self)
        menu_minimize.setStatusTip('Minimize')
        menu_minimize.triggered.connect(lambda: self.showMinimized())
        menu_qt = QAction(QIcon.fromTheme("help-about"), 'About Qt', self)
        menu_qt.setStatusTip('About Qt...')
        menu_qt.triggered.connect(lambda: QMessageBox.aboutQt(self))
        menu_dev = QAction(QIcon.fromTheme("applications-development"),
                           'Developer Manual PDF', self)
        menu_dev.setStatusTip('Open Nuitka Developer Manual PDF...')
        menu_dev.triggered.connect(
            lambda: call(OPEN + '/usr/share/doc/nuitka/Developer_Manual.pdf.gz',
                         shell=True))
        menu_usr = QAction(QIcon.fromTheme("help-contents"), 'User Docs', self)
        menu_usr.setStatusTip('Open Nuitka End User Manual PDF...')
        menu_usr.triggered.connect(
            lambda: call(OPEN + '/usr/share/doc/nuitka/README.pdf.gz',
                         shell=True))
        menu_odoc = QAction(QIcon.fromTheme("help-browser"), 'OnLine Doc', self)
        menu_odoc.setStatusTip('Open Nuitka on line Documentation pages...')
        menu_odoc.triggered.connect(
            lambda: open_new_tab('http://nuitka.net/doc/user-manual.html'))
        menu_man = QAction(QIcon.fromTheme("utilities-terminal"), 'Man', self)
        menu_man.setStatusTip('Open Nuitka technical command line Man Pages..')
        menu_man.triggered.connect(
            lambda: call('xterm -e "man nuitka"', shell=True))
        menu_tra = QAction(QIcon.fromTheme("applications-development"),
                           'View Nuitka-GUI Source Code', self)
        menu_tra.setStatusTip('View, study, edit Nuitka-GUI Libre Source Code')
        menu_tra.triggered.connect(lambda: call(OPEN + __file__, shell=True))
        menu_foo = QAction(QIcon.fromTheme("folder"), 'Open Output Dir', self)
        menu_foo.setStatusTip('Open the actual Output Directory location...')
        menu_foo.triggered.connect(
            lambda: call(OPEN + str(self.outdir.text()), shell=True))
        menu_pic = QAction(QIcon.fromTheme("camera-photo"), 'Screenshot', self)
        menu_pic.setStatusTip('Take a Screenshot for Documentation purposes..')
        menu_pic.triggered.connect(
            lambda: QPixmap.grabWindow(QApplication.desktop().winId()).save(
                QFileDialog.getSaveFileName(None, "Save", path.expanduser("~"),
                                            'PNG(*.png)', 'png')))
        menu_don = QAction(QIcon.fromTheme("emblem-favorite"),
                           'Help Nuitka', self)
        menu_don.setStatusTip('Help the Nuitka Open Source Libre Free Project')
        menu_don.triggered.connect(
            lambda: open_new_tab('http://nuitka.net/pages/donations.html'))

        # movable draggable toolbar
        self.toolbar = QToolBar(self)
        self.toolbar.setIconSize(QSize(16, 16))
        self.toolbar.toggleViewAction().setText("Show/Hide Toolbar")
        l_spacer, r_spacer = QWidget(self), QWidget(self)
        l_spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        r_spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.toolbar.addWidget(l_spacer)
        self.toolbar.addSeparator()
        self.toolbar.addActions((menu_salir, menu_minimize, menu_qt,
                                 menu_odoc, menu_foo, menu_pic, menu_don))
        if not IS_WIN:
            self.toolbar.addActions((menu_man, menu_dev, menu_tra, menu_usr))
        self.toolbar.addSeparator()
        self.toolbar.addWidget(r_spacer)
        self.addToolBar(Qt.BottomToolBarArea, self.toolbar)

        # Bottom Buttons Bar
        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setStandardButtons(
            QDialogButtonBox.Ok | QDialogButtonBox.Close)
        self.buttonBox.rejected.connect(exit)
        self.buttonBox.accepted.connect(self.run)

        self.guimode = QComboBox()
        self.guimode.addItems(('Full UX / UI', 'Simple UX / UI'))
        self.guimode.setStyleSheet("""QComboBox{background:transparent;border:0;
            margin-left:25px;color:gray;text-decoration:underline}""")
        self.guimode.currentIndexChanged.connect(self.set_guimode)

        container = QWidget()
        container_layout = QGridLayout(container)  # Y, X
        container_layout.addWidget(self.guimode, 0, 1)
        container_layout.addWidget(self.group2, 1, 0)
        container_layout.addWidget(self.group3, 2, 0)
        container_layout.addWidget(self.group0, 1, 1)
        container_layout.addWidget(self.group1, 2, 1)
        container_layout.addWidget(self.group4, 1, 2)
        container_layout.addWidget(self.group5, 2, 2)
        container_layout.addWidget(self.buttonBox, 3, 1)
        self.setCentralWidget(container)
        # Paleta de colores para pintar transparente
        if not A11Y:
            palette = self.palette()
            palette.setBrush(QPalette.Base, Qt.transparent)
            self.setPalette(palette)
            self.setAttribute(Qt.WA_OpaquePaintEvent, False)

    def get_fake_tree(self, target):
        """Return the fake tree."""
        try:
            fake_tree = check_output(NUITKA + ' --dump-xml ' + target,
                                     shell=True)
        except:
            fake_tree = "ERROR: Failed to get Tree Dump."
        finally:
            return fake_tree.strip()

    def run(self):
        ' run the actual backend process '
        self.treeview_nodes.clear()
        self.textedit_source.clear()
        self.output.clear()
        self.statusBar().showMessage('WAIT!, Working...')
        target = str(self.target.text()).strip()
        self.treeview_nodes.setText(self.get_fake_tree(target))
        self.textedit_source.setText(open(target, "r").read().strip())
        conditional_1 = sys.platform.startswith('linux')
        conditional_2 = self.combo3.currentIndex() != 2
        command_to_run_nuitka = " ".join((
            'chrt -i 0' if conditional_1 and conditional_2 else '', NUITKA,
            '--debug' if self.slider1.value() else '',
            '--verbose' if self.slider2.value() else '',
            '--show-progress' if self.slider3.value() else '',
            '--show-scons --show-modules' if self.slider4.value() else '',
            '--unstriped' if self.slider5.value() else '',
            '--trace-execution' if self.slider6.value() else '',
            '--remove-output' if self.slider7.value() else '',
            '--no-optimization' if self.slider8.value() else '',
            '--code-gen-no-statement-lines' if self.slider9.value() else '',
            '--execute' if self.slider10.value() else '',
            '--recurse-all' if self.slider1a.value() else '',
            '--recurse-none' if self.slider2a.value() else '',
            '--recurse-stdlib' if self.slider3a.value() else '',
            '--clang' if self.slider4a.value() else '',
            '--lto' if self.slider5a.value() else '',
            '--windows-disable-console' if self.slider6a.value() else '',
            '--windows-target' if self.slider7a.value() else '',
            '--python-debug' if self.slider8a.value() else '',
            '--exe' if self.slider9a.value() else '',
            '--standalone' if self.slider10a.value() else '',
            '--module' if self.slider11a.value() else '',
            '--nofreeze-stdlib' if self.slider12a.value() else '',
            '--mingw' if self.slider13a.value() else '',
            '--warn-implicit-exceptions' if self.slider11.value() else '',
            '--execute-with-pythonpath' if self.slider12.value() else '',
            '--enhanced' if self.slider13.value() else '',
            '--icon="{}"'.format(self.icon.text()) if self.icon.text() else '',
            '--python-version={}'.format(self.combo1.currentText()),
            '--jobs={}'.format(self.combo3.currentText()),
            '--output-dir="{}"'.format(self.outdir.text()), "{}".format(target)
            ))
        if DEBUG:
            print(command_to_run_nuitka)
        self.process.start(command_to_run_nuitka)
        if not self.process.waitForStarted() and not IS_WIN:
            return  # ERROR !
        self.statusBar().showMessage(__doc__.title())

    def _process_finished(self):
        """finished sucessfully"""
        self.output.setFocus()
        self.output.selectAll()

    def read_output(self):
        """Read and append output to the log"""
        self.output.append(str(self.process.readAllStandardOutput()))

    def read_errors(self):
        """Read and append errors to the log"""
        self.output.append(str(self.process.readAllStandardError()))

    def paintEvent(self, event):
        """Paint semi-transparent background,animated pattern,background text"""
        if not A11Y:
            p = QPainter(self)
            p.setRenderHint(QPainter.Antialiasing)
            p.setRenderHint(QPainter.TextAntialiasing)
            p.setRenderHint(QPainter.HighQualityAntialiasing)
            p.fillRect(event.rect(), Qt.transparent)
            # animated random dots background pattern
            for i in range(4096):
                x = randint(25, self.size().width() - 25)
                y = randint(25, self.size().height() - 25)
                # p.setPen(QPen(QColor(randint(9, 255), 255, 255), 1))
                p.drawPoint(x, y)
            p.setPen(QPen(Qt.white, 1))
            p.rotate(40)
            p.setFont(QFont('Ubuntu', 250))
            p.drawText(200, 99, "Nuitka")
            p.rotate(-40)
            p.setPen(Qt.NoPen)
            p.setBrush(QColor(0, 0, 0))
            p.setOpacity(0.8)
            p.drawRoundedRect(self.rect(), 9, 9)
            p.end()

    def set_guimode(self):
        """Switch between simple and full UX"""
        for widget in (
            self.group2, self.group3, self.group4, self.group5, self.icon,
                self.icon_label, self.btn3, self.toolbar, self.statusBar()):
            widget.hide() if self.guimode.currentIndex() else widget.show()


###############################################################################


def main():
    ' Main Loop '
    global A11Y
    app = QApplication(sys.argv)
    app.setApplicationName(__doc__.strip().lower())
    app.setOrganizationName("Nuitka")
    app.setOrganizationDomain("Nuitka")
    try:
        opts, args = getopt(sys.argv[1:], 'hv', ('version', 'help', 'a11y'))
    except:
        pass
    for o, v in opts:
        if o in ('-h', '--help'):
            print(''' Usage:
                  --a11y            Use Accessibility theme and settings.
                  -h, --help        Show help informations and exit.
                  -v, --version     Show version information and exit.''')
            return sys.exit(1)
        elif o in ('-v', '--version'):
            print(__version__)
            return sys.exit(1)
        elif o in ('--a11y', ):
            A11Y = True
    w = MyMainWindow()
    if not A11Y:
        app.setStyle('Windows')
        w.setAttribute(Qt.WA_TranslucentBackground, True)
    w.show()
    sys.exit(app.exec_())


if __name__ in '__main__':
    main()
