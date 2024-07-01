# import libs
import joblib
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from wordcloud import WordCloud

# import constants
from _constants import STOP_WORDS_WITHOUT_DASH


# @st.cache_resource()
def load_model():
    return joblib.load("trained_models/RandomForest/pipe.joblib")
    ...


model = load_model()


def sidebar():
    with st.sidebar:
        st.header("Bạn muốn kiểm tra thử comment của bạn có phân biệt vùng miền?")
        # Initialize session state for text input and prediction
        if 'text_input' not in st.session_state:
            st.session_state.text_input = ''
        if 'result' not in st.session_state:
            st.session_state.result = None

        # Capture text input
        st.session_state.text_input = st.text_area(
            "Nhập comment của bạn vào đây:", st.session_state.text_input)

        if st.button("Kiểm tra"):
            with st.spinner("Đang kiểm tra..."):
                st.session_state.result = (
                    model
                    .predict_proba(
                        [st.session_state.text_input]
                    )[0]
                )

        if st.session_state.result is not None:
            result_sorted = sorted(
                enumerate(st.session_state.result), key=lambda x: x[1], reverse=True)

            # st.write(f"Dự đoán: {st.session_state.result}")
            interpretation = [
                "khả năng là khác",
                "khả năng có tính phân biệt vùng miền",
                "khả năng có tính chống lại phân biệt vùng miền"
            ]
            result_text = f"Bình luận của bạn có Dự đoán:\n\n"
            for idx, value in result_sorted:
                result_text += f"- {value:.2%}% {interpretation[idx]}\n"
            st.write(result_text)


def plot_dataframe():
    df: pd.DataFrame = st.session_state.dataframe
    df = df[["platform", "text", "pred", "link"]]
    st.dataframe(
        data=df,
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


def count_label_pred_by_platform():
    df: pd.DataFrame = st.session_state.dataframe

    group_df = (
        df
        .groupby(['platform', 'pred'])
        .size()
        .reset_index(name='count')
        .sort_values(["platform", "pred"])
    )

    group_df["pred"] = group_df["pred"].astype(str)

    fig = px.bar(
        group_df, x='platform', y='count',
        color='pred', barmode='group',
        hover_data={'count': 'số lượng', 'pred': 'dự đoán'},
    )

    fig.update_layout(
        title='Số lượng dự đoán của từng nền tảng',  # Update title
        xaxis_title='Nền tảng',  # Update x-axis label
        yaxis_title='Số lượng',  # Update y-axis label
    )

    return st.plotly_chart(fig)


def plot_top_words():
    df: pd.DataFrame = st.session_state.dataframe

    # Get the list of unique labels
    labels = sorted(df['pred'].unique())

    # Loop through each label and plot the corresponding bar chart
    for label in labels:
        # Get the data for the current label
        label_data = df[df['pred'] == label]

        # Create a dictionary to count the frequency of words
        word_counts = {}
        for content in label_data['text']:
            words = content.split()
            for word in words:
                if word in STOP_WORDS_WITHOUT_DASH:
                    continue

                if word in word_counts:
                    word_counts[word] += 1
                else:
                    word_counts[word] = 1

        # Sort the dictionary by frequency in descending order
        sorted_counts = sorted(
            word_counts.items(),
            key=lambda x: x[1], reverse=True
        )

        # Get the top 20 most frequent words
        top_words = sorted_counts[:20]
        top_words = dict(top_words)

        # Create the bar chart
        fig = go.Figure(
            [go.Bar(x=list(top_words.keys()), y=list(top_words.values()))]
        )

        fig.update_layout(
            title=f"Top 20 words - Label: {label}",
            xaxis_title="Word",
            yaxis_title="Frequency",
            xaxis_tickangle=-45
        )

        # Append the figure to the list
        yield fig


# WordCloud
def generate_wordcloud(
    text_series: pd.Series,
    title: str = "Word Cloud"
):
    # Concatenate all text in the series into a single string
    text = ' '.join(text_series).replace(',', ' ')

    # Process the text to remove stop words and count the frequency of each word
    def process_text(text):
        # remove stop words and convert all words to lowercase
        words = [
            word.lower()
            for word in text.split()
            if word.lower() not in STOP_WORDS_WITHOUT_DASH
        ]

        # remove punctuation
        words = [
            word.strip('.,!?()[]{}-:')
            for word in words
        ]

        # count the frequency of each word
        word_counts = {word: words.count(word) for word in words}
        return word_counts

    # Create and generate a word cloud image
    wordcloud = WordCloud(
        width=800, height=400,
        background_color='white'
    )

    # Generate the word cloud
    word_count = process_text(text)
    wordcloud.generate_from_frequencies(word_count)

    # Convert the WordCloud image to a numpy array
    image_array = wordcloud.to_array()

    # Create a Plotly figure
    fig = px.imshow(image_array)
    fig.update_layout(
        title=title,
        xaxis=dict(showgrid=False, zeroline=False, visible=False),
        yaxis=dict(showgrid=False, zeroline=False, visible=False),
    )

    # Return the Plotly figure
    return fig


def plot_wordcloud():
    df: pd.DataFrame = st.session_state.dataframe

    label: list[int] = sorted(df['pred'].unique())
    for i in label:
        series_text = df[df['pred'] == i]['text']

        if series_text.empty:
            st.text(f"Word Cloud - Label: {i} is empty")
            continue

        wordcloud_fig = generate_wordcloud(
            series_text,
            title=f"Word Cloud - Label: {i}"
        )

        st.plotly_chart(wordcloud_fig)
