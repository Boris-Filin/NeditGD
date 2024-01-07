from typing import TypeAlias

Groups: TypeAlias = list[int]
# Object: TypeAlias = dict[int]


def robtop_to_dict(str_obj: str) -> dict:
    obj = {}
    arr_obj = str_obj.split(',')
    encoded_pairs = [(arr_obj[i], arr_obj[i+1])
                     for i in range(0, len(arr_obj), 2)]
    for (k, v) in encoded_pairs:
        obj[int(k)] = decode_property_pair(int(k), v)
    return obj

def dict_to_robtop(obj: dict):
    pairs = obj.items()
    res = ''
    for (k, v) in pairs:
        v_enc = encode_property(v)
        res += f'{k},{v_enc},'
    return res[:-1]

def decode_property_pair(p_id: int, data: str) -> int | list[int]:
    if p_id == 57:
        return decode_list(data)
    return int(data)

def encode_property(data: str) -> str:
    if type(data) is list:
        return encode_list(data)
    return str(data)


def decode_list(data: str) -> list[int]:
    return list(map(int, data.split('.')))

def encode_list(data: list[int]) -> str:
    return '.'.join(map(str, data))
