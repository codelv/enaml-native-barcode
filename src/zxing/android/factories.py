"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on Nov 5, 2017

@author: jrm
"""


def barcode_view_factory():
    from .android_barcode import AndroidBarcodeView
    return AndroidBarcodeView


def barcode_finder_view_factory():
    from .android_barcode import AndroidBarcodeFinderView
    return AndroidBarcodeFinderView


def install():
    """ Add any barcode specific android widgets to the `enamlnative.android.factories` """
    from enamlnative.android import factories

    factories.ANDROID_FACTORIES.update({
        'BarcodeView': barcode_view_factory,
        'BarcodeFinderView': barcode_finder_view_factory,
    })
