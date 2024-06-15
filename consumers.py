# import libs
from bin.streaming.consumer import Consumer

# import constants
from _constants import *


if __name__ == '__main__':
    con: Consumer = Consumer(
        topic=CAPTURE_TOPIC,
    )

    print(con.get_message())
