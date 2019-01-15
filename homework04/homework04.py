# bencoding
# http://www.bittorrent.org/beps/bep_0003.html

def int_decode(str, offset=0):
    if type(str) is bytes:
        str = str.decode('utf-8')
    res = ''
    for i, j in enumerate(str[offset+1:]):
        if j != 'e':
            res += j
        else:
            return int(res), i + offset + 2


def str_decode(str, offset=0):
    if type(str) is bytes:
        str = str.decode('utf-8')
    length = int(str[offset:].split(':')[0])
    offset1 = len(str[offset:].split(':')[0])
    return bytes(str[offset + offset1 + 1: offset + offset1 + 1 + length], 'utf-8'), offset + offset1 + 1 + length


def list_decode(str, offset=0):
    result = []
    if type(str) is bytes:
        str = str.decode('utf-8')
    if str[offset + 1] == 'i':
        i, j = int_decode(bytes(str[offset + 1:], 'utf-8'))
        j += offset + 1
        result.append(i)
        if str[j] == 'e':
            return result, j+1
        else:
            return result + list_decode(bytes(str, 'utf-8'), j-1)[0], list_decode(bytes(str, 'utf-8'), j-1)[1]
    elif str[offset + 1] == 'l':
        return result + [list_decode(str, offset + 1)[0]], list_decode(str, offset + 1)[1]


    elif str[offset + 1] in ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9'):
        i, j = str_decode(bytes(str, 'utf-8'), offset + 1)
        result.append(i)
        if str[j] == 'e':
            return result, j+1
        else:
            return result + list_decode(bytes(str, 'utf-8'), j-1)[0], list_decode(bytes(str, 'utf-8'), j-1)[1]


def dict_decode(str, offset=0):
    if type(str) is bytes:
        str = str.decode('utf-8')
    result = {}
    i, j = str_decode(bytes(str[offset+1:], 'utf-8'))
    j += offset +1
    if str[j] in ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9'):
        result[i] = str_decode(bytes(str[j:], 'utf-8'))[0]
        j += str_decode(bytes(str[j:], 'utf-8'))[1]
    elif str[j] == 'i':
        result[i] = int_decode(bytes(str[j:], 'utf-8'))[0]
        j += int_decode(bytes(str[j:], 'utf-8'))[1]
    elif str[j] == 'l':
        result[i] = list_decode(bytes(str[j:], 'utf-8'))[0]
        j += list_decode(bytes(str[j:], 'utf-8'))[1]

    if str[j] == 'e':
        return result, j+1
    else:
        return {**result, **dict_decode(bytes(str, 'utf-8'), j-1)[0]}, dict_decode(bytes(str, 'utf-8'), j-1)[1]


def int_encode(val):
    assert type(val) is int
    return bytes('i' + str(val) + 'e', 'utf-8')


def str_encode(val):
    if type(val) is bytes:
        val = val.decode('utf-8')
    return bytes(str(len(val)) + ':' + val, 'utf-8')


def list_encode(val):
    result = 'l'
    for item in val:
        if type(item) is int:
            result += int_encode(item).decode('utf-8')
        elif type(item) is bytes:
            result += str_encode(item).decode('utf-8')
        elif type(item) is list:
            result += list_encode(item).decode('utf-8')
    return bytes(result + 'e', 'utf-8')


def dict_encode(val):
    assert type(val) is dict
    result = 'd'
    for key in val.keys():
        result += str_encode(key).decode('utf-8')
        if type(val[key]) is int:
            result += int_encode(val[key]).decode('utf-8')
        elif type(val[key]) is bytes:
            result += str_encode(val[key]).decode('utf-8')
        elif type(val[key]) is list:
            result += list_encode(val[key]).decode('utf-8')
        elif type(val[key]) is dict:
            result += dict_encode(val[key]).decode('utf-8')
    return bytes(result + 'e', 'utf-8')


def encode(val):
    if type(val) is int:
        return int_encode(val)
    elif type(val) in (bytes,  str):
        return str_encode(val)
    elif type(val) is list:
        return list_encode(val)
    elif type(val) is dict:
        return dict_encode(val)


def decode(val):
    val = val.decode('utf-8')
    if val[0] == 'i':
        return int_decode(val)[0]
    elif val[0] == 'l':
        return list_decode(val)[0]
    elif val[0] == 'd':
        return dict_decode(val)[0]
    elif val[0] in ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9'):
        return str_decode(val)[0]


if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags=doctest.IGNORE_EXCEPTION_DETAIL)
