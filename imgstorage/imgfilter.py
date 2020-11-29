"""image filter
"""
from PIL import Image

class ImgFilter:
    """Filter
    image filter base class  
    """
    def __init__(self):
        self.name = ''
        self.next_filter = None

    def __add__(self, filt):
        self.set_next_filter(filt)
        return self

    def __str__(self):
        return self.name

    def apply(self, data):
        return data if self.next_filter is None else self.next_filter.apply(data)

    def set_next_filter(self, filt):
        if self.next_filter is None:
            self.next_filter = filt
        else:
            self.next_filter.set_next_filter(filt)

class Null(ImgFilter):
    """Null Filter
    No process  
    """
    def __init__(self):
        super().__init__()
        self.name = 'Null Filter'

class Crop(ImgFilter):
    """Crop Filter
    Cropping image to specified aspect ratio  

    :param ratio: image aspect ratio  
    """
    def __init__(self, ratio):
        super().__init__()
        self.name = 'Crop Filter (%.f)' % ratio
        self.ratio = ratio

    def apply(self, data):
        width, height = data.size
        expect_width = height * self.ratio

        cropping_size_x1 = 0
        cropping_size_y1 = 0
        cropping_size_x2 = width
        cropping_size_y2 = height

        if width < expect_width:
            # over height
            expect_height = width / float(self.ratio)
            cropping_size_y1 = (height - expect_height) // 2
            cropping_size_y2 = (height + expect_height) // 2
        elif width > expect_width:
            # over width
            cropping_size_x1 = (width - expect_width) // 2
            cropping_size_x2 = (width + expect_width) // 2
        else:
            pass

        ret_data = data.crop(
            (cropping_size_x1, cropping_size_y1, cropping_size_x2, cropping_size_y2)
        )

        return ret_data if self.next_filter is None else self.next_filter.apply(ret_data)

class Resize(ImgFilter):
    """Resize Filter
    Resize image to specified size  
    This filter is not retain aspect ratio  

    :param width: resized width  
    :param height: resized height  
    """
    def __init__(self, width, height):
        super().__init__()
        self.name = 'Resize filter (%dx%d)' % (width, height)
        self.width = width
        self.height = height

    def apply(self, data):
        ret_data = data.resize((self.width, self.height), Image.LANCZOS)

        return ret_data if self.next_filter is None else self.next_filter.apply(ret_data)

class Shrink(ImgFilter):
    """Shrink Filter
    Shrink image to specified size or less with retaining aspect ratio

    :param max_width: maximum width of image  
    :param max_height: maximum height of image   
    """
    def __init__(self, max_width=100000, max_height=100000):
        super().__init__()
        self.name = 'Shrink filter (%dx%d)' % (max_width, max_height)
        self.max_width = max_width
        self.max_height = max_height

    def apply(self, data):
        ratio_w = data.size[0] / float(self.max_width)
        ratio_h = data.size[1] / float(self.max_height)

        shrink_ratio = 1.0

        if ratio_w <= 1.0 and ratio_h <= 1.0:
            # no oversize, original size
            pass
        elif 1.0 < ratio_w and ratio_h <= 1.0:
            # oversize width only, shrink base on width
            shrink_ratio = 1.0 / ratio_w
        elif ratio_w <= 1.0 and 1.0 < ratio_h:
            # oversize height only, shrink base on height
            shrink_ratio = 1.0 / ratio_h
        else:
            # oversize width and height
            if ratio_w >= ratio_h:
                # more oversize width, shrink base on width
                shrink_ratio = 1.0 / ratio_w
            else:
                # more oversize height, shrink base on height
                shrink_ratio = 1.0 / ratio_h

        resize = Resize(
            width=int(data.size[0] * shrink_ratio),
            height=int(data.size[1] * shrink_ratio)
        )

        ret_data = resize.apply(data)

        return ret_data if self.next_filter is None else self.next_filter.apply(ret_data)
