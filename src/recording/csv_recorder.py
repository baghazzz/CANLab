"""
csv_recorder.py

Buffered CSV recorder.

Records every CAN frame while minimizing
disk I/O.

The recorder is protocol agnostic.
"""

from pathlib import Path
import csv
import time

from models.can_frame import CANFrame


class CSVRecorder:

    HEADER = [

        "timestamp",

        "direction",

        "can_id",

        "extended",

        "dlc",

        "data",

    ]

    # ----------------------------------------------------------

    def __init__(

        self,

        csv_path: Path,

        flush_interval: float = 0.25,

        batch_size: int = 500,

    ):

        self.file = open(

            csv_path,

            "w",

            newline="",

            encoding="utf-8",

        )

        self.writer = csv.writer(self.file)

        self.writer.writerow(self.HEADER)

        #
        # Buffer
        #

        self.buffer = []

        self.batch_size = batch_size

        self.flush_interval = flush_interval

        self.last_flush = time.time()

        #
        # Statistics
        #

        self.frames_logged = 0

        self.flush_count = 0

    # ----------------------------------------------------------

    def record(

        self,

        frame: CANFrame,

        direction: str,

    ):

        self.buffer.append(

            [

                f"{frame.timestamp:.6f}",

                direction,

                hex(frame.arbitration_id),

                int(frame.is_extended_id),

                frame.dlc,

                frame.data.hex().upper(),

            ]

        )

        self.frames_logged += 1

        #
        # Flush if needed
        #

        now = time.time()

        if (

            len(self.buffer) >= self.batch_size

            or

            (now - self.last_flush) >= self.flush_interval

        ):

            self.flush()

    # ----------------------------------------------------------

    def flush(self):

        if not self.buffer:

            return

        self.writer.writerows(self.buffer)

        self.file.flush()

        self.buffer.clear()

        self.last_flush = time.time()

        self.flush_count += 1

    # ----------------------------------------------------------

    def stats(self):

        return {

            "frames_logged": self.frames_logged,

            "buffer_size": len(self.buffer),

            "flushes": self.flush_count,

        }

    # ----------------------------------------------------------

    def close(self):

        self.flush()

        self.file.close()