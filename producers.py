"""
This module contains the functions used to produce the data.
"""

# import libs
import threading

# import bin
from bin.streaming.producer import Producer

# import constants
from _constants import CAPTURE_TOPIC


def main():
    """
    Main function.
    """

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

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()


if __name__ == '__main__':
    # Run the main asyncio loop
    main()
