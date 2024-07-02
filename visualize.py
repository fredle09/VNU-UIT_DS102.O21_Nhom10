"""
This module contains code for visualizing data in a dashboard for region differentiation.

It imports necessary libraries, defines utility functions, and sets up the Streamlit dashboard.

Functions:
- decode_label(label: int) -> str: Decodes a label into its corresponding string value.
- init_connection(): Initializes a connection to the MongoDB database.
- fetch_data(): Fetches data from the database and updates the session state.
- visualize(): Visualizes the data in the Streamlit dashboard.
- main(): Main function that runs the Streamlit dashboard.

"""

# import libs
import asyncio
import streamlit as st
import pandas as pd

# import bin
from bin.store import MongoDB
from bin.visualize import sidebar, plot_top_words, \
    plot_wordcloud, count_label_pred_by_platform, \
    plot_dataframe


if "dataframe" not in st.session_state:
    st.session_state.dataframe = pd.DataFrame(
        columns=["platform", "text", "pred", "link"]
    )


def decode_label(label: int) -> str:
    """
    Decodes a label into its corresponding string value.

    Args:
        label (int): The label to decode.

    Returns:
        str: The decoded string value of the label.
    """

    default_value: str = "Không xác định"
    hashed_dict: dict[int, str] = {
        0: "Khác",
        1: "Phân biệt",
        2: "Ủng hộ"
    }

    return hashed_dict.get(label, default_value)


st.set_page_config(
    page_title="Dashboard Phân biệt vùng miền",
    page_icon="🙀",
    layout="wide",
    initial_sidebar_state="auto"
)

st.markdown("# Dashboard Phân biệt vùng miền")


@st.cache_resource
def init_connection():
    """
    Initializes a connection to the MongoDB database.

    Returns:
        MongoDB: A MongoDB object representing the connection to the database.
    """

    return MongoDB(
        url=st.secrets["MONGODB_ATLAS_URL"],
        db_name=st.secrets["MONGODB_ATLAS_DB_NAME"],
    )


database = init_connection()


# Function to fetch data from the database
async def fetch_data():
    """
    Fetches data from the database and updates the session state.
    """

    items = database["predicts"].find()
    dataframe: pd.DataFrame = (
        pd
        .DataFrame(items)[
            ["platform", "text", "pred", "link"]
        ]
    )
    dataframe["pred"] = dataframe["pred"].apply(decode_label)

    st.session_state.dataframe = dataframe


# Function to visualize the data
def visualize():
    """
    Visualizes the data in the Streamlit dashboard.
    """

    with st.container():
        if ("dataframe" not in st.session_state
                or st.session_state.dataframe.empty):
            st.write("No data available")
            return

        st_1, st_2 = st.columns([1, 1])
        with st_1:
            st.metric(
                "Thống kê số lượng dữ liệu",
                st.session_state.dataframe.shape[0]
            )
        with st_2:
            st.metric(
                "Số lượng bình luận có tính phân biệt được xác định",
                st.session_state.dataframe[
                    # label của phân biệt
                    st.session_state.dataframe["pred"] == decode_label(1)
                ].shape[0]
            )

        # plot dataframe
        plot_dataframe()

        # plot count label predict by platform chart
        count_label_pred_by_platform()

        # plot top words chart
        st.markdown("## Top từ được sử dụng theo từng nhóm")
        for fig in plot_top_words():
            st.plotly_chart(
                fig,
                use_container_width=True,
            )

        # plot wordcloud chart
        plot_wordcloud()


async def main():
    """
    Main function that runs the Streamlit dashboard.
    """

    placeholder = st.container()
    sidebar()
    with placeholder.empty():
        # while True:
        await fetch_data()

        visualize()
        await asyncio.sleep(5)


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
    finally:
        print("Closing Loop")
        loop.close()
