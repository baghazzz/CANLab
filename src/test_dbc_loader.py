from decoder.dbc_loader import DBCLoader

loader = DBCLoader(
    "resources/dbc/OBD-v4.4.dbc"
)

print("DBC Loaded Successfully")

print()

print(f"Messages: {len(loader.messages)}")

print()

for message in loader.messages[:10]:
    print(
        hex(message.frame_id),
        message.name
    )