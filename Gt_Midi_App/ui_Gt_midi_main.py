# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Gt_midi_main.ui'
##
## Created by: Qt User Interface Compiler version 6.9.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QDial, QFrame,
    QGridLayout, QHBoxLayout, QLabel, QMainWindow,
    QMenu, QMenuBar, QPushButton, QSizePolicy,
    QSlider, QStatusBar, QTextEdit, QVBoxLayout,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1162, 731)
        self.actionOpen_Midi_Window = QAction(MainWindow)
        self.actionOpen_Midi_Window.setObjectName(u"actionOpen_Midi_Window")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.Device_label = QLabel(self.centralwidget)
        self.Device_label.setObjectName(u"Device_label")
        font = QFont()
        font.setPointSize(15)
        self.Device_label.setFont(font)

        self.horizontalLayout_2.addWidget(self.Device_label)

        self.device_combo = QComboBox(self.centralwidget)
        self.device_combo.setObjectName(u"device_combo")
        self.device_combo.setMinimumSize(QSize(400, 0))

        self.horizontalLayout_2.addWidget(self.device_combo)

        self.Channel_label = QLabel(self.centralwidget)
        self.Channel_label.setObjectName(u"Channel_label")
        self.Channel_label.setFont(font)

        self.horizontalLayout_2.addWidget(self.Channel_label)

        self.channel_combo = QComboBox(self.centralwidget)
        self.channel_combo.setObjectName(u"channel_combo")

        self.horizontalLayout_2.addWidget(self.channel_combo)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.frame_wave = QFrame(self.centralwidget)
        self.frame_wave.setObjectName(u"frame_wave")
        self.frame_wave.setMinimumSize(QSize(0, 200))
        self.frame_wave.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_wave.setFrameShadow(QFrame.Shadow.Raised)

        self.verticalLayout.addWidget(self.frame_wave)

        self.wave_slider = QSlider(self.centralwidget)
        self.wave_slider.setObjectName(u"wave_slider")
        self.wave_slider.setOrientation(Qt.Orientation.Horizontal)

        self.verticalLayout.addWidget(self.wave_slider)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.log = QTextEdit(self.centralwidget)
        self.log.setObjectName(u"log")

        self.horizontalLayout.addWidget(self.log)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setFont(font)
        self.label_3.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.label_3, 0, 0, 1, 1)

        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setFont(font)
        self.label_4.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.label_4, 0, 1, 1, 1)

        self.min_note_len_dial = QDial(self.centralwidget)
        self.min_note_len_dial.setObjectName(u"min_note_len_dial")

        self.gridLayout.addWidget(self.min_note_len_dial, 1, 0, 1, 1)

        self.amp_thresh_dial = QDial(self.centralwidget)
        self.amp_thresh_dial.setObjectName(u"amp_thresh_dial")

        self.gridLayout.addWidget(self.amp_thresh_dial, 1, 1, 1, 1)

        self.btn_record = QPushButton(self.centralwidget)
        self.btn_record.setObjectName(u"btn_record")

        self.gridLayout.addWidget(self.btn_record, 2, 0, 1, 1)

        self.btn_play = QPushButton(self.centralwidget)
        self.btn_play.setObjectName(u"btn_play")

        self.gridLayout.addWidget(self.btn_play, 2, 1, 1, 1)

        self.btn_load = QPushButton(self.centralwidget)
        self.btn_load.setObjectName(u"btn_load")

        self.gridLayout.addWidget(self.btn_load, 3, 0, 1, 1)

        self.btn_convert = QPushButton(self.centralwidget)
        self.btn_convert.setObjectName(u"btn_convert")

        self.gridLayout.addWidget(self.btn_convert, 3, 1, 1, 1)


        self.horizontalLayout.addLayout(self.gridLayout)


        self.verticalLayout.addLayout(self.horizontalLayout)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1162, 24))
        self.menuMidi_Pianoroll = QMenu(self.menubar)
        self.menuMidi_Pianoroll.setObjectName(u"menuMidi_Pianoroll")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuMidi_Pianoroll.menuAction())
        self.menuMidi_Pianoroll.addAction(self.actionOpen_Midi_Window)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionOpen_Midi_Window.setText(QCoreApplication.translate("MainWindow", u"Open Midi Window", None))
        self.Device_label.setText(QCoreApplication.translate("MainWindow", u"Device", None))
        self.Channel_label.setText(QCoreApplication.translate("MainWindow", u"Channel", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Note", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Threshold", None))
        self.btn_record.setText(QCoreApplication.translate("MainWindow", u"Rec", None))
        self.btn_play.setText(QCoreApplication.translate("MainWindow", u"Play", None))
        self.btn_load.setText(QCoreApplication.translate("MainWindow", u"Load", None))
        self.btn_convert.setText(QCoreApplication.translate("MainWindow", u"ToMIDI", None))
        self.menuMidi_Pianoroll.setTitle(QCoreApplication.translate("MainWindow", u"Midi Pianoroll", None))
    # retranslateUi

