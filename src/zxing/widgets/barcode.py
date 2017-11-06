"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on Nov 6, 2017

@author: jrm
"""
from atom.api import Bool, Enum, Event, Typed, List, ForwardTyped, observe
from enaml.core.declarative import d_
from enamlnative.widgets.view_group import ViewGroup, ProxyViewGroup
from enamlnative.widgets.frame_layout import FrameLayout, ProxyFrameLayout


class ProxyBarcodeView(ProxyViewGroup):
    declaration = ForwardTyped(lambda: BarcodeView)

    def set_active(self, active):
        raise NotImplementedError

    def set_scanning(self, scanning):
        raise NotImplementedError

    def set_light(self, light):
        raise NotImplementedError

    def set_mode(self, mode):
        raise NotImplementedError


class ProxyBarcodeFinderView(ProxyFrameLayout, ProxyBarcodeView):
    declaration = ForwardTyped(lambda: BarcodeFinderView)


class BarcodeView(ViewGroup):
    """ Camera preview. 
    
    Note: This should not be used directly! 
    
    """

    #: Camera is active
    active = d_(Bool(True))

    #: Flashlight enabled
    light = d_(Bool())

    #: Scanning is active
    scanning = d_(Bool(False))

    #: Trigger a scan
    mode = d_(Enum('single', 'continuous'), readable=False)

    #: Scan result
    scanned = d_(Event(dict), writable=False)

    #: Reference to the proxy implementation
    proxy = Typed(ProxyBarcodeView)

    @observe('light', 'active', 'mode', 'scanning')
    def _update_proxy(self, change):
        """ Update the proxy """
        #: The superclass implementation is sufficient
        super(BarcodeView, self)._update_proxy(change)


class BarcodeFinderView(FrameLayout, BarcodeView):
    """ Like BarcodeView but displays a line showing where it is scanning. 
    
    """
    #: Reference to the proxy implementation
    proxy = Typed(ProxyBarcodeFinderView)
