import pytest
from PIL import Image
from imgstorage import imgfilter

SAMPLE_IMAGE_FILE = 'tests/data/sample.jpg'

@pytest.mark.filter_null
def test_filter_null():
    f = imgfilter.Null()

    img = Image.open(SAMPLE_IMAGE_FILE)
    img2 = f.apply(img)

    assert img2.size[0] == 4608
    assert img2.size[1] == 3456

@pytest.mark.filter_crop
def test_filter_crop_1():
    f = imgfilter.Crop(1.0)

    img = Image.open(SAMPLE_IMAGE_FILE)
    img2 = f.apply(img)

    assert img2.size[0] == 3456
    assert img2.size[1] == 3456

@pytest.mark.filter_crop
def test_filter_crop_wide():
    f = imgfilter.Crop(2.0/1.0)

    img = Image.open(SAMPLE_IMAGE_FILE)
    img2 = f.apply(img)

    assert img2.size[0] == 4608
    assert img2.size[1] == 2304

@pytest.mark.filter_crop
def test_filter_crop_long():
    f = imgfilter.Crop(1.0/2.0)

    img = Image.open(SAMPLE_IMAGE_FILE)
    img2 = f.apply(img)

    assert img2.size[0] == 1728
    assert img2.size[1] == 3456

@pytest.mark.filter_crop
def test_filter_crop_same():
    f = imgfilter.Crop(4608.0/3456.0)

    img = Image.open(SAMPLE_IMAGE_FILE)
    img2 = f.apply(img)

    assert img2.size[0] == 4608
    assert img2.size[1] == 3456

@pytest.mark.filter_resize
def test_filter_resize():
    f = imgfilter.Resize(1600, 1200)

    img = Image.open(SAMPLE_IMAGE_FILE)
    img2 = f.apply(img)

    assert img2.size[0] == 1600
    assert img2.size[1] == 1200

@pytest.mark.filter_shrink
def test_filter_shrink_none():
    f = imgfilter.Shrink(10000, 10000)

    img = Image.open(SAMPLE_IMAGE_FILE)
    img2 = f.apply(img)

    assert img2.size[0] == 4608
    assert img2.size[1] == 3456

@pytest.mark.filter_shrink
def test_filter_shrink_width():
    f = imgfilter.Shrink(2000, 10000)

    img = Image.open(SAMPLE_IMAGE_FILE)
    img2 = f.apply(img)

    assert img2.size[0] == 2000
    assert img2.size[1] == 1500

@pytest.mark.filter_shrink
def test_filter_shrink_height():
    f = imgfilter.Shrink(10000, 1500)

    img = Image.open(SAMPLE_IMAGE_FILE)
    img2 = f.apply(img)

    assert img2.size[0] == 2000
    assert img2.size[1] == 1500

@pytest.mark.filter_shrink
def test_filter_shrink_both_base_width():
    f = imgfilter.Shrink(2000, 3000)

    img = Image.open(SAMPLE_IMAGE_FILE)
    img2 = f.apply(img)

    assert img2.size[0] == 2000
    assert img2.size[1] == 1500

@pytest.mark.filter_shrink
def test_filter_shrink_both_base_height():
    f = imgfilter.Shrink(3000, 1500)

    img = Image.open(SAMPLE_IMAGE_FILE)
    img2 = f.apply(img)

    assert img2.size[0] == 2000
    assert img2.size[1] == 1500
