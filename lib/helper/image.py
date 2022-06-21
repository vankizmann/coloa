import cv2 as cv
import numpy as np
import os as os
import re as regex
from PIL import Image as pimg, ImageFile as pimgfile, ImageEnhance as pimgenhance
import mozjpeg_lossless_optimization as mopzjpeg

class ImageHelper:

    @staticmethod
    def resize(capture, size=[None, None]):
        src = np.array(capture.shape[:2])

        if ( isinstance(size, int) and src[0] > src[1] ):
            size = [None, size]

        if ( isinstance(size, int) and src[1] > src[0] ):
            size = [size, None]

        if ( isinstance(size, int) and src[1] == src[0] ):
            size = [size, size]

        if ( size[0] == None and size[1] == None ):
            return capture

        if ( size[0] != None ):
            dist = [size[0], int(src[0] * size[0] / float(src[1]))]

        if ( size[1] != None ):
            dist = [int(src[1] * size[1] / float(src[0])), size[1]]

        cache = pimg.fromarray(capture.copy()).resize(dist)
#         cache = cv.resize(capture.copy(), dist)

        return np.asarray(cache)

    @staticmethod
    def crop_resize(capture, size=[1920,1080], focus=[0.5,0.5]):
        # Get original sizes
        src = np.array(capture.shape[:2])

        # Store original sizes
        tmp = np.array(capture.shape[:2])

        # Flip size
        size = np.flip(size)

        # Convert for pillow
        cache = pimg.fromarray(capture.copy())

        for key in range(len(size)) :
            upscale = False

            # If requested size is bigger than original size
            # start upscaling process
            if ( size[key] > src[key] ):
                upscale = True

            ratio = 1

            # If upscale is enabled calculate the required ratio
            if ( upscale ) :
                ratio = 1 / src[key] * size[key]

            # Resize image if all target sizes are to big for image
            if ( size[0] > src[0] or size[1] > src[1] ):
                src[0] = int(src[0] * ratio)
                src[1] = int(src[1] * ratio)

        # target 900x1280 source 800x1200

        # Resize capture accordingly to the target size
        cache = cache.resize((src[1], src[0]))

        # Sharpen kernel
        kernel = np.array([
            [0, -1, 0],
            [-1, 5,-1],
            [0, -1, 0]
            ])

        # Sharp image incase of upscaling
        if ( tmp[0] < src[0] or tmp[1] < src[1] ):
            cache = pimgenhance.Sharpness(cache).enhance(0.5)

        # Calculate possible aspect ratios for the source image
        aspect = (1/size[0]*size[1], 1/size[1]*size[0])


        if ( aspect[0] >= aspect[1] ):

            arun = int(src[1]*aspect[1])
            brun = int(src[0]*aspect[0])

            if ( arun > src[0] ):
                dist = (src[0], brun)

            else:
                dist = (arun, src[1])

        else:

            arun = int(src[1]*aspect[1])
            brun = int(src[0]*aspect[0])

            if ( arun > src[1] ):
                dist = (src[0], brun)

            else:
                dist = (src[1], arun)

        # Calculate resized boundry boxes
        resized = np.array([
            [int(src[0]*focus[1]-dist[0]/2), int(src[0]*focus[1]+dist[0]/2)],
            [int(src[1]*focus[0]-dist[1]/2), int(src[1]*focus[0]+dist[1]/2)],
            ])

        # Normalize if first height is smaller than zero
        if (resized[0,0] < 0):
            resized[0,1] -= resized[0,0]
            resized[0,0] = 0

        # Normalize if first height is bigger than source size
        if (resized[0,1] > src[0]):
            resized[0,0] -= resized[0,1] - src[0]
            resized[0,1] = src[0]

        # Normalize if first width is smaller than zero
        if (resized[1,0] < 0):
            resized[1,1] -= resized[1,0]
            resized[1,0] = 0

        # Normalize if first width is bigger than source size
        if (resized[1,1] > src[1]):
            resized[1,0] -= resized[1,1] - src[1]
            resized[1,1] = src[1]


        crop = (
            resized[1,0], resized[0,0],
            resized[1,1], resized[0,1]
            )

        # Crop image to size
        cache = cache.crop(crop)

        # Resize image to target dimensions
        cache = cache.resize([size[1], size[0]])

        return np.asarray(cache)

    @staticmethod
    def optimize(path, mime='none'):
        # Load file with Pillow
        capture = pimg.open(path)

        pimgfile.MAXBLOCK = capture.size[0]*capture.size[1]

        #if ( mime == 'image/png' ):
        #    capture = capture.quantize(method=pimg.LIBIMAGEQUANT, palette=pimg.WEB).convert('RGBA')

        # Save image with given quality
        capture.save(path, quality="medium", optimize=True, progressive=True)

        # Open saved file as binary
        binary = open(path, "rb").read()

        # Optimize binary
        if ( mime == 'image/jpeg' ):
            binary = mopzjpeg.optimize(binary)

        # Save final file
        open(path, "wb").write(binary)

        # Output size
        print(int(os.path.getsize(path)/1024), 'kb')

    @staticmethod
    def webp(path):
        # Load file with Pillow
        capture = pimg.open(path)

        # Change file ending
        path = regex.sub('\.(.*?)$', '.webp', path)

        # Save image with given quality
        capture.save(path, optimize=True, progressive=True, quality="medium", format="webp")

        # Output size
        print(int(os.path.getsize(path)/1024), 'kb')