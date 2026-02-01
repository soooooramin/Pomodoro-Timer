import streamlit as st
import time
import numpy as np
import pandas as pd
df = pd.read_csv("(ここにURLを入力)")

st.set_page_config(
    page_title="Evaluation Page",
    page_icon="📖",
)

st.write("# Evaluation Page 📖")

st.markdown("""
            This is a evaluation page for the Streamlit application.
            Here you can find various evaluation metrics and results.
            """)

