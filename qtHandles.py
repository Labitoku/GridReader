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

class GridWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Gready")
        #Quand j'aurais une icone
        #self.setWindowIcon()
        self.setGeometry(0, 0, 1280, 720) 
        self.dimensions = QDesktopWidget().screenGeometry()

        ############VARIABLES############

        self.image_url = "grid_samples/im8.png"
        self.image = Image.open(self.image_url)


        self.angle = 0
        self.color = QColor(255,0,0,0)
        self.tolerance = 0

        self.size_cell = (0, 0)
        self.offset_cell = (0, 0)
        self.full_cell = True

        ############VARIABLES############


        self.setMenubar()
        self.setTools()
        self.setWorkspace()

        """style = '''
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
            '''"""

        #self.setStyleSheet(style)

        self.showMaximized()



    def setMenubar(self):
        menubar = self.menuBar()

        self.mb_y = menubar.size().height()

        file_menu = QMenu('&File', self)

        openAct = QAction('Open file', self)
        openAct.setShortcut('Ctrl+O')
        openAct.setStatusTip('Open image file')
        openAct.triggered.connect(self.open_file)

        file_menu.addAction(openAct)

        #file_menu.addAction("Open file")

        menubar.addMenu(file_menu)


    def open_file(self):

        try:
            name = QFileDialog.getOpenFileName(self, 'Open File', 'C\\', 'PNG files (*.png)')
            self.image_url = name[0]
            
        except FileNotFoundError:
            pass







    ############TOOLS############
    def setTools(self):
        tools_container = QWidget(self)
        tools_container.setGeometry(QRect(0, self.mb_y, self.dimensions.width() / 5, self.dimensions.height()))
        #tools_container.setStyleSheet("background-color: rgba(60,60,60,255);")
        
        self.tools_layout = QVBoxLayout(tools_container)


        ############TRANSPARENCE############
        transp_lb = QLabel("Auto transparency removing")
        self.tools_layout.addWidget(transp_lb)  

        transp_btn = QPushButton("Remove", self)
        transp_btn.clicked.connect(self.onAutoTransp)
        self.tools_layout.addWidget(transp_btn)
        
        self.tools_layout.addStretch()


        ############COULEURS############
        color_layout = QHBoxLayout()
        bycolor_lb = QLabel("Auto resizing by color")
        color_layout.addWidget(bycolor_lb)

        test_button = QPushButton(self)
        color_layout.addWidget(test_button)
        test_button.clicked.connect(self.colorPicker)
        self.tools_layout.addLayout(color_layout)

        tolerance_layout = QHBoxLayout()
        tolerance_lb = QLabel("Tolerance : ")
        tolerance_layout.addWidget(tolerance_lb)

        tolerance_edit = QLineEdit(self)
        tolerance_layout.addWidget(tolerance_edit)
        tolerance_edit.textChanged.connect(self.onToleranceEdit)
        self.tools_layout.addLayout(tolerance_layout)

        self.tools_layout.addStretch()


        ############ROTATION############
        rotate_lb = QLabel("Rotation")
        self.tools_layout.addWidget(rotate_lb)

        rotate_edit = QLineEdit(self)
        rotate_edit.textChanged.connect(self.onAngleEdit)
        self.tools_layout.addWidget(rotate_edit)

        rotate_sld = QSlider(Qt.Horizontal)
        rotate_sld.setMinimum(0)
        rotate_sld.setMaximum(360)
        rotate_sld.setSingleStep(0.1)
        rotate_sld.valueChanged.connect(self.onSliderEdit)
        self.tools_layout.addWidget(rotate_sld)

        rotate_btn = QPushButton("Auto rotate", self)
        rotate_btn.clicked.connect(self.onAutoAngle)
        self.tools_layout.addWidget(rotate_btn)

        

        self.tools_layout.addStretch()


        ############CELLULES############
        cells_lb = QLabel("Cells")
        self.tools_layout.addWidget(cells_lb)

        cells_size_lb = QLabel("Size : ")
        self.tools_layout.addWidget(cells_size_lb)

        size_layout = QHBoxLayout()
        x_lb = QLabel("X : ")
        size_layout.addWidget(x_lb)

        x_edit = QLineEdit(self)
        x_edit.textChanged.connect(self.onSizeXEdit)
        size_layout.addWidget(x_edit)
        
        y_lb = QLabel("Y : ")
        size_layout.addWidget(y_lb)

        y_edit = QLineEdit(self)
        size_layout.addWidget(y_edit)
        y_edit.textChanged.connect(self.onSizeYEdit)
        self.tools_layout.addLayout(size_layout)

        cells_offset_lb = QLabel("Offset : ")
        self.tools_layout.addWidget(cells_offset_lb)

        offset_layout = QHBoxLayout()

        offset_x_lb = QLabel("X : ")
        offset_layout.addWidget(offset_x_lb)

        offset_x_edit = QLineEdit(self)
        offset_x_edit.textChanged.connect(self.onOffsetXEdit)
        offset_layout.addWidget(offset_x_edit)


        offset_y_lb = QLabel("Y : ")
        offset_layout.addWidget(offset_y_lb)

        offset_y_edit = QLineEdit(self)
        offset_y_edit.textChanged.connect(self.onOffsetYEdit)
        offset_layout.addWidget(offset_y_edit)

        self.tools_layout.addLayout(offset_layout)

        full_cell_lb = QLabel("Full cell : ")
        self.tools_layout.addWidget(full_cell_lb)

        full_cell_cb = QCheckBox(self)
        full_cell_cb.stateChanged.connect(lambda:self.onFullCellChanged(full_cell_cb))
        self.tools_layout.addWidget(full_cell_cb)

        self.tools_layout.addStretch()


    ############TRANSPARENCE############
    def onAutoTransp(self):
        #removeTransp()
        i = 0

    ############COULEURS############
    def colorPicker(self):
        self.color = QColorDialog.getColor()

    def onToleranceEdit(self, text):
        if text == '':
            val = 0
        else:
            val = int(text)
        self.tolerance = val

    ############ROTATION############
    def onAngleEdit(self, text):
        if text == '':
            self.angle = 0
        else:
            self.angle = int(text)

    def onSliderEdit(self, angle):
        self.angle = angle

    def onAutoAngle(self):
        self.angle = 12
        #self.angle = getAngle()

    ############CELLULES############
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
        
    def onFullCellChanged(self, button):
        self.full_cell = button.isChecked()


    ############WORKSPACE############
    def setWorkspace(self):
        workspace_container = QWidget(self)
        workspace_container.setGeometry(QRect(self.dimensions.width() / 5, self.mb_y, self.dimensions.width() * .8, self.dimensions.height()))
        workspace_container.setStyleSheet("background-color: rgba(230,230,230,255);")
        self.workspace_layout = QGridLayout(workspace_container)
        self.workspace_layout.setAlignment(Qt.AlignCenter)

        label = QLabel(self)
        pix = QPixmap(self.image_url)
        label.setPixmap(pix)
        self.workspace_layout.addWidget(label)





    
    ############UTILITARY############
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

