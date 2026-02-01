import streamlit as st
import csv
import numpy as np
import pandas as pd

st.set_page_config(
    page_title="Unit Management Page",
    page_icon="💯",
)

df = pd.read_csv('Pages/data/units.csv')

st.write("# Unit Management Page 💯")
st.markdown("This is a unit management page where you can track your class attendance and add new units.")

col1, col2, = st.columns([3, 1])
with col1:
    sel_unit = st.selectbox("Select Unit", options=sorted(df['Unit Name'].unique(), reverse=True))
with col2:
    if st.button("Attend Class"):
        df.loc[df['Unit Name'] == sel_unit, 'Completed Classes'] += 1
        df['percentage'] = (df['Completed Classes'] / df['Number of Classes'] * 100).round(2)
        df.to_csv('Pages/data/units.csv', index=False)


tab1, tab2 = st.tabs(["Add New Unit", "Unit attendance counter"])

with tab1:
    st.subheader("Add New Unit")

    col1, col2, col3 = st.columns(3)
    with col1:
        unit_name = st.text_input('Unit Name')
    with col2:
        num_classes = st.number_input('Number of classes', min_value=1, max_value=100, step=1)
    with col3:
        if st.button("Add Unit"):
            st.success(f'Unit "{unit_name}" with {num_classes} classes added successfully!')
            with open('Pages/data/units.csv', 'a') as f:
                writer = csv.writer(f)
                writer.writerow([unit_name, num_classes, 0, 0])
    
with tab2:
    st.dataframe(
        df,
        column_config={
            "Unit Name": "Unit Name",
            "Number of Classes": "Number of Classes",
            "Completed Classes": "Completed Classes",
            "percentage": "Completion Percentage",
        },
        use_container_width=True,
        )
