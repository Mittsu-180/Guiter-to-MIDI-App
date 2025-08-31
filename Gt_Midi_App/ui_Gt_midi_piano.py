# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Gt_midi_piano.ui'
##
## Created by: Qt User Interface Compiler version 6.9.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QLabel, QSizePolicy,
    QSlider, QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(912, 519)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.Pianoroll_label = QLabel(Form)
        self.Pianoroll_label.setObjectName(u"Pianoroll_label")
        self.Pianoroll_label.setMaximumSize(QSize(16777215, 100))
        font = QFont()
        font.setPointSize(15)
        self.Pianoroll_label.setFont(font)

        self.verticalLayout.addWidget(self.Pianoroll_label)

        self.frame_piano = QFrame(Form)
        self.frame_piano.setObjectName(u"frame_piano")
        self.frame_piano.setMinimumSize(QSize(0, 250))
        self.frame_piano.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_piano.setFrameShadow(QFrame.Shadow.Raised)

        self.verticalLayout.addWidget(self.frame_piano)

        self.midi_slider = QSlider(Form)
        self.midi_slider.setObjectName(u"midi_slider")
        self.midi_slider.setOrientation(Qt.Orientation.Horizontal)

        self.verticalLayout.addWidget(self.midi_slider)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.Pianoroll_label.setText(QCoreApplication.translate("Form", u"Pianoroll", None))
    # retranslateUi

