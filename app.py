import streamlit as st
# アプリケーションのタイトル
st.title('シンプルなX(旧Twitter)⾵アプリ')
# テキスト⼊⼒欄
post_content = st.text_input('あなたの投稿を⼊⼒してください:')
# 投稿ボタン
st.button('投稿する')