# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.
import sys
sys.path.append('../stylegan3')

from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np
import cv2

import torch
import dnnlib
import legacy

from functools import partial

from projector import run_projection


network_pkl = "./models/ffhq1024.pkl"

print('Loading networks from "%s"...' % network_pkl)
device = torch.device('cuda')
with dnnlib.util.open_url(network_pkl) as f:
    print("Loading Generator...")
    G = legacy.load_network_pkl(f)['G_ema'].to(device) # type: ignore

ogLatentVector = latentVector = np.random.randn(1, 512)

numDirection = "20k"

emotionHappyVector = np.load("./out/directions/"+numDirection+"/emotion_happy_1.npy")
emotionNeutralVector = np.load("./out/directions/"+numDirection+"/emotion_neutral_1.npy")
emotionAngryVector = np.load("./out/directions/"+numDirection+"/emotion_angry_1.npy")
emotionSurpriseVector = np.load("./out/directions/"+numDirection+"/emotion_surprise_1.npy")

raceWhiteVector = np.load("./out/directions/"+numDirection+"/race_white.npy")
raceBlackVector = np.load("./out/directions/"+numDirection+"/race_black.npy")
raceAsianVector = np.load("./out/directions/"+numDirection+"/race_asian.npy")
raceMidEastVector = np.load("./out/directions/"+numDirection+"/race_mideast.npy")

hairBlackVector = np.load("./out/directions/"+numDirection+"/hair_black.npy")
hairBlondVector = np.load("./out/directions/"+numDirection+"/hair_blond.npy")
hairBrownVector = np.load("./out/directions/"+numDirection+"/hair_brown.npy")
hairGrayVector = np.load("./out/directions/"+numDirection+"/hair_gray.npy")

ageOldVector = np.load("./out/directions/"+numDirection+"/age_old.npy")
ageYoungVector = np.load("./out/directions/"+numDirection+"/age_young.npy")
genderVector = np.load("./out/directions/"+numDirection+"/sex.npy")
beardVector = np.load("./out/directions/"+numDirection+"/beard.npy")
glassesVector = np.load("./out/directions/"+numDirection+"/glasses.npy")
hatVector = np.load("./out/directions/"+numDirection+"/hat.npy")
baldVector = np.load("./out/directions/"+numDirection+"/hair_bald.npy")

projectionTarget = ""

# Order: happy, white, hairblack, bald, age, neutral, raceblack, blond, beard, gender, angry, asian, brown, glasses, sad, indian, gray, hat
vectors = [
    emotionHappyVector, raceWhiteVector, hairBlackVector, baldVector, ageYoungVector,
    emotionNeutralVector, raceBlackVector, hairBlondVector, beardVector, ageOldVector,
    emotionAngryVector, raceAsianVector, hairBrownVector, glassesVector, genderVector,
    emotionSurpriseVector, raceMidEastVector, hairGrayVector, hatVector
]

text = [
    "Happy:  ", "White:  ", "Hair Black:  ", "Bald:  ", "Young:  ",
    "Neutral:  ", "Race Black:  ", "Hair Blond:  ", "Beard:  ", "Old:  ",
    "Angry:  ", "Asian:  ", "Hair Brown:  ", "Glasses:  ", "Gender (♀ - | ♂ +) :  ",
    "Surprise:  ", "MidEast:  ", "Hair Gray:  ", "Hat:  "
]

originalNerfingValues = [20, 40, 40, 40, 40,
                                        20, 40, 40, 40, 40,
                                        20, 10, 40, 40, 40,
                                        20, 5, 40, 5]

nerfingValues = originalNerfingValues.copy()
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1065, 880)
        MainWindow.setFixedSize(1065, 880)
        MainWindow.setLayoutDirection(QtCore.Qt.LeftToRight)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

