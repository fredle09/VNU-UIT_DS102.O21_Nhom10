# import libs
import asyncio
import streamlit as st
import pandas as pd

# import bin
from bin.store import MongoDB
from bin.visualize import init_page, plot_top_words, \
    plot_wordcloud, count_label_pred_by_platform


dataframe = pd.DataFrame(columns=["platform", "text", "pred", "link"])


def init_connection():
    return MongoDB(
        url=st.secrets["MONGODB_ATLAS_URL"],
        db_name=st.secrets["MONGODB_ATLAS_DB_NAME"],
    )


database = init_connection()
count = 0


# Function to fetch data from the database
async def fetch_data():
    global dataframe, count
    items = database["predicts"].find()
    dataframe = pd.DataFrame(items)
    count += 1


# Function to visualize the data
def visualize():
    with st.container():
        if dataframe.empty:
            st.write("No data available")
            return

        st.dataframe(
            data=dataframe[["platform", "text", "pred", "link"]],
            use_container_width=True,
            column_config={
                "platform": "platform",
                "text": "Comment",
                "pred": "Predict",
                "link": st.column_config.LinkColumn(
                    "Link of comment",
                ),
            },
        )

        # plot count label predict by platform chart
        count_label_pred_by_platform(dataframe)

        # plot top words chart
        for fig in plot_top_words(dataframe):
            st.plotly_chart(fig)

        # plot wordcloud chart
        plot_wordcloud(dataframe)


async def main():
    init_page()
    placeholder = st.container()
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
