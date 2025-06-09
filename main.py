import streamlit as st
import requests
from urllib.parse import urlencode

# Spotify 앱 정보
client_id = "YOUR_CLIENT_ID"
client_secret = "YOUR_CLIENT_SECRET"
redirect_uri = "http://localhost:8501"
scope = "user-read-recently-played"

auth_url = "https://accounts.spotify.com/authorize?" + urlencode({
    "client_id": client_id,
    "response_type": "code",
    "redirect_uri": redirect_uri,
    "scope": scope
})

st.title("🎧 Spotify 청취 기록 분석기")
st.markdown(f"[👉 Spotify 로그인]({auth_url})")

# ✅ 최신 방식으로 query string 파싱
query = st.query_params
code = query["code"][0] if "code" in query else None

if code:
    st.success("✅ 인증 코드 수신 완료")
    # 토큰 요청 및 분석 코드 이어서 작성
