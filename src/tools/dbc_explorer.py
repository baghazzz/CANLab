from decoder import DBCLoader


class DBCExplorer:

    def __init__(self, loader: DBCLoader):
        self.loader = loader

    def summary(self):

        print("=" * 80)
        print("DBC SUMMARY")
        print("=" * 80)

        print(f"Messages : {len(self.loader.messages)}")

        print()

        for message in self.loader.messages:

            print(
                f"{hex(message.frame_id):<12}"
                f"{message.name:<20}"
                f"DLC={message.length}"
            )

    def explore_message(self, frame_id: int):

        message = self.loader.get_message_by_frame_id(frame_id)

        if message is None:
            print("Message not found.")
            return

        print("=" * 80)
        print(message.name)
        print("=" * 80)

        print(f"Frame ID : {hex(message.frame_id)}")
        print(f"Length   : {message.length}")

        print()

        print("Signals")
        print("-" * 80)

        for signal in message.signals:

            print("=" * 80)

            print(signal.name)

            print(f"Multiplexer       : {signal.is_multiplexer}")

            print(f"Multiplexer IDs   : {signal.multiplexer_ids}")

            print(f"Start             : {signal.start}")

            print(f"Length            : {signal.length}")

            print(f"Scale             : {signal.scale}")

            print(f"Offset            : {signal.offset}")

            print(f"Unit              : {signal.unit}")