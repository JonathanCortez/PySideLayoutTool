from typing import Dict, Callable, Any, List
from PySideLayoutTool.UIEditorWindows import MainEditorWindow
from PySideLayoutTool.UIEditorWindows import MainLayoutWindow
from PySideLayoutTool.UIEditorLib import UIEditorMediators

class WindowsManger:

    UI_Wins_Names: Dict[str, List[str]] = {}
    UI_Wins: Dict[str, Dict[str, Dict[str,Any]]] = {}
    UI_Wins_Names_Category: Dict[str, Dict[str, List[str]]] = {}

    DCC_parent_func: Callable[..., Any] = None
    Save_Path = ''

    #TODO: Refactor this function.
    @classmethod
    def add_to_stack(cls, main_name_given: str, editor_obj: Any, layout_obj: Any, win_category) -> None:
        editor_name = main_name_given + '_editor'
        temp_editor_dict = {}
        temp_editor_dict[editor_name] = editor_obj

        layout_name = main_name_given + '_layout'
        temp_layout_dict = {}
        temp_layout_dict[layout_name] = layout_obj

        temp_editor_dict.update(temp_layout_dict)
        temp_UI_Win = {}
        temp_UI_Win[main_name_given] = temp_editor_dict

        cls.UI_Wins_Names[main_name_given] = [editor_name, layout_name]

        if win_category in cls.UI_Wins:
            cls.UI_Wins[win_category].update(temp_UI_Win)
        else:
            cls.UI_Wins[win_category] = temp_UI_Win

        temp_UI_Win_Names = {}
        temp_UI_Win_Names[main_name_given] = [editor_name, layout_name]
        cls.UI_Wins_Names_Category[win_category] = temp_UI_Win_Names


    @classmethod
    def root_save(cls):
        return cls.Save_Path

    @classmethod
    def set_root_save(cls, path: str):
        cls.Save_Path = path

    @classmethod
    def setParentDCC(cls, func: Callable[..., Any]):
        cls.DCC_parent_func = func

    @classmethod
    def get_Stack(cls, find_name: str, category_name: str):
        if category_name in cls.UI_Wins:
            if find_name in cls.UI_Wins[category_name]:
                return cls.UI_Wins[category_name][find_name]
        else:
            ValueError('Category name not in stack')

        return None

    @classmethod
    def window_names(cls):
        return cls.UI_Wins_Names.keys()

    @classmethod
    def category_names(cls):
        return cls.UI_Wins_Names_Category.keys()

    @classmethod
    def isNameInCategory(cls, find_name: str, category_name: str):
        if category_name in cls.UI_Wins:
            if find_name in cls.UI_Wins[category_name]:
                return True
            else:
                return False
        return False

    @classmethod
    def InitilizeWindows(cls,win_name: str, path_save: str, win_category='User'):
        new_editor = MainEditorWindow.EditorWindow(win_name, path_save, win_category)
        new_layout = MainLayoutWindow.MainWindowLayout(win_name)
        meditor = UIEditorMediators.EditorsMediator(new_editor, new_layout)
        meditor.notify_full_serialization()
        cls.add_to_stack(win_name, new_editor, new_layout, win_category)


    @classmethod
    def WindowShow(cls, instance):
        if cls.DCC_parent_func:
            instance.show()
            cls.DCC_parent_func(instance)
        else:
            instance.show()


    @classmethod
    def restoreState(cls,data):
        win_instance_editor = cls.get_Stack(data['Name'],data['Category'])[data['Name'] + '_editor']
        win_instance_editor.restoreUIState(data)




