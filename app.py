import streamlit as st
import time
import csv
import os
from datetime import datetime, timedelta

if 'running' not in st.session_state:
    st.session_state.running = False
if 'phase' not in st.session_state:
    st.session_state.phase = "WORK"  # WORK または REST
if 'count' not in st.session_state:
    st.session_state.count = 0
if 'start_dt' not in st.session_state:
    st.session_state.start_dt = None

def nihonzikan():
    return datetime.utcnow() + timedelta(hours=9)

st.title("Ultimate Smooth Pomodoro")

col1, col2 = st.columns(2)
with col1:
    work_min = st.slider("Work Time (min)", 1, 60, 25)
with col2:
    rest_min = st.slider("Rest Time (min)", 1, 30, 5)

# フェーズに応じた設定
total_sec = work_min * 60 if st.session_state.phase == "WORK" else rest_min * 60
percent = min((st.session_state.count / total_sec) * 100, 100.0)
rem = max(total_sec - st.session_state.count, 0)
m, s = divmod(rem, 60)

# 表示ラベルの設定
if st.session_state.running:
    status_label = "💻 Working..." if st.session_state.phase == "WORK" else "☕ Resting..."
else:
    status_label = "⏸ Paused" if st.session_state.count > 0 else "⏳ Ready"

# タイマーUIの表示
st.markdown(f"""
    <div id="timer-container" style="text-align:center; margin-bottom:20px;">
        <div style="font-family:sans-serif; color:#666; margin-bottom:10px;">{status_label}</div>
        <div style="
            width: 150px; height: 150px; border-radius: 50%;
            background: conic-gradient({'#4CAF50' if st.session_state.phase == "WORK" else '#2196F3'} {percent * 3.6}deg, #e0e0e0 0deg);
            margin: 0 auto; display: flex; align-items: center; justify-content: center;
        ">
            <div style="width: 120px; height: 120px; border-radius: 50%; background: white;
                display: flex; flex-direction: column; align-items: center; justify-content: center;
                font-family: sans-serif; color: #333;">
                <div style="font-size: 24px; font-weight: bold;">{m:02d}:{s:02d}</div>
                <div style="font-size: 12px; color: #666;">{int(percent)}%</div>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

# 操作ボタン
a_btn1, a_btn2 = st.columns(2)
with a_btn1:
    if st.session_state.running:
        if st.button("Timer Stop"):
            st.session_state.running = False
            st.rerun()
    else:
        if st.button("Start Timer"):
            st.session_state.running = True
            if st.session_state.count == 0 and st.session_state.phase == "WORK":
                st.session_state.start_dt = nihonzikan()
            st.rerun()

with a_btn2:
    if st.button("Reset"):
        st.session_state.running = False
        st.session_state.count = 0
        st.session_state.phase = "WORK"
        st.session_state.start_dt = None
        st.rerun()

# タイマー実行ロジック
if st.session_state.running:
    if st.session_state.count < total_sec:
        time.sleep(1)
        st.session_state.count += 60 # 本番用は + 1
        st.rerun()
    else:
        # フェーズ終了時の自動入れ替え処理
        if st.session_state.phase == "WORK":
            st.session_state.phase = "REST"
        else:
            st.session_state.phase = "WORK"
        
        st.session_state.count = 0
        st.rerun()

# 履歴保存条件の判定：ストップ中かつ5分（300秒）以上経過している場合
if not st.session_state.running and st.session_state.count >= 300:
    syuryo_dt = nihonzikan()
    file_path = 'rireki.csv'
    file_ari = os.path.isfile(file_path)
    
    # 履歴保存実行
    no_count = 1
    if file_ari:
        with open(file_path, 'r', encoding='utf-8-sig') as f:
            no_count = sum(1 for line in f)
    
    with open(file_path, 'a', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=["No", "年", "月", "日", "時刻", "勉強時間", "休憩時間"])
        if not file_ari: writer.writeheader()
        writer.writerow({
            "No": no_count,
            "年": st.session_state.start_dt.strftime('%Y'),
            "月": st.session_state.start_dt.strftime('%m'),
            "日": st.session_state.start_dt.strftime('%d'),
            "時刻": f"{st.session_state.start_dt.strftime('%H:%M')}～{syuryo_dt.strftime('%H:%M')}",
            "勉強時間": f"{st.session_state.count // 60}分",
            "休憩時間": f"{rest_min}分"
        })
    
    # 保存後にカウントをリセットして重複保存を防止
    st.session_state.count = 0
    st.session_state.start_dt = None
    st.success("5分以上の活動履歴を保存しました")
    st.rerun()

# 履歴表示セクション
st.write("---")
st.subheader("📊 学習履歴")
if os.path.isfile('rireki.csv'):
    with open('rireki.csv', 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        cols = st.columns([0.5, 0.7, 0.5, 0.5, 1.8, 1, 1]) 
        headers = ["No", "年", "月", "日", "時刻", "勉強", "休憩"]
        for i, h in enumerate(headers): cols[i].write(f"**{h}**")
        for row in reader:
            c = st.columns([0.5, 0.7, 0.5, 0.5, 1.8, 1, 1]) 
            c[0].write(row["No"]); c[1].write(row["年"]); c[2].write(row["月"])
            c[3].write(row["日"]); c[4].write(row["時刻"])
            c[5].write(row["勉強時間"]); c[6].write(row["休憩時間"])