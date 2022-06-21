from fastapi.responses import FileResponse
from lib.file import File
import re as regex
import numpy as np
import glob as glob
import os as os
import time as time

class Router:

    url = 'https://coloa.vanki.de'

    @staticmethod
    def run(url, size):
        # Clean files
        Router.clean()

        # Initiate file
        file = File(url)

        # Convert size
        size = Router.param(size, data_type='int')

        # Resize file and return path
        path = file.convert().init().resize(size=size)

        # Clean file
        file.clean()

        # Return plain file
        return FileResponse(path)


    @staticmethod
    def get(url, focus, size, detect):
        # Clean files
        Router.clean()

        # Initiate file
        file = File(url)

        # Initiate image
        image = file.convert().init()

        # Prepare result object
        result =  {}

        # Analyze image for objects
        if ( detect ):
            result = image.analyze()

        # Convert focus point
        focus = Router.param(focus, data_type='float')

        # Get calculated focus point
        if ( focus[0] == None or focus[1] == None ):
            focus = image.focus()

        # Convert sizes
        sizes = Router.params(size, data_type='int')

        # Get paths
        result['urls'] = image.crop_resize_many(sizes=sizes, focus=focus)

        # Convert paths into urls
        for key, value in result['urls'].items():
            result['urls'][key] = regex.sub('^.', Router.url, value)

        # Convert yolo path to url
        if ( hasattr(result, 'yolo') ):
            result['yolo'] = regex.sub('^.', ref, result['image'])

        # Set focus to result
        result['focus'] = { "x": focus[0], "y": focus[1]}

        # Clean file
        file.clean()

        return result


    @staticmethod
    def params(sizes, fallback=None, data_type = 'int', fix_none = True):
        if ( sizes == None ):
            sizes = []

        for index, size in enumerate(sizes):
            sizes[index] = Router.param(size, fallback, data_type, fix_none)

        return sizes


    @staticmethod
    def param(size, fallback=None, data_type = 'int', fix_none = True):
        if ( size == None ):
            size = [fallback, fallback]

        if ( isinstance(size, str) ):
            size = regex.split('[,:]', size)

        if ( size[0] == 'auto' and fix_none == True ):
            size[0] = fallback

        if ( size[1] == 'auto' and fix_none == True ):
            size[1] = fallback

        if ( isinstance(size[0], str) and data_type == 'int' ):
            size[0] = int(size[0])

        if ( isinstance(size[1], str) and data_type == 'int' ):
            size[1] = int(size[1])

        if ( isinstance(size[0], str) and data_type == 'float' ):
            size[0] = round(float(size[0]), 2)

        if ( isinstance(size[1], str) and result_type == 'float' ):
            size[1] = round(float(size[1]), 2)

        return size

    @staticmethod
    def clean():

        for path in glob.glob('./temp/*', recursive=False):
            if ( Router.is_junk(path) ):
                os.remove(path)

        for path in glob.glob('./dist/*', recursive=False):
            if ( Router.is_empty(path) ):
                os.rmdir(path)

        for path in glob.glob('./dist/**/*.*', recursive=True):
            if ( Router.is_junk(path) ):
                os.remove(path)


    @staticmethod
    def is_junk(path):
        # Get current time
        now = time.time()

        # Wildcard for gitignore
        if ( os.path.basename(path) == '.gitignore' ):
            return False

        # Wildcard for folders
        if ( os.path.isdir(path) == True ):
            return False

        # Wildcard for files
        if ( os.path.isfile(path) == False ):
            return False

        # Returns if file is older than an hour
        return os.stat(path).st_mtime < now - 60*60


    @staticmethod
    def is_empty(path):
        # Get current time
        now = time.time()

        # Wildcard for files
        if ( os.path.isfile(path) == True ):
            return False

        # Wildcard for files
        if ( os.path.isdir(path) == False ):
            return False

        if ( len(os.listdir(path)) != 0 ):
            return False

        return os.stat(path).st_mtime < now - 60*60