import functools



def robtop_to_dict(str_obj: str) -> dict:
    obj = {}
    arr_obj = str_obj.split(',')
    encoded_pairs = [(arr_obj[i], arr_obj[i+1])
                     for i in range(0, len(arr_obj), 2)]
    for (k, v) in encoded_pairs:
        obj[int(k)] = v
    return obj

def dict_to_robtop(obj: dict):
    pairs = obj.items()
    res = ''
    for (k, v) in pairs:
        res += f'{k},{v},'
    return res[:-1]
