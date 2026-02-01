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
    
    # --- 1. 作業時間のカウントダウン ---
    status_text.info("💻 Working...")
    total_seconds = work_min * 60
    
    for i in range(total_seconds + 1):
        # 経過時間の計算
        percent = (i / total_seconds) * 100
        remaining_seconds = total_seconds - i
        
        # "分:秒" の形式に変換 (例 24:59)
        mins, secs = divmod(remaining_seconds, 60)
        time_label = f"{mins:02d}:{secs:02d}"
        
        # HTMLを生成して表示更新
        timer_placeholder.markdown(
            get_circular_progress_html(percent, time_label), 
            unsafe_allow_html=True
        )
        time.sleep(0.01) # 1秒待つ（テスト時は 0.01 などにすると早送りできます）

    # --- 2. 休憩時間のカウントダウン ---
    status_text.success("☕ Break Time!")
    total_seconds = rest_min * 60
    
    for i in range(total_seconds + 1):
        percent = (i / total_seconds) * 100
        remaining_seconds = total_seconds - i
        
        mins, secs = divmod(remaining_seconds, 60)
        time_label = f"{mins:02d}:{secs:02d}"
        
        # 色を変えたい場合は HTML関数の #4CAF50 を別の色コードに変えてみてください
        timer_placeholder.markdown(
            get_circular_progress_html(percent, time_label), 
            unsafe_allow_html=True
        )
        time.sleep(0.01)

    status_text.warning("⏰ All Done!")

if st.button("Timer Stop"):
    timer_placeholder.markdown(get_circular_progress_html(0,"00:00"),unsafe_allow_html=True)