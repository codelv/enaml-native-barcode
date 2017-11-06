"""
Created with 'enaml-native init-package'

This defines what files to include when a user installs this into
their app's virtualenv. It should include any required `android`
and`ios` libraries as data_files so they can be linked to the
app when this package is installed.

## Customize the project

## Adding P4A Recipes for python sources
This packages contents are NOT installed on the app! That is
done by any p4a_recipes added here using the p4a_recipe entry point.
The user must also include your recipe in their apps `package.json` 
in the app dependencies.

## Linking native libraries
You can define an `enaml_native_linker` and `enaml_native_unlinker`
entry_points here to customize how this package "links" it's native
libraries to the users's android and ios projects.

Likewise, you can define `enaml_native_post_install` and `enaml_native_pre_install`
entry points to preform any operations when this package is installed or removed.

## Customizing the cli

You can add your own commands to the enaml-native cli with the 
`enaml_native_command` entry point. A command must be a subclass of the enaml-native
Command class. Any commands added in can be used via `enaml-native <command>`
when your package is installed.

"""
import os
import fnmatch
from setuptools import setup


def find_data_files(dest, folders):
    matches = dict()
    #: Want to install outside the venv volder in the packages folder
    dest = os.path.join('packages', dest)

    excluded_types = ['.pyc', '.enamlc', '.apk', '.iml', '.zip', '.tar.gz', '.so']
    excluded_dirs = ['android/build', 'android/captures', 'android/assets']
    for folder in folders:
        if not os.path.exists(folder):
            continue
        if not os.path.isdir(folder):
            k = os.path.join(dest, dirpath)
            matches[k].append(os.path.join(dest,folder))
            continue
        for dirpath, dirnames, files in os.walk(folder):
            #: Skip build folders and exclude hidden dirs
            if ([d for d in dirpath.split("/") if d.startswith(".")] or
                    [excluded_dir for excluded_dir in excluded_dirs if excluded_dir in dirpath]):
                continue
            k = os.path.join(dest, dirpath)
            if k not in matches:
                matches[k] = []
            for f in fnmatch.filter(files, '*'):
                if [p for p in excluded_types if f.endswith(p)]:
                    continue
                m = os.path.join(dirpath, f)
                matches[k].append(m)
    return matches.items()


setup(
    name="enaml-native-barcode",
    version="1.0",
    author="CodeLV",
    author_email="frmdstryr@gmail.com",
    license='MIT',
    url="https://github.com/codelv/enaml-native-barcode",
    description="QRCode and barcode scanning for enaml-native using zxing",
    long_description=open("README.md").read(),
    py_modules=['enaml_native_barcode'],
    data_files=find_data_files("enaml-native-barcode", ['android', 'ios', 'src']),
    install_requires=['enaml-native-cli'],
    entry_points={
        #: Add any other recipes here
        'p4a_recipe': [
            'enaml_native_barcode = enaml_native_barcode:get_recipe'
        ],

        #: Customize linking of native projects
        #'enaml_native_linker': ['enaml_native_barcode:app_linker'],
        #'enaml_native_unlinker': ['enaml_native_barcode:app_unlinker'],
        #'enaml_native_post_install': ['enaml_native_barcode:app_post_install'],
        #'enaml_native_pre_uninstall': ['enaml_native_barcode:app_pre_uninstall'],

        #: Add custom commands to the enaml-native cli
        #'enaml_native_command': [
        #    'enaml_native_barcode:<CommandSubclass>'
        #],
    },
)
