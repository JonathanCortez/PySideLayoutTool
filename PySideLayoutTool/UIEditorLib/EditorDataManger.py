from typing import Dict, List, Any

#TODO: Intergrate this module to work with the whole process of the tool as are reflecting system.

class DataManager:

    __data : Dict[str, Any] = {}

    @classmethod
    def add_data(cls, key_name : str, value : Any):
        cls.__data[key_name] = value

    @classmethod
    def get_data(cls, name : str):
        return cls.__data[name]

    @classmethod
    def get_all_registered_data(cls) -> List[str]:
        return list(cls.__data.keys())