"""
pid_scheduler.py

Scheduler for ONE PID only.
"""

import time

from obd.pid_catalog import (
    ACTIVE_PID,
    POLL_INTERVAL,
)


class PIDScheduler:

    def __init__(self):

        self.last_tx = 0.0

    def get_next_pid(self):

        now = time.time()

        if (now - self.last_tx) >= POLL_INTERVAL:

            self.last_tx = now

            return ACTIVE_PID

        return None