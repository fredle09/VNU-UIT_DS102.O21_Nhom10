# import libs
from bin.streaming.producer import Producer

# import constants
from _constants import *


if __name__ == '__main__':
    prod: Producer = Producer()
    prod.send_message(
        topic=CAPTURE_TOPIC,
        csv_file_path="youtube_dataset_pbvm.csv",
    )
