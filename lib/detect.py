from lib.helper.image import ImageHelper
import torch as torch
import cv2 as cv
import numpy as np


class Detect:

    # Use only matches over 0.X
    confident = 0.5

    # Tagret box color
    boxcolor = (200,50,50)

    def __init__(self):
        # self.net = torch.hub.load('./yolov5', 'custom', path='./yolov5/runs/train/exp3/weights/best.pt', source='local')
        self.net = torch.hub.load('./yolov5', 'custom', path='./weights/yolov5s.pt', source='local')

    def parse(self, image):
        cache = ImageHelper.resize(image.copy(), 640)

        self.model = self.net(cache)

        return self

    def point(self, xyxyn):
        # Collect rect locations
        xmin, ymin, xmax, ymax, conf, cla, label = xyxyn[0:]

        # If confidence is to low abort
        if conf < self.confident:
            return None

        if ( label == 'person' ):
            ymax = (ymin+ymin+ymin+ymax+ymax)/5

        return ((xmin+xmax)/2, (ymin+ymax)/2)

    def rect(self, capture, xyxyn):
        # Collect rect locations
        xmin, ymin, xmax, ymax, conf, cla, label = xyxyn[0:]

        # If confidence is to low abort
        if conf < self.confident:
            return capture

        # Calculate top left, bottom left
        rect_a = (int(xmin*capture.shape[1]), int(ymin*capture.shape[0]))

        # Calculate top right, bottom right
        rect_b = (int(xmax*capture.shape[1]), int(ymax*capture.shape[0]))

        # Modify capture
        capture = cv.rectangle(capture, rect_a, rect_b,
            color=self.boxcolor, thickness=1)

        return capture

    def text(self, capture, xyxyn, fontScale=0.3):
        # Collect rect locations
        xmin, ymin, xmax, ymax, conf, cla, label = xyxyn[0:]

        # If confidence is to low abort
        if conf < self.confident:
            return capture

        # Get text target size
        text = cv.getTextSize(label, fontScale=fontScale,
            fontFace=cv.FONT_HERSHEY_DUPLEX, thickness=1)[0]

        # Calculate top left, bottom left
        rect_a = (int(xmin*capture.shape[1]), int(ymin*capture.shape[0]))

        # Calculate top right, bottom right
        rect_b = (int(xmax*capture.shape[1]), int(ymax*capture.shape[0]))

        # Calculate top left, bottom left
        text_a = (rect_a[0], rect_b[1] - text[1] - 6)

        # Calculate top right, bottom right
        text_b = (rect_a[0] + text[0] + 6, rect_b[1])

        # Return if label is bigger than box
        if (text_a[1] < rect_a[1] or text_b[0] > rect_b[0]):
            return capture

        # Print background box
        cache = cv.rectangle(capture, text_a, text_b,
            color=self.boxcolor, thickness=-1)

        # Calculate top left, bottom center
        text_c = (text_a[0] + 3, text_b[1] - int(text[1]/2))

        # Print text box
        capture = cv.putText(capture, label, text_c, color=(255,255,255), fontScale=fontScale,
            fontFace=cv.FONT_HERSHEY_DUPLEX, thickness=1, lineType=cv.LINE_AA)

        return capture


    def image(self):
        # Get cache image
        cache = self.model.imgs[0].copy()

        for xyxyn in np.array(self.model.pandas().xyxyn[0]):
            # Print boundry box
            self.rect(cache, xyxyn)

            # Print text box
            self.text(cache, xyxyn)

        return cache

    def focus(self):
        # Set base focus
        focus = [0.5,0.5]

        # Convert to array
        arr = np.array(self.model.pandas().xyxyn[0])

        for xyxyn in np.flip(arr, axis=0):
            # Get closest point matrix
            temp = self.point(xyxyn)

            # Break if empty
            if ( temp == None ):
                continue

            weight = 0.1

            if ( xyxyn[6] == 'person' ) :
                weight = 1.9

            # Override focus with given data
            focus = [
                round((focus[0]*(2-weight)+temp[0]*weight)/2, 2),
                round((focus[1]*(2-weight)+temp[1]*weight)/2, 2)
                ]

        return focus

    def matches(self):
        # Tags container
        tags = []

        for xyxyn in np.array(self.model.pandas().xyxyn[0]):
            # Collect rect locations
            xmin, ymin, xmax, ymax, conf, cla, label = xyxyn[0:]

            # If confidence is to low abort
            if conf < self.confident:
                continue

            tags += [{
                     "label": label,
                     "rate": conf,
                     "xpos": (xmin+ymin)/2,
                     "ypos": (xmax+ymax)/2,
                     }]

        return tags