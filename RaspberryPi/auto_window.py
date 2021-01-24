from PyQt5.QtCore import pyqtSignal, Qt, QTimer
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QWidget
from arduino import *
import numpy as np
from imutils.object_detection import non_max_suppression
import pytesseract
import cv2
from time import sleep
from math import sqrt, fabs


def decode_predictions(scores, geometry):
    # grab the number of rows and columns from the scores volume, then
    # initialize our set of bounding box rectangles and corresponding
    # confidence scores
    (numRows, numCols) = scores.shape[2:4]
    rects = []
    confidences = []

    # loop over the number of rows
    for y in range(0, numRows):
        # extract the scores (probabilities), followed by the
        # geometrical data used to derive potential bounding box
        # coordinates that surround text
        scoresData = scores[0, 0, y]
        xData0 = geometry[0, 0, y]
        xData1 = geometry[0, 1, y]
        xData2 = geometry[0, 2, y]
        xData3 = geometry[0, 3, y]
        anglesData = geometry[0, 4, y]

        # loop over the number of columns
        for x in range(0, numCols):
            # if our score does not have sufficient probability,
            # ignore it
            if scoresData[x] < 0.5:
                continue

            # compute the offset factor as our resulting feature
            # maps will be 4x smaller than the input image
            (offsetX, offsetY) = (x * 4.0, y * 4.0)

            # extract the rotation angle for the prediction and
            # then compute the sin and cosine
            angle = anglesData[x]
            cos = np.cos(angle)
            sin = np.sin(angle)

            # use the geometry volume to derive the width and height
            # of the bounding box
            h = xData0[x] + xData2[x]
            w = xData1[x] + xData3[x]

            # compute both the starting and ending (x, y)-coordinates
            # for the text prediction bounding box
            endX = int(offsetX + (cos * xData1[x]) + (sin * xData2[x]))
            endY = int(offsetY - (sin * xData1[x]) + (cos * xData2[x]))
            startX = int(endX - w)
            startY = int(endY - h)

            # add the bounding box coordinates and probability score
            # to our respective lists
            rects.append((startX, startY, endX, endY))
            confidences.append(scoresData[x])

    # return a tuple of the bounding boxes and associated confidences
    return (rects, confidences)


def getFrame(camera):
    return_value, image = camera.read()
    orig = image.copy()
    (origH, origW) = image.shape[:2]

    # set the new width and height and then determine the ratio in change
    # for both the width and height
    (newW, newH) = (640, 480)  ## WIDTH HEIGHT
    rW = origW / float(newW)
    rH = origH / float(newH)

    # resize the image and grab the new image dimensions
    image = cv2.resize(image, (newW, newH))
    (H, W) = image.shape[:2]

    # define the two output layer names for the EAST detector model that
    # we are interested -- the first is the output probabilities and the
    # second can be used to derive the bounding box coordinates of text
    layerNames = [
        "feature_fusion/Conv_7/Sigmoid",
        "feature_fusion/concat_3"]

    # load the pre-trained EAST text detector
    net = cv2.dnn.readNet("frozen_east_text_detection.pb")

    # construct a blob from the image and then perform a forward pass of
    # the model to obtain the two output layer sets
    blob = cv2.dnn.blobFromImage(image, 1.0, (W, H),
                                 (123.68, 116.78, 103.94), swapRB=True, crop=False)
    net.setInput(blob)
    (scores, geometry) = net.forward(layerNames)

    # decode the predictions, then  apply non-maxima suppression to
    # suppress weak, overlapping bounding boxes
    (rects, confidences) = decode_predictions(scores, geometry)
    boxes = non_max_suppression(np.array(rects), probs=confidences)

    # initialize the list of results
    results = []

    # loop over the bounding boxes
    for (startX, startY, endX, endY) in boxes:
        # scale the bounding box coordinates based on the respective
        # ratios
        startX = int(startX * rW)
        startY = int(startY * rH)
        endX = int(endX * rW)
        endY = int(endY * rH)

        # in order to obtain a better OCR of the text we can potentially
        # apply a bit of padding surrounding the bounding box -- here we
        # are computing the deltas in both the x and y directions
        dX = int((endX - startX) * 0.0)
        dY = int((endY - startY) * 0.2)

        # apply padding to each side of the bounding box, respectively
        startX = max(0, startX - dX)
        startY = max(0, startY - dY)
        endX = min(origW, endX + (dX * 2))
        endY = min(origH, endY + (dY * 2))

        # extract the actual padded ROI
        roi = orig[startY:endY, startX:endX]

        # in order to apply Tesseract v4 to OCR text we must supply
        # (1) a language, (2) an OEM flag of 4, indicating that the we
        # wish to use the LSTM neural net model for OCR, and finally
        # (3) an OEM value, in this case, 7 which implies that we are
        # treating the ROI as a single line of text
        config = ("-l eng --oem 1 --psm 7")
        text = pytesseract.image_to_string(roi, config=config)

        # add the bounding box coordinates and OCR'd text to the list
        # of results
        results.append(((startX, startY, endX, endY), text))

    # sort the results bounding box coordinates from top to bottom
    results = sorted(results, key=lambda r: r[0][1])

    # loop over the results
    for ((startX, startY, endX, endY), text) in results:
        # display the text OCR'd by Tesseract
        #print("OCR TEXT")
        #print("========")
        #print("{}\n".format(text))
        # x = (endX + startX) / 2
        # y = (endY + startY) / 2
        #print((endX + startX) / 2)
        #print((endY + startY) / 2)

        # strip out non-ASCII text so we can draw the text on the image
        # using OpenCV, then draw the text and a bounding box surrounding
        # the text region of the input image
        text = "".join([c if ord(c) < 128 else "" for c in text]).strip()# + " x: " + str(x) + " y: " + str(y)
        #output = orig.copy()
        cv2.rectangle(orig, (startX, startY), (endX, endY), (0, 0, 255), 2)
        cv2.putText(orig, text, (startX, startY - 20), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)

        # show the output image
        #cv2.imshow("Text Detection", output)
        #cv2.waitKey(0)

    height, width, channel = orig.shape
    bytesPerLine = 3 * width
    qImg = QImage(orig.data, width, height, bytesPerLine, QImage.Format_RGB888)
    #       qpixmap = QPixmap(qimg)
    return qImg, results


