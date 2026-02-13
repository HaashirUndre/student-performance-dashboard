import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Student Performance Dashboard",
    layout="wide"
)

st.title("Student Performance Dashboard")
uploaded_file = st.file_uploader("Upload student marks CSV", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    df["Total"] = df[["Math", "Science", "English"]].sum(axis=1)
    df["Percentage"] = df["Total"] / 3

    def grade(p):
        if p >= 90: return "A+"
        elif p >= 80: return "A"
        elif p >= 70: return "B"
        elif p >= 60: return "C"
        else: return "D"

    df["Grade"] = df["Percentage"].apply(grade)

    st.subheader("Student Data")
    st.dataframe(df, use_container_width=True)

    topper = df.loc[df["Percentage"].idxmax()]
    st.success(f"Topper: {topper['Name']} ({topper['Percentage']:.2f}%)")

    subject_avg = df[["Math", "Science", "English"]].mean()

    fig1, ax1 = plt.subplots(figsize=(4, 3))
    ax1.bar(subject_avg.index, subject_avg.values)
    ax1.set_title("Subject-wise Average Marks")

    grade_counts = df["Grade"].value_counts()

    fig2, ax2 = plt.subplots(figsize=(4, 3))
    ax2.pie(
        grade_counts.values,
        labels=grade_counts.index,
        autopct="%1.1f%%",
        startangle=90
    )
    ax2.set_title("Grade Distribution")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Subject-wise Averages:")
        st.pyplot(fig1, use_container_width=True)

    with col2:
        st.subheader("Grade Distribution:")
        st.pyplot(fig2, use_container_width=True)