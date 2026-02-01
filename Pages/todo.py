import streamlit as st

# セッション状態を共
if 'todo_items' not in st.session_state: st.session_state.todo_items = []

st.markdown("""
    <style>
        .stApp { background-color: #0d1616; color: #d0d0d0; }
        .main-title { font-family: 'Times New Roman', serif; font-size: 3.5rem; text-align: center; letter-spacing: 0.2em; color: #8fbcb3; margin-bottom: 0px; text-shadow: 0 0 15px rgba(143, 188, 179, 0.4); }
        .sub-title { text-align: center; font-size: 0.9rem; color: #5a7a7a; margin-top: -10px; margin-bottom: 40px; letter-spacing: 0.15em; }
        .card { background-color: #152222; border-radius: 20px; padding: 25px; box-shadow: 0 8px 20px rgba(0,0,0,0.4); border: 1px solid #1f3333; margin-bottom: 20px; }
        div.stButton > button { background: linear-gradient(90deg, #5c9c8f 0%, #4a8a7f 100%); color: white; border-radius: 25px; border: none; padding: 12px 24px; font-weight: bold; width: 100%; transition: 0.3s; margin-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>TODO LIST</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>EVALUATION PAGE</p>", unsafe_allow_html=True)

with st.form("new_task_form", clear_on_submit=True):
    col_in, col_btn = st.columns([0.85, 0.15])
    new_task = col_in.text_input("挑戦を記録", placeholder="例: 税理士試験 過去問10ページ")
    if col_btn.form_submit_button("ADD"):
        if new_task:
            st.session_state.todo_items.append({"task": new_task, "done": False})
            st.rerun()

if not st.session_state.todo_items:
    st.info("現在、挑戦中のタスクはありません。")
else:
    for i, item in enumerate(st.session_state.todo_items):
        st.markdown("<div class='card' style='padding:15px; margin-bottom:10px;'>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns([0.1, 0.8, 0.1])
        done = c1.checkbox("", value=item["done"], key=f"t_{i}")
        if done != item["done"]:
            st.session_state.todo_items[i]["done"] = done
            st.rerun()
        style = "text-decoration: line-through; color: #5a7a7a;" if item["done"] else "color: #d0d0d0;"
        c2.markdown(f"<p style='margin: 5px 0; {style}'>{item['task']}</p>", unsafe_allow_html=True)
        if c3.button("DEL", key=f"d_{i}"):
            st.session_state.todo_items.pop(i); st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)