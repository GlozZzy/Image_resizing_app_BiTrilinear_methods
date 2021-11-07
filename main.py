import math
import os

from PyQt5.Qt import QWIDGETSIZE_MAX
from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QLabel, QGridLayout, QFileDialog
from PyQt5.QtGui import QPainter, QPen, QImage, qRgba, QColor
from PyQt5.QtGui import QPixmap
from PIL import Image as im
import numpy as np


class Label(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)
        self.p = QPixmap()
        self.points = []

    def setPixmap(self, p):
        self.p = p
        self.update()

    def drawPoint(self, e):
        self.points.append(QPoint(e.x() - 10, e.y() - 10))
        self.update()

    def clearPoints(self):
        self.points = []
        self.update()

    def paintEvent(self, event):
        if not self.p.isNull():
            painter = QPainter(self)
            painter.setRenderHint(QPainter.SmoothPixmapTransform)
            painter.drawPixmap(self.rect(), self.p)
            painter.setPen(QPen(Qt.red, 5, Qt.SolidLine))
            for i in self.points:
                painter.drawPoint(i)


class CreateWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.ez_alg = True

        self.lab2 = QLabel()
        self.lab1 = QLabel()
        self.arr_input_pic1_points = []
        self.arr_input_pic2_points = []

        self.button_alg = QPushButton("USE SPECIAL ALGORITHM", self)
        self.button_form = QPushButton("FORMAT PIC", self)
        self.button_fix = QPushButton("FIX WINDOW SIZE", self)
        self.button_ch = QPushButton("CHOUSE PIC", self)
        self.button_cl = QPushButton("CLEAR", self)

        self.pic1 = Label(self)
        self.pic2 = Label(self)
        self.grid = QGridLayout()

        self.setGeometry(200, 50, 800, 500)
        self.setMinimumSize(300, 300)

        self.spacing = 3
        self.filename = None

        self.setMouseTracking(True)
        self.paint = False

        self.UIcomponents()
        self.show()

    def UIcomponents(self):
        self.grid.setSpacing(self.spacing)

        # Label 1
        self.lab1.setStyleSheet("border-style: solid; border-width: 1px; border-color: Black;")

        # Label 2
        self.lab2.setStyleSheet("border-style: solid; border-width: 1px; border-color: Black;")

        # Button CHOUSE
        self.button_ch.clicked.connect(self.setimage)

        # Button CLEAR
        self.button_cl.clicked.connect(self.clear)

        # Button FIX WINDOW SIZE
        self.button_fix.clicked.connect(self.fixWndSize)

        # Button FORMAT PIC
        self.button_form.clicked.connect(self.format_pic)

        # Button FORMAT PIC
        self.button_alg.clicked.connect(self.format_pic)

        # positionate the buttons
        self.grid.addWidget(self.lab1, 0, 0)
        self.grid.addWidget(self.lab2, 0, 1)
        self.grid.addWidget(self.button_ch, 10, 0)
        self.grid.addWidget(self.button_fix, 10, 0)
        self.grid.addWidget(self.button_form, 10, 0)
        self.grid.addWidget(self.button_alg, 10, 0)
        self.grid.addWidget(self.button_cl, 10, 1)

        self.setLayout(self.grid)

    def setimage(self):
        self.filename, _ = QFileDialog.getOpenFileName(self, "Выбрать файл",
                                                       ".",
                                                       "JPEG Files(*.jpg);;\
                                                       PNG Files(*.png);;GIF File(*.gif)")

        if self.filename:
            # Picture 1
            self.pic1.setPixmap(QPixmap(self.filename))
            self.grid.addWidget(self.pic1, 0, 0)
            self.setLayout(self.grid)
            self.pic1.setVisible(True)

            # CHOUSE -> FIX WINDOW SIZE
            self.button_ch.setVisible(False)

    def allowResizeAndClearPoints(self):
        self.setMaximumSize(QWIDGETSIZE_MAX, QWIDGETSIZE_MAX);
        self.setMinimumSize(300, 300)

        self.arr_input_pic1_points = []
        self.arr_input_pic2_points = []
        self.pic1.clearPoints()
        self.paint = False

        if os.path.exists("temp.jpeg"):
            os.remove("temp.jpeg")

    def clear(self):
        # FIX WINDOW SIZE -> CHOUSE
        self.button_ch.setVisible(True)
        self.button_fix.setVisible(True)
        self.button_form.setVisible(True)

        self.paint = False
        self.ez_alg = True

        self.pic1.setVisible(False)
        self.pic2.setVisible(False)

        self.allowResizeAndClearPoints()

        self.grid.addWidget(self.button_cl, 10, 1)
        self.update()

    def fixWndSize(self):
        # FIX WINDOW SIZE -> FORMAT PIC
        self.button_fix.setVisible(False)

        self.setFixedSize(self.width(), self.height())
        self.paint = True

    def format_pic(self):
        if len(self.arr_input_pic1_points) == 3 and len(self.arr_input_pic2_points) == 3:
            beg_pos_lab2 = 10 + self.lab1.size().width() + self.spacing
            M1 = np.array([[self.arr_input_pic1_points[0].x() - 10, self.arr_input_pic1_points[0].y() - 10, 1, 0, 0, 0],
                           [0, 0, 0, self.arr_input_pic1_points[0].x() - 10, self.arr_input_pic1_points[0].y() - 10, 1],
                           [self.arr_input_pic1_points[1].x() - 10, self.arr_input_pic1_points[1].y() - 10, 1, 0, 0, 0],
                           [0, 0, 0, self.arr_input_pic1_points[1].x() - 10, self.arr_input_pic1_points[1].y() - 10, 1],
                           [self.arr_input_pic1_points[2].x() - 10, self.arr_input_pic1_points[2].y() - 10, 1, 0, 0, 0],
                           [0, 0, 0, self.arr_input_pic1_points[2].x() - 10, self.arr_input_pic1_points[2].y() - 10,
                            1]])

            v1 = np.array([self.arr_input_pic2_points[0].x() - beg_pos_lab2, self.arr_input_pic2_points[0].y() - 10,
                           self.arr_input_pic2_points[1].x() - beg_pos_lab2, self.arr_input_pic2_points[1].y() - 10,
                           self.arr_input_pic2_points[2].x() - beg_pos_lab2, self.arr_input_pic2_points[2].y() - 10])

            result = np.linalg.solve(M1, v1)
            mat_result = np.array([[result[0], result[1], result[2]],
                                   [result[3], result[4], result[5]],
                                   [0, 0, 1]])

            ObrMatrix = np.linalg.inv(mat_result)

            if self.ez_alg:
                self.easy_algorithm(ObrMatrix)
            else:
                self.grid.addWidget(self.button_cl, 10, 0, 1, 2)
                # max distance between two points on pic 1
                distance_bwn_two_points_1_pic1 = np.sqrt(
                    (self.arr_input_pic1_points[1].x() - self.arr_input_pic1_points[0].x()) ** 2 +
                    (self.arr_input_pic1_points[1].y() - self.arr_input_pic1_points[0].y()) ** 2
                )
                distance_bwn_two_points_2_pic1 = np.sqrt(
                    (self.arr_input_pic1_points[2].x() - self.arr_input_pic1_points[1].x()) ** 2 +
                    (self.arr_input_pic1_points[2].y() - self.arr_input_pic1_points[1].y()) ** 2
                )
                distance_bwn_two_points_3_pic1 = np.sqrt(
                    (self.arr_input_pic1_points[2].x() - self.arr_input_pic1_points[0].x()) ** 2 +
                    (self.arr_input_pic1_points[2].y() - self.arr_input_pic1_points[0].y()) ** 2
                )

                distance_bwn_two_points_pic1_max = max(distance_bwn_two_points_1_pic1, distance_bwn_two_points_2_pic1,
                                                       distance_bwn_two_points_3_pic1)

                # max distance between two points on pic 2
                distance_bwn_two_points_1_pic2 = np.sqrt(
                    (self.arr_input_pic2_points[1].x() - self.arr_input_pic2_points[0].x()) ** 2 +
                    (self.arr_input_pic2_points[1].y() - self.arr_input_pic2_points[0].y()) ** 2
                )
                distance_bwn_two_points_2_pic2 = np.sqrt(
                    (self.arr_input_pic2_points[2].x() - self.arr_input_pic2_points[1].x()) ** 2 +
                    (self.arr_input_pic2_points[2].y() - self.arr_input_pic2_points[1].y()) ** 2
                )
                distance_bwn_two_points_3_pic2 = np.sqrt(
                    (self.arr_input_pic2_points[2].x() - self.arr_input_pic2_points[0].x()) ** 2 +
                    (self.arr_input_pic2_points[2].y() - self.arr_input_pic2_points[0].y()) ** 2
                )

                distance_bwn_two_points_pic2_max = max(distance_bwn_two_points_1_pic2, distance_bwn_two_points_2_pic2,
                                                       distance_bwn_two_points_3_pic2)

                if distance_bwn_two_points_pic1_max > distance_bwn_two_points_pic2_max:
                    print("decrease -> trilinear algorithm")
                    self.trilinear_algorithm(ObrMatrix)
                else:
                    print("increase -> bilinear algorithm")
                    self.bilinear_algorithm(ObrMatrix)

    def easy_algorithm(self, ObrMatrix):
        image = im.open(self.filename)
        image = image.resize((self.pic1.size().width(), self.pic1.size().height()))
        rgb_im = image.convert('RGB')

        final_image = im.new('RGB', [image.size[0], image.size[1]], 0x000000)
        for x in range(final_image.size[0]):
            for y in range(final_image.size[1]):
                cur_p = np.array([x, y, 1])
                M = ObrMatrix.dot(cur_p)
                M[0] = int(M[0])
                M[1] = int(M[1])

                r, g, b = 255, 255, 255
                if 0 <= M[0] < image.size[0] and 0 <= M[1] < image.size[1]:
                    r, g, b = rgb_im.getpixel((M[0], M[1]))

                final_image.putpixel((x, y), (r, g, b))

        final_image.save("temp.jpeg")

        # Picture 2
        self.pic2.setPixmap(QPixmap("temp.jpeg"))
        self.grid.addWidget(self.pic2, 0, 1)
        self.setLayout(self.grid)
        self.pic2.setVisible(True)

        if os.path.exists("temp.jpeg"):
            os.remove("temp.jpeg")
        self.ez_alg = False
        self.button_form.setVisible(False)

    def bilinear_algorithm(self, ObrMatrix):
        image = im.open(self.filename)
        image = image.resize((self.pic1.size().width(), self.pic1.size().height()))
        rgb_im = image.convert('RGB')

        final_image = im.new('RGB', [image.size[0], image.size[1]], 0x000000)
        for x in range(final_image.size[0]):
            for y in range(final_image.size[1]):
                cur_p = np.array([x, y, 1])
                M = ObrMatrix.dot(cur_p)
                Mx = M[0]
                My = M[1]

                r, g, b = 255, 255, 255
                if 0 <= M[0] <= image.size[0] and 0 <= M[1] <= image.size[1]:
                    # math.ceil() /\ | math.floor() \/ | x - M[0] | y -M[1]
                    IxyPxl = list(rgb_im.getpixel((math.floor(Mx), math.floor(My))))
                    IXyPxl = list(rgb_im.getpixel((math.ceil(Mx), math.floor(My))))
                    IxYPxl = list(rgb_im.getpixel((math.floor(Mx), math.ceil(My))))
                    IXYPxl = list(rgb_im.getpixel((math.ceil(Mx), math.ceil(My))))

                    IxyRed = (IxyPxl[0] * (math.ceil(Mx) - Mx) + IXyPxl[0] * (Mx - math.floor(M[0]))) * (
                            math.ceil(My) - My) + (
                                     IxYPxl[0] * (math.ceil(Mx) - Mx) + IXYPxl[0] * (Mx - math.floor(Mx))) * (
                                     My - math.floor(My))
                    IxyGreen = (IxyPxl[1] * (math.ceil(Mx) - Mx) + IXyPxl[1] * (Mx - math.floor(M[0]))) * (
                                math.ceil(My) - My) + (
                                           IxYPxl[1] * (math.ceil(Mx) - Mx) + IXYPxl[1] * (Mx - math.floor(Mx))) * (
                                           My - math.floor(My))
                    IxyBlue = (IxyPxl[2] * (math.ceil(Mx) - Mx) + IXyPxl[2] * (Mx - math.floor(M[0]))) * (
                                math.ceil(My) - My) + (
                                          IxYPxl[2] * (math.ceil(Mx) - Mx) + IXYPxl[2] * (Mx - math.floor(Mx))) * (
                                          My - math.floor(My))
                    r, g, b = (IxyRed, IxyGreen, IxyBlue)
                final_image.putpixel((x, y), (int(r), int(g), int(b)))

        final_image.save("temp.jpeg")

        # Picture 2
        self.pic2.setPixmap(QPixmap("temp.jpeg"))
        self.grid.addWidget(self.pic2, 0, 1)
        self.setLayout(self.grid)
        self.pic2.setVisible(True)
        self.allowResizeAndClearPoints()

    def trilinear_algorithm(self, ObrMatrix):
        image = im.open(self.filename)
        image = image.resize((self.pic1.size().width(), self.pic1.size().height()))
        final_image = im.new('RGB', [image.size[0], image.size[1]], 0x000000)

        # creating arr of decreases pictures
        width = self.pic1.size().width()
        height = self.pic1.size().height()
        images = [image]
        while width > 1 or height > 1:
            if width > 1:
                width = math.ceil(width / 2)
            if height > 1:
                height = math.ceil(height / 2)
            images.append(im.open(self.filename).resize((width, height), im.BILINEAR).convert('RGB'))

        for x in range(final_image.size[0]):
            for y in range(final_image.size[1]):
                Pi1 = ObrMatrix.dot(np.array([x, y, 1]))
                Pi2 = ObrMatrix.dot(np.array([x + 1, y + 1, 1]))
                Kx = abs(Pi1[0] - Pi2[0])
                Ky = abs(Pi1[1] - Pi2[1])
                K = (Kx + Ky) / 2

                M2 = 1
                i = 0
                while M2 <= K:
                    M2 *= 2
                    i += 1
                M1 = M2 / 2

                r, g, b = 255, 255, 255
                if 0 <= Pi1[0] <= image.size[0] and 0 <= Pi1[1] <= image.size[1]:
                    IM1K = images[i - 1].getpixel((math.floor(Pi1[0] / M1), math.floor(Pi1[1] / M1)))
                    IM2K = images[i].getpixel((math.floor(Pi1[0] / M2), math.floor(Pi1[1] / M2)))

                    IRed = int((IM1K[0] * (M2 - K) + IM2K[0] * (K - M1)) / M1)
                    Igreen = int((IM1K[1] * (M2 - K) + IM2K[1] * (K - M1)) / M1)
                    Iblue = int((IM1K[2] * (M2 - K) + IM2K[2] * (K - M1)) / M1)

                    r, g, b = IRed, Igreen, Iblue
                final_image.putpixel((x, y), (r, g, b))
        final_image.save("temp.jpeg")

        # Picture 2
        self.pic2.setPixmap(QPixmap("temp.jpeg"))
        self.grid.addWidget(self.pic2, 0, 1)
        self.setLayout(self.grid)
        self.pic2.setVisible(True)
        self.allowResizeAndClearPoints()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and self.paint:
            if 10 <= event.x() <= 10 + self.lab1.size().width() and 10 <= event.y() <= 10 + self.lab1.size().height():
                if len(self.arr_input_pic1_points) < 3:
                    self.arr_input_pic1_points.append(QPoint(event.x(), event.y()))
                    self.pic1.drawPoint(event.pos())

            beg_pos_lab2 = 10 + self.lab1.size().width() + self.spacing
            if (beg_pos_lab2 <= event.x() <= beg_pos_lab2 + self.lab2.size().width()) and \
                    (10 <= event.y() <= self.lab2.size().height() + 10):
                if len(self.arr_input_pic2_points) < 3:
                    self.arr_input_pic2_points.append(QPoint(event.x(), event.y()))
                    self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        pen = QPen(Qt.red, 5)
        painter.setPen(pen)
        for i in self.arr_input_pic1_points:
            painter.drawPoint(i)
        for i in self.arr_input_pic2_points:
            painter.drawPoint(i)


if __name__ == '__main__':
    app = QApplication([])
    wind = CreateWindow()
    wind.setWindowTitle("Image resizing")
    app.exec_()
