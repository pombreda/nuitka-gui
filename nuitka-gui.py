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
#


# metadata
' Python Nuitka-GUI '
__version__ = ' 0.8 '
__license__ = ' Apache '
__author__ = ' juancarlospaco '
__email__ = ' juancarlospaco@ubuntu.com '
__url__ = 'nuitka.net'
__date__ = '2013/03/10'
__prj__ = 'nuitka_gui'
__docformat__ = 'html'
__source__ = ''


# imports
import sys
import os
import datetime
import subprocess
import webbrowser
import random
try:
    from PyQt4.QtCore import *
    from PyQt4.QtGui import *
    from PyQt4 import QtCore
    from PyQt4 import QtGui
except ImportError:
    exit(" ERROR: No Qt4 avaliable!\n (sudo apt-get install python-qt4)")


# constants
DEBUG = False


print(('#' * 80))
print((__doc__ + ',v.' + __version__ + '(' + __license__ + '), ' + __author__))
print((' INFO: Starting ' + str(datetime.datetime.now())))


###############################################################################


class FaderWidget(QWidget):
    ' Custom Widget class for progressive fade-in and fade-out effects '
    def __init__(self, old_widget, new_widget):
        ' init the fade widget '
        QWidget.__init__(self, new_widget)
        self.old_pixmap = QPixmap(new_widget.size())
        old_widget.render(self.old_pixmap)
        self.pixmap_opacity = 1.0
        self.timeline = QTimeLine()
        self.timeline.valueChanged.connect(self.animate)
        self.timeline.finished.connect(self.close)
        self.timeline.setDuration(4000)
        self.timeline.start()
        self.resize(new_widget.size())
        self.show()

    def paintEvent(self, event):
        ' we use QPainter for the magics '
        painter = QPainter()
        painter.begin(self)
        painter.setOpacity(self.pixmap_opacity)
        painter.drawPixmap(0, 0, self.old_pixmap)
        painter.end()

    def animate(self, value):
        ' simple animations '
        self.pixmap_opacity = 1.0 - value
        self.repaint()


class StackedWidget(QStackedWidget):
    ' traditional QStackedWidget but with the FaderWidget class wrapped in '
    def __init__(self, parent=None):
        ' init the stacked widget '
        QStackedWidget.__init__(self, parent)

    def setCurrentIndex(self, index):
        ' set the current index of the stack '
        self.fader_widget = FaderWidget(self.currentWidget(),
                                        self.widget(index))
        QStackedWidget.setCurrentIndex(self, index)

    def setPage1(self):
        ' go to page 1 '
        self.setCurrentIndex(0)

    def setPage2(self):
        ' go to page 2 '
        self.setCurrentIndex(1)
        # more pages can be added below


###############################################################################


