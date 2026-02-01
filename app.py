import streamlit as st
import time
import csv
import os
from datetime import datetime, timedelta

# --- セッションステートの初期化 ---
if 'running' not in st.session_state:
    st.session_state.running = False # タイマーが動いているか
if 'phase' not in st.session_state:
    st.session_state.phase = "WORK" # 現在のモード
if 'count' not in st.session_state:
    st.session_state.count = 0      # タイマーの終了のためのカウント
if 'total_study_sec' not in st.session_state:
    st.session_state.total_study_sec = 0 # 総集中時間
if 'total_rest_sec' not in st.session_state:
    st.session_state.total_rest_sec = 0 # 総休憩時間
if 'start_dt' not in st.session_state:
    st.session_state.start_dt = None # 開始時間
if 'last_stop_time' not in st.session_state:
    st.session_state.last_stop_time = None # 停止時間


def nihonzikan():
    return datetime.utcnow() + timedelta(hours=9) # 日本時間を取得

def save_log(study_sec, rest_sec):
    # 開始時間が何らかの理由で取れていない場合は現在時刻を仮定（エラー回避）
    if st.session_state.start_dt is None:
        st.session_state.start_dt = nihonzikan()

    syuryo_dt = nihonzikan()
    file_path = 'rireki.csv'
    file_ari = os.path.isfile(file_path)
    no_count = 1
    
    # Noの計算
    if file_ari:
        with open(file_path, 'r', encoding='utf-8-sig') as f:
            try:
                # ヘッダーがあるため行数をカウント
                no_count = sum(1 for line in f)
            except:
                no_count = 1

    with open(file_path, 'a', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=["No", "年", "月", "日", "時刻", "勉強時間", "休憩時間"])
        if not file_ari: 
            writer.writeheader()
        
        writer.writerow({
            "No": no_count,
            "年": st.session_state.start_dt.strftime('%Y'),
            "月": st.session_state.start_dt.strftime('%m'),
            "日": st.session_state.start_dt.strftime('%d'),
            "時刻": f"{st.session_state.start_dt.strftime('%H:%M')}～{syuryo_dt.strftime('%H:%M')}",
            "勉強時間": f"{study_sec // 60}分",
            "休憩時間": f"{rest_sec // 60}分"
        })
    
    # 保存後に値をリセット
    st.session_state.count = 0
    st.session_state.total_study_sec = 0
    st.session_state.total_rest_sec = 0
    st.session_state.start_dt = None
    st.session_state.last_stop_time = None


st.set_page_config(layout="centered",page_title="Pomodo-ro Timer")

# --- CSS設定（元のまま） ---
st.markdown("""
    <style>
        /*背景色と文字色*/
        .stApp{
            background-color: #0d1616;
            color: #d0d0d0;  
        }

        /* 一番上に詰める */
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
            
        .tab-container{
            display: flex !important;
            flex-direction: row !important;
            background-color: #121b1b;
            border-radius: 25px;
            
            width : 600px;
            margin: 0 auto 20px auto;
            border: 1px solid #1f3333;    
            
        }
            
        .tab-item {
            flex: 1;                          /* 1:1 で幅を分け合う */
            display: flex;
            align-items: center;
            justify-content: center;
            height: 100%;
            border-radius: 25px;
            font-weight: bold;
            transition: all 0.4s ease;        /* アニメーション */
            cursor: default;
        }

        /* アクティブな時 */
        .tab-active {
            background: linear-gradient(135deg, #5c9c8f 0%, #4a8a7f 100%);
            color: white;
            box-shadow: 0 2px 10px rgba(92, 156, 143, 0.3);
        }
        
        /* 非アクティブな時 */
        .tab-inactive {
            background-color: transparent;
            color: #4a6666;
        }
            
        
            
        /* スライダーを入れるとこ */
        .card{
            background-color: #152222;    
            border-radius: 20px;
            padding: 20;
            box-shadow: 0 4px 15px rgba(0,0,0,0.3);
            border: 1px aolid ##1f3333;
        }
            
        /* スライダーの丸 */
        div[data-baseweb="slider"] div[role="slider"] {
            background-color: #fff !important;
            border: 2px solid #75bfae;
            height: 24px !important;
            width: 24px !important;
        }
            
        /* スライダーのバー */
        div[data-baseweb="slider"] div[data-testid="stTickBar"] {
             background-color: #1f3333 !important; 
        }

        div.stButton > button {
            background: linear-gradient(90deg, #5c9c8f 0%, #4a8a7f 100%);
            color: white;
            border-radius: 20px;  
            border: none;
            padding: 10px 24px;
            font-weight: bold;
            font-size: 18px;
            box-shadow: 0 0 15px rgba(92, 156, 143, 0.4);
            transition: 0.3s;
            width: 100%; 
        }
            
        /*ボタンにカーソルを合わせると*/
        div.stButton > button:hover { 
            background: linear-gradient(90deg, #6abcb0 0%, #5caea2 100%);
            color: white;
            box-shadow: 0 0 25px rgba(92, 156, 143, 0.6);
            transform: scale(1.02);
        }
        
        
    </style>
""", unsafe_allow_html=True)

