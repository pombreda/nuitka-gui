#!/usr/bin/env python
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
__url__ = 'nuitka.net'
__date__ = '2014/05'
__prj__ = 'nuitka_gui'
__docformat__ = 'html'


# imports
from subprocess import check_output
import sys
from getopt import getopt
from os import path
from random import randint
from webbrowser import open_new_tab
from getpass import getuser

from PyQt4.QtCore import QDir, QSize, Qt, QProcess
from PyQt4.QtGui import (QAction, QApplication, QColor, QComboBox, QCompleter,
                         QCursor, QDialogButtonBox, QDirModel, QFileDialog,
                         QFont, QGridLayout, QGroupBox, QIcon, QLabel,
                         QLineEdit, QMainWindow, QMessageBox, QPainter,
                         QPalette, QPen, QPixmap, QPushButton, QSizePolicy,
                         QSlider, QTextOption, QToolBar, QToolButton, QWidget,
                         QVBoxLayout)
try:
    from PyKDE4.kdeui import KTextEdit as QTextEdit
except ImportError:
    from PyQt4.QtGui import QTextEdit  # lint:ok


# constants
DEBUG = False


###############################################################################


class MyMainWindow(QMainWindow):
    ' Main Window '
    def __init__(self, parent=None):
        ' Initialize QWidget inside MyMainWindow '
        super(MyMainWindow, self).__init__(parent)
        self.statusBar().showMessage("We are ready " + getuser().capitalize())
        self.setWindowTitle(__doc__)
        self.setMinimumSize(600, 800)
        self.setMaximumSize(2048, 1024)
        self.resize(1024, 800)
        self.setWindowIcon(QIcon.fromTheme("face-monkey"))
        self.setStyleSheet('''QWidget { color: #fff;/*background-color:#323232*/
            font-family: 'Ubuntu Light'; font-size: 14px
            }
            QWidget:item:hover {
                background-color: QLinearGradient(x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #ffa02f, stop: 1 #ca0619); color: #000
            }
            QWidget:item:selected {
                background-color: QLinearGradient(x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #ffa02f, stop: 1 #d7801a)
            }
            QWidget:disabled { color: #404040; background-color: #323232 }
            QWidget:focus {
                background-image: None;
                border: 2px solid QLinearGradient(x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #ffa02f, stop: 1 #d7801a)
            }
            QPushButton {
                background-color: QLinearGradient(spread:pad, x1:0, y1:0, x2:1,
                    y2:0.27, stop:0 rgba(99, 99, 99, 250), stop:1 #1e1e1e);
                padding: 3px; border: 1px solid #1e1e1e; border-radius: 10px;
                margin: 0; border-width: 1px; font-size: 12px;
                padding-left: 5px; padding-right: 5px
            }
            QLineEdit, QTextEdit {
                background-color: QLinearGradient(spread:pad, x1:0, y1:0, x2:1,
                    y2:0.27, stop:0 #000, stop:1 #1e1e1e);
                padding: 3px; border: 1px solid #1e1e1e; border-radius: 10px;
                margin: 0; font-size: 12px; padding-left: 5px;
                padding-right: 5px
            }
            QPushButton:pressed {
                background-color: QLinearGradient(x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #2d2d2d, stop: 0.1 #2b2b2b, stop: 0.5 #292929,
                    stop: 0.9 #282828, stop: 1 #252525)
            }
            QComboBox {
                background-color: QLinearGradient(spread:pad, x1:0, y1:0, x2:1,
                    y2:0.273, stop:0 rgba(99, 99, 99, 250), stop:1 #1e1e1e);
                padding: 3px; border: 3px solid #1e1e1e; border-radius: 15px;
                margin: 0
            }
            QComboBox:hover, QPushButton:hover {
                border: 1px solid QLinearGradient(x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #ffa02f, stop: 1 #d7801a)
            }
            QComboBox QAbstractItemView {
                border: 1px solid darkgray; background:grey;
                selection-background-color: QLinearGradient(x1: 0, y1: 0,
                    x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #d7801a);
            }
            QComboBox::drop-down {
                 subcontrol-origin: padding; subcontrol-position: top right;
                 width: 0; height: 0; border-left-width: 0; opacity: 0;
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
                    y2:0.273, stop:0 rgba(0, 0, 0, 255),
                    stop:1 rgba(150, 255, 255, 255));
                height: 5px; border: 1px dotted #fff; text-align: center;
                border-top-left-radius: 2px; border-bottom-left-radius: 2px;
                border-top-right-radius: 2px; border-bottom-right-radius 2px;
                margin-left: 2px; margin-right: 2px;
            }
            QSlider::handle:vertical:hover {
                border: 2px solid #ffaa00; margin-left: 2px; margin-right: 2px;
            }
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
                background-color: QLinearGradient(spread:pad, x1:0, y1:0, x2:1,
                    y2:0.27, stop:0 rgba(0, 0, 0, 255),
                    stop:1 rgba(150, 255, 255, 255));
                border: 1px solid grey; border-radius: 9px; width: 19px;
                height: 19px; margin: 0.5px
            }
            QGroupBox {
                border: 1px solid gray; border-radius: 9px; padding-top: 9px;
            }''')

        self.process = QProcess()
        self.process.readyReadStandardOutput.connect(self.read_output)
        self.process.readyReadStandardError.connect(self.read_errors)
        self.process.finished.connect(self._process_finished)
        self.process.error.connect(self._process_finished)

        group0, group1 = QGroupBox("Options"), QGroupBox("Paths")
        group2, group3 = QGroupBox("Nodes Tree"), QGroupBox("Python Code")
        group4, group5 = QGroupBox("Logs"), QGroupBox("Info")
        g0grid, g1vlay = QGridLayout(group0), QVBoxLayout(group1)

        self.treeview_nodes, self.textedit_source = QTextEdit(), QTextEdit()
        self.output = QTextEdit()
        self.treeview_nodes.setAutoFormatting(QTextEdit.AutoAll)
        self.treeview_nodes.setWordWrapMode(QTextOption.NoWrap)
        QVBoxLayout(group2).addWidget(self.treeview_nodes)
        QVBoxLayout(group3).addWidget(self.textedit_source)
        QVBoxLayout(group4).addWidget(self.output)

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

        self.slider9a = QSlider()
        self.slider9a.setValue(1)
        g0grid.addWidget(self.slider9a, 8, 2)
        g0grid.addWidget(QLabel('Create standalone executable'), 8, 3)

        self.combo1 = QComboBox()
        self.combo1.addItems(('2', '3'))
        g0grid.addWidget(self.combo1, 10, 2)
        g0grid.addWidget(QLabel('Python interpreter version'), 10, 3)
        self.combo2 = QComboBox()
        self.combo2.addItems(('20', '0', '10', '15', '-5', '-10', '-15', '-20'))
        g0grid.addWidget(self.combo2, 9, 2)
        g0grid.addWidget(QLabel('Backend Nice CPU priority'), 9, 3)
        self.combo3 = QComboBox()
        self.combo3.addItems(('1', '2', '3', '4', '5', '6', '7', '8', '9'))
        g0grid.addWidget(self.combo3, 10, 0)
        g0grid.addWidget(QLabel('MultiProcessing Workers'), 10, 1)

        for each_widget in (
            self.slider1, self.slider2, self.slider3, self.slider4,
            self.slider5, self.slider6, self.slider7, self.slider8,
            self.slider9, self.slider10, self.slider1a, self.slider2a,
            self.slider3a, self.slider4a, self.slider5a, self.slider6a,
                self.slider7a, self.slider8a, self.slider9a):
            each_widget.setRange(0, 1)
            each_widget.setCursor(QCursor(Qt.OpenHandCursor))
            each_widget.setTickInterval(1)
            each_widget.TickPosition(QSlider.TicksBothSides)

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
        self.outdir.setCompleter(self.completer)

        self.btn1 = QPushButton(QIcon.fromTheme("document-open"), '')
        self.btn1.clicked.connect(
            lambda: open('.nuitka-output-dir.txt', 'w').write(str(
                QFileDialog.getExistingDirectory(self, 'Open Output Directory',
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
            lambda: self.clearButton.setVisible(False))
        self.target.setPlaceholderText('Target Python App to Binary Compile')
        self.target.setCompleter(self.completer)
        self.btn2 = QPushButton(QIcon.fromTheme("document-open"), '')
        self.btn2.clicked.connect(lambda: self.target.setText(str(
            QFileDialog.getOpenFileName(
                self, "Open", path.expanduser("~"),
                ';;'.join(['{}(*.{})'.format(e.upper(), e)
                           for e in ('py', 'pyw', '*')])))))
        g1vlay.addWidget(QLabel('Input File'))
        g1vlay.addWidget(self.target)
        g1vlay.addWidget(self.btn2)

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
            lambda: subprocess.call(
                'xdg-open /usr/share/doc/nuitka/Developer_Manual.pdf.gz',
                shell=True))
        menu_usr = QAction(QIcon.fromTheme("help-contents"), 'User Docs', self)
        menu_usr.setStatusTip('Open Nuitka End User Manual PDF...')
        menu_usr.triggered.connect(
            lambda: subprocess.call(
                'nice -n 19 xdg-open /usr/share/doc/nuitka/README.pdf.gz',
                shell=True))
        menu_odoc = QAction(QIcon.fromTheme("help-browser"), 'OnLine Doc', self)
        menu_odoc.setStatusTip('Open Nuitka on line Documentation pages...')
        menu_odoc.triggered.connect(lambda:
                                    open_new_tab('http://nuitka.net/doc'))
        menu_man = QAction(QIcon.fromTheme("utilities-terminal"), 'Man', self)
        menu_man.setStatusTip('Open Nuitka technical command line Man Pages..')
        menu_man.triggered.connect(lambda: system('xterm -e "man nuitka"'))
        menu_tra = QAction(QIcon.fromTheme("applications-development"),
                           'View Nuitka-GUI Source Code', self)
        menu_tra.setStatusTip('View, study, edit Nuitka-GUI Libre Source Code')
        menu_tra.triggered.connect(lambda: system('xdg-open ' + __file__))
        menu_foo = QAction(QIcon.fromTheme("folder"), 'Open Output Dir', self)
        menu_foo.setStatusTip('Open the actual Output Directory location...')
        menu_foo.triggered.connect(lambda: system('xdg-open ' +
                                   str(self.outdir.text())))
        menu_pic = QAction(QIcon.fromTheme("camera-photo"), 'Screenshot', self)
        menu_pic.setStatusTip('Take a Screenshot for Documentation purposes..')
        menu_pic.triggered.connect(
            lambda: QPixmap.grabWindow(QApplication.desktop().winId()).save(
                QFileDialog.getSaveFileName(self, "Save", path.expanduser("~"),
                                            'PNG(*.png)', 'png')))

        # movable draggable toolbar
        self.toolbar = QToolBar(self)
        self.toolbar.setIconSize(QSize(16, 16))
        l_spacer, r_spacer = QWidget(self), QWidget(self)
        l_spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        r_spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.toolbar.addWidget(l_spacer)
        self.toolbar.addSeparator()
        self.toolbar.addActions((
            menu_salir, menu_minimize, menu_qt, menu_man, menu_dev, menu_tra,
            menu_odoc, menu_usr, menu_foo, menu_pic))
        self.toolbar.addSeparator()
        self.toolbar.addWidget(r_spacer)
        self.addToolBar(Qt.BottomToolBarArea, self.toolbar)

        # Bottom Buttons Bar
        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setStandardButtons(
            QDialogButtonBox.Ok | QDialogButtonBox.Close)
        self.buttonBox.rejected.connect(exit)
        self.buttonBox.accepted.connect(self.run)

        container = QWidget()
        container_layout = QGridLayout(container)  # Y, X
        container_layout.addWidget(QLabel("<center><b>" + __doc__), 0, 1)
        container_layout.addWidget(group2, 1, 0)
        container_layout.addWidget(group3, 2, 0)
        container_layout.addWidget(group0, 1, 1)
        container_layout.addWidget(group1, 2, 1)
        container_layout.addWidget(group4, 1, 2)
        container_layout.addWidget(group5, 2, 2)
        container_layout.addWidget(self.buttonBox, 3, 2)
        self.setCentralWidget(container)
        # Paleta de colores para pintar transparente
        palette = self.palette()
        palette.setBrush(QPalette.Base, Qt.transparent)
        self.setPalette(palette)
        self.setAttribute(Qt.WA_OpaquePaintEvent, False)

    def run(self):
        ' run the actual backend process '
        self.treeview_nodes.clear()
        self.textedit_source.clear()
        self.output.clear()
        self.statusBar().showMessage('Working...')
        target = str(self.target.text()).strip()
        fake_tree = check_output('nuitka --dump-tree ' + target, shell=True)
        self.treeview_nodes.setText(fake_tree.strip())
        self.textedit_source.setText(open(target, "r").read().strip())
        self.output.append('Working on ' + target)

        # Parse Value of Slider1 as the Debug flag parameter
        if self.slider1.value() == 0:
            arg1 = ''
        else:
            arg1 = '--debug '
        # Parse Value of Slider2 as the verbose flag parameter
        if self.slider2.value() == 0:
            arg2 = ''
        else:
            arg2 = '--verbose '
        # Parse Value of Slider3 as the show progress flag parameter
        if self.slider3.value() == 0:
            arg3 = ''
        else:
            arg3 = '--show-progress '
        # Parse Value of Slider4 as the show scons flag parameter
        if self.slider4.value() == 0:
            arg4 = ''
        else:
            arg4 = '--show-scons '
        # Parse Value of Slider4 as the unstripped flag parameter
        if self.slider5.value() == 0:
            arg5 = ''
        else:
            arg5 = '--unstriped '
        # Parse Value of Slider5 as the trace executions flag parameter
        if self.slider6.value() == 0:
            arg6 = ''
        else:
            arg6 = '--trace-execution '
        # Parse Value of Slider5 as the remove output flag parameter
        if self.slider7.value() == 0:
            arg7 = ''
        else:
            arg7 = '--remove-output '
        # Parse Value of Slider5 as the no optimiztions flag parameter
        if self.slider8.value() == 0:
            arg8 = ''
        else:
            arg8 = '--no-optimization '
        # Parse Value of Slider5 as the no statement lines flag parameter
        if self.slider9.value() == 0:
            arg9 = ''
        else:
            arg9 = '--code-gen-no-statement-lines '
        # Parse Value of Slider5 as the execute flag parameter
        if self.slider10.value() == 0:
            arg10 = ''
        else:
            arg10 = '--execute '
        # Parse Value of Slider5 as the recurse all flag parameter
        if self.slider1a.value() == 0:
            arg1a = ''
        else:
            arg1a = '--recurse-all '
        # Parse Value of Slider5 as the recurse none flag parameter
        if self.slider2a.value() == 0:
            arg2a = ''
        else:
            arg2a = '--recurse-none '
        # Parse Value of Slider5 as the recurse std libs flag parameter
        if self.slider3a.value() == 0:
            arg3a = ''
        else:
            arg3a = '--recurse-stdlib '
        # Parse Value of Slider5 as the clangs flag parameter
        if self.slider4a.value() == 0:
            arg4a = ''
        else:
            arg4a = '--clang '
        # Parse Value of Slider5 as the lto flag parameter
        if self.slider5a.value() == 0:
            arg5a = ''
        else:
            arg5a = '--lto '
        # Parse Value of Slider5 as the windows disable console flag parameter
        if self.slider6a.value() == 0:
            arg6a = ''
        else:
            arg6a = '--windows-disable-console '
        # Parse Value of Slider5 as the windows targets flag parameter
        if self.slider7a.value() == 0:
            arg7a = ''
        else:
            arg7a = '--windows-target '
        # Parse Value of Slider5 as the python debug flag parameter
        if self.slider8a.value() == 0:
            arg8a = ''
        else:
            arg8a = '--python-debug '
        # Parse Value of Slider5 as the exe flag parameter
        if self.slider9a.value() == 0:
            arg9a = ''
        else:
            arg9a = '--exe '
        # parse value of combo 1 as the python version
        if self.combo1.currentText() == 2:
            pyv = '2.7'
        else:
            pyv = '3.2'
        # run the subprocesses
        command_to_run_nuitka = ('nice --adjustment=' +
         str(self.combo2.currentText()).lower().strip() + ' nuitka ' +
         arg1 + arg2 + arg3 + arg4 + arg5 + arg6 + arg7 + arg8 + arg9 + arg10 +
         arg1a + arg2a + arg3a + arg4a + arg5a + arg6a + arg7a + arg8a +
         arg9a +
            '--jobs=' + str(self.combo3.currentText()).lower().strip() + ' ' +
            '--python-version="' + pyv +
            '" ' +
            '--output-dir=' + str(self.outdir.text()).lower().strip() +
            ' ' + target +
            ' && mv --verbose ' +
            str(self.outdir.text()).lower().strip() + '/' +
            str(target).replace('.py', '.exe ').split('/')[-1] +
            str(self.outdir.text()).lower().strip() + '/' +
            str(target).split('.')[0].split('/')[-1] +
            ' ; nice -n 19  notify-send "[Nuitka-GUI]" "Python Compile Done."')
        if DEBUG:
            print(command_to_run_nuitka)
        #self.process.start(command_to_run_nuitka)
        #if not self.process.waitForStarted():
            #return  # ERROR

    def _process_finished(self):
        """finished sucessfully"""
        self.output.setFocus()
        self.output.selectAll()

    def read_output(self):
        """Read and append output to the log"""
        self.output.append(self.process.readAllStandardOutput())

    def read_errors(self):
        """Read and append errors to the log"""
        self.output.append(self.process.readAllStandardError())

    def paintEvent(self, event):
        """Paint semi-transparent background,animated pattern,background text"""
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        p.setRenderHint(QPainter.TextAntialiasing)
        p.setRenderHint(QPainter.HighQualityAntialiasing)
        p.fillRect(event.rect(), Qt.transparent)
        # animated random dots background pattern
        for i in range(4096):
            x = randint(25, self.size().width() - 25)
            y = randint(25, self.size().height() - 25)
            # p.setPen(QPen(QColor(random.randint(9, 255), 255, 255), 1))
            p.drawPoint(x, y)
        p.setPen(QPen(Qt.white, 1))
        p.rotate(40)
        p.setFont(QFont('Ubuntu', 250))
        p.drawText(200, 99, "Nuitka")
        p.rotate(-40)
        p.setPen(Qt.NoPen)
        p.setBrush(QColor(0, 0, 0))
        p.setOpacity(0.8)
        p.drawRoundedRect(self.rect(), 100, 50)
        p.end()


###############################################################################


def main():
    ' Main Loop '
    app, w = QApplication(sys.argv), MyMainWindow()
    app.setStyle('Windows')
    try:
        opts, args = getopt(sys.argv[1:], 'hv', ('version', 'help'))
    except:
        pass
    for o, v in opts:
        if o in ('-h', '--help'):
            print(''' Usage:
                  -h, --help        Show help informations and exit.
                  -v, --version     Show version information and exit.''')
            return sys.exit(1)
        elif o in ('-v', '--version'):
            print(__version__)
            return sys.exit(1)
    w.setAttribute(Qt.WA_TranslucentBackground, True)
    w.show()
    sys.exit(app.exec_())


if __name__ in '__main__':
    main()
