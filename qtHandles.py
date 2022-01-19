# coding: utf8 
from email.mime import image
from PIL import Image, ImageDraw

# coding: utf8 
from PyQt5.QtWidgets import *
import subprocess
from PyQt5.QtWidgets import * 
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 
import sys
import os

import cropHandles
import transformHandles

class GridWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Gready")
        #Quand j'aurais une icone
        #self.setWindowIcon()
        self.setGeometry(0, 0, 1280, 720) 
        self.dimensions = QDesktopWidget().screenGeometry()

        self.clearAll()
        ############HOVER FEATURES ??############
        self.onTranspBt = False

        ############VARIABLES############

        self.image_url = 'tmp.png'
        self.image_url_mod = 'tmp_mod.png'
        self.image = Image.open(self.image_url)
        self.image_mod = None
        self.left, self.top, self.right, self.bottom = cropHandles.getTransparencyMarks(self.image)

        self.angle = 0
        self.color = QColor(255,255,255,255)
        self.tolerance = 0
        self.approximation_area = 0

        self.size_cell = (10, 10)
        self.offset_cell = (0, 0)
        self.full_cell = True

        self.cell_qty_x = 10
        self.cell_qty_y = 10

        ############LAYOUT SETTING############


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
        menubar.addMenu(file_menu)


    def open_file(self):

        try:
            name = QFileDialog.getOpenFileName(self, 'Open File', 'C\\', 'PNG files (*.png)')
            self.image = Image.open(name[0])
            self.image.save(self.image_url)
            self.updateWorskspace()
            self.generateTranspRect()
            
        except FileNotFoundError:
            pass

    """UPDATE FUNCTIONS (IMAGE / WORKSPACE)"""

    def updateWorskspace(self):
        for i in reversed(range(self.workspace_layout.count())):
            self.workspace_layout.itemAt(i).widget().deleteLater()

        self.left, self.top, self.right, self.bottom = cropHandles.getTransparencyMarks(self.image)
        label = QLabel(self)
        pix = QPixmap(self.image_url_mod)
        diag = (pix.width()**2 + pix.height()**2)**0.5
        label.setMinimumSize(diag, diag)
        label.setAlignment(QtCore.Qt.AlignCenter)
        label.setPixmap(pix)
        self.workspace_layout.addWidget(label)


    def updateImage(self):
        self.image_mod = Image.open(self.image_url)
        """if os.path.isfile('tmp_transp.png'):
            transp = Image.open('tmp_transp.png')
            self.image.paste(transp, (0, 0), transp)"""
        if os.path.isfile('tmp_approx.png'):
            approx = Image.open('tmp_approx.png')
            self.image_mod.paste(approx, (0, 0), approx)

        if os.path.isfile('tmp_cells.png'):
            cells = Image.open('tmp_cells.png')
            self.image_mod.paste(cells, (0, 0), cells)


        self.image_mod.save(self.image_url_mod)
        self.updateWorskspace()


    ############TOOLS############
    def setTools(self):
        tools_container = QWidget(self)
        tools_container.setGeometry(QRect(0, self.mb_y, self.dimensions.width() / 8, self.dimensions.height()))
        
        self.tools_layout = QVBoxLayout(tools_container)


        ############TRANSPARENCE############
        transp_lb = QLabel("Auto transparency removing")
        self.tools_layout.addWidget(transp_lb)  

        self.transp_btn = QPushButton("Remove", self)
        self.transp_btn.clicked.connect(self.onAutoTransp)
        """
        ############EVENT FILTER############
        #self.transp_btn.installEventFilter(self)
        ############EVENT FILTER############
        """
        self.tools_layout.addWidget(self.transp_btn)
        
        self.tools_layout.addStretch()


        ############COULEURS############
        color_layout = QHBoxLayout()
        bycolor_lb = QLabel("Auto resizing by color")
        color_layout.addWidget(bycolor_lb)

        self.color_button = QPushButton(self)
        color_layout.addWidget(self.color_button)
        self.color_button.clicked.connect(self.colorPicker)
        self.color_button.setStyleSheet(f'background-color: rgba({self.color.red()},{self.color.green()},{self.color.blue()},{self.color.alpha()})')
        self.tools_layout.addLayout(color_layout)

        approx_size_lb = QLabel("Approximation area size : ")
        self.tools_layout.addWidget(approx_size_lb)

        approx_edit = QLineEdit(self)
        approx_edit.textChanged.connect(self.onApproxSizeEdit)
        approx_edit.editingFinished.connect(self.onApproxSizeFinished)
        self.tools_layout.addWidget(approx_edit)


        tolerance_layout = QHBoxLayout()
        tolerance_lb = QLabel("Tolerance : ")
        tolerance_layout.addWidget(tolerance_lb)

        tolerance_edit = QLineEdit(self)
        tolerance_layout.addWidget(tolerance_edit)
        tolerance_edit.textChanged.connect(self.onToleranceEdit)
        self.tools_layout.addLayout(tolerance_layout)

        color_crop_button = QPushButton("Crop with color", self)
        color_crop_button.clicked.connect(self.onColorCrop)
        self.tools_layout.addWidget(color_crop_button)


        self.tools_layout.addStretch()


        ############ROTATION############
        rotate_lb = QLabel("Rotation")
        self.tools_layout.addWidget(rotate_lb)

        rotate_edit = QLineEdit(self)
        rotate_edit.textChanged.connect(self.onAngleEdit)
        self.tools_layout.addWidget(rotate_edit)

        """
        ############SLIDER############
        rotate_sld = QSlider(Qt.Horizontal)
        rotate_sld.setMinimum(0)
        rotate_sld.setMaximum(360)
        rotate_sld.setSingleStep(0.1)
        rotate_sld.valueChanged.connect(self.onSliderEdit)
        rotate_sld.sliderReleased.connect(self.onSliderRelease)
        self.tools_layout.addWidget(rotate_sld)
        ############SLIDER############
        """

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
        x_edit.editingFinished.connect(self.onCellModFinished)
        size_layout.addWidget(x_edit)
        
        y_lb = QLabel("Y : ")
        size_layout.addWidget(y_lb)

        y_edit = QLineEdit(self)
        size_layout.addWidget(y_edit)
        y_edit.textChanged.connect(self.onSizeYEdit)
        y_edit.editingFinished.connect(self.onCellModFinished)
        self.tools_layout.addLayout(size_layout)

        cells_offset_lb = QLabel("Offset : ")
        self.tools_layout.addWidget(cells_offset_lb)

        offset_layout = QHBoxLayout()

        offset_x_lb = QLabel("X : ")
        offset_layout.addWidget(offset_x_lb)

        offset_x_edit = QLineEdit(self)
        offset_x_edit.textChanged.connect(self.onOffsetXEdit)
        offset_x_edit.editingFinished.connect(self.onCellModFinished)
        offset_layout.addWidget(offset_x_edit)


        offset_y_lb = QLabel("Y : ")
        offset_layout.addWidget(offset_y_lb)

        offset_y_edit = QLineEdit(self)
        offset_y_edit.textChanged.connect(self.onOffsetYEdit)
        offset_y_edit.editingFinished.connect(self.onCellModFinished)
        offset_layout.addWidget(offset_y_edit)

        self.tools_layout.addLayout(offset_layout)

        full_cell_lb = QLabel("Full cell : ")
        self.tools_layout.addWidget(full_cell_lb)

        full_cell_cb = QCheckBox(self)
        full_cell_cb.stateChanged.connect(lambda:self.onFullCellChanged(full_cell_cb))
        self.tools_layout.addWidget(full_cell_cb)

        self.tools_layout.addStretch()

    def clearAll(self):
        if os.path.isfile('tmp_transp.png'):
            os.remove('tmp_transp.png')
        if os.path.isfile('tmp_approx.png'):
            os.remove('tmp_approx.png')
        if os.path.isfile('tmp_cells.png'):
            os.remove('tmp_cells.png')


    ############TRANSPARENCE############
    def onAutoTransp(self):
        print(self.left, self.top, self.right, self.bottom)
        self.image = cropHandles.cropByMarks(self.image, self.left, self.top, self.right, self.bottom)
        self.image.save(self.image_url)
        self.updateImage()

    def generateTranspRect(self):
        #shape = [(x0, y0), (x1, y1)]
        print(self.left, self.top, self.right, self.bottom)

        left_shape = [(0, 0), (self.left, self.image.height)]
        top_shape = [(0, 0), (self.image.width, self.top)]
        right_shape = [(self.right, 0), (self.image.width, self.image.height)]
        bottom_shape = [(0, self.bottom), (self.image.width, self.image.height)]
        
        transp_img = Image.new('RGBA', [self.image.width, self.image.height])
        transp_rects = ImageDraw.Draw(transp_img)
        transp_rects.rectangle(left_shape, fill = "#ff000099", outline= "red")
        transp_rects.rectangle(top_shape, fill = "#ff000099", outline= "red")
        transp_rects.rectangle(right_shape, fill = "#ff000099", outline= "red")
        transp_rects.rectangle(bottom_shape, fill = "#ff000099", outline= "red")
        
        transp_img.save('tmp_transp.png')
        self.updateImage()



    ############COULEURS############
    def colorPicker(self):
        self.color = QColorDialog.getColor()
        self.color_button.setStyleSheet(f'background-color: rgba({self.color.red()},{self.color.green()},{self.color.blue()},{self.color.alpha()})')

    def onApproxSizeEdit(self, text):
        if text == '':
            val = 0
        else:
            val = int(text)

        self.approximation_area = val

    def onApproxSizeFinished(self):
        self.generateApproxAreaRects()

    def onToleranceEdit(self, text):
        if text == '':
            val = 0
        else:
            val = int(text)
        self.tolerance = val

    def onColorCrop(self):
        rgb_col = (self.color.red(), self.color.green(), self.color.blue())
        self.image = cropHandles.cropByColor(self.image, rgb_col, self.tolerance)
        self.updateImage()

    def generateApproxAreaRects(self):
        top_shape = [(0, 0), (self.approximation_area, self.approximation_area)]
        bottom_shape = [(0, self.image.height - self.approximation_area), (self.approximation_area, self.image.height)]

        approx_img = Image.new('RGBA', [self.image.width, self.image.height])
        transp_rects = ImageDraw.Draw(approx_img)
        transp_rects.rectangle(top_shape, outline= "blue")
        transp_rects.rectangle(bottom_shape, outline= "blue")
        
        approx_img.save('tmp_approx.png')
        self.updateImage()


    ############ROTATION############
    def onAngleEdit(self, text):
        if text == '':
            self.angle = 0
        else:
            self.angle = int(text)

    def onAngleFinish(self):
        self.image = self.image.rotate(self.angle, resample=Image.BICUBIC, expand=True)
        self.image.save(self.image_url)
        self.clearAll()
        self.updateImage()

    """
    def onSliderEdit(self, angle):
        self.new_angle = angle - self.angle


    def onSliderRelease(self):
        self.angle = self.angle + self.new_angle
        self.image = self.image.rotate(self.angle, resample=Image.BICUBIC, expand=True)
        self.updateImage(self.image_url)"""


    def onAutoAngle(self):
        rgb_col = (self.color.red(), self.color.green(), self.color.blue())
        top_mark, bottom_mark = transformHandles.getMarkersByColor(self.image, rgb_col, self.approximation_area, self.tolerance)
        self.image = transformHandles.adjustTransform(self.image, top_mark, bottom_mark)
        self.image.save(self.image_url)
        self.clearAll()
        self.updateImage()


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
        self.onCellModFinished()

    def onCellModFinished(self):
        self.cell_qty_x, self.cell_qty_y = cropHandles.getCellsQty(self.image, self.size_cell, self.offset_cell, self.full_cell)
        print(self.cell_qty_x, self.cell_qty_y)
        self.generateCellsRects()


    def generateCellsRects(self):
                #shape = [(x0, y0), (x1, y1)]


        cells_img = Image.new('RGBA', [self.image_mod.width, self.image_mod.height])
        cells_rects = ImageDraw.Draw(cells_img)

        for j in range (0, self.cell_qty_y):
            for i in range(0, self.cell_qty_x):
                x0 = i * self.size_cell[0] + i * self.offset_cell[0]
                y0 = j * self.size_cell[1] + j * self.offset_cell[1]
                x1 = x0 + self.size_cell[0]
                y1 = y0 + self.size_cell[1]
                
                shape = [(x0, y0), (x1, y1)]
                cells_rects.rectangle(shape, fill = "#ff000044", outline= "red")
        
        cells_img.save('tmp_cells.png')
        self.updateImage()

    ############WORKSPACE############
    def setWorkspace(self):
        workspace_container = QWidget(self)
        workspace_container.setGeometry(QRect(self.dimensions.width() / 8, self.mb_y, self.dimensions.width() - self.dimensions.width() / 8, self.dimensions.height()))
        workspace_container.setStyleSheet("background-color: rgba(230,230,230,255);")
        self.workspace_layout = QGridLayout(workspace_container)
        self.workspace_layout.setAlignment(Qt.AlignCenter)



        label = QLabel(self)
        pix = QPixmap(self.image_url)
        diag = (pix.width()**2 + pix.height()**2)**0.5
        label.setMinimumSize(diag, diag)
        label.setAlignment(QtCore.Qt.AlignCenter)
        label.setPixmap(pix)
        self.workspace_layout.addWidget(label)



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
