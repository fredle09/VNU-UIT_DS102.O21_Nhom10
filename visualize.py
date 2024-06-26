# # import libs
# import streamlit as st
# from streamlit.runtime.scriptrunner import add_script_run_ctx
# from streamlit_autorefresh import st_autorefresh
# import random
#
#
# # import _constants
# from _constants import *
#
# # import bin
# from bin.store import MongoDB
#
#
# data: pd.DataFrame = pd.DataFrame(columns=["platform", "text", "pred", "link"])
#
#
# def init_page():
#     st.set_page_config(
#         page_title="Dashboard Phân biệt vùng miền",
#         page_icon="🙀",
#         layout="wide",
#         initial_sidebar_state="expanded"
#     )
#
#     st.markdown("# Graduate Admission Predictor")
#     st.markdown("## Drop in The required Inputs and we will do the rest")
#     st.markdown("### Submission for The Python Week")
#
#     with st.sidebar:
#         st.header("What is this Project about?")
#         st.text(
#             "It a Web app that would help the user in determining whether they will get admission in a Graduate Program or not.")
#         st.header("What tools where used to make this?")
#         st.text("The Model was made using a dataset from Kaggle along with using Kaggle notebooks to train the model. We made use of Sci-Kit learn in order to make our Linear Regression Model.")
#
#
#
# def fetch_data_thread():
#     global data
#
#     @st.cache_resource
#     def init_connection():
#         return MongoDB()
#
#     database = init_connection()
#
#     @st.cache_data(ttl=5)
#     def get_data():
#         items = database["predicts"].find()
#         data = pd.DataFrame(items)
#         return data
#
#     while True:
#         data = get_data()
#         print("(thread fetch_data_thread) data:", data)
#         sleep(5)
#
#
# def main():
#     global data
#     # st.dataframe(data)
#     print("(thread main) data:", data)
#     if len(data) != 0:
#         st.dataframe(
#             data=data[["text", "pred", "link"]],
#             use_container_width=True,
#             column_config={
#                 "text": "Comment",
#                 "pred": "Predict",
#                 "link": st.column_config.LinkColumn(
#                     "Link of comment",
#                 ),
#             },
#         )
#
#         st.dataframe(
#             data=(
#                 data.groupby(['platform', 'pred'])
#                 .size()
#                 .reset_index(name='count')
#             )
#         )
#
#         st.bar_chart(
#             data=(
#                 data.groupby(['platform', 'pred'])
#                 .size()
#                 .reset_index(name='count')
#             ),
#             x="platform",
#             y="count",
#             color=[]
#         )
#
#     st.experimental_rerun()
#     ...
#
#
# if __name__ == '__main__':
#     init_page()
#     print("Lmao")
#     threads = [
#         threading.Thread(target=target)
#         for target in [fetch_data_thread, main]
#     ]
#
#     add_script_run_ctx(threads[0])
#     add_script_run_ctx(threads[1])
#     threads[0].start()
#     threads[1].start()

# import libs
import streamlit as st
import pandas as pd
import threading
import time

# import constants
from _constants import *

# import bin
from bin.store import MongoDB


# Initialize Streamlit page configuration
def init_page():
    st.set_page_config(
        page_title="Dashboard Phân biệt vùng miền",
        page_icon="🙀",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    st.markdown("# Graduate Admission Predictor")
    st.markdown("## Drop in The required Inputs and we will do the rest")
    st.markdown("### Submission for The Python Week")

    with st.sidebar:
        st.header("What is this Project about?")
        st.text(
            "It is a Web app that helps the user determine whether they will get admission to a Graduate Program or not."
        )
        st.header("What tools were used to make this?")
        st.text(
            "The model was made using a dataset from Kaggle and trained using Kaggle notebooks. "
            "We used Scikit-learn to create a Linear Regression Model."
        )

# Cached function to initialize the database connection


@st.cache_resource
def init_connection():
    return MongoDB()

# Function to fetch data from the database


def fetch_data():
    database = init_connection()
    items = database["predicts"].find()
    data = pd.DataFrame(items)
    return data

# Function to run in a separate thread for fetching data periodically


def fetch_data_thread():
    while True:
        st.session_state.data = fetch_data()
        sleep(5)


def main():
    init_page()

    # Initialize session state variables
    if "data" not in st.session_state:
        st.session_state.data = pd.DataFrame(
            columns=["platform", "text", "pred", "link"])
    if "thread_started" not in st.session_state:
        st.session_state.thread_started = False

    # Start the data fetching thread if it hasn't been started yet
    if not st.session_state.thread_started:
        thread = threading.Thread(
            target=fetch_data_thread, args=(), daemon=True)
        thread.start()
        st.session_state.thread_started = True

    # Display the data in Streamlit
    data = st.session_state.data
    if not data.empty:
        st.dataframe(
            data=data[["text", "pred", "link"]],
            use_container_width=True,
            column_config={
                "text": "Comment",
                "pred": "Predict",
                "link": st.column_config.LinkColumn(
                    "Link of comment",
                ),
            },
        )

        grouped_data = data.groupby(
            ['platform', 'pred']).size().reset_index(name='count')

        st.dataframe(grouped_data)

        st.bar_chart(
            data=grouped_data.pivot(
                index='platform', columns='pred', values='count').fillna(0),
            use_container_width=True
        )


if __name__ == '__main__':
    main()
