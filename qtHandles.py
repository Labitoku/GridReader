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

        self.setMenubar()

        self.showMaximized()



    def setMenubar(self):
        menubar = self.menuBar()

        file_menu = QMenu("&File", self)
        file_menu.addAction("Open file")
        menubar.addMenu(file_menu)


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