class MyMainWindow(QMainWindow):
    ' Main Window '
    def __init__(self, parent=None):
        ' Initialize QWidget inside MyMainWindow '
        super(MyMainWindow, self).__init__(parent)
        QWidget.__init__(self)
        try:
            self.statusBar().showMessage(
                'Nuitka-GUI the Python 3 Binary Compiler and Node Inspector ' +
                subprocess.check_output('nuitka --version', shell=True))
            self.setToolTip(' Nuitka-GUI Python Binary Compiler ' +
                subprocess.check_output('nuitka --version', shell=True).strip()
                )
        except:
            print('\n WARNING: Backend Error: Cant find Nuitka executable! \n')
            self.statusBar().showMessage(__doc__)

        # Main Window initial Geometry
        self.resize(600, 800)

        # Main Window initial Title
        self.setWindowTitle(__doc__)

        # Main Window Minimum Size
        self.setMinimumSize(600, 800)

        # Main Window Maximum Size
        self.setMaximumSize(640, 800)

        # Main Window initial Font type
        self.setFont(QtGui.QFont('Ubuntu Light', 10))

        # Set Window Icon, if find on filesystem or default to a STD one
        self.setWindowIcon(QtGui.QIcon.fromTheme("face-monkey"))

        # QSS Pre-Processor
        # instead of Static StyleSheet, this allow timed dynamic changing style
        qsstimer = QtCore.QTimer(self)
        qsstimer.start(1000)
        qsstimer.timeout.connect(
            lambda: self.setStyleSheet(' QWidget { color: rgba( ' +
            str(datetime.datetime.now().second * 4) +
            ''', 255, 255, 255 ) ;
            /*background-color: #323232;*/
            font-family: 'Ubuntu Light';
            font-size: 14px;
            }

            QWidget:item:hover {
                background-color: QLinearGradient(
                    x1: 0, y1: 0,
                    x2: 0, y2: 1,
                    stop: 0 #ffa02f,
                    stop: 1 #ca0619
                );
                color: #000000;
            }

            QWidget:item:selected {
                background-color: QLinearGradient(
                    x1: 0, y1: 0,
                    x2: 0, y2: 1,
                    stop: 0 #ffa02f,
                    stop: 1 #d7801a
                );
            }

            QWidget:disabled {
                color: #404040;
                background-color: #323232;
            }

            QWidget:focus {
                background-image: None;
                border: 2px solid QLinearGradient(
                    x1: 0, y1: 0,
                    x2: 0, y2: 1,
                    stop: 0 #ffa02f,
                    stop: 1 #d7801a
                );
            }

            QPushButton {
                background-color: QLinearGradient(spread:pad, x1:0, y1:0, x2:1,
                    y2:0.273, stop:0 rgba(99, 99, 99, 250),
                    stop:1 #1e1e1e
                    );
                padding: 3px;
                border: 3px solid #1e1e1e;
                border-radius: 10px;
                margin: 0px;
                border-width: 1px;
                font-size: 12px;
                padding-left: 5px;
                padding-right: 5px;
                background-image: None;
            }

            QLineEdit, QTextEdit {
                background-color: QLinearGradient(spread:pad, x1:0, y1:0, x2:1,
                    y2:0.273, stop:0 #000,
                    stop:1 #1e1e1e
                    );
                padding: 3px;
                border: 3px solid #1e1e1e;
                border-radius: 10px;
                margin: 0px;
                font-size: 12px;
                padding-left: 5px;
                padding-right: 5px;
                background-image: None;
            }

            QPushButton:pressed {
                background-image: None;
                background-color: QLinearGradient(
                    x1: 0, y1: 0,
                    x2: 0, y2: 1,
                    stop: 0 #2d2d2d,
                    stop: 0.1 #2b2b2b,
                    stop: 0.5 #292929,
                    stop: 0.9 #282828,
                    stop: 1 #252525
                );
            }

            QComboBox {
                background-color: QLinearGradient(spread:pad, x1:0, y1:0, x2:1,
                    y2:0.273, stop:0 rgba(99, 99, 99, 250),
                    stop:1 #1e1e1e
                    );
                padding: 3px;
                border: 3px solid #1e1e1e;
                border-radius: 15px;
                margin: 0px;
            }

            QComboBox:hover, QPushButton:hover {
                border: 2px solid QLinearGradient(
                    x1: 0, y1: 0,
                    x2: 0, y2: 1,
                    stop: 0 #ffa02f,
                    stop: 1 #d7801a
                );
            }

            QComboBox QAbstractItemView {
                border: 2px solid darkgray;
                selection-background-color: QLinearGradient(
                    x1: 0, y1: 0,
                    x2: 0, y2: 1,
                    stop: 0 #ffa02f,
                    stop: 1 #d7801a
                );
            }

            QComboBox::drop-down {
                 subcontrol-origin: padding;
                 subcontrol-position: top right;
                 width: 0px;
                 height: 0px;
                 border-left-width: 0px;
                 opacity: 0;
             }

            QSlider {
                padding: 3px;
                font-size: 8px;
                padding-left: 2px;
                padding-right: 2px;
                border-style: solid;
                border: 5px solid #1e1e1e;
            }

            QSlider::sub-page:vertical {
                background-color: QLinearGradient(spread:pad, x1:0, y1:0, x2:1,
                    y2:0.273, stop:0 rgba(255, 0, 0, 255),
                    stop:1 rgba(50, 0, 0, 200)
                    );
                border-style: solid;
                border: 4px solid #1e1e1e;
                border-radius: 5px;
            }

            QSlider::add-page:vertical {
                background-color: QLinearGradient(spread:pad, x1:0, y1:0, x2:1,
                    y2:0.273, stop:0 rgba(0, 255, 0, 255),
                    stop:1 rgba(0, 99, 0, 255)
                    );
                border-style: solid;
                border: 4px solid #1e1e1e;
                border-radius: 5;
            }

            QSlider::handle:vertical {
                background-color: QLinearGradient(spread:pad, x1:0, y1:0, x2:1,
                    y2:0.273, stop:0 rgba(0, 0, 0, 255),
                    stop:1 rgba(150, 255, 255, 255)
                    );
                height: 5px;
                border: 1px dotted #fff;
                text-align: center;
                border-top-left-radius: 2px;
                border-bottom-left-radius: 2px;
                border-top-right-radius: 2px;
                border-bottom-right-radius 2px;
                margin-left: 2px;
                margin-right: 2px;
            }

            QSlider::handle:vertical:hover {
                border: 2px solid #ffaa00;
                margin-left: 2px;
                margin-right: 2px;
            }

            QSlider::sub-page:vertical:disabled {
                background: #bbb;
                border-color: #999;
            }

            QSlider::add-page:vertical:disabled {
                background: #eee;
                border-color: #999;
            }

            QSlider::handle:vertical:disabled {
                background: #eee;
                border: 1px solid #aaa;
                border-radius: 4px;
            }

            QToolBar, QStatusBar, QDockWidget::title{background-color:#323232;}

            QToolBar::handle {
                background-color: QLinearGradient(spread:pad, x1:0, y1:0, x2:1,
                    y2:0.273, stop:0 rgba(0, 0, 0, 255),
                    stop:1 rgba(150, 255, 255, 255)
                    );
                border: 1px solid grey;
                border-radius: 9px;
                width: 19px;
                margin: 0.5px;
            } '''))

        self.stack = StackedWidget(self)
        #self.stack.resize(self.size())
        self.stack.setGeometry(QtCore.QRect(25, 50, 550, 675))
        self.stack.setFrameShape(QtGui.QFrame.NoFrame)
        self.stack.setFrameShadow(QtGui.QFrame.Plain)
        self.stack.setMidLineWidth(0)

        self.page1 = QtGui.QWidget()
        self.page1.setObjectName("page1")
        self.groupBox1 = QtGui.QGroupBox(self.page1)
        self.groupBox1.setAlignment(QtCore.Qt.AlignHCenter
                                                         | QtCore.Qt.AlignTop)
        self.groupBox1.setFlat(True)
        self.groupBox1.setCheckable(False)
        self.groupBox1.setObjectName("groupBox1")
        self.stack.addWidget(self.groupBox1)

        self.page2 = QtGui.QWidget()
        self.page2.setObjectName("page2")
        self.groupBox2 = QtGui.QGroupBox(self.page2)
        self.groupBox2.setAlignment(QtCore.Qt.AlignHCenter
                                                         | QtCore.Qt.AlignTop)
        self.groupBox2.setFlat(True)
        self.groupBox2.setCheckable(False)
        self.groupBox2.setObjectName("groupBox2")
        self.stack.addWidget(self.groupBox2)

        self.page1Button = QPushButton(" Configs and Compiler ", self)
        self.page1Button.setGeometry(QtCore.QRect(300, 25, 275, 25))
        self.page2Button = QPushButton(" Nodes Tree Inspector ", self)
        self.page2Button.setGeometry(QtCore.QRect(25, 25, 275, 25))
        self.page1Button.clicked.connect(self.stack.setPage1)
        self.page2Button.clicked.connect(self.stack.setPage2)

        #######################################################################

        self.vboxlayout = QtGui.QVBoxLayout(self.groupBox2)
        self.vboxlayout.setObjectName("vboxlayout")
        self.gridlayout = QtGui.QGridLayout()
        self.gridlayout.setObjectName("gridlayout")
        self.dockWidget = QtGui.QDockWidget(self.groupBox2)
        self.dockWidget.setWindowModality(QtCore.Qt.NonModal)
        self.dockWidget.setWindowOpacity(0.7)
        self.dockWidget.setWindowTitle(
            "You can Undock and Resize the Nodes Tree Inspector Widget ! --->")
        self.dockWidget.setToolTip(" You can Undock and Resize this Widget ! ")
        self.dockWidget.setFeatures(QtGui.QDockWidget.DockWidgetFloatable |
            QtGui.QDockWidget.DockWidgetMovable)
        self.dockWidget.setObjectName("dockWidget")
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.verticalLayout = QtGui.QVBoxLayout(self.dockWidgetContents)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.treeview_nodes = QtGui.QTextEdit(self.dockWidgetContents)
        self.treeview_nodes.setObjectName("treeview_nodes")
        self.treeview_nodes.setAutoFormatting(QTextEdit.AutoAll)
        self.treeview_nodes.setWordWrapMode(QTextOption.NoWrap)
        self.gridLayout.addWidget(self.treeview_nodes, 1, 0, 1, 1)
        self.textedit_source = QtGui.QTextEdit(self.dockWidgetContents)
        self.textedit_source.setObjectName("textedit_source")
        self.gridLayout.addWidget(self.textedit_source, 1, 2, 1, 1)
        self.label_source = QtGui.QLabel(self.dockWidgetContents)
        self.label_source.setObjectName("label_source")
        self.gridLayout.addWidget(self.label_source, 0, 2, 1, 1)
        self.label_nodetree = QtGui.QLabel(self.dockWidgetContents)
        self.label_nodetree.setObjectName("label_nodetree")
        self.gridLayout.addWidget(self.label_nodetree, 0, 0, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.dockWidget.setWidget(self.dockWidgetContents)
        self.gridlayout.addWidget(self.dockWidget, 0, 0, 2, 1)
        self.vboxlayout.addLayout(self.gridlayout)
        QtCore.QMetaObject.connectSlotsByName(self.groupBox2)
        self.label_source.setText("<b> Python Source Code </b>")
        self.label_nodetree.setText("<b> Nodes Tree View </b>")

        #######################################################################

        self.label1 = QtGui.QLabel(self.groupBox1)
        self.label1.setText(' Use low level Debug  (SLOW!)')
        self.label1.setToolTip('Show Nuitka debug output (Defaults are Ok)')
        self.label1.setGeometry(QtCore.QRect(30, 35, 200, 25))
        self.label1.setObjectName("label1")

        self.slider1 = QtGui.QSlider(self.groupBox1)
        self.slider1.setGeometry(QtCore.QRect(225, 25, 30, 35))
        self.slider1.setObjectName("slider1")
        self.slider1.setTickInterval(1)
        self.slider1.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))
        self.slider1.TickPosition(QSlider.TicksBothSides)
        self.slider1.setRange(0, 1)
        self.slider1.setValue(0)
        self.sli1lbl = QtGui.QLabel(str(self.slider1.value()), self.slider1)
        self.sli1lbl.move(10, 9)
        self.sli1lbl.setAutoFillBackground(False)
        self.slider1.valueChanged.connect(
            lambda: self.sli1lbl.setText(str(self.slider1.value()))
            )
        self.slider1.sliderPressed.connect(
            lambda: self.slider1.setCursor(
                QtGui.QCursor(QtCore.Qt.ClosedHandCursor))
            )
        self.slider1.sliderReleased.connect(
            lambda: self.slider1.setCursor(
                QtGui.QCursor(QtCore.Qt.OpenHandCursor))
            )

        self.label2 = QtGui.QLabel(self.groupBox1)
        self.label2.setText(' Be Verbose')
        self.label2.setToolTip(
           'Show Verbose output (Defaults are Ok)')
        self.label2.setGeometry(QtCore.QRect(25, 75, 200, 25))
        self.label2.setObjectName("label2")

        self.slider2 = QtGui.QSlider(self.groupBox1)
        self.slider2.setGeometry(QtCore.QRect(225, 75, 30, 35))
        self.slider2.setObjectName("slider2")
        self.slider2.setTickInterval(1)
        self.slider2.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))
        self.slider2.TickPosition(QSlider.TicksBothSides)
        self.slider2.setRange(0, 1)
        self.slider2.setValue(1)
        self.sli2lbl = QtGui.QLabel(str(self.slider2.value()), self.slider2)
        self.sli2lbl.move(10, 9)
        self.sli2lbl.setAutoFillBackground(False)
        self.slider2.valueChanged.connect(
            lambda: self.sli2lbl.setText(str(self.slider2.value()))
            )
        self.slider2.sliderPressed.connect(
            lambda: self.slider2.setCursor(
                QtGui.QCursor(QtCore.Qt.ClosedHandCursor))
            )
        self.slider2.sliderReleased.connect(
            lambda: self.slider2.setCursor(
                QtGui.QCursor(QtCore.Qt.OpenHandCursor))
            )

        self.label3 = QtGui.QLabel(self.groupBox1)
        self.label3.setText(' Show the compiling progress')
        self.label3.setToolTip(
            'Show progress information and statistics (Defaults are Ok)')
        self.label3.setGeometry(QtCore.QRect(25, 125, 200, 25))
        self.label3.setObjectName("label3")

        self.slider3 = QtGui.QSlider(self.groupBox1)
        self.slider3.setGeometry(QtCore.QRect(225, 130, 30, 35))
        self.slider3.setObjectName("slider3")
        self.slider3.setTickInterval(1)
        self.slider3.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))
        self.slider3.TickPosition(QSlider.TicksBothSides)
        self.slider3.setRange(0, 1)
        self.slider3.setValue(1)
        self.sli3lbl = QtGui.QLabel(str(self.slider3.value()), self.slider3)
        self.sli3lbl.move(10, 9)
        self.sli3lbl.setAutoFillBackground(False)
        self.slider3.valueChanged.connect(
            lambda: self.sli3lbl.setText(str(self.slider3.value()))
            )
        self.slider3.sliderPressed.connect(
            lambda: self.slider3.setCursor(
                QtGui.QCursor(QtCore.Qt.ClosedHandCursor))
            )
        self.slider3.sliderReleased.connect(
            lambda: self.slider3.setCursor(
                QtGui.QCursor(QtCore.Qt.OpenHandCursor))
            )

        self.label4 = QtGui.QLabel(self.groupBox1)
        self.label4.setText(' Show Scons building debug')
        self.label4.setToolTip(
            'Operate Scons in non-quiet mode, showing the executed commands')
        self.label4.setGeometry(QtCore.QRect(25, 175, 200, 25))
        self.label4.setObjectName("label4")

        self.slider4 = QtGui.QSlider(self.groupBox1)
        self.slider4.setGeometry(QtCore.QRect(225, 175, 30, 35))
        self.slider4.setObjectName("slider4")
        self.slider4.setTickInterval(1)
        self.slider4.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))
        self.slider4.TickPosition(QSlider.TicksBothSides)
        self.slider4.setRange(0, 1)
        self.slider4.setValue(1)
        self.sli4lbl = QtGui.QLabel(str(self.slider4.value()), self.slider4)
        self.sli4lbl.move(10, 9)
        self.sli4lbl.setAutoFillBackground(False)
        self.slider4.valueChanged.connect(
            lambda: self.sli4lbl.setText(str(self.slider4.value()))
            )
        self.slider4.sliderPressed.connect(
            lambda: self.slider4.setCursor(
                QtGui.QCursor(QtCore.Qt.ClosedHandCursor))
            )
        self.slider4.sliderReleased.connect(
            lambda: self.slider4.setCursor(
                QtGui.QCursor(QtCore.Qt.OpenHandCursor))
            )

        self.label5 = QtGui.QLabel(self.groupBox1)
        self.label5.setText(' Keep debug unstriped binary')
        self.label5.setToolTip(
            'Keep debug info in the resulting file for better gdb interaction')
        self.label5.setGeometry(QtCore.QRect(25, 225, 200, 25))
        self.label5.setObjectName("label5")

        self.slider5 = QtGui.QSlider(self.groupBox1)
        self.slider5.setGeometry(QtCore.QRect(225, 225, 30, 35))
        self.slider5.setObjectName("slider5")
        self.slider5.setTickInterval(1)
        self.slider5.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))
        self.slider5.TickPosition(QSlider.TicksBothSides)
        self.slider5.setRange(0, 1)
        self.slider5.setValue(0)
        self.sli5lbl = QtGui.QLabel(str(self.slider5.value()), self.slider5)
        self.sli5lbl.move(10, 9)
        self.sli5lbl.setAutoFillBackground(False)
        self.slider5.valueChanged.connect(
            lambda: self.sli5lbl.setText(str(self.slider5.value()))
            )
        self.slider5.sliderPressed.connect(
            lambda: self.slider5.setCursor(
                QtGui.QCursor(QtCore.Qt.ClosedHandCursor))
            )
        self.slider5.sliderReleased.connect(
            lambda: self.slider5.setCursor(
                QtGui.QCursor(QtCore.Qt.OpenHandCursor))
            )

        self.label6 = QtGui.QLabel(self.groupBox1)
        self.label6.setText(' Traced execution outputs')
        self.label6.setToolTip(
            'Trace execution output, output line of code before executing it')
        self.label6.setGeometry(QtCore.QRect(25, 275, 200, 25))
        self.label6.setObjectName("label6")

        self.slider6 = QtGui.QSlider(self.groupBox1)
        self.slider6.setGeometry(QtCore.QRect(225, 275, 30, 35))
        self.slider6.setObjectName("slider6")
        self.slider6.setTickInterval(1)
        self.slider6.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))
        self.slider6.TickPosition(QSlider.TicksBothSides)
        self.slider6.setRange(0, 1)
        self.slider6.setValue(0)
        self.sli6lbl = QtGui.QLabel(str(self.slider6.value()), self.slider6)
        self.sli6lbl.move(10, 9)
        self.sli6lbl.setAutoFillBackground(False)
        self.slider6.valueChanged.connect(
            lambda: self.sli6lbl.setText(str(self.slider6.value()))
            )
        self.slider6.sliderPressed.connect(
            lambda: self.slider6.setCursor(
                QtGui.QCursor(QtCore.Qt.ClosedHandCursor))
            )
        self.slider6.sliderReleased.connect(
            lambda: self.slider6.setCursor(
                QtGui.QCursor(QtCore.Qt.OpenHandCursor))
            )

        self.label7 = QtGui.QLabel(self.groupBox1)
        self.label7.setText(' Remove the build folder')
        self.label7.setToolTip(
            ' Removes the build directory after producing the module or file')
        self.label7.setGeometry(QtCore.QRect(25, 325, 200, 25))
        self.label7.setObjectName("label7")

        self.slider7 = QtGui.QSlider(self.groupBox1)
        self.slider7.setGeometry(QtCore.QRect(225, 325, 30, 35))
        self.slider7.setObjectName("slider7")
        self.slider7.setTickInterval(1)
        self.slider7.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))
        self.slider7.TickPosition(QSlider.TicksBothSides)
        self.slider7.setRange(0, 1)
        self.slider7.setValue(1)
        self.sli7lbl = QtGui.QLabel(str(self.slider7.value()), self.slider7)
        self.sli7lbl.move(10, 9)
        self.sli7lbl.setAutoFillBackground(False)
        self.slider7.valueChanged.connect(
            lambda: self.sli7lbl.setText(str(self.slider7.value()))
            )
        self.slider7.sliderPressed.connect(
            lambda: self.slider7.setCursor(
                QtGui.QCursor(QtCore.Qt.ClosedHandCursor))
            )
        self.slider7.sliderReleased.connect(
            lambda: self.slider7.setCursor(
                QtGui.QCursor(QtCore.Qt.OpenHandCursor))
            )

        self.label8 = QtGui.QLabel(self.groupBox1)
        self.label8.setText(' No use Python Optimizations')
        self.label8.setToolTip(
            'Disable all unnecessary optimizations on Python')
        self.label8.setGeometry(QtCore.QRect(25, 375, 200, 25))
        self.label8.setObjectName("label8")

        self.slider8 = QtGui.QSlider(self.groupBox1)
        self.slider8.setGeometry(QtCore.QRect(225, 375, 30, 35))
        self.slider8.setObjectName("slider8")
        self.slider8.setTickInterval(1)
        self.slider8.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))
        self.slider8.TickPosition(QSlider.TicksBothSides)
        self.slider8.setRange(0, 1)
        self.slider8.setValue(0)
        self.sli8lbl = QtGui.QLabel(str(self.slider8.value()), self.slider8)
        self.sli8lbl.move(10, 9)
        self.sli8lbl.setAutoFillBackground(False)
        self.slider8.valueChanged.connect(
            lambda: self.sli8lbl.setText(str(self.slider8.value()))
            )
        self.slider8.sliderPressed.connect(
            lambda: self.slider8.setCursor(
                QtGui.QCursor(QtCore.Qt.ClosedHandCursor))
            )
        self.slider8.sliderReleased.connect(
            lambda: self.slider8.setCursor(
                QtGui.QCursor(QtCore.Qt.OpenHandCursor))
            )

        self.label9 = QtGui.QLabel(self.groupBox1)
        self.label9.setText(' No Statements line numbers')
        self.label9.setToolTip(
            'Disable all unnecessary optimizations on Python')
        self.label9.setGeometry(QtCore.QRect(25, 425, 200, 25))
        self.label9.setObjectName("label9")

        self.slider9 = QtGui.QSlider(self.groupBox1)
        self.slider9.setGeometry(QtCore.QRect(225, 425, 30, 35))
        self.slider9.setObjectName("slider9")
        self.slider9.setTickInterval(1)
        self.slider9.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))
        self.slider9.TickPosition(QSlider.TicksBothSides)
        self.slider9.setRange(0, 1)
        self.slider9.setValue(0)
        self.sli9lbl = QtGui.QLabel(str(self.slider9.value()), self.slider9)
        self.sli9lbl.move(10, 9)
        self.sli9lbl.setAutoFillBackground(False)
        self.slider9.valueChanged.connect(
            lambda: self.sli9lbl.setText(str(self.slider9.value()))
            )
        self.slider9.sliderPressed.connect(
            lambda: self.slider9.setCursor(
                QtGui.QCursor(QtCore.Qt.ClosedHandCursor))
            )
        self.slider9.sliderReleased.connect(
            lambda: self.slider9.setCursor(
                QtGui.QCursor(QtCore.Qt.OpenHandCursor))
            )

        self.label10 = QtGui.QLabel(self.groupBox1)
        self.label10.setText(' Execute the output binary')
        self.label10.setToolTip(
            'Execute the created binary or import the compiled module')
        self.label10.setGeometry(QtCore.QRect(25, 475, 200, 25))
        self.label10.setObjectName("label10")

        self.slider10 = QtGui.QSlider(self.groupBox1)
        self.slider10.setGeometry(QtCore.QRect(225, 475, 30, 35))
        self.slider10.setObjectName("slider10")
        self.slider10.setTickInterval(1)
        self.slider10.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))
        self.slider10.TickPosition(QSlider.TicksBothSides)
        self.slider10.setRange(0, 1)
        self.slider10.setValue(0)
        self.sli10lbl = QtGui.QLabel(str(self.slider10.value()), self.slider10)
        self.sli10lbl.move(10, 9)
        self.sli10lbl.setAutoFillBackground(False)
        self.slider10.valueChanged.connect(
            lambda: self.sli10lbl.setText(str(self.slider10.value()))
            )
        self.slider10.sliderPressed.connect(
            lambda: self.slider10.setCursor(
                QtGui.QCursor(QtCore.Qt.ClosedHandCursor))
            )
        self.slider10.sliderReleased.connect(
            lambda: self.slider10.setCursor(
                QtGui.QCursor(QtCore.Qt.OpenHandCursor))
            )

        self.label1a = QtGui.QLabel(self.groupBox1)
        self.label1a.setText(' Descendent Recursive Compile')
        self.label1a.setToolTip('Attempt to descend into all imported modules')
        self.label1a.setGeometry(QtCore.QRect(300, 25, 200, 25))
        self.label1a.setObjectName("label1a")

        self.slider1a = QtGui.QSlider(self.groupBox1)
        self.slider1a.setGeometry(QtCore.QRect(500, 25, 30, 35))
        self.slider1a.setObjectName("slider1a")
        self.slider1a.setTickInterval(1)
        self.slider1a.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))
        self.slider1a.TickPosition(QSlider.TicksBothSides)
        self.slider1a.setRange(0, 1)
        self.slider1a.setValue(0)
        self.sli1albl = QtGui.QLabel(str(self.slider1a.value()), self.slider1a)
        self.sli1albl.move(10, 9)
        self.sli1albl.setAutoFillBackground(False)
        self.slider1a.valueChanged.connect(
            lambda: self.sli1albl.setText(str(self.slider1a.value()))
            )
        self.slider1a.sliderPressed.connect(
            lambda: self.slider1a.setCursor(
                QtGui.QCursor(QtCore.Qt.ClosedHandCursor))
            )
        self.slider1a.sliderReleased.connect(
            lambda: self.slider1a.setCursor(
                QtGui.QCursor(QtCore.Qt.OpenHandCursor))
            )

        self.label2a = QtGui.QLabel(self.groupBox1)
        self.label2a.setText(' Force non recursive compile')
        self.label2a.setToolTip(
           'Not descend into any imported modules, overrides other recursions')
        self.label2a.setGeometry(QtCore.QRect(300, 75, 200, 25))
        self.label2a.setObjectName("label2a")

        self.slider2a = QtGui.QSlider(self.groupBox1)
        self.slider2a.setGeometry(QtCore.QRect(500, 75, 30, 35))
        self.slider2a.setObjectName("slider2a")
        self.slider2a.setTickInterval(1)
        self.slider2a.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))
        self.slider2a.TickPosition(QSlider.TicksBothSides)
        self.slider2a.setRange(0, 1)
        self.slider2a.setValue(1)
        self.sli2albl = QtGui.QLabel(str(self.slider2a.value()), self.slider2a)
        self.sli2albl.move(10, 9)
        self.sli2albl.setAutoFillBackground(False)
        self.slider2a.valueChanged.connect(
            lambda: self.sli2lbl.setText(str(self.slider2.value()))
            )
        self.slider2a.sliderPressed.connect(
            lambda: self.slider2a.setCursor(
                QtGui.QCursor(QtCore.Qt.ClosedHandCursor))
            )
        self.slider2a.sliderReleased.connect(
            lambda: self.slider2a.setCursor(
                QtGui.QCursor(QtCore.Qt.OpenHandCursor))
            )

        self.label3a = QtGui.QLabel(self.groupBox1)
        self.label3a.setText(' STD Lib Recursive Compile')
        self.label3a.setToolTip(
            'Also descend into imported modules from standard library')
        self.label3a.setGeometry(QtCore.QRect(300, 125, 200, 25))
        self.label3a.setObjectName("label3a")

        self.slider3a = QtGui.QSlider(self.groupBox1)
        self.slider3a.setGeometry(QtCore.QRect(500, 125, 30, 35))
        self.slider3a.setObjectName("slider3a")
        self.slider3a.setTickInterval(1)
        self.slider3a.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))
        self.slider3a.TickPosition(QSlider.TicksBothSides)
        self.slider3a.setRange(0, 1)
        self.slider3a.setValue(0)
        self.sli3albl = QtGui.QLabel(str(self.slider3a.value()), self.slider3a)
        self.sli3albl.move(10, 9)
        self.sli3albl.setAutoFillBackground(False)
        self.slider3a.valueChanged.connect(
            lambda: self.sli3albl.setText(str(self.slider3a.value()))
            )
        self.slider3a.sliderPressed.connect(
            lambda: self.slider3a.setCursor(
                QtGui.QCursor(QtCore.Qt.ClosedHandCursor))
            )
        self.slider3a.sliderReleased.connect(
            lambda: self.slider3a.setCursor(
                QtGui.QCursor(QtCore.Qt.OpenHandCursor))
            )

        self.label4a = QtGui.QLabel(self.groupBox1)
        self.label4a.setText(' Enforce the use of Clang')
        self.label4a.setToolTip(
            'Enforce the use of clang (clang 3 or higher)')
        self.label4a.setGeometry(QtCore.QRect(300, 175, 200, 25))
        self.label4a.setObjectName("label4a")

        self.slider4a = QtGui.QSlider(self.groupBox1)
        self.slider4a.setGeometry(QtCore.QRect(500, 175, 30, 35))
        self.slider4a.setObjectName("slider4a")
        self.slider4a.setTickInterval(1)
        self.slider4a.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))
        self.slider4a.TickPosition(QSlider.TicksBothSides)
        self.slider4a.setRange(0, 1)
        self.slider4a.setValue(0)
        self.sli4albl = QtGui.QLabel(str(self.slider4a.value()), self.slider4a)
        self.sli4albl.move(10, 9)
        self.sli4albl.setAutoFillBackground(False)
        self.slider4a.valueChanged.connect(
            lambda: self.sli4albl.setText(str(self.slider4a.value()))
            )
        self.slider4a.sliderPressed.connect(
            lambda: self.slider4a.setCursor(
                QtGui.QCursor(QtCore.Qt.ClosedHandCursor))
            )
        self.slider4a.sliderReleased.connect(
            lambda: self.slider4a.setCursor(
                QtGui.QCursor(QtCore.Qt.OpenHandCursor))
            )

        self.label5a = QtGui.QLabel(self.groupBox1)
        self.label5a.setText(' Use G++ link time optimizations')
        self.label5a.setToolTip(
            'Use link time optimizations if available (g++ 4 and higher)')
        self.label5a.setGeometry(QtCore.QRect(300, 225, 200, 25))
        self.label5a.setObjectName("label5a")

        self.slider5a = QtGui.QSlider(self.groupBox1)
        self.slider5a.setGeometry(QtCore.QRect(500, 225, 30, 35))
        self.slider5a.setObjectName("slider5a")
        self.slider5a.setTickInterval(1)
        self.slider5a.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))
        self.slider5a.TickPosition(QSlider.TicksBothSides)
        self.slider5a.setRange(0, 1)
        self.slider5a.setValue(1)
        self.sli5albl = QtGui.QLabel(str(self.slider5a.value()), self.slider5a)
        self.sli5albl.move(10, 9)
        self.sli5albl.setAutoFillBackground(False)
        self.slider5a.valueChanged.connect(
            lambda: self.sli5albl.setText(str(self.slider5a.value()))
            )
        self.slider5a.sliderPressed.connect(
            lambda: self.slider5a.setCursor(
                QtGui.QCursor(QtCore.Qt.ClosedHandCursor))
            )
        self.slider5a.sliderReleased.connect(
            lambda: self.slider5a.setCursor(
                QtGui.QCursor(QtCore.Qt.OpenHandCursor))
            )

        self.label6a = QtGui.QLabel(self.groupBox1)
        self.label6a.setText(' Disable the console window')
        self.label6a.setToolTip(
            'When compiling for Microsoft Windows, disable the console window')
        self.label6a.setGeometry(QtCore.QRect(300, 275, 200, 25))
        self.label6a.setObjectName("label6a")

        self.slider6a = QtGui.QSlider(self.groupBox1)
        self.slider6a.setGeometry(QtCore.QRect(500, 275, 30, 35))
        self.slider6a.setObjectName("slider6a")
        self.slider6a.setTickInterval(1)
        self.slider6a.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))
        self.slider6a.TickPosition(QSlider.TicksBothSides)
        self.slider6a.setRange(0, 1)
        self.slider6a.setValue(0)
        self.sli6albl = QtGui.QLabel(str(self.slider6a.value()), self.slider6a)
        self.sli6albl.move(10, 9)
        self.sli6albl.setAutoFillBackground(False)
        self.slider6a.valueChanged.connect(
            lambda: self.sli6albl.setText(str(self.slider6a.value()))
            )
        self.slider6a.sliderPressed.connect(
            lambda: self.slider6a.setCursor(
                QtGui.QCursor(QtCore.Qt.ClosedHandCursor))
            )
        self.slider6a.sliderReleased.connect(
            lambda: self.slider6a.setCursor(
                QtGui.QCursor(QtCore.Qt.OpenHandCursor))
            )

        self.label7a = QtGui.QLabel(self.groupBox1)
        self.label7a.setText(' Force compile for MS Windows')
        self.label7a.setToolTip(
            'Force compilation for MS Windows, useful for cross-compilation')
        self.label7a.setGeometry(QtCore.QRect(300, 325, 200, 25))
        self.label7a.setObjectName("label7a")

        self.slider7a = QtGui.QSlider(self.groupBox1)
        self.slider7a.setGeometry(QtCore.QRect(500, 325, 30, 35))
        self.slider7a.setObjectName("slider7a")
        self.slider7a.setTickInterval(1)
        self.slider7a.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))
        self.slider7a.TickPosition(QSlider.TicksBothSides)
        self.slider7a.setRange(0, 1)
        self.slider7a.setValue(0)
        self.sli7albl = QtGui.QLabel(str(self.slider7a.value()), self.slider7a)
        self.sli7albl.move(10, 9)
        self.sli7albl.setAutoFillBackground(False)
        self.slider7a.valueChanged.connect(
            lambda: self.sli7albl.setText(str(self.slider7a.value()))
            )
        self.slider7a.sliderPressed.connect(
            lambda: self.slider7a.setCursor(
                QtGui.QCursor(QtCore.Qt.ClosedHandCursor))
            )
        self.slider7a.sliderReleased.connect(
            lambda: self.slider7a.setCursor(
                QtGui.QCursor(QtCore.Qt.OpenHandCursor))
            )

        self.label8a = QtGui.QLabel(self.groupBox1)
        self.label8a.setText(' Use Python Debug versions')
        self.label8a.setToolTip(
            'Use Python debug version or not, most likely a non-debug version')
        self.label8a.setGeometry(QtCore.QRect(300, 375, 200, 25))
        self.label8a.setObjectName("label8a")

        self.slider8a = QtGui.QSlider(self.groupBox1)
        self.slider8a.setGeometry(QtCore.QRect(500, 375, 30, 35))
        self.slider8a.setObjectName("slider8a")
        self.slider8a.setTickInterval(1)
        self.slider8a.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))
        self.slider8a.TickPosition(QSlider.TicksBothSides)
        self.slider8a.setRange(0, 1)
        self.slider8a.setValue(0)
        self.sli8albl = QtGui.QLabel(str(self.slider8a.value()), self.slider8a)
        self.sli8albl.move(10, 9)
        self.sli8albl.setAutoFillBackground(False)
        self.slider8a.valueChanged.connect(
            lambda: self.sli8albl.setText(str(self.slider8a.value()))
            )
        self.slider8a.sliderPressed.connect(
            lambda: self.slider8a.setCursor(
                QtGui.QCursor(QtCore.Qt.ClosedHandCursor))
            )
        self.slider8.sliderReleased.connect(
            lambda: self.slider8a.setCursor(
                QtGui.QCursor(QtCore.Qt.OpenHandCursor))
            )

        self.label9a = QtGui.QLabel(self.groupBox1)
        self.label9a.setText(' Create standalone executable')
        self.label9a.setToolTip(
            'Create a standalone executable instead of a compiled extensions')
        self.label9a.setGeometry(QtCore.QRect(300, 425, 200, 25))
        self.label9a.setObjectName("label9a")

        self.slider9a = QtGui.QSlider(self.groupBox1)
        self.slider9a.setGeometry(QtCore.QRect(500, 425, 30, 35))
        self.slider9a.setObjectName("slider9a")
        self.slider9a.setTickInterval(1)
        self.slider9a.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))
        self.slider9a.TickPosition(QSlider.TicksBothSides)
        self.slider9a.setRange(0, 1)
        self.slider9a.setValue(1)
        self.sli9albl = QtGui.QLabel(str(self.slider9a.value()), self.slider9a)
        self.sli9albl.move(10, 9)
        self.sli9albl.setAutoFillBackground(False)
        self.slider9a.valueChanged.connect(
            lambda: self.sli9albl.setText(str(self.slider9a.value()))
            )
        self.slider9a.sliderPressed.connect(
            lambda: self.slider9a.setCursor(
                QtGui.QCursor(QtCore.Qt.ClosedHandCursor))
            )
        self.slider9a.sliderReleased.connect(
            lambda: self.slider9a.setCursor(
                QtGui.QCursor(QtCore.Qt.OpenHandCursor))
            )

        self.label10a = QtGui.QLabel(self.groupBox1)
        self.label10a.setText(' Backend Nice CPU priority')
        self.label10a.setToolTip('Backend Nice CPU priority number setting')
        self.label10a.setGeometry(QtCore.QRect(300, 475, 200, 25))
        self.label10a.setObjectName("label10a")

        self.combo2 = QtGui.QComboBox(self.groupBox1)
        self.combo2.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.combo2.addItems([
            '19', '0', '5', '10', '15', '-5', '-10', '-15', '-20'])
        self.combo2.setToolTip('Compiler Nice priority (-20 = High, 19 = Low)')
        self.combo2.setGeometry(QtCore.QRect(500, 475, 35, 35))
        self.combo2.setObjectName("combo2")

        self.label11 = QtGui.QLabel(self.groupBox1)
        self.label11.setText(' Python interpreter version')
        self.label11.setToolTip('The Python interpreter version to use')
        self.label11.setGeometry(QtCore.QRect(300, 525, 200, 25))
        self.label11.setObjectName("label11")

        self.combo1 = QtGui.QComboBox(self.groupBox1)
        self.combo1.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.combo1.addItems(['2', '3'])
        self.combo1.setToolTip('The Python interpreter version to use')
        self.combo1.setGeometry(QtCore.QRect(500, 525, 35, 35))
        self.combo1.setObjectName("combo1")

        self.label12 = QtGui.QLabel(self.groupBox1)
        self.label12.setText(' Output Directory')
        self.label12.setToolTip(
            'Specify Output Directory for C++ files. Defaults  to current dir')
        self.label12.setGeometry(QtCore.QRect(25, 575, 125, 25))
        self.label12.setObjectName("label12")

        self.outdir = QtGui.QLineEdit(self.groupBox1)
        self.outdir.setGeometry(QtCore.QRect(152, 575, 350, 25))
        self.outdir.setToolTip(
            'Specify Output Directory for C++ files. Defaults  to current dir')

        self.clearButton = QtGui.QToolButton(self.outdir)
        self.clearButton.setIcon(QtGui.QIcon.fromTheme("edit-clear"))
        self.clearButton.setIconSize(QSize(25, 20))
        self.clearButton.setCursor(QtCore.Qt.ArrowCursor)
        self.clearButton.setStyleSheet("QToolButton{border:none;}")
        self.clearButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.clearButton.hide()
        self.clearButton.clicked.connect(self.outdir.clear)
        self.clearButton.move(320, 1)
        self.outdir.textChanged.connect(
            lambda: self.clearButton.setVisible(True))
        self.clearButton.clicked.connect(
            lambda: self.clearButton.setVisible(False))
        self.outdir.setPlaceholderText(' Output Directory')
        # try to read the output directory, except if fail use users home
        if os.path.isfile('.nuitka-output-dir.txt'):
            self.outdir.setText(open('.nuitka-output-dir.txt', 'r').read())
        else:
            self.outdir.setText(os.path.expanduser("~"))
        # directory auto completer
        self.completer = QCompleter(self)
        self.dirs = QDirModel(self)
        self.dirs.setFilter(QDir.Dirs | QDir.NoDotAndDotDot)
        self.completer.setModel(self.dirs)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.completer.setCompletionMode(QCompleter.PopupCompletion)
        #self.completer.setCompletionMode(QCompleter.InlineCompletion)
        self.outdir.setCompleter(self.completer)

        self.btn1 = QtGui.QPushButton('', self.groupBox1)
        self.btn1.setIcon(QtGui.QIcon.fromTheme("document-open"))
        self.btn1.setGeometry(505, 575, 35, 35)
        self.btn1.setToolTip(
            'Specify Output Directory for C++ files. Defaults  to current dir')
        self.btn1.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        # Ask the User for the source output directory
        self.btn1.clicked.connect(lambda:
            open('.nuitka-output-dir.txt', 'w').write(str(
            QFileDialog.getExistingDirectory(self,
            'Please, Open an Output Directory to write C++ code and binary...',
            os.path.expanduser("~")))))
        self.btn1.released.connect(lambda: self.outdir.setText(
            open('.nuitka-output-dir.txt', 'r').read()))

        self.label13 = QtGui.QLabel(self.groupBox1)
        self.label13.setText(' Target Python')
        self.label13.setToolTip('Specify Target Python App to Binary Compile')
        self.label13.setGeometry(QtCore.QRect(25, 625, 125, 25))
        self.label13.setObjectName("label13")

        self.target = QtGui.QLineEdit(self.groupBox1)
        self.target.setGeometry(QtCore.QRect(152, 625, 350, 25))
        self.target.setToolTip('Specify Target Python App to Binary Compile')

        self.clearButton2 = QtGui.QToolButton(self.target)
        self.clearButton2.setIcon(QtGui.QIcon.fromTheme("edit-clear"))
        self.clearButton2.setIconSize(QSize(25, 20))
        self.clearButton2.setCursor(QtCore.Qt.ArrowCursor)
        self.clearButton2.setStyleSheet("QToolButton{border:none;}")
        self.clearButton2.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.clearButton2.hide()
        self.clearButton2.clicked.connect(self.target.clear)
        self.clearButton2.move(320, 1)
        self.target.textChanged.connect(
            lambda: self.clearButton2.setVisible(True))
        self.clearButton2.clicked.connect(
            lambda: self.clearButton.setVisible(False))
        self.target.setPlaceholderText(' Target Python App to Binary Compile')
        # directory auto completer
        self.target.setCompleter(self.completer)

        self.btn2 = QtGui.QPushButton('', self.groupBox1)
        self.btn2.setIcon(QtGui.QIcon.fromTheme("document-open"))
        self.btn2.setGeometry(505, 625, 35, 35)
        self.btn2.setToolTip(
            'Specify Output Directory for C++ files. Defaults  to current dir')
        self.btn2.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        # Ask the User for the source output directory
        self.btn2.clicked.connect(lambda: self.target.setText(str(
            QFileDialog.getOpenFileName(self,
            " Please, open a .py file to be compiled to C++ ... ",
            # read output dir from file if it exist else use users home dir
            str(open('.nuitka-output-dir.txt', 'r').read())
                if os.path.isfile('.nuitka-output-dir.txt')
                    else os.path.expanduser("~"),
            # file extensions, plus a wildcard
            ';;'.join(['(*%s)' % e for e in ['.py', '.PY', '.pyw', '']])))))

        self.label13 = QtGui.QLabel(self.groupBox1)
        self.label13.setText(' MultiProcessing Workers')
        self.label13.setToolTip('Backend Nice CPU priority number setting')
        self.label13.setGeometry(QtCore.QRect(25, 525, 200, 25))
        self.label13.setObjectName("label13a")

        self.combo3 = QtGui.QComboBox(self.groupBox1)
        self.combo3.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.combo3.addItems(['1', '2', '3', '4', '5', '6', '7', '8', '9'])
        self.combo3.setToolTip('Compiler MultiProcessing workers to spawn')
        self.combo3.setGeometry(QtCore.QRect(225, 525, 35, 35))
        self.combo3.setObjectName("combo3")

        # Menu Bar inicialization and detail definitions
        menu_salir = QtGui.QAction(QtGui.QIcon.fromTheme("application-exit"),
            'Quit', self)
        # set the quit shortcut to CTRL + Q
        menu_salir.setShortcut('Ctrl+Q')
        # set the triggered signal to the quit slot
        menu_salir.setStatusTip('Quit')
        menu_salir.triggered.connect(exit)

        # Minimize, hide
        menu_minimize = QtGui.QAction(QtGui.QIcon.fromTheme("go-down"),
            'Minimize', self)
        # set the triggered signal to the quit slot
        menu_minimize.setStatusTip('Minimize')
        menu_minimize.triggered.connect(lambda: self.showMinimized())

        # about Qt
        menu_qt = QtGui.QAction(QtGui.QIcon.fromTheme("help-about"),
            'About Qt', self)
        # set the status tip for this menu item
        menu_qt.setStatusTip('About Qt...')
        # set the triggered signal to lambda for the about qt built-in gui
        menu_qt.triggered.connect(lambda: QMessageBox.aboutQt(self))

        # open dev docs
        menu_dev = QtGui.QAction(
            QtGui.QIcon.fromTheme("applications-development"),
            'Nuitka Developer Manual PDF', self)
        # set the status tip for this menu item
        menu_dev.setStatusTip('Open Nuitka Developer Manual PDF...')
        # set the triggered signal to lambda for the about qt built-in gui
        menu_dev.triggered.connect(lambda: subprocess.call(
        'xdg-open /usr/share/doc/nuitka/Developer_Manual.pdf.gz', shell=True))

        # open user docs
        menu_usr = QtGui.QAction(
            QtGui.QIcon.fromTheme("help-contents"),
            'Nuitka End User Manual PDF', self)
        # set the status tip for this menu item
        menu_usr.setStatusTip('Open Nuitka End User Manual PDF...')
        # set the triggered signal to lambda for the about qt built-in gui
        menu_usr.triggered.connect(lambda: subprocess.call(
        'nice -n 19 xdg-open /usr/share/doc/nuitka/README.pdf.gz', shell=True))

        # open online docs
        menu_odoc = QtGui.QAction(QtGui.QIcon.fromTheme("help-browser"),
            'Nuitka on line Docs', self)
        # set the status tip for this menu item
        menu_odoc.setStatusTip('Open Nuitka on line Documentation pages...')
        # set the triggered signal to lambda for the about qt built-in gui
        menu_odoc.triggered.connect(lambda:
                            webbrowser.open_new_tab('http://nuitka.net/doc'))

        # open Man Pages
        menu_man = QtGui.QAction(QtGui.QIcon.fromTheme("utilities-terminal"),
            'Nuitka Man Pages', self)
        # set the status tip for this menu item
        menu_man.setStatusTip('Open Nuitka technical command line Man Pages..')
        # set the triggered signal to lambda for the about qt built-in gui
        menu_man.triggered.connect(lambda: os.system('xterm -e "man nuitka"'))

        # open source code
        menu_tra = QtGui.QAction(
            QtGui.QIcon.fromTheme("applications-development"),
            'View Nuitka-GUI Source Code', self)
        # set the status tip for this menu item
        menu_tra.setStatusTip('View, study, edit Nuitka-GUI Libre Source Code')
        # set the triggered signal to lambda for the about qt built-in gui
        menu_tra.triggered.connect(lambda: os.system('xdg-open ' + __file__))

        # open output dir
        menu_foo = QtGui.QAction(QtGui.QIcon.fromTheme("folder"),
            'Open Output Directory location', self)
        # set the status tip for this menu item
        menu_foo.setStatusTip('Open the actual Output Directory location...')
        # set the triggered signal to lambda for the about qt built-in gui
        menu_foo.triggered.connect(lambda: os.system('nice -n 19 xdg-open ' +
                                                     str(self.outdir.text())))

        # about keyboard shortcuts
        menu_kb = QtGui.QAction(QtGui.QIcon.fromTheme("input-keyboard"),
            'Keyboard Shortcuts', self)
        # set the status tip for this menu item
        menu_kb.setStatusTip('Keyboard Shortcuts...')
        # set the triggered signal to lambda for the about qt built-in gui
        menu_kb.triggered.connect(lambda: QtGui.QMessageBox.information(self,
            'Keyboard Shortcuts', ' Ctrl+Q = Quit '))

        # take a shot
        menu_pic = QtGui.QAction(QtGui.QIcon.fromTheme("camera-photo"),
            'Take Screenshot', self)
        # set the status tip for this menu item
        menu_pic.setStatusTip('Take a Screenshot for Documentation purposes..')
        menu_pic.triggered.connect(lambda: QtGui.QPixmap.grabWindow(
            QtGui.QApplication.desktop().winId()).save(
            QtGui.QFileDialog.getSaveFileName(self, " Save Screenshot As ...",
            os.path.expanduser("~"), ';;.png', 'png'))
        )

        # movable draggable toolbar
        self.toolbar = QtGui.QToolBar(self)
        self.toolbar.setIconSize(QSize(16, 16))
        # spacer widget for left
        self.left_spacer = QtGui.QWidget(self)
        self.left_spacer.setSizePolicy(QtGui.QSizePolicy.Expanding,
                                                QtGui.QSizePolicy.Expanding)
        # spacer widget for right
        self.right_spacer = QtGui.QWidget(self)
        self.right_spacer.setSizePolicy(QtGui.QSizePolicy.Expanding,
                                                QtGui.QSizePolicy.Expanding)
        # add spacer left
        self.toolbar.addWidget(self.left_spacer)
        # actions
        self.toolbar.addSeparator()
        self.toolbar.addAction(menu_salir)
        self.toolbar.addAction(menu_minimize)
        self.toolbar.addSeparator()
        self.toolbar.addAction(menu_qt)
        self.toolbar.addSeparator()
        self.toolbar.addAction(menu_man)
        self.toolbar.addAction(menu_dev)
        self.toolbar.addAction(menu_tra)
        self.toolbar.addSeparator()
        self.toolbar.addAction(menu_odoc)
        self.toolbar.addAction(menu_usr)
        self.toolbar.addSeparator()
        self.toolbar.addAction(menu_foo)
        self.toolbar.addAction(menu_kb)
        self.toolbar.addAction(menu_pic)
        self.toolbar.addSeparator()
        # add spacer right
        self.toolbar.addWidget(self.right_spacer)
        # add toolbar, set initial position
        self.addToolBar(Qt.BottomToolBarArea, self.toolbar)

        # Bottom Buttons Bar
        self.buttonBox = QtGui.QDialogButtonBox(self)
        # set the geometry of buttonbox
        self.buttonBox.setGeometry(QtCore.QRect(25, 715, 550, 32))
        # set the orientation, can be horizontal or vertical
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        # define the buttons to use on it, std buttons uncomment to use
        self.buttonBox.setStandardButtons(
            QtGui.QDialogButtonBox.Ok |
            QtGui.QDialogButtonBox.Cancel |
            QtGui.QDialogButtonBox.Close |
            QtGui.QDialogButtonBox.Help)
        # set if buttons are centered or not
        self.buttonBox.setCenterButtons(False)
        # give the object a name
        self.buttonBox.setObjectName("buttonBox")
        # Help Button Action connection helpRequested() to a QMessageBox
        self.buttonBox.helpRequested.connect(lambda: QMessageBox.about(self,
            __doc__, str(__doc__ + ', using Nuitka ' +
            subprocess.check_output('nuitka --version', shell=True) +
            'GUI version ' + __version__ + ' (' + __license__ + '),\n by ' +
            __author__ + ', ( ' + __email__ + ' ). \n \n \n ' +
            'Nuitka Python Compiler converts plain standard Python 2/3 code ' +
            'to C++ binaries and/or sources consisting of stand-alone ' +
            'executables and/or Python binary modules. \n \n ' +
            'This is a PyQt GUI frontend to a command line backend program.' +
            ' \n \n Please visit Nuitka.net...'
            )))
        # Help Button Action connection to a quit() slot
        self.buttonBox.rejected.connect(exit)
        # Help Button Action connection to a quit() slot
        self.buttonBox.accepted.connect(self.run)
        # Paleta de colores para pintar transparente
        palette = self.palette()
        # add a transparent to the brush of palette
        palette.setBrush(QPalette.Base, Qt.transparent)
        # set the palette to the page in the widget
        self.setPalette(palette)
        # set the opaque paint to false
        self.setAttribute(Qt.WA_OpaquePaintEvent, False)
        self.center()

    def run(self):
        ' run the actual conversion '
        print((' INFO: Working compiling at ' + str(datetime.datetime.now())))
        target = str(self.target.text()).strip()
        # Fill the tab2 and display it
        fake_tree = subprocess.check_output('nuitka --dump-tree ' + target,
                                                                    shell=True)
        self.treeview_nodes.setText(fake_tree)
        self.textedit_source.setText(file(target).read())
        self.stack.setPage2()
        self.statusBar().showMessage(' Loading Nodes Tree Report on Tab 2...')

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
        #
        # debug
        if DEBUG is True:
            print(arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8, arg9, arg10,
            arg1a, arg2a, arg3a, arg4a, arg5a, arg6a, arg7a, arg8a, arg9a,
            arg10a, str(self.combo1.currentText()), str(self.outdir.text()))
        print((' INFO: Started Compiling at ' + str(datetime.datetime.now())))
        # run the subprocesses
        subprocess.Popen('nice --adjustment=' +
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
            ' ; nice -n 19  notify-send "[Nuitka-GUI]" "Python Compile Done."',
            shell=True)

    def center(self):
        ' Center the window '
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def paintEvent(self, event):
        'Paint semi-transparent background, animated pattern, background text'
        # because we are on 2012 !, its time to showcase how Qt we are !
        QWidget.paintEvent(self, event)
        # make a painter
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        p.setRenderHint(QPainter.TextAntialiasing)
        p.setRenderHint(QPainter.HighQualityAntialiasing)
        # fill a rectangle with transparent painting
        p.fillRect(event.rect(), Qt.transparent)
        # animated random dots background pattern
        for i in range(4096):
            x = random.randint(25, self.size().width() - 25)
            y = random.randint(25, self.size().height() - 25)
            # p.setPen(QPen(QColor(random.randint(9, 255), 255, 255), 1))
            p.drawPoint(x, y)
        # set pen to use white color
        p.setPen(QPen(Qt.white, 1))
        # Rotate painter 45 Degree
        p.rotate(45)
        # Set painter Font for text
        p.setFont(QFont('Ubuntu', 175))
        # draw the background text, with antialiasing
        p.drawText(99, 99, "Nuitka")
        # Rotate -45 the QPen back !
        p.rotate(-45)
        # set the pen to no pen
        p.setPen(Qt.NoPen)
        # Background Color
        p.setBrush(QColor(0, 0, 0))
        # Background Opacity
        p.setOpacity(0.75)
        # Background Rounded Borders
        p.drawRoundedRect(self.rect(), 100, 50)
        # finalize the painter
        p.end()


