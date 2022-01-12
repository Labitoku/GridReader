# coding: utf8 
from PIL import Image

# coding: utf8 
from PyQt5.QtWidgets import *
import subprocess
from PyQt5.QtWidgets import * 
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 
import sys 
#import smtplib
#from email.mime.text import MIMEText
import smtplib 
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders 

class GridWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Gready")
        #Quand j'aurais une icone
        #self.setWindowIcon()
        self.setGeometry(0, 0, 1280, 720) 
        self.dimensions = QDesktopWidget().screenGeometry()

        ############VARIABLES############

        self.angle = 0
        self.color = None

        self.size_cell = (0, 0)
        self.offset_cell = (0, 0)
        self.full_cell = True

        ############VARIABLES############


        self.setMenubar()
        self.setTools()
        self.setWorkspace()

        style = '''
            QWidget{
                background-color: rgba(60,60,60,255)
            }

            QLabel {
                color: rgba(230,230,230,255)
            }

            QPushButton {
                background-color: #006325;
                color: white;

                min-width: 50px;
                min-height: 50px;
                max-height: 50px;

                border-radius: 25px;
                border-width: 1px;
                border-color: #ae32a0;
                border-style: solid;
            }
            QPushButton:hover {
                background-color: #328930;
            }
            QPushButton:pressed {
                background-color: #80c342;
            }
            '''

        self.setStyleSheet(style)

        self.showMaximized()



    def setMenubar(self):
        menubar = self.menuBar()

        self.mb_y = menubar.size().height()

        file_menu = QMenu("&File", self)
        file_menu.addAction("Open file")
        menubar.addMenu(file_menu)

    def setTools(self):
        tools_container = QWidget(self)
        tools_container.setGeometry(QRect(0, self.mb_y, self.dimensions.width() / 5, self.dimensions.height()))
        #tools_container.setStyleSheet("background-color: rgba(60,60,60,255);")
        
        self.tools_layout = QVBoxLayout(tools_container)
        
        transp_lb = QLabel("Auto transparency removing")
        self.tools_layout.addWidget(transp_lb)        
        transp_btn = QPushButton("Remove", self)
        self.tools_layout.addWidget(transp_btn)
        
        bycolor_lb = QLabel("Auto resizing by color")
        self.tools_layout.addWidget(bycolor_lb)
        bycolor_swatch = QColorDialog(self)
        self.tools_layout.addWidget(bycolor_swatch)


        rotate_lb = QLabel("Rotation")
        self.tools_layout.addWidget(rotate_lb)
        rotate_edit = QLineEdit(self)
        self.tools_layout.addWidget(rotate_edit)
        rotate_sld = QSlider(Qt.Horizontal)
        self.tools_layout.addWidget(rotate_sld)
        rotate_btn = QPushButton("Auto rotate", self)
        self.tools_layout.addWidget(rotate_btn)

        cells_lb = QLabel("Cells")
        self.tools_layout.addWidget(cells_lb)
        cells_size_lb = QLabel("Size : ")
        self.tools_layout.addWidget(cells_size_lb)

        size_layout = QHBoxLayout()
        x_lb = QLabel("X : ")
        size_layout.addWidget(x_lb)
        x_edit = QLineEdit(self)
        size_layout.addWidget(x_edit)
        x_edit.textChanged.connect(self.onSizeXEdit)

        
        y_lb = QLabel("Y : ")
        size_layout.addWidget(y_lb)
        y_edit = QLineEdit(self)
        size_layout.addWidget(y_edit)
        self.tools_layout.addLayout(size_layout)
        y_edit.textChanged.connect(self.onSizeYEdit)

        cells_offset_lb = QLabel("Offset : ")
        self.tools_layout.addWidget(cells_offset_lb)

        offset_layout = QHBoxLayout()
        offset_x_lb = QLabel("X : ")
        offset_layout.addWidget(offset_x_lb)
        offset_x_edit = QLineEdit(self)
        offset_layout.addWidget(offset_x_edit)
        offset_x_edit.textChanged.connect(self.onOffsetXEdit)
        
        offset_y_lb = QLabel("Y : ")
        offset_layout.addWidget(offset_y_lb)
        offset_y_edit = QLineEdit(self)
        offset_layout.addWidget(offset_y_edit)
        offset_y_edit.textChanged.connect(self.onOffsetYEdit)

        self.tools_layout.addLayout(offset_layout)

        full_cell_lb = QLabel("Full cell : ")
        self.tools_layout.addWidget(full_cell_lb)
        full_cell_cb = QCheckBox(self)
        self.tools_layout.addWidget(full_cell_cb)



        self.tools_layout.addStretch()


    def onSizeXEdit(self, text):
        if text == '':
            val = 0
        else:
            val = int(text)

        l = list(self.size_cell)
        l[0] = val
        self.size_cell = tuple(l) 

    def onSizeYEdit(self, text):
        if text == '':
            val = 0
        else:
            val = int(text)

        l = list(self.size_cell)
        l[1] = val
        self.size_cell = tuple(l) 

    def onOffsetXEdit(self, text):
        if text == '':
            val = 0
        else:
            val = int(text)

        l = list(self.offset_cell)
        l[0] = val
        self.offset_cell = tuple(l) 

    def onOffsetYEdit(self, text):
        if text == '':
            val = 0
        else:
            val = int(text)

        l = list(self.offset_cell)
        l[1] = val
        self.offset_cell = tuple(l) 
        
        
    def onColorSwatchClick(self):
        

        return color

    def setWorkspace(self):
        workspace_container = QWidget(self)
        workspace_container.setGeometry(QRect(self.dimensions.width() / 5, self.mb_y, self.dimensions.width() * .8, self.dimensions.height()))
        workspace_container.setStyleSheet("background-color: rgba(230,230,230,255);")
        self.tools_layout = QVBoxLayout(workspace_container)



    def fade(self, widget):
        self.effect = QGraphicsOpacityEffect()
        widget.setGraphicsEffect(self.effect)
        self.animation = QtCore.QPropertyAnimation(self.effect, b"opacity")
        self.animation.setDuration(500)
        self.animation.setStartValue(1)
        self.animation.setEndValue(0)
        self.animation.start()


    def unfade(self, widget):
        self.effect = QGraphicsOpacityEffect()
        widget.setGraphicsEffect(self.effect)

        self.animation = QtCore.QPropertyAnimation(self.effect, b"opacity")
        self.animation.setDuration(500)
        self.animation.setStartValue(0)
        self.animation.setEndValue(1)
        self.animation.start()

