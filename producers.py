# import libs
from bin.streaming.producer import Producer

# import constants
from _constants import *


if __name__ == '__main__':
    prod: Producer = Producer(topic=CAPTURE_TOPIC)
    prod.send_message_from_csv(
        csv_file_path="reddit_pbvm_Huong.csv",
    )
