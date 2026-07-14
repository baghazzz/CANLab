"""
HarrierCANLab

Phase 2

High-performance synchronized CAN + OBD acquisition.

Responsibilities
----------------
1. Continuously drain SocketCAN RX queue.
2. Record every received CAN frame.
3. Periodically transmit ONE OBD request.
4. Record transmitted OBD requests.
5. Buffered CSV logging.
"""

import time

from capture.socketcan_capture import SocketCANCapture

from obd.client import OBDClient

from recording.csv_recorder import CSVRecorder
from recording.session_manager import SessionManager


#
# Acquisition loop timing
#

MAIN_LOOP_SLEEP = 0.001        # 1 ms

#
# Statistics interval
#

STATS_INTERVAL = 1.0


def main():

    print("=" * 80)
    print("HarrierCANLab")
    print("Phase 2 - High Performance Logger")
    print("=" * 80)

    #
    # ------------------------------------------------------------
    # Session
    # ------------------------------------------------------------
    #

    session = SessionManager(

        vehicle="Tata Harrier EV",

        interface="can0",

        bitrate=500000,

        dbc_version="OBD-v4.4",

    )

    session.start()

    recorder = CSVRecorder(

        session.session_csv()

    )

    #
    # ------------------------------------------------------------
    # CAN
    # ------------------------------------------------------------
    #

    capture = SocketCANCapture("can0")

    capture.connect()

    #
    # ------------------------------------------------------------
    # OBD
    # ------------------------------------------------------------
    #

    obd = OBDClient(

        capture=capture,

        recorder=recorder,

    )

    print()
    print("Recording started.")
    print("CTRL+C to stop.")
    print()

    last_stats = time.time()

    try:

        while True:

            #
            # ======================================================
            # 1. Drain SocketCAN completely
            # ======================================================
            #

            frames = capture.drain()

            #
            # ======================================================
            # 2. Record all received frames
            # ======================================================
            #

            for frame in frames:

                recorder.record(

                    frame,

                    direction="RX",

                )

            #
            # ======================================================
            # 3. Send ONE OBD request
            # ======================================================
            #

            obd.poll()

            #
            # ======================================================
            # 4. Statistics
            # ======================================================
            #

            now = time.time()

            if now - last_stats >= STATS_INTERVAL:

                r = recorder.stats()

                t = obd.stats()

                print(
                    f"[RX:{r['frames_logged']:,}] "
                    f"[Buffered:{r['buffer_size']}] "
                    f"[Flushes:{r['flushes']}] "
                    f"[TX:{t['success']}] "
                    f"[Failed:{t['failed']}] "
                    f"[Skipped:{t['skipped']}]"
                )

                last_stats = now

            #
            # ======================================================
            # 5. Small sleep
            # ======================================================
            #

            time.sleep(MAIN_LOOP_SLEEP)

    except KeyboardInterrupt:

        print()

        print("Stopping session...")

    finally:

        recorder.close()

        capture.disconnect()

        session.stop()

        print()

        print("Session saved.")

        print(session.session_dir)


if __name__ == "__main__":

    main()