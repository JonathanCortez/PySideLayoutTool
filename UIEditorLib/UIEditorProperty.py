import inspect
from abc import abstractmethod
from functools import wraps
from collections import namedtuple
from typing import Callable, Any, Dict
from PySide2 import QtWidgets



class IWidgetProperties(QtWidgets.QWidget):

    def __init__(self):
        super(IWidgetProperties, self).__init__()
        self.setContentsMargins(0,0,0,0)
        self._layout = QtWidgets.QVBoxLayout()
        self._layout.setSpacing(0)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self._layout)

        self._parent = None


    def addParent(self, parent):
        self._parent = parent

    @abstractmethod
    def override_default(self, defaults: tuple):
        pass

    @abstractmethod
    def setValue(self, value):
        pass

    @abstractmethod
    def value(self):
        pass


class PropertyFactory:

    registeredUI: Dict[str, Callable[..., Any]] = {}

    @classmethod
    def register(cls, name: str) -> Callable:

        def inner_wrapper(wrapped_class):
            if not hasattr(wrapped_class, '__UICProperties__'):
                TypeError('UIClass must have minimum 1 UICProperty func')

            if name in cls.registeredUI:
                TypeError('UIClass with %s already exist. Will replace it', name)
            cls.registeredUI[name] = wrapped_class
            return wrapped_class

        return inner_wrapper

    @classmethod
    def create_property(cls, name: str) -> Any or None:

        if name not in cls.registeredUI:
            TypeError ('UIClass %s does not exist in the registry', name)
            return None

        exec_class = cls.registeredUI[name]
        return exec_class


class UICProperty:
    def __init__(self, func):
        self._cls = None
        self._fget = func

    def __get__(self, obj, cls):
        if cls is None:
            cls = type(obj)
        return self._fget.__get__(obj, cls)()

    # def __set__(self, obj, value):
    #     if not self._fset:
    #         raise AttributeError("can't set attribute")
    #     type_ = type(obj)
    #     return self._fset.__get__(obj, type_)(value)

    def __set_name__(self, owner, name):
        self._cls = owner
        if hasattr(owner,'__UICProperties__'):
            getattr(owner,'__UICProperties__').append(self._fget.__name__)
        else:
            setattr(owner, '__UICProperties__', [self._fget.__name__])



def UIProperty(metaWidget: str, label:str = None, category:str = None, category_args=(False,300), defaults=None, use_separator:bool=False, neighbor=False):
    class PrepareCls:
        def __init__(self, func):
            self._metaWidget = PropertyFactory.create_property(metaWidget)
            self._func = func
            self._cls = None
            self._value = None
            self._names = None
            self._new_instanceWidget = None
            setattr(self, '__UIProperty__', True)


        def convert(self, dictionary):
            return namedtuple('PropertyValues', dictionary.keys())(**dictionary)

        def _process_instance(self):
            self._new_instanceWidget = self._metaWidget()

            if defaults:
                self._new_instanceWidget.override_default(defaults)

            self._names = getattr(self._new_instanceWidget, '__UICProperties__')
            valueDict = {}
            for attribute in dir(self._new_instanceWidget):
                # Check that it is callable
                if attribute in self._names:
                    attribute_value = getattr(self._new_instanceWidget, attribute)
                    valueDict[attribute] = attribute_value

            if len(valueDict) > 1:
                self._value = self.convert(valueDict)
            else:
                self._value = list(valueDict.values())[0]

            self._label = label
            if self._label is None:
                self._label = self._func.__name__

            return self._new_instanceWidget, self._func.__name__, self._label, category, category_args, use_separator

        def _init_update(self, cls_instance):
            new_value_dict = {}
            property_instance = cls_instance.__property_instances__[self._func.__name__]
            for attribute in property_instance.__class__.__UICProperties__:
                if attribute in self._names:
                    attribute_value = getattr(property_instance, attribute)
                    new_value_dict[attribute] = attribute_value

            if type(self._value).__name__ == 'PropertyValues':
                self._value = self.convert(new_value_dict)
            else:
                self._value = list(new_value_dict.values())[0]

            if not hasattr(cls_instance, '__property_values__'):
                new_dict = {self._func.__name__: self._value}
                setattr(cls_instance, '__property_values__', new_dict)
            else:
                getattr(cls_instance, '__property_values__')[self._func.__name__] = self._value

            # self._func(cls_instance)


        def __get__(self, instance, owner):
            if instance is not None:
                if hasattr(instance, '__property_values__'):
                    self._value = instance.__property_values__[self._func.__name__]

            return self


        def __set_name__(self, owner, name):
            self._cls = owner
            if hasattr(owner, '__UIProperties__'):
                getattr(owner, '__UIProperties__').append(self._func.__name__)
            else:
                setattr(owner, '__UIProperties__', [self._func.__name__])


        def __call__(self):
            return self._value

    return PrepareCls



def ProcessUIProperties(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        cls_mro = []
        for i in inspect.getmro(args[0]):
            if i.__name__ == 'mainWidget':
                cls_mro.append(i)
                break
            else:
                cls_mro.append(i)

        widget_instances = []
        cls_mro.reverse()
        for cls in cls_mro:
            for item in cls.__dict__.values():
                if hasattr(item,'__UIProperty__'):
                    Property_instance = namedtuple('Property_Instance', ['property_widget','func_owner','label','category','category_args','separator'])
                    widget_instance,func_owner, label_str, category_str,cat_args, bSep = item._process_instance()
                    new_property = Property_instance(widget_instance, func_owner, label_str, category_str,cat_args, bSep)
                    widget_instances.append(new_property)

        return widget_instances

    return wrapper


