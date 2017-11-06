package com.codelv.enamlnative.barcode;

import android.app.Activity;
import android.util.Log;

import com.codelv.enamlnative.EnamlActivity;
import com.codelv.enamlnative.EnamlPackage;
import com.codelv.enamlnative.Bridge;
import com.google.zxing.integration.android.IntentIntegrator;
import com.google.zxing.integration.android.IntentResult;
import com.journeyapps.barcodescanner.BarcodeResult;
import com.journeyapps.barcodescanner.CaptureManager;

import java.util.HashMap;

/**
 * Created by jrm on 11/5/17.
 */
public class BarcodePackage implements EnamlPackage {

    EnamlActivity mActivity;
    BarcodeResultListener mBarcodeResultListener;
    static BarcodePackage mInstance;

    /**
     * So we can get it from python
     * @return
     */
    public static BarcodePackage getInstance() {
        return mInstance;
    }

    @Override
    public void onCreate(EnamlActivity activity) {
        mActivity = activity;
        mInstance = this;
    }

    /**
     * Add special bridge packers required by map components
     */
    @Override
    public void onStart() {
        Bridge bridge = mActivity.getBridge();

        // Add a decoder for IntentResults
        // could just let the default "toString" but this retains types
        Bridge.Packer intentResultPacker = (packer, id, object)->{
            IntentResult result = (IntentResult) object;
            packer.packMapHeader(5);

            packer.packString("image_path");
            String imagePath = result.getBarcodeImagePath();
            if (imagePath==null) {
                packer.packNil();
            } else {
                packer.packString(imagePath);
            }

            packer.packString("contents");
            String contents = result.getContents();
            if (contents==null) {
                packer.packNil();
            } else {
                packer.packString(contents);
            }

            packer.packString("orientation");
            if (result.getOrientation()==null) {
                packer.packNil();
            } else {
                packer.packInt(result.getOrientation());
            }

            packer.packString("format");
            String format = result.getFormatName();
            if (format==null) {
                packer.packNil();
            } else {
                packer.packString(format);
            }

            packer.packString("error_level");
            String errorLevel = result.getErrorCorrectionLevel();
            if (errorLevel==null) {
                packer.packNil();
            } else {
                packer.packString(errorLevel);
            }

            //packer.packString("data");
            /*byte[] data = result.getRawBytes();
            packer.packBinaryHeader(data.length);
            for (int i=0; i<data.length; i++) {
                packer.pack(data[i]);
            }*/

        };

        bridge.addPacker(IntentResult.class, intentResultPacker);

        // Pack barcode results as in the same decoded format
        bridge.addPacker(BarcodeResult.class, (packer, id, object)->{
            // Convert to the same format as an IntentResult
            BarcodeResult result = (BarcodeResult) object;

            String barcodeImagePath = ""; // TODO: How do i get this??

            IntentResult intent = IntentIntegrator.parseActivityResult(
                    IntentIntegrator.REQUEST_CODE,
                    mActivity.RESULT_OK,
                    CaptureManager.resultIntent(result, barcodeImagePath)
            );

            // Now pack it with the one above
            intentResultPacker.pack(packer, id, intent);
        });

        // Add a listener for scan results
        mActivity.addActivityResultListener((requestCode, resultCode, data) ->{
            IntentResult result = IntentIntegrator.parseActivityResult(requestCode, resultCode, data);
            if(result != null) {
                if (mBarcodeResultListener!=null) {
                    mBarcodeResultListener.onBarcodeResult(result);
                }
                return true; // Handled it
            }
            return false; // Do default
        });
    }


    @Override
    public void onResume() {

    }

    @Override
    public void onPause() {

    }

    @Override
    public void onStop() {

    }

    @Override
    public void onDestroy() {

    }

    public void setBarcodeResultListener(BarcodeResultListener listener) {
        mBarcodeResultListener = listener;
    }

    interface BarcodeResultListener {
        void onBarcodeResult(IntentResult result);
    }
}
