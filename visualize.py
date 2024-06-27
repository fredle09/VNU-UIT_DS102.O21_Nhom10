# import libs
import asyncio
import streamlit as st
import pandas as pd

# import bin
from bin.store import MongoDB


dataframe = pd.DataFrame(columns=["platform", "text", "pred", "link"])


def init_connection():
    return MongoDB()


database = init_connection()
count = 0


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


# Function to fetch data from the database
async def fetch_data():
    global dataframe, count
    items = database["predicts"].find()
    dataframe = pd.DataFrame(items)
    count += 1


# Function to visualize the data
def visualize():
    with st.container():
        st.dataframe(
            data=dataframe[["text", "pred", "link"]],
            use_container_width=True,
            column_config={
                "text": "Comment",
                "pred": "Predict",
                "link": st.column_config.LinkColumn(
                    "Link of comment",
                ),
            },
        )

        st.dataframe(
            data=(
                dataframe.groupby(['platform', 'pred'])
                .size()
                .reset_index(name='count')
            )
        )

        st.bar_chart(
            data=(
                dataframe.groupby(['platform', 'pred'])
                .size()
                .reset_index(name='count')
            ),
            x="platform",
            y="count",
            color=[]
        )

        st.text(f"Count: {count}")


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