#-------------------------------------------------------------------------

        self.inputImage = QtWidgets.QLabel(self.centralwidget)
        self.inputImage.setGeometry(QtCore.QRect(10, 10, 512, 512))
        self.inputImage.setText("")
        self.inputImage.setStyleSheet("border: 1px solid black;")
        self.inputImage.setPixmap(QtGui.QPixmap("gui/images/input.png"))
        self.inputImage.setScaledContents(True)

        self.outputImage = QtWidgets.QLabel(self.centralwidget)
        self.outputImage.setGeometry(QtCore.QRect(542, 10, 512, 512))
        self.outputImage.setText("")
        self.outputImage.setStyleSheet("border: 1px solid black;")
        self.outputImage.setPixmap(QtGui.QPixmap("gui/images/output.png"))
        self.outputImage.setScaledContents(True)

#-------------------------------------------------------------------------


        for i in range(5):
            self.line = QtWidgets.QFrame(self.centralwidget)
            self.line.setGeometry(QtCore.QRect(0, 520 + 70*i, 1060, 16))
            self.line.setFrameShape(QtWidgets.QFrame.HLine)
            self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
            if i == 0:
                self.line.setGeometry(QtCore.QRect(0, 566, 1060, 1))
                self.line.setStyleSheet("border: 2px solid black;")
            if i == 1: 
                self.line.setGeometry(QtCore.QRect(0, 596, 1060, 1))
                self.line.setStyleSheet("border: 2px solid black;")


        for i in range(5):
            self.line = QtWidgets.QFrame(self.centralwidget)
            self.line.setGeometry(QtCore.QRect(212 + 212*i, 567, 16, 313))
            self.line.setFrameShape(QtWidgets.QFrame.VLine)
            self.line.setFrameShadow(QtWidgets.QFrame.Sunken)

#-------------------------------------------------------------------------

        column_names = ["Emotion", "Race", "Hair", "Complements", "Age and Gender"]
        for i in range(len(column_names)):
            self.label = QtWidgets.QLabel(self.centralwidget)
            self.label.setGeometry(QtCore.QRect(35 + 212*i, 565, 150, 30))
            self.label.setText(column_names[i])
            self.label.setAlignment(QtCore.Qt.AlignCenter)
            # bold
            font = QtGui.QFont()
            font.setBold(True)
            self.label.setFont(font)

#-------------------------------------------------------------------------

        self.label_list = []
        self.slider_list = []
        self.up_button_list = []
        self.down_button_list = []
        self.nerf_label_list = []

        x_start_labels = 6
        y_start_labels = 610
        x_start_sliders = 25
        y_start_sliders = 630
        x_offset = 212
        y_offset = 70

        for row in range(4):
            num_columns = 5 if row < 3 else 4  # Adjust the number of columns for the third and fourth row
            
            for col in range(num_columns):
                x_label, x_slider = x_start_labels + col * x_offset, x_start_sliders + col * x_offset
                y_label, y_slider = y_start_labels + row * y_offset, y_start_sliders + row * y_offset

                label = QtWidgets.QLabel(self.centralwidget)
                label.setGeometry(QtCore.QRect(x_label, y_label, 200, 13))
                label.setLayoutDirection(QtCore.Qt.LeftToRight)
                label.setAlignment(QtCore.Qt.AlignCenter)
                self.label_list.append(label)

                slider = QtWidgets.QSlider(self.centralwidget)
                slider.setGeometry(QtCore.QRect(x_slider, y_slider, 150, 22))
                slider.setOrientation(QtCore.Qt.Horizontal)
                slider.setPageStep(1)
                slider.setTickInterval(5)
                slider.setRange(-100, 100)
                slider.setTickPosition(QtWidgets.QSlider.TicksBelow)
                slider.valueChanged.connect(self.moveVector)
                slider.valueChanged.connect(self.labelChange)
                self.slider_list.append(slider)

                upArrow = QtWidgets.QToolButton(self.centralwidget)
                upArrow.setGeometry(QtCore.QRect(x_slider+157, y_slider-9, 15, 15))
                upArrow.setArrowType(QtCore.Qt.UpArrow)
                upArrow.clicked.connect(lambda _, idx=(row,col), value=1: self.arrowClicked(idx, value))
                self.up_button_list.append(upArrow)

                downArrow = QtWidgets.QToolButton(self.centralwidget)
                downArrow.setGeometry(QtCore.QRect(x_slider+157, y_slider+9, 15, 15))
                downArrow.setArrowType(QtCore.Qt.DownArrow)
                downArrow.clicked.connect(lambda _, idx=(row,col), value=-1: self.arrowClicked(idx, value))
                self.down_button_list.append(downArrow)

                label2 = QtWidgets.QLabel(self.centralwidget)
                label2.setGeometry(QtCore.QRect(x_slider+168, y_slider, 30, 13))
                label2.setLayoutDirection(QtCore.Qt.LeftToRight)
                label2.setAlignment(QtCore.Qt.AlignCenter)
                label2.setText("0")
                self.nerf_label_list.append(label2)


