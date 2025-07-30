import streamlit as st
import os
import re

st.set_page_config(layout="wide")

st.title("달무티 게임")

# 리액트 앱이 빌드될 경로 (Streamlit 앱 기준 상대 경로)
# Streamlit Cloud에서는 GitHub 리포지토리의 루트가 작업 디렉토리가 됩니다.
# 따라서, 리액트 앱의 빌드 결과물인 'dist' 폴더가 Streamlit 앱과 같은 레벨에 있다고 가정합니다.
react_app_path = os.path.join(os.path.dirname(__file__), "dist", "index.html")

if os.path.exists(react_app_path):
    with open(react_app_path, "r", encoding="utf-8") as f:
        html_content = f.read()

    # 빌드된 리액트 앱의 자산 경로를 Streamlit이 접근할 수 있도록 수정
    # 예: src="./assets/index-xxxx.js" -> src="dist/assets/index-xxxx.js"
    # 예: href="./vite.svg" -> href="dist/vite.svg"
    html_content = re.sub(r'(src|href)="\./(.*?)"|'(src|href)="/(.*?)"'
                          , r'\1="dist/\2"'
                          , html_content)

    st.components.v1.html(html_content, height=800, scrolling=True)
else:
    st.error("리액트 앱 빌드 파일을 찾을 수 없습니다. 'yarn build'를 실행했는지 확인해주세요.")
    st.info(f"예상 경로: {react_app_path}")