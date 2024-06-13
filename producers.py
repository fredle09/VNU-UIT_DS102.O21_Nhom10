# import libs
from bin.streaming.producer import using_producer_for_streaming

# import constants
from _constants import *

import findspark
findspark.init()

if __name__ == '__main__':
    using_producer_for_streaming(
        "./datasets/youtube_dataset_pbvm.csv"
    )