class AutoWindow(QWidget):

    switch_window = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.title = "Auto mode"
        self.left = 900
        self.top = 500  # 70
        self.width = 800
        self.height = 410
        self.angle = [90, 90, 90, 90, 7, 90]
        self.auto_enable = False
        self.camera = cv2.VideoCapture(0)
        self.word_sel = "STO"
        self.logs = "data:"
        self.word = None
        self.action = None
        self.frame, self.results = getFrame(self.camera)
        self.sto_pos, self.lat_pos, self.agh_pos, self.rok_pos = [None, None], [None, None], [None, None], [None, None]
        # positions not detected

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.picture = QLabel(self)
        self.picture.setGeometry(0, 0, 640, 300)
        self.picture.setScaledContents(True)
        self.picture.setPixmap(QPixmap(self.frame))

        self.start_btn = QPushButton('ułóż zdanie', self)
        self.start_btn.setToolTip('Rozpocznij układanie słowa.')
        self.start_btn.setGeometry(4, 305, 145, 100)
        self.start_btn.clicked.connect(self.switch_auto)

        self.switch_btn = QPushButton('tryb manualny', self)
        self.switch_btn.setToolTip('Przełącz na tryb manualny.')
        self.switch_btn.setGeometry(153, 305, 145, 100)
        self.switch_btn.clicked.connect(self.switch)

        self.instructions_btn = QPushButton('instrukcja', self)
        self.instructions_btn.setToolTip('Wyświetl instrukcję obsługi ramienia.')
        self.instructions_btn.setGeometry(302, 305, 145, 100)
        self.instructions_btn.clicked.connect(self.instructions)

        self.label_logs = QLabel(self)
        self.label_logs.setWordWrap(True)
        self.label_logs.setText(self.logs)
        self.label_logs.setAlignment(Qt.AlignTop)
        self.label_logs.setStyleSheet("QLabel {background-color: lightgrey;}")
        self.label_logs.setGeometry(642, 0, 158, 410)

        self.timer = QTimer()
        self.timer.setInterval(5000)  # how often to take photo
        self.timer.timeout.connect(self.auto_loop)
        self.timer.start()

    def switch_auto(self):
        for word in ["STO", "LAT", "AGH", "2020"]:
            self.word = word
            self.update_logs()
            self.move_word(word)
        self.word = "DONE"
        self.update_logs()

    def move_word(self, word):
        if word == "STO":
            current_pos = self.sto_pos
            place_pos = [160, 443]
        elif word == "LAT":
            current_pos = self.lat_pos
            place_pos = [270, 443]
        elif word == "AGH":
            current_pos = self.agh_pos
            place_pos = [370, 443]
        else:
            current_pos = self.rok_pos
            place_pos = [490, 443]

        # release
        self.angle[5] = 120
        sleep(0.5)

        # move to current_pos
        self.action = "grab word"
        self.update_logs()
        self.move_servo(current_pos)
        sleep(0.5)

        # grab
        self.angle[5] = 90
        sleep(0.5)

        # move to place_pos
        self.action = "place word"
        self.update_logs()
        self.move_servo(place_pos)
        sleep(0.5)

    def move_servo(self, pos):     # 355, 258 - 2020 in the middle
        # TODO map pos to servo angles
        pos[0] -= 150   # set centre at arm base
        pos[1] += 250

        pixel_dist = sqrt(40000 + pos[0]**2 + pos[1]**2)  # distance from block to arm servo2
        if pixel_dist <= 360:
            temp1, temp2, temp3 = 96, 40, 11
        elif pixel_dist <= 400:
            temp1, temp2, temp3 = 107, 49, 17
        elif pixel_dist <= 440:
            temp1, temp2, temp3 = 116, 59, 21
        elif pixel_dist <= 480:
            temp1, temp2, temp3 = 125, 70, 21
        elif pixel_dist <= 500:
            temp1, temp2, temp3 = 129, 80, 22
        elif pixel_dist <= 520:
            temp1, temp2, temp3 = 130, 78, 25
        elif pixel_dist <= 540:
            temp1, temp2, temp3 = 138, 82, 31
        elif pixel_dist <= 580:
            temp1, temp2, temp3 = 141, 82, 39
        elif pixel_dist <= 600:
            temp1, temp2, temp3 = 148, 82, 49
        elif pixel_dist <= 640:
            temp1, temp2, temp3 = 146, 77, 58
        elif pixel_dist <= 680:
            temp1, temp2, temp3 = 162, 97, 57
        else:
            temp1, temp2, temp3 = 180, 111, 70

        # alpha = int(np.arccos(pixel_dist/720) * 57.2958)  # calculate target angle
        diff_angle1 = temp1 - self.angle[1]
        diff_angle2 = temp2 - self.angle[2]
        diff_angle3 = temp3 - self.angle[3]
        diff_angle0 = int(np.arctan(pos[1] / pos[0]) * 57.2958 + 13) - self.angle[0]  # 13 - offset

        iterator = max(fabs(diff_angle1), fabs(diff_angle2), fabs(diff_angle3), fabs(diff_angle0))

        for i in range(int(iterator)):  # smooth out angle change for lower power consumption

            if i <= fabs(diff_angle0):
                if diff_angle1 > 0:
                    self.angle[0] += 1
                else:
                    self.angle[0] -= 1
            if i <= fabs(diff_angle1):
                if diff_angle1 > 0:
                    self.angle[1] += 1
                else:
                    self.angle[1] -= 1
            if i <= fabs(diff_angle2):
                if diff_angle2 > 0:
                    self.angle[2] += 1
                else:
                    self.angle[2] -= 1
            if i <= fabs(diff_angle3):
                if diff_angle3 > 0:
                    self.angle[3] += 1
                else:
                    self.angle[3] -= 1

            self.serial_write()
            sleep(0.5)

    def auto_loop(self):

        self.frame, self.results = getFrame(self.camera)
        self.picture.setPixmap(QPixmap(self.frame))
        for ((startX, startY, endX, endY), text) in self.results:
            text = "".join([c if ord(c) < 128 else "" for c in text]).strip()  # delete non-ASCII characters
            x = (endX + startX) / 2
            y = (endY + startY) / 2

            if "to" in text.lower():
                self.sto_pos = [x, y]
            elif "at" in text.lower():
                self.lat_pos = [x, y]
            elif "g" in text.lower():
                self.agh_pos = [x, y]
            elif "2" in text.lower():
                self.rok_pos = [x, y]

        #if self.auto_enable:
        #    self.serial_write()

        self.update_logs()

    def update_logs(self):
        self.logs = "data:\n\nSTO: " + str(self.sto_pos) + "\nLAT: " + str(self.lat_pos) + "\nAGH: " + str(self.agh_pos) + "\n2020: " + str(self.rok_pos) + "\nservos: " + str([np.uint8(200),
                            np.uint8(self.angle[0]), np.uint8(self.angle[1]), np.uint8(self.angle[2]), np.uint8(self.angle[3]), np.uint8(self.angle[4]), np.uint8(self.angle[5])]) + "\ncurrent word: " + str(self.word) + " \ncurrent action: " + str(self.action)
        self.label_logs.setText(self.logs)

    def serial_write(self):
        arduino.write([np.uint8(200), np.uint8(self.angle[0]), np.uint8(self.angle[1]), np.uint8(self.angle[2]),
                                           np.uint8(self.angle[3]), np.uint8(self.angle[4]), np.uint8(self.angle[5])])

    def instructions(self):
        dlg = InformationDialog(self)
        dlg.text.setText(
            "Here goes our long text\n of course it can be multiline")
        dlg.exec_()

    def switch(self):
        self.timer.stop()
        self.switch_window.emit()
        self.close()
