import requests as req
import uuid as uuid
import mimetypes as mimetype
import magic as magic
import re as regex
import os as os
from lib.handler.image import ImageHandler
from lib.handler.pdf import PdfHandler
from lib.handler.video import VideoHandler
from fastapi import HTTPException

class File:

    def __init__(self, url):
        self.url = url
        self.fetch()


    def temp_name(self):

        if ( hasattr(self, '_temp_name') and self._temp_name != None ):
            return self._temp_name

        self._temp_name = str(uuid.uuid4())

        return self._temp_name


    def temp_path(self):
        return './temp/' + self.temp_name()


    def dist_name(self):

        if ( hasattr(self, '_dist_name') and self._dist_name != None ):
            return self._dist_name

        self._dist_name = self.temp_name()

        # Get mime extension
        ext = regex.sub('^[^\/]+\/', '', self.mime_type())

        if ( ext != None ):
            self._dist_name = self._dist_name + '.' + ext

        return self._dist_name


    def dist_path(self, size="default"):

        path = './dist/{}/'.format(size)

        if ( os.path.isdir(path) == False ) :
            os.mkdir(path)

        return os.path.join(path, self.dist_name())


    def fetch(self):
        res = req.get(self.url)

        if ( res.status_code != 200 ):
            raise HTTPException(status_code=500, detail='File cannot be retrieved: ' + str(res.status_code))

        open(self.temp_path(), 'wb').write(res.content)

        return self

    def mime_type(self):

        if ( hasattr(self, '_mime_type') and self._mime_type != None ):
            return self._mime_type

        reader = magic.Magic(mime=True, uncompress=True)

        self._mime_type = reader.from_file(self.temp_path())

        if ( self._mime_type == None ):
            raise HTTPException(status_code=500, detail='MimeType cannot be detected')

        return self._mime_type

    def convert(self):
        mime_type = self.mime_type()

        if ( regex.search('^image\/(jpe?g|png)$', mime_type) != None ):
            return ImageHandler(self)

        if ( regex.search('^application\/pdf$', mime_type) != None ):
            return PdfHandler(self)

#         if ( regex.search('^image\/(mp4|webm)$', mime_type) != None ):
#             return VideoHandler(self)

        raise HTTPException(status_code=500, detail='Mime "' + mime_type + '" not supported')


    def refresh(self):

        self._mime_type = None

        return self


    def clean(self):
        os.remove(self.temp_path())

        return self