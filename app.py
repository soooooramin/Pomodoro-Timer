import streamlit as st
import time

st.markdown("""
    <style>
        .stApp{
            background-color: #0d1616;
            color: #d0d0d0;  /*背景色と文字色*/
        }

        .block-container{ 
            padding-top: 2rem;
        }
            
        .main-title{
            font-family: 'Times New Roman', serif;
            font-size: 3rem;
            text-align: center;
            letter-spacing: 0.2em;
            color: #8fbcb3;
            margin-bottom: 0px;
            text-shadow: 0 0 10px rgba(143, 188, 179, 0.3);
        }
            
        .sub-title{
            text-align: center;
            font-size: 0.9rem;
            color: #5a7a7a;
            margin-top: -10px;
            margin-bottom: 30px;
            letter-spacing: 0.1em;    
        }
            
        .card{
            background-color: #152222;    
            border-radius: 20px;
            padding: 20;
            boc-shadow: 0 4px 15px rgba(0,0,0,0.3);
            border: 1px aolid ##1f3333;
        }

        div.stButton > button {
            background: linear-gradient(90deg, #5c9c8f 0%, #4a8a7f 100%);
            color: white;
            border-radius: 20px;       /* 角丸にする */
            border: none;
            padding: 10px 24px;
            font-weight: bold;
            font-size: 18px;
            box-shadow: 0 0 15px rgba(92, 156, 143, 0.4);
            transition: 0.3s;
            width: 100%; /* カラム幅いっぱいに広げる */
        }
            
        div.stButton > button:hover { /*ボタンにカーソルを合わせると*/
            background-color: #ff6b6b;
            transform: scale(1.02);
        }
    </style>
""", unsafe_allow_html=True)

# 円形プログレスバーのHTMLを生成する関数
# 引数を追加：percent（グラフの進捗）と label（真ん中に表示する文字）
def get_circular_progress_html(percent, label, status):
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
                <div style="font-size: 12px; color: #666;">{status}</div>
            </div>
        </div>
    </div>
    """

st.markdown("<h1 class='main-title'style='text-align: center;'>ZENITH</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'style='text-align: center;'>ZENITH</p>", unsafe_allow_html=True)

# status_text = st.empty()
# status_text.info("")
status = ""

# タイマー表示用の場所を確保
timer_placeholder = st.empty()

timer_placeholder.markdown(get_circular_progress_html(0,"00:00"," "),unsafe_allow_html=True)




# 時間の設定
col1, col2 = st.columns(2)
with col1:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    work_placeholder = st.empty()
    work_min = st.slider("Work Time (min)", 1, 60, 25)
    work_placeholder.markdown(f"<h2 style='margin:0; color:white;'>{work_min} <span style='font-size:1rem; color:#6a8a8a'>min</span></h2>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    rest_placeholder = st.empty()
    rest_min = st.slider("Rest Time (min)", 1, 30, 5)
    rest_placeholder.markdown(f"<h2 style='margin:0; color:white;'>{rest_min} <span style='font-size:1rem; color:#6a8a8a'>min</span></h2>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# 3つのカラムを作り、真ん中(center_col)にボタンを置くことで中央寄せにする
left_col, center_col, right_col = st.columns([1, 2, 1])

start_clicked = False
with center_col:
    # use_container_width=True でカラム幅いっぱいにボタンを広げる
    if st.button("START FOCUS", use_container_width=True):
        start_clicked = True
    if st.button("timer stop", use_container_width=True):
        stop_clicked = True

if start_clicked:
    
    # --- 1. 作業時間のカウントダウン ---
    # status_text.info("💻 Working...")
    status = "💻 Working..."
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
            get_circular_progress_html(percent, time_label, status), 
            unsafe_allow_html=True
        )
        time.sleep(0.01) # 1秒待つ（テスト時は 0.01 などにすると早送りできます）

    # --- 2. 休憩時間のカウントダウン ---
    # status_text.success("☕ Break Time!")
    status = "☕ Break Time!"
    total_seconds = rest_min * 60
    
    for i in range(total_seconds + 1):
        percent = (i / total_seconds) * 100
        remaining_seconds = total_seconds - i
        
        mins, secs = divmod(remaining_seconds, 60)
        time_label = f"{mins:02d}:{secs:02d}"
        
        # 色を変えたい場合は HTML関数の #4CAF50 を別の色コードに変えてみてください
        timer_placeholder.markdown(
            get_circular_progress_html(percent, time_label,status), 
            unsafe_allow_html=True
        )
        time.sleep(0.01)

    # status_text.warning("⏰ All Done!")
    timer_placeholder.markdown(get_circular_progress_html(0,"00:00","⏰ All Done!"),unsafe_allow_html=True)

if start_clicked:
    timer_placeholder.markdown(get_circular_progress_html(0,"00:00"," "),unsafe_allow_html=True)