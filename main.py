# requirements: streamlit, requests, pandas
import streamlit as st
import requests
import pandas as pd
from urllib.parse import urlencode
from datetime import datetime
import pytz

# 1. Spotify App 정보
client_id = "YOUR_CLIENT_ID"
client_secret = "YOUR_CLIENT_SECRET"
redirect_uri = "http://localhost:8501"  # Streamlit 로컬 실행 기준
scope = "user-read-recently-played"

# 2. 인증 URL 생성
auth_url = "https://accounts.spotify.com/authorize?" + urlencode({
    "client_id": client_id,
    "response_type": "code",
    "redirect_uri": redirect_uri,
    "scope": scope
})

st.title("🎧 Spotify 청취 시간대 분석")
st.markdown(f"[👉 Spotify 로그인]({auth_url}) 해서 최근 청취 기록을 가져오세요.")

# 3. 사용자 인증 후 반환된 code 처리
code = st.experimental_get_query_params().get("code", [None])[0]

if code:
    # 4. 토큰 요청
    token_url = "https://accounts.spotify.com/api/token"
    response = requests.post(token_url, data={
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": redirect_uri,
        "client_id": client_id,
        "client_secret": client_secret
    })
    token_data = response.json()
    access_token = token_data.get("access_token")

    if access_token:
        # 5. 최근 청취 데이터 가져오기
        headers = {"Authorization": f"Bearer {access_token}"}
        res = requests.get("https://api.spotify.com/v1/me/player/recently-played?limit=50", headers=headers)
        items = res.json()["items"]

        # 6. 시간 정보 파싱
        times = []
        for item in items:
            played_at = item["played_at"]
            dt = datetime.fromisoformat(played_at.replace("Z", "+00:00"))
            dt_kst = dt.astimezone(pytz.timezone("Asia/Seoul"))  # 한국 시간 기준
            times.append({"hour": dt_kst.hour, "weekday": dt_kst.strftime('%A')})

        df = pd.DataFrame(times)
        st.subheader("📊 청취 시간대 분포")
        st.bar_chart(df['hour'].value_counts().sort_index())
        st.bar_chart(df['weekday'].value_counts())
