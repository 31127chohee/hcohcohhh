import streamlit as st
from pytrends.request import TrendReq
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.title("🎧 구글 트렌드로 알아보는 음악 검색 시간대")

# 사용자 키워드 입력
keywords = st.text_input("분석할 키워드를 쉼표로 입력하세요 (예: 멜론, 유튜브 뮤직, NewJeans)", "멜론, 유튜브 뮤직, NewJeans")
keywords = [k.strip() for k in keywords.split(",")]

# 트렌드 데이터 수집
pytrends = TrendReq(hl='ko', tz=540)
pytrends.build_payload(keywords, timeframe='now 7-d', geo='KR')
df = pytrends.interest_over_time().reset_index()
df['hour'] = df['date'].dt.hour
hourly_avg = df.groupby('hour')[keywords].mean()

# 시각화
st.subheader("⏰ 시간대별 평균 검색 관심도")
st.line_chart(hourly_avg)
