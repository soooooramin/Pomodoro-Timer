from turtle import color
import streamlit as st
import time
import numpy as np
import pandas as pd
import datetime as dt

dt_now = dt.datetime.now()
df = pd.read_csv('Pages/data/rireki.csv')

st.markdown(f"""
        <style>
        .stApp {{
            background-color: {'#0b4137'};
        }}
        </style>
        """, unsafe_allow_html=True)

st.set_page_config(
    page_title="Evaluation Page",
    page_icon="📖",
)

st.write("# Evaluation Page 📖")

st.markdown("""
            This is a evaluation page for the Pomodoro application.
            Here you can find various evaluation metrics and results.
            """) 


#ソート表示部分
col1, col2 = st.columns(2)
with col1:
    sel_year = st.selectbox("Select Year", options=sorted(df['年'].unique(), reverse=True))
with col2:
    available_months = sorted(df[df['年'] == sel_year]['月'].unique())
    sel_month = st.selectbox("Select Month", options=available_months)

btn = st.button("Show Monthly Studying Time Chart")

chart_placeholder = st.empty()

if btn:
    target_year = sel_year
    target_month = sel_month
    display_title = f"{target_year} Year {target_month} Month (Selected)"
else:
    target_year = dt_now.year
    target_month = dt_now.month
    display_title = f"{target_year} Year {target_month} Month (Current)"

df_filtered = df[(df["年"] == target_year) & (df["月"] == target_month)]
df_sum = df_filtered.groupby('日')[['勉強時間']].sum()

with chart_placeholder.container():
    st.markdown(f"### {display_title}'s Studying Time Chart 📊")
    if not df_sum.empty:
        st.bar_chart(df_sum)
    else:
        st.info("データが見つかりませんでした。")

col3, col4, = st.columns(2)
with col3:
    if st.button("Show Summary"):
        total_study_time = df_filtered['勉強時間'].sum()
        st.metric("Total Studying Time (m)", f"{total_study_time}minutes")

        avg_study_time = df_filtered['勉強時間'].mean()
        st.metric("Average Daily Studying Time (m)", f"{avg_study_time:.2f}minutes")

        total_rest_time = df_filtered['休憩時間'].sum()
        st.metric("Total Rest Time (m)", f"{total_rest_time}minutes")

with col4:
    if st.button("Show All Data"):
        st.markdown("### All Data 📊")
        st.dataframe(
            df,
            column_config={
                "No": "記入回数",
                "年": "年",
                "月": "月",
                "日":"日付",
                "勉強時間": "勉強時間 (m)",
                "休憩時間": "休憩時間 (m)"
            },
            hide_index=True, 
        )



