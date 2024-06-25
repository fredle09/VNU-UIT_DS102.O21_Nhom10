# import libs
import streamlit as st
import random


def main():
    st.markdown("# Graduate Admission Predictor")
    st.markdown("## Drop in The required Inputs and we will do the rest")
    st.markdown("### Submission for The Python Week")
    st.sidebar.header("What is this Project about?")
    st.sidebar.text(
        "It a Web app that would help the user in determining whether they will get admission in a Graduate Program or not.")
    st.sidebar.header("What tools where used to make this?")
    st.sidebar.text("The Model was made using a dataset from Kaggle along with using Kaggle notebooks to train the model. We made use of Sci-Kit learn in order to make our Linear Regression Model.")

    # part of our main method
    # taking the cgpa by giving in the range from 0 to 10
    cgpa = st.slider("Input Your CGPA", 0.0, 10.0)
    # taking the GRE by giving in the range from 0 to 340
    gre = st.slider("Input your GRE Score", 0, 340)
    # taking the TOEFL by giving in the range from 0 to 120
    toefl = st.slider("Input your TOEFL Score", 0, 120)
    # taking the input of whether or not a person has written a research paper
    research = st.slider(
        "Do You have Research Experience (0 = NO, 1 = YES)",
        0, 1,
    )
    # taking the rating of the university a person wishes to get in
    uni_rating = st.slider(
        "Rating of the University you wish to get in on a Scale 1-5", 1, 5)

    if st.button('Predict'):  # making and printing our prediction
        result = random.randint(0, 2)
        updated_res = result
        st.success(
            'The Probability of getting admission is {}'.format(updated_res)
        )

    ...


if __name__ == '__main__':
    main()
