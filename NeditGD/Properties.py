import base64
from Dictionaries.PropertyID import NAME_TO_ID
from Dictionaries.PropertyHSV import HSV


# Decode a property encoded RobTop's way
def decode_property_pair(p_id: int, data: str) -> int | float | list[int]:
    if p_id == NAME_TO_ID['groups']:
        return decode_list(data)
    
    if p_id == NAME_TO_ID['text']:
        return decode_text(data)
    
    if p_id in (NAME_TO_ID['hsv'], NAME_TO_ID['color_2_hsv']):
        return decode_HSV(data)
    
    try: return int(data)
    except: pass

    try: return float(data)
    except: pass

    try:
        return base64.b64decode(data, altchars=b'-_')
    except:
        raise Exception(
            '[Nedit]: Unknown property declaration', p_id, data)

# Encode a property RobTop's way
def encode_property(p_id: int, data: str) -> str:
    if type(data) is list:
        return encode_list(p_id, data)
    
    if type(data) is str:
        return encode_text(p_id, data)
    
    if type(data) is HSV:
        return encode_HSV(p_id, data)
    
    return f'{p_id},{data},'

# Get the name of a property if one exists,
# else get ID with leading underscore
def get_property_name(p_id: int):
    key_str = f'_{p_id}'
    for name, _id in NAME_TO_ID.items():
        if _id == p_id:
            key_str = name
            break
    return key_str

# Decode a list encoded RobTop's way
def decode_list(data: str) -> list[int]:
    return list(map(int, data.split('.')))

# Encode a list RobTop's way
def encode_list(p_id: int, data: list[int]) -> str:
    if not data:
        return ''
    str_list = '.'.join(map(str, data))
    return f'{p_id},{str_list},'


def decode_HSV(data: str) -> HSV:
    values = map(float, data.split('a'))
    return HSV(*values)

def encode_HSV(p_id: int, hsv: HSV):
    hsv_enc = 'a'.join(map(str, hsv.get_property_list()))
    return f'{p_id},{hsv_enc},'

# The text object's message is encoded in base64, this method decodes it.
def decode_text(data: bytes) -> str:
    return base64.b64decode(data, altchars=b'-_').decode()

# The text object's message is encoded in base64,
# this method encodes plaintext.
def encode_text(p_id: int, text: str) -> str:
    enc = base64.b64encode(text.encode()).decode()
    return f'{p_id},{enc},'
