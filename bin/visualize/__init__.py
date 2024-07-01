# import libs
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from wordcloud import WordCloud

# import constants
from _constants import STOP_WORDS_WITHOUT_DASH


def init_page():
    st.set_page_config(
        page_title="Dashboard Phân biệt vùng miền",
        page_icon="🙀",
        layout="centered",
        initial_sidebar_state="auto"
    )

    st.markdown("# Dashboard Phân biệt vùng miền")

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


def plot_top_words(df):
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
                if word in word_counts:
                    word_counts[word] += 1
                else:
                    word_counts[word] = 1

        # Sort the dictionary by frequency in descending order
        sorted_counts = sorted(word_counts.items(),
                               key=lambda x: x[1], reverse=True)

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


def plot_wordcloud(df: pd.DataFrame):
    label = [0, 1, 2]
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
