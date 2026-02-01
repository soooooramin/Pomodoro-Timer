import streamlit as st
import time

# 円形プログレスバーのHTMLを生成する関数
# 引数を追加：percent（グラフの進捗）と label（真ん中に表示する文字）
def get_circular_progress_html(percent, label):
    return f"""
    <div style="width: 150px; height: 150px; margin: 0 auto; position: relative;">
        <div style="
            width: 150px; height: 150px; border-radius: 50%;
            background: conic-gradient(#4CAF50 {percent * 3.6}deg, #e0e0e0 0deg);
            display: flex; align-items: center; justify-content: center;
        ">
            <div style="
                width: 120px; height: 120px; border-radius: 50%; background: white;
                display: flex; flex-direction: column; align-items: center; justify-content: center;
                font-family: sans-serif; color: #333;
            ">
                <div style="font-size: 24px; font-weight: bold;">{label}</div>
                <div style="font-size: 12px; color: #666;">{int(percent)}%</div>
            </div>
        </div>
    </div>
    """


# タイマー表示用の場所を確保
status_text = st.empty()
timer_placeholder = st.empty()

timer_placeholder.markdown(get_circular_progress_html(0,"00:00"),unsafe_allow_html=True)


st.title("Circular Pomodoro Timer")

# 時間の設定
col1, col2 = st.columns(2)
with col1:
    work_min = st.slider("Work Time (min)", 1, 60, 25)
with col2:
    rest_min = st.slider("Rest Time (min)", 1, 30, 5)



if st.button("Start Timer"):
    
    for j in range(rest_time * 60):
        latest_iteration.text(f'Rest Time {rest_time * 60 - j}')
        bar.progress((rest_time * 60 - j) / (rest_time * 60))
        time.sleep(1)
