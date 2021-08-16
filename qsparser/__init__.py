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
        if re.search(u'[\u4e00-\u9fff]', result[i]):
            result = result.replace(result[i],urllib.parse.quote(result[i]))
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
    qs = qs.replace('[',',')
    qs = qs.replace(']','')


    tempObj = {}
    result = {}
    querys = re.split('[& =]',qs)

    for i in range(len(querys)):
        if i % 2 == 0:
            tempObj.update({querys[i]:urllib.parse.unquote(querys[i+1])})


    for i in tempObj.items():
        if i[1] == 'true':
            tempObj.update({i[0]:True})
        if i[1] == 'false':
            tempObj.update({i[0]:False})
        if '%20' in i[1]:
            tempObj.update({i[0]:i[1].replace('%20',' ')})

        if len(i[0]) > 1:
            tempObj = mutiObj(i)
            for j in tempObj.keys():
                if j in result:
                    result.update({j:{**result.get(j),**tempObj.get(j)}})
                else:
                    result.update({j:tempObj.get(j)})
    for i in tempObj.keys():
        if len(i) < 2:
            result.update({i:tempObj.get(i)})
    return result

def mutiObj(query):
    key = query[0].split(',')

    for i in range(len(key)-1):
        temp = {key[i]:{key[i+1]:query[1]}}
    return temp


if __name__ == '__main__':
    print(parse('a[0]=1&a[1]=2&a[2]=3&b[0]=q&b[1]=w&b[2]=%E4%BF%8A'))


