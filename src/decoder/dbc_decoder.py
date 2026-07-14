"""
dbc_decoder.py

Converts CANFrame objects into DecodedMessage objects.
"""

from decoder.decoder_interface import DecoderInterface
from decoder.dbc_loader import DBCLoader

from models.can_frame import CANFrame
from models.signal import Signal
from models.decoded_message import DecodedMessage


class DBCDecoder(DecoderInterface):

    def __init__(self, loader: DBCLoader):

        self.loader = loader

    def decode(
        self,
        frame: CANFrame
    ) -> DecodedMessage | None:

        # Does the DBC know this CAN ID?

        message = self.loader.get_message_by_frame_id(
            frame.arbitration_id
        )

        if message is None:
            return None

        # Decode payload

        try:

            decoded = self.loader.decode(
                frame.arbitration_id,
                frame.data
            )

        except Exception:
            return None

        decoded_message = DecodedMessage(
            message_name=message.name,
            frame_id=frame.arbitration_id,
            timestamp=frame.timestamp,
        )

        for signal_name, value in decoded.items():

            # Ignore protocol bookkeeping fields
            if signal_name in (
                "Length",
                "S",
                "S01PID",
                "S02PID",
            ):
                continue

            signal_definition = message.get_signal_by_name(
                signal_name
            )

            unit = signal_definition.unit or ""

            decoded_message.add_signal(

                Signal(

                    name=signal_name,

                    value=value,

                    unit=unit,

                    timestamp=frame.timestamp,

                    source_message=message.name,
                )
            )

        return decoded_message