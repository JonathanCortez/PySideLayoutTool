from . import UIWindowManger


def editor(name: str , category: str):
    return UIWindowManger.WindowsManger.get_Stack(name, category)[name + '_editor']

def layout(name: str, category: str ):
    return UIWindowManger.WindowsManger.get_Stack(name, category)[name + '_layout']


