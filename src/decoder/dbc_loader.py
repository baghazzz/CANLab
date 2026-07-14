"""
dbc_loader.py

Loads a DBC file and provides decoding services.
"""

from pathlib import Path

import cantools


class DBCLoader:

    def __init__(self, dbc_path: str | Path):

        self.dbc_path = Path(dbc_path).expanduser().resolve()

        if not self.dbc_path.exists():
            raise FileNotFoundError(
                f"DBC file not found: {self.dbc_path}"
            )

        self.database = cantools.database.load_file(
            str(self.dbc_path)
        )

    @property
    def messages(self):
        return self.database.messages

    def get_message_by_frame_id(self, frame_id: int):

        try:
            return self.database.get_message_by_frame_id(frame_id)
        except KeyError:
            return None

    def decode(self, frame_id: int, data: bytes):
        """
        Decode a CAN payload.

        Returns
        -------
        dict
            Dictionary of decoded signals.
        """

        return self.database.decode_message(
            frame_id,
            data,
            decode_choices=True
        )