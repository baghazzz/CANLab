"""
socketcan_capture.py

SocketCAN interface for HarrierCANLab.

Responsibilities
----------------
- Connect to SocketCAN
- Send CAN frames
- Receive CAN frames
- Efficiently drain the kernel RX queue
"""

import can

from capture.base_capture import BaseCapture
from models.can_frame import CANFrame


class SocketCANCapture(BaseCapture):

    def __init__(
        self,
        channel: str = "can0",
    ):

        self.channel = channel

        self.bus = None

    # ----------------------------------------------------------

    def connect(self):

        print(f"Connecting to {self.channel}...")

        self.bus = can.interface.Bus(

            channel=self.channel,

            interface="socketcan",

        )

        print("Connected.")

    # ----------------------------------------------------------

    def disconnect(self):

        if self.bus is not None:

            self.bus.shutdown()

    # ----------------------------------------------------------

    def receive(
        self,
        timeout: float = 0.0,
    ) -> CANFrame | None:

        if self.bus is None:

            raise RuntimeError(
                "SocketCAN not connected."
            )

        msg = self.bus.recv(timeout=timeout)

        if msg is None:

            return None

        return CANFrame(

            timestamp=msg.timestamp,

            arbitration_id=msg.arbitration_id,

            dlc=msg.dlc,

            data=bytes(msg.data),

            is_extended_id=msg.is_extended_id,

            channel=self.channel,

        )

    # ----------------------------------------------------------

    def drain(self) -> list[CANFrame]:
        """
        Drain the complete SocketCAN receive queue.

        Returns
        -------
        list[CANFrame]
        """

        frames = []

        while True:

            frame = self.receive(timeout=0)

            if frame is None:

                break

            frames.append(frame)

        return frames

    # ----------------------------------------------------------

    def send(
        self,
        frame: CANFrame,
    ) -> bool:

        if self.bus is None:

            raise RuntimeError(
                "SocketCAN not connected."
            )

        message = can.Message(

            arbitration_id=frame.arbitration_id,

            data=frame.data,

            is_extended_id=frame.is_extended_id,

        )

        try:

            self.bus.send(

                message,

                timeout=0.1,

            )

            return True

        except can.CanOperationError:

            #
            print(f"SocketCAN TX Error: {e}")
            #

            return False