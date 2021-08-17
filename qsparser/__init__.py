from typing import Any
from urllib.parse import quote,unquote
from re import split,search

def stringify(obj: dict[str, Any]) -> str:
    result = ''
    keysArray = []
    valueArray = []
    for i in obj.keys():
        keysArray.append(i)
    for i in obj.values():
        valueArray.append(i)
    for i in range(len(valueArray)):
        if type(valueArray[i]) == list:
            result = string_array(keysArray[i],valueArray[i],result)
        elif type(valueArray[i]) == dict:
            result = object_array(keysArray[i],valueArray[i],result)
        elif type(valueArray[i]) == bool:
            result += '%s=' % keysArray[i] + str(valueArray[i]).lower()
        else:
            result += '%s=%s&' % (keysArray[i],valueArray[i])

    if result[len(result)-1] == '&':
        result = result[:-1]

    result = result.replace(" ","%20")
    for i in range(len(result)):
        if search(u'[\u4e00-\u9fff]', result[i]):
            result = result.replace(result[i],quote(result[i]))
    return result


def string_array(key: str, array: list, result: str) -> str:
    for i in range(len(array)):
        if type(array[i]) == list and len(array[i]) > 1:
            result = string_array('%s[%s]'% (key,i),array[i],result)
        else:
            result += '%s[%s]=%s&' % (key,i,array[i])
    return result


def object_array(key: str, object: dict, result: str) -> str:
    for i in object.keys():
        if type(object.get(i)) == dict:
            result = object_array('%s[%s]' % (key,i),object.get(i),result)
        else:
            result += '%s[%s]=%s&' % (key,i,object.get(i))
    return result


def parse(qs: str) -> dict[str, Any]:
    result = {}
    tokens = qs.split('&')
    for token in tokens:
        token = token.split('=')
        key, value = token
        items = split('\]?\[', key.removesuffix(']'))
        assign_to_result(result, items, value)
    return result


def assign_to_result(result: dict[str, Any], items: list[str], value: str) -> dict[str, Any]:
    if len(items) == 1:
        result[items[0]] = unquote(value)
        return result
    if items[0] not in result:
        result[items[0]] = {}
    assign_to_result(result[items[0]], items[1:], value)
    return result


if __name__ == '__main__':
    print(parse('a[b][c]=d&d[e]=f&d[g]=h'))