def get_tabs_html(mode="work"):
    if mode == "work":
        work_class = "tab-item tab-active"
        rest_class = "tab-item tab-inactive"
    else:
        work_class = "tab-item tab-inactive"
        rest_class = "tab-item tab-active"
    
    return f"""
    <div class="tab-container">
        <div class="{work_class}">集中</div>
        <div class="{rest_class}">休憩</div>
    </div>
    """

# 円形プログレスバー
def get_circular_progress_html(percent, label, status):
    bg_color = "#0d1616"
    bar_color = "#1f3333"
    inactive_color = "#75bfae"

    return f"""
    <div style="width: 260px; height: 260px; margin: 0 auto; position: relative;">
        <div style="
            width: 260px; height: 260px; border-radius: 50%;
            background: conic-gradient({bar_color} {percent * 3.6}deg, {inactive_color} 0deg);
            display: flex; align-items: center; justify-content: center;
            box-shadow: 0 0 20px rgba(117, 191, 174, 0.1);
        ">
            <div style="
                width: 240px; height: 240px; border-radius: 50%; background: {bg_color};
                display: flex; flex-direction: column; align-items: center; justify-content: center;
                font-family: 'Times New Roman' , serif; color: #fff;
            ">
                <div style="font-size: 4rem; font-weight: nomal; text-shadow: 0 0 10px rgba(255,255,255,0.2)">{label}</div>
                <div style="font-size: 1rem; color: #6a8a8a; margin-top: -5px; letter-spacing: 0.1em;">{status}</div>
            </div>
        </div>
    </div>
    """

st.markdown("<h1 class='main-title'>ZENITH</h1>", unsafe_allow_html=True)

# --- 保存処理のロジック修正 ---
# 停止ボタンが押された（runningがFalseになり、かつlast_stop_timeが入っている）場合
if not st.session_state.running and st.session_state.last_stop_time is not None:
    # 5秒ルールの撤廃：停止したら即保存するように修正
    # 現在のフェーズの経過時間をカウントに加算するかは、ループの抜け方によりますが、
    # 簡易的に累積時間を使って保存します。
    s_final = st.session_state.total_study_sec
    r_final = st.session_state.total_rest_sec
    
    # 集中時間、休憩時間を取得し記録
    save_log(s_final, r_final)
    
    # 再読み込みをして初期状態に戻す
    # st.rerun() # ここでrerunするとsuccessメッセージが一瞬で消えるためコメントアウトしても良い

status = ""

#切り替え表記
tab_placeholder = st.empty()
#初期表示
tab_placeholder.markdown(get_tabs_html("work"),unsafe_allow_html=True)

st.write("")

# タイマー表示用の場所を確保
timer_placeholder = st.empty()
# 初期表示
timer_placeholder.markdown(get_circular_progress_html(0,"00:00"," "),unsafe_allow_html=True)

st.write()