#-------------------------------------------------------------------------
       
        self.saveLatentCheckBox = QtWidgets.QCheckBox(self.centralwidget)
        self.saveLatentCheckBox.setGeometry(QtCore.QRect(960, 840, 120, 20))

        self.saveVideoCheckBox = QtWidgets.QCheckBox(self.centralwidget)
        self.saveVideoCheckBox.setGeometry(QtCore.QRect(960, 860, 150, 20))

        self.resetAllCheckBox = QtWidgets.QCheckBox(self.centralwidget)
        self.resetAllCheckBox.setGeometry(QtCore.QRect(960, 810, 150, 20))

#-------------------------------------------------------------------------
   
        self.openImageButton = QtWidgets.QPushButton(self.centralwidget)
        self.openImageButton.setGeometry(QtCore.QRect(125, 530, 131, 31))
        self.openImageButton.clicked.connect(self.chooseImage)

        self.projectButton = QtWidgets.QPushButton(self.centralwidget)
        self.projectButton.setGeometry(QtCore.QRect(267, 530, 131, 31))
        self.projectButton.clicked.connect(self.projectImage)

        self.projectStepsLabel = QtWidgets.QLabel(self.centralwidget)
        self.projectStepsLabel.setGeometry(QtCore.QRect(400, 535, 50, 20))
        self.projectStepsLabel.setText("Steps:")

        self.projectStepsLineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.projectStepsLineEdit.setGeometry(QtCore.QRect(440, 535, 50, 20))
        self.projectStepsLineEdit.setValidator(QtGui.QIntValidator())
        self.projectStepsLineEdit.setText("100")

        self.loadLatentButton = QtWidgets.QPushButton(self.centralwidget)
        self.loadLatentButton.setGeometry(QtCore.QRect(779, 530, 131, 31))
        self.loadLatentButton.clicked.connect(self.loadLatent)

        self.randomFaceButton = QtWidgets.QPushButton(self.centralwidget)
        self.randomFaceButton.setGeometry(QtCore.QRect(637, 530, 131, 31))
        self.randomFaceButton.clicked.connect(self.randomFace)

        self.resetButton = QtWidgets.QPushButton(self.centralwidget)
        self.resetButton.setGeometry(QtCore.QRect(865, 810, 80, 28))
        self.resetButton.setStyleSheet("background-color: #fa1414;")
        self.resetButton.clicked.connect(self.resetAll)

        self.saveButton = QtWidgets.QPushButton(self.centralwidget)
        self.saveButton.setGeometry(QtCore.QRect(865, 845, 80, 28))
        self.saveButton.setStyleSheet("background-color: #8cfa5c;")
        self.saveButton.clicked.connect(self.saveImage)


        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


    def retranslateUi(self, MainWindow):
        global nerfingValues
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))

        for i in range(len(self.label_list)):
            self.label_list[i].setText(_translate("MainWindow", text[i] + str(self.slider_list[i].value())))
        
        for i in range(len(self.nerf_label_list)):
            self.nerf_label_list[i].setText(_translate("MainWindow", str(nerfingValues[i])))

        self.saveLatentCheckBox.setText(_translate("MainWindow", "Save latent"))
        self.saveVideoCheckBox.setText(_translate("MainWindow", "Save video"))
        self.resetAllCheckBox.setText(_translate("MainWindow", "Reset All"))

        self.projectButton.setText(_translate("MainWindow", "Project"))
        self.openImageButton.setText(_translate("MainWindow", "Open Image"))
        self.loadLatentButton.setText(_translate("MainWindow", "Load Latent"))
        self.randomFaceButton.setText(_translate("MainWindow", "Random Face"))
        self.resetButton.setText(_translate("MainWindow", "Reset"))
        self.saveButton.setText(_translate("MainWindow", "Save Image"))

