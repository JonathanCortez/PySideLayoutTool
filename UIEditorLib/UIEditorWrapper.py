from typing import Callable
from PySideLayoutTool.UIEditorLib import UIWindowManger, LayoutConstructorClass


class UIParameterStateChange:

    def __init__(self, layout):
        self._current_layout = layout

    def _check_item(self, data, type, func):
        for widget in data:
            if hasattr(widget, 'templateGroup'):
                for w in widget.templateGroup().templateGroupData().values():
                    if hasattr(w, 'templateGroup'):
                        self._check_item(widget.templateGroup().templateGroupData().values(), type,func)
                    if w.type().currentItem_name == type:
                        w.add_delegate(func)
            else:
                if widget.type().currentItem_name == type:
                    widget.add_delegate(func)


    def add_callable(self, type: str, func: Callable):
        self._check_item(self._current_layout.templateLayout().templateGroupData().values(), type, func)


    def remove_callable(self, type: str, func: Callable):
        for widget in self._current_layout.templateLayout().templateGroupData().values():
            if widget.type().currentItem_name == type:
                widget.remove_delegate(func)


class UIPublicAPIWrapper:

    @classmethod
    def create_instantiated_wrapper(cls, layout) -> 'UIAPILayoutWrapper' or None:

        if not layout:
            return None

        return UIAPILayoutWrapper(layout)

    @classmethod
    def instantiate_ui(cls, name, category, file_data):
        UIWindowManger.WindowsManger.InitilizeWindows(name,
                                                      UIWindowManger.WindowsManger.root_save() + f"/{category}/" + name + ".qui",
                                                      win_category=category)
        editor_win = UIWindowManger.WindowsManger.get_Stack(name, category)[name + '_editor']
        layout_win = UIWindowManger.WindowsManger.get_Stack(name, category)[name + '_layout']

        with open(file_data) as file:
            format_type = file_data.split('.')
            if format_type[1] == 'json':
                LayoutConstructorClass.JsonConstructor.construct(file, editor_win)

        editor_win.LayoutUpdate()
        return UIAPILayoutWrapper(layout_win)


class UIAPILayoutWrapper:

    def __init__(self, layout):
        self._layout_wrap = layout

    @property
    def on_parameter_change(self):
        return UIParameterStateChange(self._layout_wrap)

    @property
    def on_folder_change(self):
        return None

    def on_post_update(self):
        pass

    def on_pre_update(self):
        pass

    def set_parameter_value(self, name: str, value):
        self._layout_wrap.parm(name).set_value(value)

    def get_parameter_value(self, name: str):
        return self._layout_wrap.parm(name).eval()