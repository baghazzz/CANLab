"""
can_worker.py

Background CAN worker.

Responsibilities
----------------
- Connect to SocketCAN
- Receive CAN frames
- Decode using DBC
- Emit Qt signals to the dashboard
"""

from PyQt6.QtCore import (
    QThread,
    pyqtSignal,
)

from capture.socketcan_capture import SocketCANCapture

from decoder.dbc_loader import DBCLoader
from decoder.dbc_decoder import DBCDecoder


class CANWorker(QThread):

    #
    # -----------------------------
    # Qt Signals
    # -----------------------------
    #

    rpm_updated = pyqtSignal(float)

    status_updated = pyqtSignal(str)

    frame_received = pyqtSignal()

    can_id_received = pyqtSignal(int)

    # --------------------------------------------------------

    def __init__(
        self,
        channel: str,
        dbc_path: str,
    ):

        super().__init__()

        self.channel = channel

        self.dbc_path = dbc_path

        self.running = True

        #
        # CAN
        #

        self.capture = SocketCANCapture(
            self.channel
        )

        #
        # Decoder
        #

        loader = DBCLoader(
            self.dbc_path
        )

        self.decoder = DBCDecoder(
            loader
        )

    # --------------------------------------------------------

    def stop(self):

        self.running = False

    # --------------------------------------------------------

    def run(self):

        #
        # Connect
        #

        try:

            self.capture.connect()

            self.status_updated.emit(
                "Connected"
            )

        except Exception as e:

            self.status_updated.emit(
                f"Connection Failed ({e})"
            )

            return

        #
        # Main Loop
        #

        while self.running:

            frame = self.capture.receive(
                timeout=0.1
            )

            if frame is None:

                continue

            #
            # Dashboard Statistics
            #

            self.frame_received.emit()

            self.can_id_received.emit(
                frame.arbitration_id
            )

            #
            # Decode
            #

            decoded = self.decoder.decode(
                frame
            )

            if decoded is None:

                continue

            #
            # Search for RPM signal
            #

            for signal in decoded:

                if signal.name == "EngineRPM":

                    self.rpm_updated.emit(
                        float(signal.value)
                    )

                    break

        #
        # Disconnect
        #

        self.capture.disconnect()

        self.status_updated.emit(
            "Disconnected"
        )