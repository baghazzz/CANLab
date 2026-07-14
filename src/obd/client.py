"""
client.py

OBD-II Client

Responsibilities
----------------
- Ask the scheduler for the next PID.
- Build OBD requests.
- Send ONE OBD request.
- Record successful transmissions.

The client DOES NOT:
- Receive CAN frames.
- Decode CAN frames.
- Process responses.
"""

import time

from obd.pid_scheduler import PIDScheduler
from obd.request_builder import OBDRequestBuilder
from obd.pid_catalog import ACTIVE_NAME


class OBDClient:

    def __init__(
        self,
        capture,
        recorder,
    ):

        self.capture = capture
        self.recorder = recorder

        self.scheduler = PIDScheduler()
        self.cooldown_until = 0.0
        #
        # Prevent accidental bursts
        #
        self.minimum_gap = 0.025
        self.last_tx = 0.0

        #
        # Statistics
        #
        self.tx_success = 0
        self.tx_failed = 0
        self.tx_skipped = 0

    # --------------------------------------------------------

    def poll(self):

        now = time.time()
        #

        if now < self.cooldown_until:
            return
        #
        # Global TX rate limiter
        #
        if (now - self.last_tx) < self.minimum_gap:

            self.tx_skipped += 1
            return

        #
        # Ask scheduler for next PID
        #
        pid = self.scheduler.get_next_pid()

        if pid is None:
            return

        #
        # Build OBD request
        #
        request = OBDRequestBuilder.build_mode01_request(pid)

        #
        # Transmit
        #
        success = self.capture.send(request)

        if success:

            self.recorder.record(
                request,
                direction="TX",
            )

            self.tx_success += 1

            self.last_tx = now

            print(f"TX -> {ACTIVE_NAME}")

        else:

            self.tx_failed += 1

            #
            # Back off for one second.
            #

            self.cooldown_until = time.time() + 1.0

            print("TX failed - entering cooldown for 1 second")

            return

    # --------------------------------------------------------

    def stats(self):

        return {

            "success": self.tx_success,

            "failed": self.tx_failed,

            "skipped": self.tx_skipped,

        }

    # --------------------------------------------------------

    def reset_stats(self):

        self.tx_success = 0
        self.tx_failed = 0
        self.tx_skipped = 0