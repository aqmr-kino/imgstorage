"""image storage
"""
import os
import io
import glob
from PIL import Image
from . import imgfilter

class ImageStore:
    """ImageStore
    Image store object

    :param storage_root: storage root directory that save image files
    """
    def __init__(self, storage_root):
        self.root = storage_root
        self.filt = dict([])

    def add_config(self, key, image_filter=imgfilter.Null()):
        """Add storing specification setting of image  

        :param key: image specification setting name, also used to relative path name from storage_root  
        :param image_filter: applied filter when storing images  
        """
        self.filt[key] = image_filter

    def image_list(self):
        """Get list of current stored image files  

        :returns path list of stored files (dictionary object)  
        """
        ret = dict([])

        for key in self.filt:
            path = os.path.join(self.root, key)
            query = os.path.join(path, '*')

            ret[key] = set([f for f in glob.glob(query)])

        return ret

    def push(self, src_image, filename):
        """Add new image to image store  

        :param src_image: source image filename, Pillow image object, or file-like object  
        :param filename: image filename with use in the store  

        :returns path list of stored files (dictionay object)  
        """
        imgdata = None

        # file open
        if type(src_image) is str:
            # src_image is filename
            imgdata = Image.open(src_image)
        elif isinstance(src_image, Image.Image):
            # src_image is Pillow Image object
            imgdata = src_image.copy()
        elif isinstance(src_image, io.IOBase):
            # src_image is file-like object
            imgdata = Image.open(src_image)
        else:
            raise TypeError('src_image type %s is unsupported' % type(src_image))

        # image transpose with orientation exif (jpeg file)
        if imgdata.format == 'JPEG':
            exif = imgdata._getexif()

            if exif is not None:
                orientation = exif.get(0x0112, 1) # 0x112: Exif orientation

                if orientation == 1:
                    pass
                elif orientation == 2:
                    imgdata = imgdata.transpose(Image.FLIP_LEFT_RIGHT)
                elif orientation == 3:
                    imgdata = imgdata.transpose(Image.ROTATE_180)
                elif orientation == 4:
                    imgdata = imgdata.transpose(Image.FLIP_TOP_BOTTOM)
                elif orientation == 5:
                    imgdata = imgdata.transpose(Image.FLIP_LEFT_RIGHT).transpose(Image.ROTATE_90)
                elif orientation == 6:
                    imgdata = imgdata.transpose(Image.ROTATE_270)
                elif orientation == 7:
                    imgdata = imgdata.transpose(Image.FLIP_LEFT_RIGHT).transpose(Image.ROTATE_270)
                elif orientation == 8:
                    imgdata = imgdata.transpose(Image.ROTATE_90)

        # filter applying and file store
        ret = dict([])

        for key in self.filt:
            path_dir = os.path.join(self.root, key)
            path_fullname = os.path.join(path_dir, filename)

            imgdata_tmp = self.filt[key].apply(imgdata)
            imgdata_tmp.save(path_fullname)

            ret[key] = path_fullname

        return ret
