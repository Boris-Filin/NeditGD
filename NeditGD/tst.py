from __future__ import annotations
from NeditGD.saveload import *
from NeditGD import Object

import json
from websocket import create_connection
from typing import List



try:
    socket = create_connection("ws://127.0.0.1:1313")
except ConnectionRefusedError:
    raise ConnectionRefusedError('No editor socket found!\nCheck that you have WSLiveEdit enabled and your editor is open.')    
packet = {
    "action": "ADD_OBJECTS",
    "objects": "1,1,2,60,3,90,57,1.9999",
}
socket.send(json.dumps(packet))