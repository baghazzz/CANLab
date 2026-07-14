import cantools


class LiveDecoder:

    def __init__(self, dbc_path):

        self.db = cantools.database.load_file(dbc_path)

    def decode(self, frame):

        try:

            decoded = self.db.decode_message(
                frame.arbitration_id,
                frame.data
            )

            return decoded

        except Exception:

            return None