""" 

Created with 'enaml-native init-package'
This defines a recipe that p4a can use to build your packages `src`
and install it on the app. Modify as needed.

"""
from pythonforandroid.recipe import EnamlNativeRecipe as BaseRecipe


class EnamlNativeRecipe(BaseRecipe):
    #: Note: You can also extend any other recipe subclass as needed
    #: Recipe version
    version = '1.0'

    #: Recipe dependencies
    depends = ['enaml-native']

    #: Name of your recipe (must add this to your package.json to use in the app
    name = 'enaml-native-barcode'

    #: Recipe zips your package's `src/` folder and uses setup file
    #: there along with this recipe build
    url = 'src.zip'


def get_recipe():
    """ Return the recipe for p4a """ 
    return (EnamlNativeRecipe(), __file__)


def app_linker(ctx):
    """ Add any code to link your native libraries here

    Parameters
    -------------
        ctx: dict is the package.json dictionary
    Returns
    ----------
        bool: True to indicate to the default linker should not be run

    """
    return False


def app_unlinker(ctx):
    """ Add any code to unlink your native libraries here

    Parameters
    -------------
        ctx: dict is the package.json dictionary
    Returns
    ----------
        bool: True to indicate to the default unlinker should not be run

    """
    return False


def app_post_install(ctx):
    """ Add any code here to run after the user installs this package
    The return value is ignored.

    Parameters
    -------------
         ctx: dict is the package.json dictionary

    """
    pass


def app_pre_uninstall(ctx):
    """ Add any code here to run when the user uninstalls this package.
    The return value is ignored.

    Parameters
    -------------
        ctx: dict is the package.json dictionary

    """
    pass

