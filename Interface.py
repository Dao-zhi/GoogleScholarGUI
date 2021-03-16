# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets    # Qt核心模块
from PyQt5.QtWidgets import QFileDialog, QGraphicsPixmapItem, QGraphicsItem, QGraphicsView, QGraphicsTextItem   # 文件对话框
from PyQt5.QtCore import QFile, QSize     # 文件模块
from PyQt5.QtGui import QFont
import sys
import os
from lxml import etree
import datetime    # 用于读取当前时间
import GoogleScholar    # 爬取主体代码
import PDFDownload
import threading
import urllib    # 用于URL编码与解码
import gc    # 用于垃圾回收
import time    # 用于延时

class MainWindow(QtWidgets.QMainWindow):#继承自父类QtWidgets.QWidget
    def closeEvent(self,event):#函数名固定不可变
        reply=QtWidgets.QMessageBox.question(self,u'警告',u'确认退出?',QtWidgets.QMessageBox.Yes,QtWidgets.QMessageBox.No)
        if reply==QtWidgets.QMessageBox.Yes:
            event.accept()#关闭窗口
        else:
            event.ignore()#忽视点击X事件

class Ui_Widget(QtWidgets.QMainWindow):
    pauseFlag = threading.Event()     # 用于暂停线程的标识
    pauseFlag.set()       # 设置为false
    exitFlag = threading.Event()      # 用于停止线程的标识
    exitFlag.clear()      # 将__exitFlag设置为false
    url_head = ''    # url头部
    url_tail = ''    # url尾部
    updated = QtCore.pyqtSignal(str)    # 用于textEdit在子线程中更新的信号量
    startFlag = False    # 用于控制开始按钮的各种功能

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        desktop = QtWidgets.QDesktopWidget()
        current_monitor = desktop.screenNumber(self)
        rect = desktop.screenGeometry(current_monitor)
        width = rect.width()
        if width == 1920:
            MainWindow.resize(680, 870)
        else:
            MainWindow.resize(824, 1185)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.groupBox_2)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.splitter = QtWidgets.QSplitter(self.groupBox_2)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.checkBoxSavePDFLink = QtWidgets.QCheckBox(self.splitter)
        self.checkBoxSavePDFLink.setObjectName("checkBoxSavePDFLink")
        self.checkBoxDownloadPDF = QtWidgets.QCheckBox(self.splitter)
        self.checkBoxDownloadPDF.setObjectName("checkBoxDownloadPDF")
        self.label_7 = QtWidgets.QLabel(self.splitter)
        self.label_7.setMaximumSize(QtCore.QSize(192, 16777215))
        self.label_7.setObjectName("label_7")
        self.spinBoxDownloadThreads = QtWidgets.QSpinBox(self.splitter)
        self.spinBoxDownloadThreads.setProperty("value", 12)
        self.spinBoxDownloadThreads.setObjectName("spinBoxDownloadThreads")
        self.gridLayout_3.addWidget(self.splitter, 0, 0, 1, 2)
        self.label_6 = QtWidgets.QLabel(self.groupBox_2)
        self.label_6.setObjectName("label_6")
        self.gridLayout_3.addWidget(self.label_6, 1, 0, 1, 1)
        self.lineEditResultSaveFile = QtWidgets.QLineEdit(self.groupBox_2)
        self.lineEditResultSaveFile.setObjectName("lineEditResultSaveFile")
        self.gridLayout_3.addWidget(self.lineEditResultSaveFile, 1, 1, 1, 1)
        self.pushButtonSelectResultSaveFile = QtWidgets.QPushButton(self.groupBox_2)
        self.pushButtonSelectResultSaveFile.setObjectName("pushButtonSelectResultSaveFile")
        self.gridLayout_3.addWidget(self.pushButtonSelectResultSaveFile, 1, 2, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.groupBox_2)
        self.label_8.setObjectName("label_8")
        self.gridLayout_3.addWidget(self.label_8, 2, 0, 1, 1)
        self.lineEditLinkSaveFile = QtWidgets.QLineEdit(self.groupBox_2)
        self.lineEditLinkSaveFile.setObjectName("lineEditLinkSaveFile")
        self.gridLayout_3.addWidget(self.lineEditLinkSaveFile, 2, 1, 1, 1)
        self.pushButtonSelectLinkSaveFile = QtWidgets.QPushButton(self.groupBox_2)
        self.pushButtonSelectLinkSaveFile.setObjectName("pushButtonSelectLinkSaveFile")
        self.gridLayout_3.addWidget(self.pushButtonSelectLinkSaveFile, 2, 2, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.groupBox_2)
        self.label_9.setObjectName("label_9")
        self.gridLayout_3.addWidget(self.label_9, 3, 0, 1, 1)
        self.lineEditPDFSavePath = QtWidgets.QLineEdit(self.groupBox_2)
        self.lineEditPDFSavePath.setObjectName("lineEditPDFSavePath")
        self.gridLayout_3.addWidget(self.lineEditPDFSavePath, 3, 1, 1, 1)
        self.pushButtonSelectPDFSavePath = QtWidgets.QPushButton(self.groupBox_2)
        self.pushButtonSelectPDFSavePath.setObjectName("pushButtonSelectPDFSavePath")
        self.gridLayout_3.addWidget(self.pushButtonSelectPDFSavePath, 3, 2, 1, 1)
        self.gridLayout.addWidget(self.groupBox_2, 1, 0, 1, 1)
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)
        self.lineEditSearchContent = QtWidgets.QLineEdit(self.groupBox)
        self.lineEditSearchContent.setObjectName("lineEditSearchContent")
        self.gridLayout_2.addWidget(self.lineEditSearchContent, 0, 1, 1, 6)
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 0, 7, 1, 1)
        self.spinBoxSearchPages = QtWidgets.QSpinBox(self.groupBox)
        self.spinBoxSearchPages.setProperty("value", 30)    # 爬取页数的默认值
        self.spinBoxSearchPages.setObjectName("spinBoxSearchPages")
        self.gridLayout_2.addWidget(self.spinBoxSearchPages, 0, 8, 1, 1)
        self.checkBoxPatent = QtWidgets.QCheckBox(self.groupBox)
        self.checkBoxPatent.setObjectName("checkBoxPatent")
        self.gridLayout_2.addWidget(self.checkBoxPatent, 1, 0, 1, 2)
        self.checkBoxQuote = QtWidgets.QCheckBox(self.groupBox)
        self.checkBoxQuote.setObjectName("checkBoxQuote")
        self.gridLayout_2.addWidget(self.checkBoxQuote, 1, 2, 1, 1)
        self.checkBoxDetails = QtWidgets.QCheckBox(self.groupBox)
        self.checkBoxDetails.setObjectName("checkBoxDetails")
        self.gridLayout_2.addWidget(self.checkBoxDetails, 1, 4, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 1, 6, 1, 1)
        self.comboBoxSort = QtWidgets.QComboBox(self.groupBox)
        self.comboBoxSort.setObjectName("comboBoxSort")
        self.comboBoxSort.addItem("")
        self.comboBoxSort.addItem("")
        self.gridLayout_2.addWidget(self.comboBoxSort, 1, 7, 1, 2)
        self.label_4 = QtWidgets.QLabel(self.groupBox)
        self.label_4.setObjectName("label_4")
        self.gridLayout_2.addWidget(self.label_4, 2, 0, 1, 1)
        self.spinBoxTimeStart = QtWidgets.QSpinBox(self.groupBox)
        self.spinBoxTimeStart.setObjectName("spinBoxTimeStart")
        self.gridLayout_2.addWidget(self.spinBoxTimeStart, 2, 2, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.groupBox)
        self.label_5.setObjectName("label_5")
        self.gridLayout_2.addWidget(self.label_5, 2, 3, 1, 1)
        self.spinBoxTimeEnd = QtWidgets.QSpinBox(self.groupBox)
        self.spinBoxTimeEnd.setObjectName("spinBoxTimeend")
        self.gridLayout_2.addWidget(self.spinBoxTimeEnd, 2, 4, 1, 1)
        self.checkBoxAnyTime = QtWidgets.QCheckBox(self.groupBox)
        self.checkBoxAnyTime.setObjectName("checkBoxAnyTime")
        self.gridLayout_2.addWidget(self.checkBoxAnyTime, 2, 5, 1, 1)
        self.gridLayout.addWidget(self.groupBox, 0, 0, 1, 1)
        self.groupBox_3 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_3.setObjectName("groupBox_3")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.groupBox_3)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.label_10 = QtWidgets.QLabel(self.groupBox_3)
        self.label_10.setObjectName("label_10")
        self.gridLayout_4.addWidget(self.label_10, 0, 0, 1, 2)
        self.label_11 = QtWidgets.QLabel(self.groupBox_3)
        self.label_11.setObjectName("label_11")
        self.gridLayout_4.addWidget(self.label_11, 1, 0, 1, 1)
        self.lineEditAgents = QtWidgets.QLineEdit(self.groupBox_3)
        self.lineEditAgents.setObjectName("lineEditAgents")
        self.gridLayout_4.addWidget(self.lineEditAgents, 1, 1, 1, 1)
        self.pushButtonSelectAgents = QtWidgets.QPushButton(self.groupBox_3)
        self.pushButtonSelectAgents.setObjectName("pushButtonSelectAgents")
        self.gridLayout_4.addWidget(self.pushButtonSelectAgents, 1, 2, 1, 1)
        self.checkBoxAgentsFlag = QtWidgets.QCheckBox(self.groupBox_3)
        self.checkBoxAgentsFlag.setObjectName("checkBoxAgentsFlag")
        self.gridLayout_4.addWidget(self.checkBoxAgentsFlag, 1, 3, 1, 1)
        self.label_12 = QtWidgets.QLabel(self.groupBox_3)
        self.label_12.setObjectName("label_12")
        self.gridLayout_4.addWidget(self.label_12, 2, 0, 1, 1)
        self.lineEditDomains = QtWidgets.QLineEdit(self.groupBox_3)
        self.lineEditDomains.setObjectName("lineEditDomains")
        self.gridLayout_4.addWidget(self.lineEditDomains, 2, 1, 1, 1)
        self.pushButtonSelectDomains = QtWidgets.QPushButton(self.groupBox_3)
        self.pushButtonSelectDomains.setObjectName("pushButtonSelectDomains")
        self.gridLayout_4.addWidget(self.pushButtonSelectDomains, 2, 2, 1, 1)
        self.checkBoxDomainsFlag = QtWidgets.QCheckBox(self.groupBox_3)
        self.checkBoxDomainsFlag.setObjectName("checkBoxDomainsFlag")
        self.gridLayout_4.addWidget(self.checkBoxDomainsFlag, 2, 3, 1, 1)
        self.label_13 = QtWidgets.QLabel(self.groupBox_3)
        self.label_13.setObjectName("label_13")
        self.gridLayout_4.addWidget(self.label_13, 3, 0, 1, 1)
        self.lineEditIPs = QtWidgets.QLineEdit(self.groupBox_3)
        self.lineEditIPs.setObjectName("lineEditIPs")
        self.gridLayout_4.addWidget(self.lineEditIPs, 3, 1, 1, 1)
        self.pushButtonSelectIPs = QtWidgets.QPushButton(self.groupBox_3)
        self.pushButtonSelectIPs.setObjectName("pushButtonSelectIPs")
        self.gridLayout_4.addWidget(self.pushButtonSelectIPs, 3, 2, 1, 1)
        self.checkBoxIPsFlag = QtWidgets.QCheckBox(self.groupBox_3)
        self.checkBoxIPsFlag.setObjectName("checkBoxIPsFlag")
        self.gridLayout_4.addWidget(self.checkBoxIPsFlag, 3, 3, 1, 1)
        self.gridLayout.addWidget(self.groupBox_3, 2, 0, 1, 1)
        self.groupBox_5 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_5.setObjectName("groupBox_5")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.groupBox_5)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.textEditLog = QtWidgets.QTextEdit(self.groupBox_5)
        self.textEditLog.setObjectName("textEditLog")
        self.gridLayout_5.addWidget(self.textEditLog, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBox_5, 4, 0, 1, 1)
        self.groupBox_4 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_4.setObjectName("groupBox_4")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.groupBox_4)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.progressBar = QtWidgets.QProgressBar(self.groupBox_4)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.horizontalLayout.addWidget(self.progressBar)
        self.pushButtonCancel = QtWidgets.QPushButton(self.groupBox_4)
        self.pushButtonCancel.setObjectName("pushButtonCancel")
        self.horizontalLayout.addWidget(self.pushButtonCancel)
        self.pushButtonStart = QtWidgets.QPushButton(self.groupBox_4)
        self.pushButtonStart.setObjectName("pushButtonStart")
        self.horizontalLayout.addWidget(self.pushButtonStart)
        self.gridLayout.addWidget(self.groupBox_4, 3, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1050, 30))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # 链接按钮与对应的槽函数
        self.pushButtonSelectResultSaveFile.clicked.connect(self.selectResultSaveFile)
        self.pushButtonSelectLinkSaveFile.clicked.connect(self.selectLinkSaveFile)
        self.pushButtonSelectPDFSavePath.clicked.connect(self.selectPDFSavePath)
        self.pushButtonSelectAgents.clicked.connect(self.selectAgents)
        self.pushButtonSelectDomains.clicked.connect(self.selectDomains)
        self.pushButtonSelectIPs.clicked.connect(self.selectIPs)
        self.checkBoxAnyTime.stateChanged.connect(self.setAnyTime)
        self.checkBoxSavePDFLink.stateChanged.connect(self.setSavePDFLink)
        self.checkBoxDownloadPDF.stateChanged.connect(self.setSavePDF)
        self.pushButtonStart.clicked.connect(self.start)
        self.pushButtonCancel.clicked.connect(self.stop)
        self.checkBoxAgentsFlag.stateChanged.connect(self.setAgents)
        self.checkBoxDomainsFlag.stateChanged.connect(self.setDomains)
        self.checkBoxIPsFlag.stateChanged.connect(self.setIPs)

        self.updated.connect(self.updateText)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "谷歌学术自动爬取"))
        self.groupBox_2.setTitle(_translate("MainWindow", "导出设置"))
        self.checkBoxSavePDFLink.setText(_translate("MainWindow", "是否导出PDF链接到文件"))
        self.checkBoxDownloadPDF.setText(_translate("MainWindow", "是否自动下载PDF"))
        self.label_7.setText(_translate("MainWindow", "下载线程数"))
        self.label_6.setText(_translate("MainWindow", "爬取结果导出"))
        self.lineEditResultSaveFile.setText(_translate("MainWindow", 'C:/Users/' + os.environ['USERNAME'] + r'/Downloads/GoogleScholar/Results.xlsx'))
        self.pushButtonSelectResultSaveFile.setText(_translate("MainWindow", "选择文件"))
        self.label_8.setText(_translate("MainWindow", "PDF链接存储文件"))
        self.lineEditLinkSaveFile.setText(_translate("MainWindow", 'C:/Users/' + os.environ['USERNAME'] + r'/Downloads/GoogleScholar/PDFList.txt'))
        self.pushButtonSelectLinkSaveFile.setText(_translate("MainWindow", "选择文件"))
        self.label_9.setText(_translate("MainWindow", "PDF保存路径"))
        self.lineEditPDFSavePath.setText(_translate("MainWindow", 'C:/Users/' + os.environ['USERNAME'] + r'/Downloads/GoogleScholar/PDF'))
        self.pushButtonSelectPDFSavePath.setText(_translate("MainWindow", "选择路径"))
        self.groupBox.setTitle(_translate("MainWindow", "搜索设置"))
        self.label.setText(_translate("MainWindow", "搜索内容"))
        self.lineEditSearchContent.setText(_translate("MainWindow", ""))    # 爬取内容的默认值
        self.label_2.setText(_translate("MainWindow", "爬取页数"))
        self.checkBoxPatent.setText(_translate("MainWindow", "包括专利"))
        self.checkBoxQuote.setText(_translate("MainWindow", "包括引用"))
        self.checkBoxDetails.setText(_translate("MainWindow", "是否爬取论文详情"))
        self.label_3.setText(_translate("MainWindow", "排序方式"))
        self.comboBoxSort.setItemText(0, _translate("MainWindow", "按相关性排序"))
        self.comboBoxSort.setItemText(1, _translate("MainWindow", "按时间排序"))
        self.label_4.setText(_translate("MainWindow", "发表时间"))
        self.spinBoxTimeStart.setMaximum(5000)
        self.spinBoxTimeEnd.setMaximum(5000)
        self.spinBoxTimeStart.setMinimum(0)
        self.spinBoxTimeEnd.setMinimum(0)
        self.spinBoxTimeStart.setValue(2010)
        self.spinBoxTimeEnd.setValue(datetime.datetime.now().year)
        self.label_5.setText(_translate("MainWindow", "-"))
        self.checkBoxAnyTime.setText(_translate("MainWindow", "时间不限"))
        self.groupBox_3.setTitle(_translate("MainWindow", "防反爬设置"))
        self.label_10.setText(_translate("MainWindow", "非专业人士请勿自行设置"))
        self.label_11.setText(_translate("MainWindow", "随机agents"))
        self.lineEditAgents.setText(_translate("MainWindow", "agents.txt"))
        self.pushButtonSelectAgents.setText(_translate("MainWindow", "选择文件"))
        self.checkBoxAgentsFlag.setText(_translate("MainWindow", "启用"))
        self.label_12.setText(_translate("MainWindow", "随机谷歌域名"))
        self.lineEditDomains.setText(_translate("MainWindow", "domains.txt"))
        self.pushButtonSelectDomains.setText(_translate("MainWindow", "选择文件"))
        self.checkBoxDomainsFlag.setText(_translate("MainWindow", "启用"))
        self.label_13.setText(_translate("MainWindow", "IP代理池"))
        self.lineEditIPs.setText(_translate("MainWindow", "ips.txt"))
        self.pushButtonSelectIPs.setText(_translate("MainWindow", "选择文件"))
        self.checkBoxIPsFlag.setText(_translate("MainWindow", "启用"))
        self.groupBox_5.setTitle(_translate("MainWindow", "日志"))
        self.groupBox_4.setTitle(_translate("MainWindow", "操作"))
        self.pushButtonCancel.setText(_translate("MainWindow", "取消"))
        self.pushButtonStart.setText(_translate("MainWindow", "开始"))

        # 设置几个LineEdit为不可编辑
        self.lineEditLinkSaveFile.setEnabled(False)    # 禁止编辑文本
        self.pushButtonSelectLinkSaveFile.setEnabled(False)    # 禁止点击按钮
        self.lineEditPDFSavePath.setEnabled(False)    # 禁止编辑文本
        self.pushButtonSelectPDFSavePath.setEnabled(False)    # 禁止点击按钮
        self.lineEditLinkSaveFile.setEnabled(False)
        self.pushButtonSelectLinkSaveFile.setEnabled(False)
        self.lineEditPDFSavePath.setEnabled(False)
        self.pushButtonSelectPDFSavePath.setEnabled(False)
        self.lineEditLinkSaveFile.setText("")
        self.lineEditPDFSavePath.setText("")
        self.lineEditAgents.setEnabled(False)
        self.pushButtonSelectAgents.setEnabled(False)
        self.lineEditDomains.setEnabled(False)
        self.pushButtonSelectDomains.setEnabled(False)
        self.lineEditIPs.setEnabled(False)
        self.pushButtonSelectIPs.setEnabled(False)

    # 选择爬取结果导出文件
    def selectResultSaveFile(self):
        fileName, filetype = QFileDialog.getSaveFileName(self,
                                    "选取文件",
                                    "./",
                                    "Text Files (*.xlsx);;All Files (*)")   #设置文件扩展名过滤,注意用双分号间隔
        self.lineEditResultSaveFile.setText(fileName)
        if fileName=="":
            self.lineEditResultSaveFile.setText(r'C:/Users/' + os.environ['USERNAME'] + r'/Downloads/GoogleScholar/Results.xlsx')
    
    # 选择PDF链接保存文件
    def selectLinkSaveFile(self):
        fileName, filetype = QFileDialog.getSaveFileName(self,
                                    "选取文件",
                                    "./",
                                    "Text Files (*.txt);;All Files (*)")   #设置文件扩展名过滤,注意用双分号间隔
        self.lineEditLinkSaveFile.setText(fileName)
        if fileName=="":
            self.lineEditLinkSaveFile.setText(r'C:/Users/' + os.environ['USERNAME'] + r'/Downloads/GoogleScholar/PDFList.txt')
    
    # 选择PDF保存文件夹
    def selectPDFSavePath(self):
        fileName =  QFileDialog.getExistingDirectory()    # 选择路径
        self.lineEditPDFSavePath.setText(fileName)
        if fileName=="":
            self.lineEditPDFSavePath.setText(r'C:/Users/' + os.environ['USERNAME'] + r'/Downloads/GoogleScholar/PDF')

    # 选择agents保存文件
    def selectAgents(self):
        fileName, filetype = QFileDialog.getOpenFileName(self,
                                    "选取文件",
                                    "./",
                                    "Text Files (*.txt);;All Files (*)")   #设置文件扩展名过滤,注意用双分号间隔
        self.lineEditAgents.setText(fileName)
        if fileName=="":
            self.lineEditAgents.setText(r"agents.txt")

    # 选择domains保存文件
    def selectDomains(self):
        fileName, filetype = QFileDialog.getOpenFileName(self,
                                    "选取文件",
                                    "./",
                                    "Text Files (*.txt);;All Files (*)")   #设置文件扩展名过滤,注意用双分号间隔
        self.lineEditDomains.setText(fileName)
        if fileName=="":
            self.lineEditDomains.setText(r"domains.txt")

    # 选择ips保存文件
    def selectIPs(self):
        fileName, filetype = QFileDialog.getOpenFileName(self,
                                    "选取文件",
                                    "./",
                                    "Text Files (*.txt);;All Files (*)")   #设置文件扩展名过滤,注意用双分号间隔
        self.lineEditIPs.setText(fileName)
        if fileName=="":
            self.lineEditIPs.setText(r"ips.txt")

    # 设置时间不限点击效果
    def setAnyTime(self):
        # self.textEditLog.append(str(self.checkBoxAnyTime.isChecked()))
        if self.checkBoxAnyTime.isChecked():
            # self.spinBoxTimeStart.setValue("")
            self.spinBoxTimeStart.setEnabled(False)
            self.spinBoxTimeEnd.setEnabled(False)
        else:
            # self.spinBoxTimeStart.setValue("2010")
            self.spinBoxTimeStart.setEnabled(True)
            self.spinBoxTimeEnd.setEnabled(True)

    # 设置导出PDF链接到文件
    def setSavePDFLink(self):
        if self.checkBoxSavePDFLink.isChecked():
            self.lineEditLinkSaveFile.setText(r'C:/Users/' + os.environ['USERNAME'] + r'/Downloads/GoogleScholar/PDFList.txt')
            self.lineEditLinkSaveFile.setEnabled(True)
            self.pushButtonSelectLinkSaveFile.setEnabled(True)
        else:
            self.lineEditLinkSaveFile.setText("")
            self.lineEditLinkSaveFile.setEnabled(False)
            self.pushButtonSelectLinkSaveFile.setEnabled(False)

    # 设置自动下载PDF
    def setSavePDF(self):
        if self.checkBoxDownloadPDF.isChecked():
            self.lineEditPDFSavePath.setText(r'C:/Users/' + os.environ['USERNAME'] + r'/Downloads/GoogleScholar/PDF')
            self.lineEditPDFSavePath.setEnabled(True)
            self.pushButtonSelectPDFSavePath.setEnabled(True)
        else:
            self.lineEditPDFSavePath.setText("")
            self.lineEditPDFSavePath.setEnabled(False)
            self.pushButtonSelectPDFSavePath.setEnabled(False)

    # 启用agents
    def setAgents(self):
        if self.checkBoxAgentsFlag.isChecked():
            self.lineEditAgents.setEnabled(True)
            self.pushButtonSelectAgents.setEnabled(True)
        else:
            self.lineEditAgents.setEnabled(False)
            self.pushButtonSelectAgents.setEnabled(False)

    # 启用domains
    def setDomains(self):
        if self.checkBoxDomainsFlag.isChecked():
            self.lineEditDomains.setEnabled(True)
            self.pushButtonSelectDomains.setEnabled(True)
        else:
            self.lineEditDomains.setEnabled(False)
            self.pushButtonSelectDomains.setEnabled(False)

    # 启用ips
    def setIPs(self):
        if self.checkBoxIPsFlag.isChecked():
            self.lineEditIPs.setEnabled(True)
            self.pushButtonSelectIPs.setEnabled(True)
        else:
            self.lineEditIPs.setEnabled(False)
            self.pushButtonSelectIPs.setEnabled(False)

    def start(self):
        if not self.startFlag:    # 线程没有启动，启动线程
            self.startFlag = True
            self.pushButtonStart.setText('暂停')
            self.pauseFlag.set()    # 开始运行
            self.exitFlag.clear()
            self.progressBar.setValue(0)
            # 读取设置信息
            # 搜索设置
            searchContent = self.lineEditSearchContent.text()    # 搜索内容
            searchPages = self.spinBoxSearchPages.value()    # 搜索页数
            containPatent = self.checkBoxPatent.isChecked()    # 是否包含专利
            containQuote = self.checkBoxQuote.isChecked()    # 是否包含引用
            detailFlag = self.checkBoxDetails.isChecked()    # 是否爬取论文详情
            sortMethod = self.comboBoxSort.currentText()    # 排序方式
            startTime = self.spinBoxTimeStart.value()    # 开始时间
            endTime = self.spinBoxTimeEnd.value()    # 结束时间
            anyTime = self.checkBoxAnyTime.isChecked()    # 时间不限
            
            # 导出设置
            savePDFLink = self.checkBoxSavePDFLink.isChecked()    # 是否导出PDF链接到文件
            downloadPDF = self.checkBoxDownloadPDF.isChecked()    # 是否自动下载PDF
            downloadThreads = self.spinBoxDownloadThreads.value()    # 下载线程数
            resultsSaveFile = self.lineEditResultSaveFile.text()    # 爬取结果导出文件
            linkSaveFile = self.lineEditLinkSaveFile.text()    # PDF链接保存文件
            pdfSavePath = self.lineEditPDFSavePath.text()    # PDF保存路径
    
            # 防反爬设置
            agentsFile = self.lineEditAgents.text()    # 随机agents
            domainsFile = self.lineEditDomains.text()    # 随机谷歌域名
            ipsFile = self.lineEditIPs.text()    # IP代理池
            agentsFlag = self.checkBoxAgentsFlag.isChecked()    # 是否启用随机agents
            domainsFlag = self.checkBoxDomainsFlag.isChecked()    # 是否启用随机谷歌域名
            ipsFlag = self.checkBoxIPsFlag.isChecked()    # 是否启用IP代理池
    
            # 输出配置信息
            # 输出搜索设置
            self.textEditLog.append('------------------------------------搜索设置------------------------------------')
            self.textEditLog.append('搜索内容：' + searchContent)
            self.textEditLog.append('爬取页数：' + str(searchPages) + '页')
            self.textEditLog.append('是否包括专利：' + ("是" if containPatent else "否"))
            self.textEditLog.append('是否包括引用：' + ("是" if containQuote else "否"))
            self.textEditLog.append('是否爬取论文详情：' + ("是" if containQuote else "否"))
            self.textEditLog.append('排序方式：' + sortMethod)
            self.textEditLog.append('发表时间：' + ("时间不限" if anyTime else str(startTime) + '-' + str(endTime)))
    
            # 输出导出设置
            self.textEditLog.append('------------------------------------导出设置------------------------------------')
            self.textEditLog.append('是否导出PDF链接到文件：' + ("是" if savePDFLink else "否"))
            self.textEditLog.append('是否自动下载PDF：' + ("是" if downloadPDF else "否"))
            self.textEditLog.append('下载线程数' + str(downloadThreads))
            self.textEditLog.append('爬取结果导出文件：' + resultsSaveFile)
            if savePDFLink:
                self.textEditLog.append('PDF链接存储文件：' + linkSaveFile)
            if downloadPDF:
                self.textEditLog.append('PDF保存路径：' + pdfSavePath)
    
            # 输出防反爬设置
            self.textEditLog.append('-----------------------------------防反爬设置-----------------------------------')
            self.textEditLog.append('是否开启随机Agents：' + ("是" if agentsFlag else "否"))
            self.textEditLog.append('是否开启随机谷歌域名：' + ("是" if domainsFlag else "否"))
            self.textEditLog.append('是否开启IP代理池：' + ("是" if ipsFlag else "否"))
            if agentsFlag:
                self.textEditLog.append('随机Agents文件：' + agentsFile)
            if domainsFlag:
                self.textEditLog.append('随机谷歌域名文件：' + domainsFile)
            if domainsFlag:
                self.textEditLog.append('IP代理池文件：' + ipsFile)
    
            # 组装URL，太太太气人了，谷歌学术又访问不了了
            # 链接https://scholar.google.com.hk/scholar?hl=zh-CN&as_sdt=0%2C5&q=%E2%80%9CEntrepreneurial+failure%E2%80%9D+OR+%E2%80%9Cbusiness+failure%E2%80%9D&btnG=
            # 新链接https://scholar.google.com.hk/scholar?start=0&q=%E2%80%9CEntrepreneurial+failure%E2%80%9D+OR+%E2%80%9Cbusiness+failure%E2%80%9D&hl=zh-CN&as_sdt=1,47&as_ylo=2010&as_vis=1
            self.url_head = r'https://scholar.google.com.hk/scholar?hl=zh-CN'
            self.url_tail = ''
            self.url_tail = self.url_tail + '&q=' + urllib.parse.quote(searchContent)    # 设置搜索的问题
            # 限定时间
            if not anyTime:
                self.url_tail = self.url_tail + '&as_ylo=' + str(startTime)
                if not (datetime.datetime.now().year == endTime):
                    self.url_tail = self.url_tail + '&as_yhi=' + str(endTime)
            # 设置排序方式
            if sortMethod == '按时间排序':
                self.url_tail = self.url_tail + '&scisbd=2'
            # 设置是否包含专利
            if not containPatent:
                self.url_tail = self.url_tail + '&as_sdt=1'
            # 设置是否包含引用
            if not containQuote:
                self.url_tail = self.url_tail + '&as_vis=1'
            
            # 开始爬取
            # self.start_crawler()    # 单线程的实现方式，已改用多线程
            # 创建爬虫线程
            try:
                new_thread = threading.Thread(target=self.start_crawler)#创建线程
                new_thread.setDaemon(True)#设置为后台线程，这里默认是False，设置为True之后则主线程不用等待子线程
                new_thread.start()    #开启线程
                # new_thread.join()
            except:
               self.textEditLog.append('Error: unable to start thread')
        elif self.startFlag and self.pushButtonStart.text() == '暂停':
            self.pushButtonStart.setText('继续')
            self.pause()    # 唤醒线程
        elif self.startFlag and self.pushButtonStart.text() == '继续':
            self.pushButtonStart.setText('暂停')
            self.resume()    # 唤醒线程
        gc.collect()
        return

    def start_crawler(self): # url_head, url_tail, self
        # while self.__running.isSet():
            # self.__flag.wait()      # 为True时立即返回, 为False时阻塞直到内部的标识位为True后返回
        pre_time = GoogleScholar.cal_time(self.spinBoxSearchPages.value())
        # self.textEditLog.append('开始爬取...\n大约需要 {}min ，请耐心等待！'.format(pre_time))#子线程更新不了
        self.updated.emit('\n\n开始爬取...\n大约需要 {}min ，请耐心等待！'.format(pre_time))
        pages = self.spinBoxSearchPages.value()    # 获取爬取的页数
        file_path = self.lineEditResultSaveFile.text()    # 获取结果保存文件
        detailFlag = self.checkBoxDetails.isChecked()    # 是否爬取论文详情
        pdfSavePath = self.lineEditPDFSavePath.text()    # PDF下载保存路径
        # 循环提取多页的内容
        with open('./config/config.txt', 'r', encoding='utf-8') as proxy_file:  # 打开文件
            lines = proxy_file.readlines()  # 读取所有行
            proxy = {'https': 'https://' + lines[0].replace('\n', ''),'http': 'http://' + lines[0].replace('\n', '')}
            agent = lines[1].replace('\n', '')
            cookie = lines[2].replace('\n', '')
            print('[config] cookie: {}'.format(cookie))
            print('[config] agent: {}'.format(agent))
            # 如果没有设置随机IP代理池，就从配置文件中读取一个
            if not self.checkBoxIPsFlag.isChecked():
                print('[config] ips:{}'.format(proxy))
            
        
        for page_count in range(0, pages):
            # 设置随机agents，随机谷歌域名，IP代理池，这块儿先用不到，以后再开
            # 随机生成UA
            if self.checkBoxAgentsFlag.isChecked():
                agents = GoogleScholar.read_agents(self.lineEditAgents.text())    # 获取所有UA
                agent = GoogleScholar.random.choice(agents)    # 随机选择一个UA
                print('[config] UA设置:{}'.format(agent))
            
            # 随机生成域名
            if self.checkBoxDomainsFlag.isChecked():
                domains = GoogleScholar.read_domains(self.lineEditDomains.text())    # 获取所有域名
                domain = GoogleScholar.random.choice(domains)    # 随机选择一个域名
                print('[config] 域名设置:{}'.format(domain))
            
            # 随机生成代理ip
            if self.checkBoxIPsFlag.isChecked():
                ips = GoogleScholar.read_ips(self.lineEditIPs.text())    # 获取所有代理ip
                ip = GoogleScholar.random.choice(ips)    # 随机选择一个ip
                print('[config] IP设置:{}'.format(ip))
                proxy = {'https': 'https://' + ip,'http': 'http://' + ip}

            # 自定义代理
            # proxy = GoogleScholar.select_proxy('socks-client')    # 获取代理地址
            # proxies = GoogleScholar.select_proxy('no')    # 不使用代理

            headers = {
            'authority': 'scholar.google.com.hk',
            'method': 'GET',
            'scheme': 'https',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            # 'cookie': 'GSP=LM=1589629500:S=bdTlYLAgGL7KA7s2; NID=204=lT8K8u-_lBsiD7Nmz6g9wkyeRx_eK_aWmJ_q7eZ77r4LpU4BY2lrrKxJ0YDqxBZXnztoRiQYtBS2szDHIW8w-S3BarOochkJZJ9uXYabKtwLp8Zm1IWs0gVpgwRCHpWzzioFMYKN1V9XR9HIa2LtrnZ9kjQu0_LiDBM_WfMhkhc',
            'cookie': cookie,
            'dnt': '1',
            'referer': 'https://scholar.google.com.hk/?hl=zh-CN',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent':agent,
            'x-client-data': 'CJe2yQEIpbbJAQjEtskBCKmdygEI0K/KAQi8sMoBCO21ygEIjrrKAQjtu8oBGLy6ygE='
            }
            # headers = {
            # 'method': 'GET',
            # 'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            # 'accept-encoding': 'gzip, deflate, br',
            # 'cookie': cookie,
            # 'user-agent':agent
            # }
            print('--------------------第{}页数据--------------------'.format(page_count + 1))
            # url = 'https://scholar.google.com.hk/scholar?start=' + str(10*page_count) + '&q=%E2%80%9CEntrepreneurial+failure%E2%80%9D+OR+%E2%80%9Cbusiness+failure%E2%80%9D&hl=zh-CN&as_sdt=1,47&as_ylo=2010&as_vis=1'    # 访问的url
            url = self.url_head + '&start=' + str(10*page_count) + self.url_tail
            self.updated.emit('访问的URL：\n' + url)
            # print(url)    # 输出url
            try:
                # 从网络获取html并解析
                data = GoogleScholar.get_data(url, headers, proxy)    # 获取数据
                if not data is None:
                    save_html_file = open("index.html", "w", encoding='utf8')
                    save_html_file.write(data)
                    save_html_file.close()
                # print(data)
                html = etree.HTML(data)    # 解析成html
                # print(data)    # 输出获取到的数据
                article_list = GoogleScholar.parse_data(html, page_count, detailFlag)    # 解析得到的数据
                # with open(file_path.replace("xlsx", "txt"), "a", encoding='utf8') as f:
                #     f.write(str(article_list))
                GoogleScholar.sava_to_excel(article_list, file_path)    # 将得到的数据保存到Excel
            except Exception as e:
                print(str(e))
                self.updated.emit('解析出错！')
            
            # time.sleep(1)
            # 设置进度条进度
            progressBarValue = page_count/pages*100
            self.progressBar.setValue(progressBarValue - 3)

            # 判断线程是否暂停
            self.pauseFlag.wait()

            # 判断是否点击了取消
            if self.exitFlag.isSet():
                return

            gc.collect()

        # 如果勾选了导出PDF链接到文件，执行PDF导出
        if self.checkBoxSavePDFLink.isChecked():
            try:
                article_list = PDFDownload.read_file(file_path)
            except:
                # self.textEditLog.append('文件打开失败！')
                self.updated.emit('文件打开失败！')
            linkSaveFile = self.lineEditLinkSaveFile.text()    # 链接保存文件
            for article in article_list:
                if not ('nan' in article['PDF Link']):
                    with open(linkSaveFile, 'a+') as writeFile:
                        writeFile.write(article['PDF Link'] + '\n')   #加\n换行显示
        # 如果勾选了自动下载PDF，根据链接自动下载PDF
        if self.checkBoxDownloadPDF.isChecked():
            article_list = PDFDownload.read_file(file_path)
            # self.textEditLog.append('开始下载文件！共有{}项需要下载。'.format(len(article_list)))
            PDFDownload.download_file(self, article_list, pdfSavePath)
        # self.textEditLog.append('')
        self.progressBar.setValue(100)
        print('操作完成！\n')
        self.updated.emit('\n\n操作完成！\n')
        self.pushButtonStart.setText('开始')
        self.startFlag = False
        gc.collect()
        return

    # 暂停线程
    def pause(self):
        self.pauseFlag.clear()    # 设置为False，让线程阻塞
        self.textEditLog.append('暂停运行！')

    # 继续执行线程
    def resume(self):
        self.pauseFlag.set()    # 设置为True，让线程停止阻塞
        self.textEditLog.append('继续运行！')

    # 停止线程
    def stop(self):
        if self.startFlag:
            reply = QtWidgets.QMessageBox.question(self,"警告","确认取消？", QtWidgets.QMessageBox.Yes|QtWidgets.QMessageBox.No,QtWidgets.QMessageBox.Yes)
            if reply==QtWidgets.QMessageBox.Yes:
                self.exitFlag.set()    # 设置为True，退出
                self.textEditLog.append('停止运行！')
                self.pushButtonStart.setText('开始')
                self.progressBar.setValue(0)
                self.startFlag = False

    # 更新textEdit的内容
    def updateText(self, text):
        self.textEditLog.append(text)

import icon_rc

if __name__ == '__main__':  
    app = QtWidgets.QApplication(sys.argv)    # 创建应用对象
    # MainWindow = QtWidgets.QMainWindow()    # 创建主界面
    MainWindow = MainWindow()    # 创建主界面
    ui = Ui_Widget()    # 创建ui对象
    ui.setupUi(MainWindow)     # 为主界面设置ui
    MainWindow.show()    # 显示主界面
    sys.exit(app.exec_())     # 安全退出