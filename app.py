import streamlit as st
import time

'Starting a long computation...'

if 'current_seconds' not in st.session_state:
    st.session_state.current_seconds = 0

time_set = st.slider("Set time (minutes)", 1, 60, 25)
rest_time = st.slider("Set rest time (minutes)", 1, 30, 5)

latest_iteration = st.empty()
bar = st.progress(0)

if st.button("Start Timer"):
    for i in range(st.session_state.current_seconds, time_set * 60):
        st.session_state.current_seconds = i
        latest_iteration.text(f'Iteration {time_set * 60 - i}')
        bar.progress((time_set * 60 - i) / (time_set * 60))
        time.sleep(1)
    
    for j in range(rest_time * 60):
        latest_iteration.text(f'Rest Time {rest_time * 60 - j}')
        bar.progress((rest_time * 60 - j) / (rest_time * 60))
        time.sleep(1)

    st.session_state.current_seconds = 0