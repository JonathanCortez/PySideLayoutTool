from typing import Callable, Dict, List, Any

class IconEditorFactory:

    iconloc_str: Dict[str, str] = {}

    @classmethod
    def register(cls, icon_name: str, string_path: str) -> None:
        """Register a widget layout type."""
        if icon_name not in cls.iconloc_str:
            cls.iconloc_str[icon_name] = string_path


    def unregister(self,character_type: str) -> None:
        """Unregister a widget layout type."""
        self.iconloc_str.pop(character_type, None)

    @classmethod
    def create(cls,icon_name: str):
        """Create a widget of a specific type, given JSON data."""
        try:
            icon_path = cls.iconloc_str[icon_name]
        except KeyError:
            raise ValueError(f"unknown icon type {icon_name!r}, not registered") from None
        return icon_path

    @classmethod
    def registered(cls) -> iconloc_str:
        """ Get all registered parameter types"""
        return cls.iconloc_str
