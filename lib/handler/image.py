from lib.handler.basic import BasicHandler
from lib.helper.image import ImageHelper
from lib.detect import Detect
from PIL import Image
import cv2 as cv
import numpy as np

class ImageHandler(BasicHandler):

    def analyze(self):
        # Initialize detect
        self.detect = Detect().parse(self.capture)

        # Get detected image
        image = self.detect.image()

        # Get yolo path
        path = self.name_path('yolov5')

        # Save detected image
        cv.imwrite(path, image)

        # Append image path
        summary = {
            "yolo": path, "tags": self.detect.matches()
            }

        return summary

    def focus(self, fallback=[0.5,0.5]):

        if ( hasattr(self, 'detect') == False ):
            return fallback

        return self.detect.focus()

    def resize_many(self, sizes=[]):

        # URL Buffer
        urls = {}

        for size in sizes:
            urls[self.size_name(size)] = self.resize(size)

        return urls

    def resize(self, size=[1920,1080]):

        # Get size filepath
        path = self.size_path(size)

        # Crop resize image to target size
        image = ImageHelper.resize(self.capture, size)

        # Read mime type
        mime_type = self.file.mime_type()

        # Save image to filesystem
        cv.imwrite(path, image)

        # Optimize file size
        ImageHelper.optimize(path, mime_type)

        # Convert to webp format
        try:
            path = ImageHelper.webp(path)
        except:
            print('Skipping webp convertion')

        return path

    def crop_resize_many(self, sizes=[], focus=[0.5,0.5]):
        # URL Buffer
        urls = {}

        for size in sizes:
            urls[self.size_name(size)] = self.crop_resize(size, focus)

        return urls


    def crop_resize(self, size=[1920,1080], focus=[0.5,0.5]):
        # Get size filepath
        path = self.size_path(size)

        # Crop resize image to target size
        image = ImageHelper.crop_resize(self.capture, size, focus)

        # Read mime type
        mime_type = self.file.mime_type()

        # Save image to filesystem
        cv.imwrite(path, image)

        # Optimize file size
        ImageHelper.optimize(path, mime_type)

        # Convert to webp format
        try:
            path = ImageHelper.webp(path)
        except:
            print('Skipping webp convertion')

        return path

    def webp(self, quality=100):
        # Get size filepath
        path = self.name_path('webp')

        # Read mime type
        mime_type = self.file.mime_type()

        # Save image to filesystem
        cv.imwrite(path, self.capture)

        # Convert to webp format
        try:
            path = ImageHelper.webp(path, quality)
        except:
            print('Skipping webp convertion')

        return path

