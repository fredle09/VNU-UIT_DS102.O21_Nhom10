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
if "delta_count_dataframe" not in st.session_state:
    st.session_state.delta_count_dataframe = 0

st.set_page_config(
    page_title="Dashboard Phân biệt vùng miền",
    page_icon="🙀",
    layout="centered",
    initial_sidebar_state="auto"
)

st.markdown("# Dashboard Phân biệt vùng miền")


@st.cache_resource
def init_connection():
    return MongoDB(
        url=st.secrets["MONGODB_ATLAS_URL"],
        db_name=st.secrets["MONGODB_ATLAS_DB_NAME"],
    )


database = init_connection()


# Function to fetch data from the database
async def fetch_data():
    global dataframe
    items = database["predicts"].find()
    st.session_state.dataframe = pd.DataFrame(items)


# Function to visualize the data
def visualize():
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
                    st.session_state.dataframe["pred"] == 1
                ].shape[0]
            )

        # plot dataframe
        plot_dataframe()

        # plot count label predict by platform chart
        count_label_pred_by_platform()

        # plot top words chart
        st.markdown("## Top từ được sử dụng theo từng nhóm")
        for fig in plot_top_words():
            st.plotly_chart(fig)

        # plot wordcloud chart
        plot_wordcloud()


async def main():
    placeholder = st.container()
    sidebar()
    with placeholder.empty():
        while True:
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
