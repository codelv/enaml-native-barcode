"""
Created with 'enaml-native init-package'
This setup file will be used to define what is actually installed
in the apps python bundle. Anything included by this setup file
will be accessible within your app. 

Note: Any c/c++/cython compiled components must be created with a 
p4a recipe!
"""
from setuptools import setup, find_packages

#: Put your library dependencies here
setup(
    name="enaml-native-barcode",
    version="1.0",
    author="jrm",
    author_email="",
    license='MIT',
    url="",
    description="enaml-native-barcode package for enaml-native",
    entry_points={
        'enaml_native_widgets': [
            'enaml_native_barcode = zxing.widgets.api:install'
        ],
        'enaml_native_android_api': [
            'enaml_native_barcode = zxing.android.api:install'
        ],
        'enaml_native_android_factories': [
            'enaml_native_barcode = zxing.android.factories:install'
        ],
    },
    packages=find_packages(),
    install_requires=['enaml-native'],
)
