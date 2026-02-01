import streamlit as st
import time
import csv
import os
from datetime import datetime, timedelta

if 'running' not in st.session_state:
    st.session_state.running = False
if 'phase' not in st.session_state:
    st.session_state.phase = "WORK"
if 'count' not in st.session_state:
    st.session_state.count = 0
if 'total_study_sec' not in st.session_state:
    st.session_state.total_study_sec = 0
if 'total_rest_sec' not in st.session_state:
    st.session_state.total_rest_sec = 0
if 'start_dt' not in st.session_state:
    st.session_state.start_dt = None
if 'last_stop_time' not in st.session_state:
    st.session_state.last_stop_time = None

def nihonzikan():
    return datetime.utcnow() + timedelta(hours=9)

def save_log(study_sec, rest_sec):
    if st.session_state.start_dt is None:
        return
    syuryo_dt = nihonzikan()
    file_path = 'Pages/data/rireki.csv'
    file_ari = os.path.isfile(file_path)
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
            "勉強時間": f"{study_sec // 60}",
            "休憩時間": f"{rest_sec // 60}"
        })
    st.session_state.count = 0
    st.session_state.total_study_sec = 0
    st.session_state.total_rest_sec = 0
    st.session_state.start_dt = None
    st.session_state.last_stop_time = None

st.markdown("""
    <style>
        .stApp { background-color: #0d1616; color: #d0d0d0; }
        .main-title { font-family: 'Times New Roman', serif; font-size: 3.5rem; text-align: center; letter-spacing: 0.2em; color: #8fbcb3; margin-bottom: 0px; text-shadow: 0 0 15px rgba(143, 188, 179, 0.4); }
        .sub-title { text-align: center; font-size: 0.9rem; color: #5a7a7a; margin-top: -10px; margin-bottom: 40px; letter-spacing: 0.15em; }
        .card { background-color: #152222; border-radius: 20px; padding: 25px; box-shadow: 0 8px 20px rgba(0,0,0,0.4); border: 1px solid #1f3333; margin-bottom: 20px; }
        div.stButton > button { background: linear-gradient(90deg, #5c9c8f 0%, #4a8a7f 100%); color: white; border-radius: 25px; border: none; padding: 12px 24px; font-weight: bold; font-size: 16px; box-shadow: 0 4px 15px rgba(92, 156, 143, 0.3); transition: 0.3s; width: 100%; }
        div.stButton > button:hover { background: #ff6b6b; transform: scale(1.02); color: white; }
    </style>
""", unsafe_allow_html=True)

if not st.session_state.running and st.session_state.last_stop_time is not None:
    elapsed = (nihonzikan() - st.session_state.last_stop_time).total_seconds()
    if elapsed >= 5: #テスト用（本番は300） 
        s_final = st.session_state.total_study_sec + (st.session_state.count if st.session_state.phase == "WORK" else 0)
        r_final = st.session_state.total_rest_sec + (st.session_state.count if st.session_state.phase == "REST" else 0)
        save_log(s_final, r_final)
        st.rerun()

