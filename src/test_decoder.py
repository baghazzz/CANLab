from decoder import DBCLoader
from decoder.dbc_decoder import DBCDecoder

from models.can_frame import CANFrame


loader = DBCLoader(
    "resources/dbc/OBD-v4.4.dbc"
)

decoder = DBCDecoder(loader)


frame = CANFrame(
    timestamp=0.0,
    arbitration_id=0x7E8,
    dlc=8,
    data=bytes.fromhex("03 41 0D 3C 00 00 00 00"),
    is_extended_id=False,
    channel="can0"
)


decoded = decoder.decode(frame)

print(decoded)