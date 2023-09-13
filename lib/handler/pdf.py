from lib.handler.basic import BasicHandler
from lib.handler.image import ImageHandler
from PIL import Image as pimg
import fitz as fitz

class PdfHandler(BasicHandler):

    def init(self):
        # Convert pdf to image
        self.convert()

        # Return image instance
        return ImageHandler(self.file).init()

    def convert(self):
        # Get current temp path
        path = self.file.temp_path()

        # Open Pdf file
        pdf = fitz.open(path)

        # Get first page
        page = pdf.loadPage(0)

        # Convert page to pixel map
        pix = page.getPixmap(matrix=fitz.Matrix(300/72, 300/72))

        # Convert pix to pillow
        jpeg = pimg.frombytes("RGB", [pix.width, pix.height], pix.samples)

        # Save jpeg to temp
        jpeg.save(path, format='jpeg', quality=100, subsampling=0)