###############################################################################


def main():
    ' Main Loop '
    ################################CLI Args###################################
    import getopt
    OPAQUE = True
    BORDER = True
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hvob',
                                   ['version', 'help', 'opaque', 'border'])
        pass
    except:
        pass
    for o, v in opts:
        if o in ('-h', '--help'):
            print('''
            Usage:
                  -h, --help        Show help informations and exit.
                  -v, --version     Show version information and exit.
                  -o, --opaque      Use Opaque GUI.
                  -b, --border      Use WM Borders.
                  Run without parameters and arguments to use the GUI.
            ''')
            return sys.exit(1)
        elif o in ('-v', '--version'):
            print(__version__)
            return sys.exit(1)
        elif o in ('-o', '--opaque'):
                OPAQUE = False
        elif o in ('-b', '--border'):
                BORDER = False
    ####################################Qt#####################################
    # define our App
    app = QApplication(sys.argv)
    # App Style, others ignore some QSS stylesheet parameters
    app.setStyle('Windows')
    # w is gonna be the mymainwindow class
    w = MyMainWindow()
    # set the class with the attribute of translucent background as true
    if OPAQUE is True:
        w.setAttribute(Qt.WA_TranslucentBackground, True)
    # WM Borders
    if BORDER is True:
        w.setWindowFlags(w.windowFlags() | QtCore.Qt.FramelessWindowHint)
    # run the class
    w.show()
    # if exiting the loop take down the app
    sys.exit(app.exec_())


if __name__ == '__main__':
    ' Do NOT add anything here!, use main() function instead. '
    main()
