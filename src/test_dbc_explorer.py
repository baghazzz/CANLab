from decoder import DBCLoader
from tools.dbc_explorer import DBCExplorer


loader = DBCLoader(
    "resources/dbc/OBD-v4.4.dbc"
)

explorer = DBCExplorer(loader)

explorer.summary()

print()

explorer.explore_message(0x7E8)