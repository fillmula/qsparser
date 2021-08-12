from typing import Any
import urllib.parse
import re

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
            result = stringArray(keysArray[i],valueArray[i],result)
        elif type(valueArray[i]) == dict:
            result = objectArray(keysArray[i],valueArray[i],result)
        elif type(valueArray[i]) == bool:
            result += '%s=' % keysArray[i] + str(valueArray[i]).lower()
        else:
            result += '%s=%s&' % (keysArray[i],valueArray[i])

    if result[len(result)-1] == '&':
        result = result[:-1]

    result = result.replace(" ","%20")
    for i in range(len(result)):
        if re.search(u'[\u4e00-\u9fff]', result[i]):
            result = result.replace(result[i],urllib.parse.quote(result[i]))
    return result


def stringArray(key,array,result):
    for i in range(len(array)):
        if type(array[i]) == list and len(array[i]) > 1:
            result = stringArray('%s[%s]'% (key,i),array[i],result)
        else:
            result += '%s[%s]=%s&' % (key,i,array[i])
    return result

def objectArray(key,object,result):
    for i in object.keys():
        if type(object.get(i)) == dict:
            result = objectArray('%s[%s]' % (key,i),object.get(i),result)
        else:
            result += '%s[%s]=%s&' % (key,i,object.get(i))
    return result

def parse(qs: str) -> dict[str, Any]:
    return {}

if __name__ == '__main__':
    print(stringify({' a':'俊','c':'d'}))


