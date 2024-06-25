# import constants
from _constants import *

# import bin
from bin.streaming.consumer import Consumer
from bin.pipeline import Pipeline
from bin.store import MongoDB


data_bucket: list[Any] = []


def consume_messages():
    global data_bucket

    con: Consumer = Consumer(
        topic=CAPTURE_TOPIC,
    )

    try:
        for message in con.get_message():
            platform = message["key"]
            data = json_dumps(message["value"])

            data_bucket.append({"platform": platform, **data})
            print("Catched data")
    except KeyboardInterrupt:
        print("Exiting...")
        exit(0)
    ...


def predict_and_store():
    global data_bucket

    pipe: Pipeline = Pipeline()
    database = MongoDB()

    i = 0

    try:
        while True:
            if len(data_bucket) != 0:
                local_data_bucket = data_bucket
                data_bucket = []  # clear data_bucket

                df_raw = pd.DataFrame(local_data_bucket)
                y_pred = pipe.run(df_raw)
                df_predict = df_raw.join(y_pred)
                df_predict_to_records = df_predict.to_dict(orient="records")
                database["predicts"].insert_many(df_predict_to_records)

                i += 1
            else:
                print("No data to predict")
            sleep(5)
    except KeyboardInterrupt:
        print("Exiting...")
        exit(0)
    ...


if __name__ == '__main__':
    consumer_thread = threading.Thread(target=consume_messages)
    predict_thread = threading.Thread(target=predict_and_store)

    threads = [consumer_thread, predict_thread]
    [thread.start() for thread in threads]
    try:
        [thread.join() for thread in threads]
    except KeyboardInterrupt:
        print("Exiting...")
        exit(0)
