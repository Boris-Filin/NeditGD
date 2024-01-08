

def decode_property_pair(p_id: int, data: str) -> int | list[int]:
    if p_id == 57:
        return decode_list(data)
    return int(data)

def encode_property(p_id: int, data: str) -> str:
    if type(data) is list:
        return encode_list(p_id, data)
    return f'{p_id},{data},'


def decode_list(data: str) -> list[int]:
    return list(map(int, data.split('.')))

def encode_list(p_id: int, data: list[int]) -> str:
    if not data:
        return ''
    str_list = '.'.join(map(str, data))
    return f'{p_id},{str_list},'
