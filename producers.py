# import bin
from bin.streaming.producer import Producer

# import constants
from _constants import *


def main():
    # Create instances of Producer
    prod = Producer(topic=CAPTURE_TOPIC)

    # List of tasks to run concurrently
    threads = [
        threading.Thread(
            target=prod.send_message_from_csv,
            kwargs={
                "csv_file_path": "reddit_pbvm_Huong.csv"
            }
        ),
        threading.Thread(
            target=prod.send_message_from_csv,
            kwargs={
                "csv_file_path": "tiktok_pbvm_Dat.csv"
            }
        ),
        threading.Thread(
            target=prod.send_message_from_csv,
            kwargs={
                "csv_file_path": "youtube_pbvm_Hieu.csv"
            }
        ),
    ]

    [thread.start() for thread in threads]
    [thread.join() for thread in threads]


if __name__ == '__main__':
    # Run the main asyncio loop
    main()
