# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 6.10.0
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
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QHBoxLayout,
    QLabel, QLayout, QLineEdit, QPushButton,
    QSizePolicy, QSlider, QSpacerItem, QVBoxLayout,
    QWidget)

class Ui_Widget(object):
    def setupUi(self, Widget):
        if not Widget.objectName():
            Widget.setObjectName(u"Widget")
        Widget.resize(339, 716)
        Widget.setMinimumSize(QSize(339, 716))
        Widget.setMaximumSize(QSize(339, 716))
        Widget.setStyleSheet(u"background-color: rgb(2, 13, 58);")
        self.verticalLayout_6 = QVBoxLayout(Widget)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, -1, -1, -1)
        self.verticalSpacer_2 = QSpacerItem(20, 70, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum)

        self.verticalLayout_4.addItem(self.verticalSpacer_2)

        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(9, -1, 9, -1)
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_2 = QLabel(Widget)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout.addWidget(self.label_2)

        self.lineEdit = QLineEdit(Widget)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setStyleSheet(u"QLineEdit {\n"
"	color: #fff;\n"
"	background-color: #193676;\n"
"	border: none;\n"
"	padding: 5;\n"
"}\n"
"QLineEdit:hover {\n"
" \n"
"	background-color: rgb(35, 77, 167);\n"
"}")

        self.verticalLayout.addWidget(self.lineEdit)

        self.label = QLabel(Widget)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label)

        self.comboBox = QComboBox(Widget)
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setStyleSheet(u"QComboBox {\n"
"    border: none;\n"
"	background-color: rgb(25, 54, 118);\n"
"    color: #FFFFFF;\n"
"	padding: 5;\n"
"}\n"
"\n"
"QComboBox:hover {\n"
"	background-color: rgb(32, 71, 153);\n"
"	border: 1px solid #FF6D12;\n"
"}\n"
"\n"
"QComboBox::drop-down {\n"
"	    subcontrol-origin: padding;\n"
"    	subcontrol-position: top right;\n"
"    	width: 20px;\n"
"		border:none;\n"
"   	    background: none;\n"
"}\n"
"\n"
"QComboBox QAbstractItemView {\n"
"    border: 1px solid #FF6D1;\n"
"}\n"
"\n"
"")

        self.verticalLayout.addWidget(self.comboBox)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_3 = QLabel(Widget)
        self.label_3.setObjectName(u"label_3")

        self.verticalLayout_2.addWidget(self.label_3)

        self.comboBox_2 = QComboBox(Widget)
        self.comboBox_2.setObjectName(u"comboBox_2")
        self.comboBox_2.setStyleSheet(u"QComboBox {\n"
"    border: none;\n"
"	background-color: rgb(25, 54, 118);\n"
"    color: #FFFFFF;\n"
"	padding: 5;\n"
"}\n"
"\n"
"QComboBox:hover {\n"
"	background-color: rgb(32, 71, 153);\n"
"	border: 1px solid #FF6D12;\n"
"}\n"
"\n"
"QComboBox::drop-down {\n"
"	    subcontrol-origin: padding;\n"
"    	subcontrol-position: top right;\n"
"    	width: 20px;\n"
"		border:none;\n"
"   	    background: none;\n"
"}\n"
"\n"
"QComboBox QAbstractItemView {\n"
"    border: 1px solid #FF6D1;\n"
"}\n"
"")

        self.verticalLayout_2.addWidget(self.comboBox_2)


        self.verticalLayout.addLayout(self.verticalLayout_2)


        self.verticalLayout_5.addLayout(self.verticalLayout)

        self.label_4 = QLabel(Widget)
        self.label_4.setObjectName(u"label_4")

        self.verticalLayout_5.addWidget(self.label_4)

        self.horizontalSlider = QSlider(Widget)
        self.horizontalSlider.setObjectName(u"horizontalSlider")
        self.horizontalSlider.setStyleSheet(u"QSlider::groove:horizontal {\n"
"    height: 2px;\n"
"    background: #ffffff;\n"
"    border-radius: 3px;\n"
"}\n"
"\n"
"QSlider::handle:horizontal {\n"
"    background: #FF9500;\n"
"    width: 15px;\n"
"    height: 10px;\n"
"    margin: -6px 0; \n"
"	border: 1px solid #0078d7;\n"
"	border-radius: 7px;\n"
"}\n"
"\n"
"QSlider::sub-page:horizontal {\n"
"    background: #3498db;\n"
"    border-radius: 3px;\n"
"}\n"
"\n"
"QSlider::add-page:horizontal {\n"
"    background: #eee;\n"
"    border-radius: 3px;\n"
"}\n"
"")
        self.horizontalSlider.setOrientation(Qt.Orientation.Horizontal)

        self.verticalLayout_5.addWidget(self.horizontalSlider)


        self.verticalLayout_4.addLayout(self.verticalLayout_5)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(9, 0, 9, -1)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(30, 10, QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.frame = QFrame(Widget)
        self.frame.setObjectName(u"frame")
        self.frame.setStyleSheet(u"border: none;\n"
"background-color: rgb(25, 54, 118);")
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayoutWidget = QWidget(self.frame)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(0, 0, 89, 30))
        self.horizontalLayout_3 = QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_4)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_2)

        self.frameColor = QFrame(self.horizontalLayoutWidget)
        self.frameColor.setObjectName(u"frameColor")
        self.frameColor.setMinimumSize(QSize(20, 20))
        self.frameColor.setMaximumSize(QSize(20, 20))
        self.frameColor.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.frameColor.setStyleSheet(u"border: none")
        self.frameColor.setFrameShape(QFrame.Shape.StyledPanel)
        self.frameColor.setFrameShadow(QFrame.Shadow.Raised)
        self.frameColor.setLineWidth(1)

        self.horizontalLayout_3.addWidget(self.frameColor)

        self.colorHex = QLabel(self.horizontalLayoutWidget)
        self.colorHex.setObjectName(u"colorHex")

        self.horizontalLayout_3.addWidget(self.colorHex)


        self.horizontalLayout.addWidget(self.frame)

        self.colorPick = QPushButton(Widget)
        self.colorPick.setObjectName(u"colorPick")
        self.colorPick.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.colorPick.setStyleSheet(u"background-color: rgb(255, 109, 18);\n"
"border: none;\n"
"height: 28")

        self.horizontalLayout.addWidget(self.colorPick)

        self.horizontalSpacer_3 = QSpacerItem(30, 20, QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_3)


        self.verticalLayout_3.addLayout(self.horizontalLayout)


        self.verticalLayout_4.addLayout(self.verticalLayout_3)

        self.verticalSpacer = QSpacerItem(20, 30, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer)

        self.horizontalFrame_2 = QFrame(Widget)
        self.horizontalFrame_2.setObjectName(u"horizontalFrame_2")
        self.horizontalFrame_2.setStyleSheet(u"background-color: rgb(255, 109, 18);")
        self.horizontalFrame_2.setLineWidth(1)
        self.horizontalLayout_2 = QHBoxLayout(self.horizontalFrame_2)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(1, -1, -1, -1)
        self.verticalSpacer_3 = QSpacerItem(1, 70, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum)

        self.horizontalLayout_2.addItem(self.verticalSpacer_3)

        self.horizontalSpacer_6 = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_6)

        self.pushButton_2 = QPushButton(self.horizontalFrame_2)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.pushButton_2.setStyleSheet(u"QPushButton {\n"
"	background-color: #112577;\n"
"	border: none;\n"
"	height: 34;\n"
"	width: 80;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"	\n"
"	border: 1px solid rgb(255, 109, 18); \n"
"}")

        self.horizontalLayout_2.addWidget(self.pushButton_2)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_5)


        self.verticalLayout_4.addWidget(self.horizontalFrame_2)


        self.verticalLayout_6.addLayout(self.verticalLayout_4)


        self.retranslateUi(Widget)

        QMetaObject.connectSlotsByName(Widget)
    # setupUi

    def retranslateUi(self, Widget):
        Widget.setWindowTitle(QCoreApplication.translate("Widget", u"Widget", None))
        self.label_2.setText(QCoreApplication.translate("Widget", u"\u0421\u0441\u044b\u043b\u043a\u0430 \u0434\u043b\u044f obs", None))
        self.label.setText(QCoreApplication.translate("Widget", u"\u0410\u0432\u0430\u0442\u0430\u0440\u044b", None))
        self.comboBox.setItemText(0, QCoreApplication.translate("Widget", u"\u041d\u043e\u0432\u044b\u0439 \u044d\u043b\u0435\u043c\u0435\u043d\u0442", None))
        self.comboBox.setItemText(1, QCoreApplication.translate("Widget", u"\u041d\u043e\u0432\u044b\u0439 \u044d\u043b\u0435\u043c\u0435\u043d\u0442", None))

        self.label_3.setText(QCoreApplication.translate("Widget", u"\u041c\u0438\u043a\u0440\u043e\u0444\u043e\u043d", None))
        self.label_4.setText(QCoreApplication.translate("Widget", u"\u0427\u0443\u0432\u0441\u0442\u0432\u0438\u0442\u0435\u043b\u044c\u043d\u043e\u0441\u0442\u044c", None))
        self.colorHex.setText(QCoreApplication.translate("Widget", u"#0000000", None))
        self.colorPick.setText(QCoreApplication.translate("Widget", u"\u0412\u044b\u0431\u0440\u0430\u0442\u044c \u0446\u0432\u0435\u0442", None))
        self.pushButton_2.setText(QCoreApplication.translate("Widget", u"\u041f\u0440\u0438\u043c\u0435\u043d\u0438\u0442\u044c", None))
    # retranslateUi

