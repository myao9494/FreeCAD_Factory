# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'WF_ObjParCurve2DEditGui_2016.ui'
#
# Created: Thu Feb  2 19:33:38 2017
#      by: PySide UI code generator 4.11.3
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(1039, 460)
        self.gridLayout_3 = QtGui.QGridLayout(Form)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.groupBox_2 = QtGui.QGroupBox(Form)
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.gridLayout = QtGui.QGridLayout(self.groupBox_2)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.button_load = QtGui.QPushButton(self.groupBox_2)
        self.button_load.setObjectName(_fromUtf8("button_load"))
        self.horizontalLayout.addWidget(self.button_load)
        self.button_save = QtGui.QPushButton(self.groupBox_2)
        self.button_save.setObjectName(_fromUtf8("button_save"))
        self.horizontalLayout.addWidget(self.button_save)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.gridLayout_3.addWidget(self.groupBox_2, 0, 0, 1, 1)
        self.tableWidget = QtGui.QTableWidget(Form)
        self.tableWidget.setObjectName(_fromUtf8("tableWidget"))
        self.tableWidget.setColumnCount(10)
        self.tableWidget.setRowCount(2)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(5, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(6, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(7, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(8, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(9, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setItem(0, 0, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setItem(0, 1, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setItem(0, 2, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setItem(0, 3, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setItem(0, 4, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setItem(0, 5, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setItem(0, 6, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setItem(0, 7, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setItem(0, 8, item)
        self.gridLayout_3.addWidget(self.tableWidget, 1, 0, 1, 1)
        self.groupBox = QtGui.QGroupBox(Form)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.gridLayout_2 = QtGui.QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.button_addRow = QtGui.QPushButton(self.groupBox)
        self.button_addRow.setObjectName(_fromUtf8("button_addRow"))
        self.horizontalLayout_2.addWidget(self.button_addRow)
        self.button_removeRow = QtGui.QPushButton(self.groupBox)
        self.button_removeRow.setObjectName(_fromUtf8("button_removeRow"))
        self.horizontalLayout_2.addWidget(self.button_removeRow)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.gridLayout_2.addLayout(self.horizontalLayout_2, 0, 0, 1, 1)
        self.gridLayout_3.addWidget(self.groupBox, 2, 0, 1, 1)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.comboBox_select = QtGui.QComboBox(Form)
        self.comboBox_select.setEnabled(False)
        self.comboBox_select.setMaximumSize(QtCore.QSize(0, 0))
        self.comboBox_select.setFrame(True)
        self.comboBox_select.setModelColumn(1)
        self.comboBox_select.setObjectName(_fromUtf8("comboBox_select"))
        self.horizontalLayout_4.addWidget(self.comboBox_select)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem2)
        self.gridLayout_3.addLayout(self.horizontalLayout_4, 3, 0, 1, 1)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.button_quit = QtGui.QPushButton(Form)
        self.button_quit.setObjectName(_fromUtf8("button_quit"))
        self.horizontalLayout_3.addWidget(self.button_quit)
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem3)
        self.gridLayout_3.addLayout(self.horizontalLayout_3, 4, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.groupBox_2.setTitle(_translate("Form", "2D Database", None))
        self.button_load.setToolTip(_translate("Form", "Click to load common and customs curves.", None))
        self.button_load.setText(_translate("Form", "Load", None))
        self.button_save.setToolTip(_translate("Form", "This will save customs curves only in your HOME directory under \"Parametric2D.dat\".", None))
        self.button_save.setText(_translate("Form", "Save", None))
        item = self.tableWidget.verticalHeaderItem(0)
        item.setText(_translate("Form", "1", None))
        item = self.tableWidget.verticalHeaderItem(1)
        item.setText(_translate("Form", "2", None))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Form", "Name", None))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Form", "a (t) ", None))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("Form", "b (a, t) ", None))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("Form", "X (a,b,c,t)", None))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("Form", "Y (a,b,c,t)", None))
        item = self.tableWidget.horizontalHeaderItem(5)
        item.setText(_translate("Form", "t min", None))
        item = self.tableWidget.horizontalHeaderItem(6)
        item.setText(_translate("Form", "t max", None))
        item = self.tableWidget.horizontalHeaderItem(7)
        item.setText(_translate("Form", "t step", None))
        item = self.tableWidget.horizontalHeaderItem(8)
        item.setText(_translate("Form", "Polar", None))
        item = self.tableWidget.horizontalHeaderItem(9)
        item.setText(_translate("Form", "Comments", None))
        __sortingEnabled = self.tableWidget.isSortingEnabled()
        self.tableWidget.setSortingEnabled(False)
        item = self.tableWidget.item(0, 0)
        item.setText(_translate("Form", "Circle", None))
        item = self.tableWidget.item(0, 1)
        item.setText(_translate("Form", "10 # Radius", None))
        item = self.tableWidget.item(0, 2)
        item.setText(_translate("Form", "a", None))
        item = self.tableWidget.item(0, 3)
        item.setText(_translate("Form", "a*cos(t)", None))
        item = self.tableWidget.item(0, 4)
        item.setText(_translate("Form", "a*sin(t)", None))
        item = self.tableWidget.item(0, 5)
        item.setText(_translate("Form", "0", None))
        item = self.tableWidget.item(0, 6)
        item.setText(_translate("Form", "2*pi", None))
        item = self.tableWidget.item(0, 7)
        item.setText(_translate("Form", "0.01", None))
        item = self.tableWidget.item(0, 8)
        item.setText(_translate("Form", "0", None))
        self.tableWidget.setSortingEnabled(__sortingEnabled)
        self.groupBox.setTitle(_translate("Form", "Row", None))
        self.button_addRow.setToolTip(_translate("Form", "Add a row into the table.", None))
        self.button_addRow.setText(_translate("Form", "add", None))
        self.button_removeRow.setToolTip(_translate("Form", "Remove a row from the table.", None))
        self.button_removeRow.setText(_translate("Form", "remove", None))
        self.button_quit.setText(_translate("Form", "Quit", None))

