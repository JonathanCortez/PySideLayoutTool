from typing import Callable, Dict, List, Any

class WidgetFactory:

    widget_creation_funcs: Dict[str, Callable[..., Any]] = {}
    widget_category: Dict[str, List[dict]] = {}

    @classmethod
    def registerCategory(cls, category: str):
        if category not in cls.widget_category:
            cls.widget_category[category] = []

    @classmethod
    def unregisterCategory(self, category_name: str):
        self.widget_category.pop(category_name, None)

    @classmethod
    def register(cls, widget_type: str, creator_fn: Callable[..., Any]) -> None:
        """Register a widget layout type."""
        if widget_type not in cls.widget_creation_funcs:
            cls.widget_creation_funcs[widget_type] = creator_fn
            module_path = creator_fn.__module__  # type: ignore
            module_path = module_path.split('.')
            index = None
            for i in enumerate(module_path):
                if i[1] in cls.widget_category:
                    index = i[0]
                    break

            tempDict = {}
            tempDict[widget_type] = creator_fn
            cls.widget_category[module_path[index]].append(tempDict)

    @classmethod
    def unregister(cls, widget_name: str) -> None:
        """Unregister a widget layout type."""
        cls.widget_creation_funcs.pop(widget_name, None)

        temp_widget_category = dict(cls.widget_category)

        for category in temp_widget_category:
            for i in temp_widget_category[category]:
                if widget_name in i:
                    cls.widget_category[category].remove(i)
                    break

            if len(cls.widget_category[category]) == 0:
                cls.unregisterCategory(category)


    @classmethod
    def create(cls,widget_name: str):
        """Create a widget of a specific type, given JSON data."""
        try:
            creator_func = cls.widget_creation_funcs[widget_name]
        except KeyError:
            raise ValueError(f"unknown widget type {widget_name!r}, not registered") from None
        return creator_func()

    @classmethod
    def registered(cls) -> widget_category:
        """ Get all registered parameter types"""
        return cls.widget_category


    @classmethod
    def ItemCategoryIn(cls, item):
        r_key = ''
        for key in cls.widget_category:
            for i in cls.widget_category[key]:
                keys = i.keys()
                if item == list(keys)[0]:
                    r_key = key
                    break

        return r_key

    @classmethod
    def sortCategoryItems(cls, key_list):
        tempList = []
        for i in key_list:
            tempList.append(list(i)[0])

        return sorted(tempList, key=lambda x: x.lower())



