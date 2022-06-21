import cv2 as cv
import numpy as np

CONFIDENCE = 0.5
SCORE_THRESHOLD = 0.5
IOU_THRESHOLD = 0.5

class YoloParser:

    config = './yolov3/yolov3.cfg'
    weights = './yolov3/yolov3.weights'
    labels = './yolov3/coco.names'

    def __init__(self, file):
        self.file = file


    def initFile(self):
        path = self.file.getTempPath()

        self.capture = cv.imread(path)


    def analyzeFile(self):
        labels = open(self.labels).read().strip().split("\n")

        colors = np.random.randint(0, 255, size=(len(labels), 3), dtype="uint8")

        net = cv.dnn.readNetFromDarknet(self.config, self.weights)

        blob = cv.dnn.blobFromImage(self.capture, 1/255.0, (416, 416), swapRB=True, crop=False)

        net.setInput(blob)

        h, w = self.capture.shape[:2]

        ln = net.getLayerNames()
        ln = [ln[i-1] for i in net.getUnconnectedOutLayers()]

        layer_outputs = net.forward(ln)

        boxes, confidences, class_ids = [], [], []

        for output in layer_outputs:
            # Loop on every object
            '''
            detection.shape is equal to 85, the first 4 values represent the position of the object, the (x, y) coordinates are the center point and the width and height of the bounding box, and the remaining numbers correspond to the object labels, because this is the COCO data set, it has 80 types of labels .

        For example, if the detected object is a person, the first value in the 80-length vector should be 1, and all other values should be 0, the second number of bicycles, the third number of cars, up to the 80th Object. Then use np.argmax()
        Function to get the class id because it returns the index of the maximum value in the 80-length vector.
        '''
            for detection in output:
                # Extract class id (label) and confidence (as probability)
                # Current target detection
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > CONFIDENCE:
                     # Relative to the bounding box coordinates
                     # The size of the self.capture, remember that YOLO actually
                     # Return the center (x, y) coordinates of the boundary
                     # Box, then the width and height of the box
                    box = detection[:4] * np.array([w, h, w, h])
                    (centerX, centerY, width, height) = box.astype("int")

                    # Use the center (x, y) coordinates to export x and y
                    # And the left corner of the bounding box
                    x = int(centerX - (width / 2))
                    y = int(centerY - (height / 2))

                    # Update bounding box coordinates, trust level, and class ID
                    boxes.append([x, y, int(width), int(height)])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)
        #Perform non-maximum suppression based on the previously defined score
        idxs = cv.dnn.NMSBoxes(boxes, confidences, SCORE_THRESHOLD, IOU_THRESHOLD)
        font_scale = 2
        thickness = 2
        # Make sure there is at least one test
        if len(idxs) > 0:
            # Cycle through our saved indexes
            for i in idxs.flatten():
                # Extract bounding box coordinates
                x, y = boxes[i][0], boxes[i][1]
                w, h = boxes[i][2], boxes[i][3]
                # Draw border rectangles and labels on the self.capture
                color = [int(c) for c in colors[class_ids[i]]]
                cv.rectangle(self.capture, (x, y), (x + w, y + h), color=color, thickness=thickness)
                text = f"{labels[class_ids[i]]}: {confidences[i]:.2f}"
                # Calculate the text width and height to draw a transparent box as the text background
                (text_width, text_height) = cv.getTextSize(text, cv.FONT_HERSHEY_SIMPLEX, fontScale=font_scale, thickness=thickness)[0]
                text_offset_x = x
                text_offset_y = y - 5
                box_coords = ((text_offset_x, text_offset_y), (text_offset_x + text_width + 2, text_offset_y - text_height))
                overlay = self.capture.copy()
                cv.rectangle(overlay, box_coords[0], box_coords[1], color=color, thickness=cv.FILLED)
                #Add (transparency of cuboid)
                self.capture = cv.addWeighted(overlay, 0.6, self.capture, 0.4, 0)
                cv.putText(self.capture, text, (x, y - 5), cv.FONT_HERSHEY_SIMPLEX,
                    fontScale=font_scale, color=(0, 0, 0), thickness=thickness)

        cv.imwrite(self.file.getDistPath('yolo'), self.capture)


