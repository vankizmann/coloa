import cv2 as cv
import numpy as np
from lib.helper.image import ImageHelper

class BasicHandler:

    def __init__(self, file):
        self.file = file

    def init(self):
        # Initialize cv capture
        self.capture = cv.imread(self.file.temp_path(), cv.IMREAD_UNCHANGED)

        return self


    def size_name(self, size=[1920,1080]):
        # Return human string size
        final = size.copy()

        if ( final[0] == None ):
            final[0] = 'auto'

        if ( final[1] == None ):
            final[1] = 'auto'

        return str(final[0]) + '-' + str(final[1])


    def size_path(self, size=[1920,1080]):
        # Return human file path
        return self.file.dist_path(self.size_name(size))


    def name_path(self, name='default'):
        # Return human file path
        return self.file.dist_path(name)