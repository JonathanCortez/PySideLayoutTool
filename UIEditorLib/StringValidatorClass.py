import re

_specialChars = re.compile('[{};:?/|!~`$%@^&*()-+=.\><]')

def checkString(string: str) -> str:
    if _specialChars.search(string) is None:
        newstring = string.replace(' ','')
        return newstring
    else:
        result = [m.start(0) for m in re.finditer(_specialChars, string)]
        for index in result:
            string = string.replace(string[index],'_')

        return checkString(string)


def check_prefix_name(check_string: str):
    if _specialChars.search(check_string) is not None:
        raise TypeError(f'Prefix name ({check_string}) can only contain [chars, numbers, _ , #]')

    return check_string

def check_names(name: str, check_item) -> str:
    """

    :param name: string that is being evaluated.
    :param check_item: data that is being evaluated against.
    :return: get new name.
    """
    if name in check_item:
        str_lenght = len(name)-1
        if name[str_lenght].isdigit():
            str_num = str(int(name[str_lenght]) + 1)
            name = name.replace(name[str_lenght], str_num)
        else:
            name += '1'

        return check_names(name,check_item)

    return name


def check_string_len(string: str, max_length:int = 10):

    if len(string) > max_length:
        string = string.replace(string[10-3:],'...')

    return string


def hash_char_to_index(string: str):
    update_string = ''
    return update_string

def check_similarName(string: str) -> str:
    pass
