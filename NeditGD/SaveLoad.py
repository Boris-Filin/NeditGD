import os
import struct
import base64, gzip, zlib
import xml.etree.ElementTree as ET

# from Properties import *
from Object import Object

SAVE_FILE = "CCLocalLevels.dat"
PATH_TO_SAVE = os.getenv("localappdata") + "\\GeometryDash\\"


# Read the file from the save path
def load_gamesave() -> bytes:
    fr = open(PATH_TO_SAVE + SAVE_FILE, "rb")
    data = fr.read()
    fr.close()
    return data

# Write the file to the save path
def overwrite_gamesave(data: bytes):
    fw = open(PATH_TO_SAVE + SAVE_FILE, "wb")
    fw.write(data)
    fw.close()



# Apply xor to decode/encode data
def xor_data(data, key) -> str:
    res = []
    for i in data:
        res.append(i ^ key)
    return bytearray(res).decode()



# Decrypt gamesave
def decrypt_gamesave(data: bytes = None) -> bytes:
    if data is None: data = load_gamesave()
        # if data is None else data

    res = xor_data(data, 11)
    compressed = base64.b64decode(res, altchars=b'-_')
    fin = zlib.decompress(compressed[10:], -zlib.MAX_WBITS)
    return fin

# Encrypt the gamesave from XML string
def encryptGamesave(data: bytes):
    compressedData = zlib.compress(data)
    crc32 = struct.pack("I", zlib.crc32(data))
    dataSize = struct.pack("I", len(data))

    encrypted = (
        b"\x1f\x8b\x08\x00\x00\x00\x00\x00\x00\x0b"
        + compressedData[2:-4]
        + crc32
        + dataSize
    )
    encoded = (
        base64.b64encode(encrypted)
        .decode()
        .replace("+", "-")
        .replace("/", "_")
        .encode()
    )
    fin = xor_data(encoded, 11).encode()
    
    overwrite_gamesave(fin)



# Read the gamesave XML;
def read_gamesave_xml(gamesave: bytes = None) -> ET:
    if gamesave is None: gamesave = decrypt_gamesave()
    
    tree = ET.ElementTree(ET.fromstring(gamesave))
    return tree.getroot()



# Get the last ('current') level on the custom levels list
def get_working_level_node(root: ET = None) -> ET:
    if root is None: root = read_gamesave_xml()
    
    try:
        levels_node = root[0][1][3]
    except:
        raise Exception('[Nedit]: No levels could be found!')

    name, level = None, None

    for (i, child) in enumerate(levels_node):
        if child.text == 'k2':
            name = levels_node[i+1].text
        if child.text == 'k4':
            level = levels_node[i+1]
            break

    print('[Nedit]: Reading', name)

    if level is None:
        print('[Nedit]: Level has not been initialised! '
              'Loading default level data...')
        k4_el = ET.Element('k')
        k4_el.text = 'k4'
        levels_node.append(k4_el)
        
        level = ET.Element('s')
        levels_node.append(level)
    
    return level

# Get the data of the current level
def get_working_level(level: ET = None) -> str:
    if level is None: level = get_working_level_node()
    
    return level.text

# Set the data for the level node
def set_level_data(level: ET, level_encrypted: str):
    level.text = level_encrypted



# Decode the level data 
def get_working_level_string(gamesave: str = None) -> str:
    if gamesave is None: gamesave = get_working_level()

    base64_decoded = base64.urlsafe_b64decode(gamesave.encode())
    # window_bits = 15 | 32 will autodetect gzip or not
    decompressed = zlib.decompress(base64_decoded, 15 | 32)
    return decompressed.decode()

# Encrypt the level dictionary
def encrypt_level_string(dls) -> str:
    compressed_data = gzip.compress(dls)
    encoded_data = base64.b64encode(compressed_data, altchars=b'-_')
    return encoded_data.decode()



# Read individual objects from the given level string as a list
def read_level_objects(level_string: str) -> dict:
    if level_string is None: level_string = get_working_level_string()

    objects = level_string.split(';')[1:]
    while objects and not objects[-1]:
        if objects and not objects[-1]:
            objects = objects[:-1]
    objects = list(map(Object.from_robtop, objects))
    return objects

# Read the level head info - for save purposes only
def read_level_head(level_string: str) -> str:
    if level_string is None: level_string = get_working_level_string()

    return level_string.split(';')[0]

# Construct the save string from modified objects and head
def get_level_save_string(objects: list[Object], level_head: str):
    obj_encodings = [obj.to_robtop() for obj in objects]
    obj_string = ';'.join(obj_encodings)
    level_string = f'{level_head};{obj_string};'
    return level_string



'''
Decryption/Encryption process:

Encoded .dat file
A       ↕   Read the file
File bytes
B       ↕   XOR with key (11)
Compressed base64 bytes
C       ↕   base64 encode/decode
Compressed data
D       ↕   zlib decompress
XML string bytes
E       ↕   XML to/from string
XML ETree of all levels


Level decryption/encryption:

XML ETree of all levels
F       ↕   Locating the most recent ('current') file
XML node of level data
G       ↕   Reading the level data
Level bytes
H       ↕   base64 encode/decode
Compressed level data
I       ↕   zlib decompress
level string bytes
J       ↕   string decode
readable level string
K       ↕   Split by ';'
Level head and individual objects
L       ↕   Decode objects depending and property IDs
List of objects and string head



Methods responsible for each step of decryption:
load_gamesave:          A
xor_data:               B
decrypt_gamesave:       C, D
read_gamesave_xml:      E

get_working_level_node: F
get_working_level:      G
decode_level_string:    H, I, J
read_level_objects,
 read_level_head:       K

GameObject does L itself


'''