st.markdown("<h1 class='main-title'>ZENITH</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>PRECISION FOCUS SYSTEM</p>", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    work_min = st.slider("Work Time (min)", 1, 60, 25)
    st.markdown(f"<h2 style='margin:0; color:white;'>{work_min} <span style='font-size:1rem; color:#6a8a8a'>min</span></h2>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
with col2:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    rest_min = st.slider("Rest Time (min)", 1, 30, 5)
    st.markdown(f"<h2 style='margin:0; color:white;'>{rest_min} <span style='font-size:1rem; color:#6a8a8a'>min</span></h2>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

curr_s = st.session_state.total_study_sec + (st.session_state.count if st.session_state.phase == "WORK" else 0)
curr_r = st.session_state.total_rest_sec + (st.session_state.count if st.session_state.phase == "REST" else 0)
total_sec = work_min * 60 if st.session_state.phase == "WORK" else rest_min * 60
percent = min((st.session_state.count / total_sec) * 100, 100.0)
rem = max(total_sec - st.session_state.count, 0)
m, s = divmod(int(rem), 60)

p_color = "#8fbcb3" if st.session_state.phase == "WORK" else "#5c9c8f"
p_label = "FOCUSING" if st.session_state.phase == "WORK" else "BREAKING"

st.markdown(f"""
    <div style="text-align:center; margin-bottom:30px;">
        <div style="color:#5a7a7a; font-size: 0.85rem; margin-bottom: 15px; letter-spacing: 0.1em;">
            Study: {curr_s // 60}m / Rest: {curr_r // 60}m
        </div>
        <div style="width: 200px; height: 200px; border-radius: 50%; 
            background: conic-gradient({p_color} {percent * 3.6}deg, #1a2a2a 0deg); 
            margin: 0 auto; display: flex; align-items: center; justify-content: center;
            box-shadow: 0 0 30px rgba(143, 188, 179, 0.2);">
            <div style="width: 170px; height: 170px; border-radius: 50%; background: #0d1616; 
                display: flex; flex-direction: column; align-items: center; justify-content: center;">
                <div style="font-size: 36px; font-weight: bold; color: #d0d0d0; font-family: 'Courier New', monospace;">
                    {m:02d}:{s:02d}
                </div>
                <div style="font-size: 11px; color: #5a7a7a; margin-top: 8px; letter-spacing: 0.2em;">{p_label}</div>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

_, center_col, _ = st.columns([1, 2, 1])
with center_col:
    if not st.session_state.running:
        if st.button("START FOCUS"):
            st.session_state.running = True
            st.session_state.last_stop_time = None
            if st.session_state.count == 0 and st.session_state.total_study_sec == 0:
                st.session_state.start_dt = nihonzikan()
            st.rerun()
    else:
        if st.button("STOP TIMER"):
            st.session_state.running = False
            st.session_state.last_stop_time = nihonzikan()
            st.rerun()
    
    st.write("") 
    if st.button("RESET SYSTEM"):
        st.session_state.running = False
        st.session_state.count = 0
        st.session_state.total_study_sec = 0
        st.session_state.total_rest_sec = 0
        st.session_state.phase = "WORK"
        st.session_state.start_dt = None
        st.session_state.last_stop_time = None
        st.rerun()

if st.session_state.running:
    if st.session_state.count < total_sec:
        time.sleep(1)
        st.session_state.count += 60 #テスト用（本番は１）
        st.rerun()
    else:
        if st.session_state.phase == "WORK":
            st.session_state.total_study_sec += st.session_state.count
            st.session_state.phase = "REST"
        else:
            st.session_state.total_rest_sec += st.session_state.count
            st.session_state.phase = "WORK"
        st.session_state.count = 0
        st.rerun()

if not st.session_state.running and st.session_state.last_stop_time is not None:
    time.sleep(10)
    st.rerun()

st.markdown("<h3 style='color:#8fbcb3; text-align:center; margin-top:40px; letter-spacing:0.2em;'>LOG DATA</h3>", unsafe_allow_html=True)
if os.path.isfile('rireki.csv'):
    with open('rireki.csv', 'r', encoding='utf-8-sig') as f:
        reader = list(csv.DictReader(f))
        if reader:
            cols = st.columns([0.5, 0.7, 0.5, 0.5, 2, 1, 1])
            headers = ["No", "年", "月", "日", "時刻", "勉強", "休憩"]
            for i, h in enumerate(headers): 
                cols[i].markdown(f"<p style='color:#5a7a7a; font-size:0.75rem; font-weight:bold;'>{h}</p>", unsafe_allow_html=True)
            for row in reversed(reader):
                c = st.columns([0.5, 0.7, 0.5, 0.5, 2, 1, 1])
                c[0].write(row["No"]); c[1].write(row["年"]); c[2].write(row["月"])
                c[3].write(row["日"]); c[4].write(row["時刻"])
                c[5].write(row["勉強時間"]); c[6].write(row["休憩時間"])