##########################################################################
# GUI Functions

    def resetAll(self):
        """ Resets all sliders, images and latent vector"""
        global latentVector, ogLatentVector, nerfingValues, originalNerfingValues

        for i in range(len(self.slider_list)):
            self.slider_list[i].setValue(0)


        if self.resetAllCheckBox.isChecked():
            latentVector = ogLatentVector = np.random.randn(1, 512)
            self.inputImage.setPixmap(QtGui.QPixmap("gui/images/input.png"))
            self.outputImage.setPixmap(QtGui.QPixmap("gui/images/output.png"))
            nerfingValues = originalNerfingValues
            for i in range(len(self.nerf_label_list)):
                self.nerf_label_list[i].setText(str(nerfingValues[i]))


    def labelChange(self):
        """ Update labels with slider values"""
        for i in range(len(self.label_list)):
            self.label_list[i].setText(text[i] + str(self.slider_list[i].value()))
      
#-------------------------------------------------------------------------

    def arrowClicked(self, index, value):
        global nerfingValues
        """ Increase nerfing value of slider by 1"""
        row, col = index
        index = row * 5 + col     
        newValue = nerfingValues[index] + value
        if newValue == 0:
            nerfingValues[index] = 1   
        else:
            nerfingValues[index] += value
        self.nerf_label_list[index].setText(str(nerfingValues[index]))
        self.moveVector()

#-------------------------------------------------------------------------
# Image IO Functions
    def chooseImage(self):
        """ Opens file dialog and sets input image to selected image"""
        global projectionTarget

        projectionTarget = QtWidgets.QFileDialog.getOpenFileName()[0]
        
        if projectionTarget:
            self.inputImage.setPixmap(QtGui.QPixmap(projectionTarget))
    
    def saveImage(self):
        global latentVector
        """ Open file dialog, get save path and save image. If checkbox is checked, save latent as well. """
        # SAVE_PATH = QtWidgets.QFileDialog.getExistingDirectory(None, "Select Directory")
        SAVE_PATH = QtWidgets.QFileDialog.getSaveFileName(None, "Save File", "", "PNG files (*.png)")[0]
        if SAVE_PATH:
            try:
                self.outputImage.pixmap().save(SAVE_PATH+".png", "PNG")
                
                if self.saveLatentCheckBox.isChecked():
                    np.save(SAVE_PATH + ".npy", latentVector)

                if self.saveVideoCheckBox.isChecked() or self.saveVideoCheckBox2.isChecked():
                    self.saveVideo(SAVE_PATH)

            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Error", f"Error saving image: {e}")

    def saveVideo(self, SAVE_PATH):
        global latentVector, ogLatentVector

        numSteps = sum([abs(self.slider_list[i].value()) for i in range(len(self.slider_list))])
        fps = numSteps / 5
        interpolation = []
        interpolation.append(ogLatentVector)


        for i in range(len(vectors)):
            if self.slider_list[i].value() == 0:
                continue
            baseVector = interpolation[-1]
            value = self.slider_list[i].value()
            step = -1 if value < 0 else 1
            nth = np.divide(vectors[i], nerfingValues[i])

            for j in range(0, value, step):
                aux = np.multiply(nth, j)
                auxVector = np.add(baseVector, aux)
                interpolation.append(auxVector)

        out = cv2.VideoWriter(SAVE_PATH + "_1by1.mp4", cv2.VideoWriter_fourcc(*'MP4V'), fps, (1024, 1024))
        for vector in interpolation:
            img = self.latent2Image(vector)
            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
            out.write(img)

        out.release()

        interpolation = [ogLatentVector]
    
        # METHOD 2 self.saveVideoCheckBox2       
        for i in range(1, numSteps):
            interpolation.append(ogLatentVector + (latentVector - ogLatentVector) * i / numSteps)

        out = cv2.VideoWriter(SAVE_PATH + "_mashup.mp4", cv2.VideoWriter_fourcc(*'MP4V'), fps, (1024, 1024))
        for vector in interpolation:
            img = self.latent2Image(vector)
            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
            out.write(img)

        out.release()

        """ Save video of latent vector movement"""