# 時間の設定
col1, col2 = st.columns(2)
with col1:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    work_placeholder = st.empty()
    work_min = st.slider("", 1, 60, 25)
    work_placeholder.markdown(f"<h2 style='margin:0; font-family: 'Times New Roman',serif; color:white;'>{work_min} <span style='font-size:1rem; color:#6a8a8a'>min</span></h2>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    rest_placeholder = st.empty()
    rest_min = st.slider("", 1, 30, 5)
    rest_placeholder.markdown(f"<h2 style='margin:0; font-family: 'Times New Roman', serif; color:white;'>{rest_min} <span style='font-size:1rem; color:#6a8a8a'>min</span></h2>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# 3つのカラムを作り、真ん中(center_col)にボタンを置くことで中央寄せにする
left_col, center_col, right_col = st.columns([1, 2, 1])

with center_col:
    # use_container_width=True でカラム幅いっぱいにボタンを広げる
    # STARTボタン
    if st.button("START FOCUS", use_container_width=True):
        st.session_state.running = True
        st.session_state.last_stop_time = None
        st.session_state.start_dt = nihonzikan() # 開始時間を取得
        st.rerun() # 状態を反映させるためにリロード
    
    # STOPボタン
    if st.button("STOP FORCUS", use_container_width=True):
        st.session_state.running = False
        st.session_state.last_stop_time = nihonzikan() #終了時間を取得
        st.rerun() # 状態を反映させて保存処理（スクリプト冒頭）へ

# --- タイマー実行部分の修正 ---
# start_clicked フラグではなく、session_state.running を監視する
if st.session_state.running:

    # 無限ループさせてWork/Restを繰り返す
    # 停止ボタン(st.session_state.running)の変化を検知できるように条件変更
    while st.session_state.running:
    
        status = "💻 Working..."
        st.session_state.phase = "WORK"
        total_seconds = work_min * 60
        tab_placeholder.markdown(get_tabs_html("work"),unsafe_allow_html=True)
        
        for i in range(total_seconds + 1):
            if not st.session_state.running: break # ストップボタン対策

            # 経過時間の計算
            percent = (i / total_seconds) * 100
            remaining_seconds = total_seconds - i
            
            # 形式を変換 （mm:ss)
            mins, secs = divmod(remaining_seconds, 60)
            time_label = f"{mins:02d}:{secs:02d}"
            
            # HTMLを生成して表示更新
            timer_placeholder.markdown(
                get_circular_progress_html(percent, time_label, status), 
                unsafe_allow_html=True
            )
            time.sleep(0.01) # 1秒待つ

        # 完了または中断時の計算
        st.session_state.count = total_seconds
        st.session_state.total_study_sec += st.session_state.count
        
        if not st.session_state.running: break # ストップされていたらループを抜ける

        # --- 休憩モードへ ---

        tab_placeholder.markdown(get_tabs_html("rest"),unsafe_allow_html=True)

        
        status = "☕ Break Time!"
        st.session_state.phase = "REST"
        total_seconds = rest_min * 60
        
        for i in range(total_seconds + 1):
            if not st.session_state.running: break # ストップボタン対策

            percent = (i / total_seconds) * 100
            remaining_seconds = total_seconds - i
            
            mins, secs = divmod(remaining_seconds, 60)
            time_label = f"{mins:02d}:{secs:02d}"
            
            timer_placeholder.markdown(
                get_circular_progress_html(percent, time_label,status), 
                unsafe_allow_html=True
            )
            time.sleep(0.01)
        
        st.session_state.count = total_seconds
        st.session_state.total_rest_sec += st.session_state.count

        if not st.session_state.running: break

        # timer_placeholder.markdown(get_circular_progress_html(0,"00:00","⏰ All Done!"),unsafe_allow_html=True)
    

# 停止状態時の表示
if not st.session_state.running:
    timer_placeholder.markdown(get_circular_progress_html(0,"00:00"," "),unsafe_allow_html=True)

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
                c[0].write(row.get("No"))
                c[1].write(row.get("年"))
                c[2].write(row.get("月"))
                c[3].write(row.get("日"))
                c[4].write(row.get("時刻"))
                c[5].write(row.get("勉強時間"))
                c[6].write(row.get("休憩時間"))