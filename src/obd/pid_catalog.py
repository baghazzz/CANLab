"""
pid_catalog.py

Select ONE PID to acquire.

Change ACTIVE_PID for each experiment.
"""

from obd.pid import PID

#
# Select ONE signal
#

ACTIVE_PID = PID.THROTTLE

ACTIVE_NAME = "THROTTLE_POSITION"

POLL_INTERVAL = 0.1
