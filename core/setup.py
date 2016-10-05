from distutils.core import setup, Extension

multi_img = Extension('multi_img',
                    include_dirs = ['/usr/local/include','/Users/vincUk/Desktop/Cython/boost_1_62_0/'],
                    library_dirs = ['/usr/local/lib','/Users/vincUk/Desktop/Cython/boost_1_62_0/stage/lib/'],
                    sources = ['multi_img.cpp','multi_img_wrap.cxx'],
                    language = "c++")

setup (name = 'multi_img',
       # version = '1.0',
       # description = 'This is a multi_img package',
       ext_modules = [multi_img])
