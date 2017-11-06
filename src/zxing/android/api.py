"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on Nov 5, 2017

@author: jrm
"""


def scan_barcode(*args):
    """ Open a scanner view to scan a barcode"""
    from .android_barcode import IntentIntegrator
    return IntentIntegrator.scan(*args)
