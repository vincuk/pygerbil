from distutils.core import setup, Extension

mimm = Extension('_multi_img_py',
    include_dirs = ['.','/usr/local/include','/usr/local/include/opencv2/core/',
                    '/usr/local/include/opencv2/highgui','/Users/vincUk/Desktop/Cython/boost_1_62_0/'],
    library_dirs = ['/usr/local/lib','/Users/vincUk/Desktop/Cython/boost_1_62_0/stage/lib/'],
    libraries=['opencv_core','opencv_highgui','boost/filesystem'],
    sources = ['multi_img_wrap.cxx', 'multi_img.cpp', 'multi_img_io_ext.cpp'],
    language = "c++")

setup (name = 'multi_img_py',
       # version = '1.0',
       # description = 'This is a multi_img package',
       ext_modules = [mimm])
