"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on Nov 5, 2017

@author: jrm
"""
from atom.api import Atom, Typed, set_default
from enamlnative.android.bridge import JavaBridgeObject, JavaMethod, JavaCallback, JavaStaticMethod
from enamlnative.android.android_view_group import AndroidViewGroup, ViewGroup
from enamlnative.android.android_frame_layout import AndroidFrameLayout, FrameLayout
from enamlnative.android.app import AndroidApplication
from zxing.widgets.barcode import ProxyBarcodeView, ProxyBarcodeFinderView


class BarcodePackage(JavaBridgeObject):
    __nativeclass__ = set_default('com.codelv.enamlnative.barcode.BarcodePackage')

    #: Save the id
    _instance = None

    @staticmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = BarcodeView(__id__=BarcodeView.getInstance())
        return cls._instance

    #: To get an instance
    getInstance = JavaStaticMethod(returns='com.codelv.enamlnative.barcode.BarcodePackage')

    #: Get the
    setBarcodeResultListener = JavaMethod(
        'com.codelv.enamlnative.barcode.BarcodePackage$BarcodeResultListener')
    onBarcodeResult = JavaCallback('com.google.zxing.integration.android.IntentResult')


class IntentIntegrator(JavaBridgeObject):
    __nativeclass__ = set_default('com.google.zxing.integration.android.IntentIntegrator')
    __signature__ = set_default(('android.app.Activity',))
    setDesiredBarcodeFormats = JavaMethod('java.util.Collection')
    setCameraId = JavaMethod('int')
    setBeepEnabled = JavaMethod('boolean')
    setBarcodeImageEnabled = JavaMethod('boolean')
    setOrientationLocked = JavaMethod('boolean')
    setTitle = JavaMethod('java.lang.String')
    setMessage = JavaMethod('java.lang.String')
    setPrompt = JavaMethod('java.lang.String')
    setButtonYes = JavaMethod('java.lang.String')
    setButtonNo = JavaMethod('java.lang.String')
    setTargetApplications = JavaMethod('java.util.List')

    initiateScan = JavaMethod()# 'java.util.Collection', 'int')

    PRODUCT_CODE_TYPES = ["UPC_A", "UPC_E", "EAN_8", "EAN_13", "RSS_14"]
    ONE_D_CODE_TYPES = ["UPC_A", "UPC_E", "EAN_8", "EAN_13", "CODE_39", "CODE_93", "CODE_128",
                        "ITF", "RSS_14", "RSS_EXPANDED"]
    QR_CODE_TYPES = ["QR_CODE"]
    DATA_MATRIX_TYPES = ["DATA_MATRIX"]
    ALL_CODE_TYPES = None

    @classmethod
    def scan(cls, formats=ALL_CODE_TYPES, camera=-1):
        """ Shortcut only one at a time will work... """
        app = AndroidApplication.instance()
        r = app.create_future()

            #: Initiate a scan
        pkg = BarcodePackage.instance()
        pkg.setBarcodeResultListener(pkg.getId())
        pkg.onBarcodeResult.connect(r.set_result)

        intent = cls(app)
        if formats:
            intent.setDesiredBarcodeFormats(formats)
        if camera != -1:
            intent.setCameraId(camera)
        intent.initiateScan()

        return r


class IntentResult(JavaBridgeObject):
    __nativeclass__ = set_default('com.google.zxing.integration.android.IntentResult')


class BarcodeMixin(Atom):
    setTorch = JavaMethod('boolean')
    resume = JavaMethod()
    pause = JavaMethod()

    decodeSingle = JavaMethod('com.journeyapps.barcodescanner.BarcodeCallback')
    decodeContinuous = JavaMethod('com.journeyapps.barcodescanner.BarcodeCallback')
    stopDecoding = JavaCallback()

    barcodeResult = JavaCallback('com.journeyapps.barcodescanner.BarcodeResult')
    possibleResultPoints = JavaCallback('java.util.List')


class BarcodeView(ViewGroup, BarcodeMixin):
    __nativeclass__ = set_default('com.journeyapps.barcodescanner.BarcodeView')


class DecoratedBarcodeView(FrameLayout, BarcodeMixin):
    __nativeclass__ = set_default('com.journeyapps.barcodescanner.DecoratedBarcodeView')
    setTorchOn = JavaMethod()
    setTorchOff = JavaMethod()


class AndroidBarcodeView(AndroidViewGroup, ProxyBarcodeView):
    """ An Android implementation of a BarcodeView """
    #: A reference to the widget created by the proxy.
    widget = Typed(BarcodeView)

    # --------------------------------------------------------------------------
    # Initialization API
    # --------------------------------------------------------------------------
    def create_widget(self):
        """ Create the underlying widget.
        """
        self.widget = BarcodeView(self.get_context())

    def init_widget(self):
        """ Initialize the underlying widget.
        """
        super(AndroidBarcodeView, self).init_widget()
        d = self.declaration

        #: Observe activity state changes
        app = self.get_context()
        app.observe('state', self.on_activity_lifecycle_changed)

        if d.active:
            self.set_active(d.active)
        if d.light:
            self.set_light(d.light)
        self.widget.barcodeResult.connect(self.on_barcode_result)
        if d.scanning:
            self.set_scanning(d.scanning)

    def on_activity_lifecycle_changed(self, change):
        """ If the app pauses without pausing the barcode scanner
            the camera can't be reopened. So we must do it here. 
        """
        d = self.declaration
        if d.active:
            if change['value'] == 'paused':
                self.widget.pause(now=True)
            elif change['value'] == 'resumed':
                self.widget.resume()

    def destroy(self):
        """ Cleanup the activty lifecycle listener """
        if self.widget:
            self.set_active(False)
        super(AndroidBarcodeView, self).destroy()

    # --------------------------------------------------------------------------
    # ZXing API
    # --------------------------------------------------------------------------
    def on_barcode_result(self, result):
        d = self.declaration
        if d.mode == 'single':
            with self.widget.pause.suppressed():
                d.scanning = False
        d.scanned(result)

    # --------------------------------------------------------------------------
    # ProxyBarcodeView API
    # --------------------------------------------------------------------------
    def set_light(self, light):
        self.widget.setTorch(light)

    def set_active(self, active):
        if active:
            app = self.get_context()

            def on_request_result(result):
                """ Check if we now have the camera permission """
                if result['android.permission.CAMERA']:
                    self.widget.resume()
                else:
                    #: User denied access, set active to the false state
                    with self.widget.pause.suppressed():
                        d = self.declaration
                        d.active = False  #: Permission request denied

            def on_permission_result(allowed):
                """ Check if we have the camera permission """
                if allowed:
                    self.widget.resume()
                else:
                    #: Request it
                    app.request_permissions(['android.permission.CAMERA']).then(on_request_result)

            #: Check permission and activate if allowed
            app.has_permission('android.permission.CAMERA').then(on_permission_result)
        else:
            self.widget.pause()

    def set_scanning(self, scanning):
        d = self.declaration
        if scanning:
            if d.mode == 'single':
                self.widget.decodeSingle(self.widget.getId())
            else:
                self.widget.decodeContinuous(self.widget.getId())
        #: Single stops automatically
        #: stopDecoding does not work with the finder and hence is skipped here


class AndroidBarcodeFinderView(AndroidFrameLayout, AndroidBarcodeView, ProxyBarcodeFinderView):
    """ An Android implementation of a BarcodeView """
    #: A reference to the widget created by the proxy.
    widget = Typed(DecoratedBarcodeView)

    # --------------------------------------------------------------------------
    # Initialization API
    # --------------------------------------------------------------------------
    def create_widget(self):
        """ Create the underlying widget.
        """
        self.widget = DecoratedBarcodeView(self.get_context())

    def set_light(self, light):
        if light:
            self.widget.setTorchOn()
        else:
            self.widget.setTorchOff()
