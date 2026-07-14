import can

bus = can.interface.Bus(
    channel="can0",
    interface="socketcan"
)

msg = can.Message(
    arbitration_id=0x7D0,
    data=[0x02, 0x01, 0x0D, 0, 0, 0, 0, 0],
    is_extended_id=False,
)

print("Sending request...")

bus.send(msg)

print("Done.")