#-------------------------------------------------------------------------
# Latent Generation Functions
    def loadLatent(self):
        """ Open file dialog and load latent vector"""

        global latentVector, ogLatentVector

        INPUT_PATH = QtWidgets.QFileDialog.getOpenFileName(None, "Window name", "", "NPY files (*.npy)")[0]
        if INPUT_PATH:
            ogLatentVector = np.load(INPUT_PATH)
            print(ogLatentVector.shape)
            latentVector = ogLatentVector
            img = self.latent2Image(ogLatentVector)
            qImg = QtGui.QImage(img.data.tobytes(), 1024, 1024, 3072, QtGui.QImage.Format_RGB888)
            self.inputImage.setPixmap(QtGui.QPixmap(qImg))
            self.moveVector()

    def projectImage(self):
        """ Project input image onto latent space"""
        global ogLatentVector, latentVector, projectionTarget

        steps = self.projectStepsLineEdit.text()
        ogLatentVector = run_projection(G=G, target_fname=projectionTarget, num_steps=int(steps), device=device)

        img = self.latent2Image(ogLatentVector)
        qImg = QtGui.QImage(img.data.tobytes(), 1024, 1024, 3072, QtGui.QImage.Format_RGB888)
        self.inputImage.setPixmap(QtGui.QPixmap(qImg))        
        self.moveVector()

    def randomFace(self):
        """ Generate random latent vector and display image"""
        global latentVector, ogLatentVector

        # call projection functions     
        latentVector = ogLatentVector = np.random.randn(1, 512)

        img = self.latent2Image(ogLatentVector)
        qImg = QtGui.QImage(img.data.tobytes(), 1024, 1024, 3072, QtGui.QImage.Format_RGB888)
        self.inputImage.setPixmap(QtGui.QPixmap(qImg))
        self.moveVector()


#-------------------------------------------------------------------------
# Latent Manipulation Functions

    def moveVector(self):
        """ Move latentVector in the direction of the attributes"""
        global latentVector, ogLatentVector, vectors
        
        latentVector = ogLatentVector
    
        for i in range(len(vectors)):
            nth = np.divide(vectors[i], nerfingValues[i])
            aux = np.multiply(nth, self.slider_list[i].value())
            latentVector = np.add(latentVector, aux)

        img = self.latent2Image(latentVector)
        qImg = QtGui.QImage(img.data.tobytes(), 1024, 1024, 3072, QtGui.QImage.Format_RGB888)
        self.outputImage.setPixmap(QtGui.QPixmap(qImg))
     
    def latent2Image(self, vector):
        """ Pass latent vector through generator and display image"""
        z = torch.from_numpy(vector).float().to(device)
        label = torch.zeros([1, G.c_dim], device=device)

        img = G(z, label, truncation_psi=1, noise_mode='const')
        img = (img.permute(0, 2, 3, 1) * 127.5 + 128).clamp(0, 255).to(torch.uint8)[0].cpu().numpy()

        return img


        
##########################################################################


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
