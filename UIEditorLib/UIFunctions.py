from . import UIWindowManger
from inspect import stack

def editor(name: str , category: str):
    return UIWindowManger.WindowsManger.get_Stack(name, category)[name + '_editor']

def layout(name: str, category: str ):
    return UIWindowManger.WindowsManger.get_Stack(name, category)[name + '_layout']

def current_main():
    print(stack()[1].function)
