from setuptools import setup

setup(
    name='imgstorage',
    version='0.1.0',
    description='Image file auto scaling library',
    author='aqmr-kino',
    url='https://github.com/aqmr-kino/imgstorage',
    license='MIT',
    setup_requires=[
        'wheel',
        'Pillow',
    ],
    tests_require=[
        'pytest',
    ],
    packages=[
        'imgstorage',
    ],
    python_requires='>=3.4',
)
