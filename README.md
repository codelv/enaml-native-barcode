# enaml-native-barcode

A QRCode reader and barcode scanning package for enaml-native using [zxing](https://github.com/zxing/zxing).
More specifically, it uses the embedded version provided by [zxing-android-embedded](https://github.com/journeyapps/zxing-android-embedded).

[![See the demo on youtube](https://img.youtube.com/vi/lYF8XioDd78/0.jpg)](https://youtu.be/lYF8XioDd78)



### Installation

To install:

`enaml-native install enaml-native-barcode`

__And add `enaml-native-barcode:""` to your app's project dependencies!__

To remove:

`enaml-native uninstall enaml-native-barcode`


### Usage

See the example in examples. Versions used are listed in the `requirements.txt`

1. Install the latest `enaml-native-cli==1.3.1` 
2. Create a new app `enaml-native init BarcodeDemo com.example.barcode apps/`
3. Activate the venv `cd apps/BarcodeDemo` and `source venv/bin/activate`
4. Install `enaml-native install enaml-native-barcode`
5. Add `enaml-native-barcode: ""` to your apps `package.json` under the android dependencies
6. Copy in the `main.py` and `view.enaml` from the example folder to your apps `src` folder
7. Run `enaml-native build-python`
8. Run `enaml-native run-android`

Enjoy!
