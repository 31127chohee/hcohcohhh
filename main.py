import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 앱 제목
st.title("📊 기상청 날씨 데이터 시각화")

# 데이터 로딩 함수 (캐싱 사용)
@st.cache_data
def load_data():
    df = pd.read_csv("OBS_ASOS_ANL_20250613120855.csv", encoding='euc-kr')
    df['일시'] = pd.to_datetime(df['일시'], errors='coerce')  # 날짜 형식 변환
    return df

# 데이터 불러오기
df = load_data()

# 사이드바: 날짜 필터
st.sidebar.header("📅 날짜 범위 선택")
start_date = st.sidebar.date_input("시작 날짜", df['일시'].min().date())
end_date = st.sidebar.date_input("종료 날짜", df['일시'].max().date())

# 날짜 필터링
mask = (df['일시'] >= pd.to_datetime(start_date)) & (df['일시'] <= pd.to_datetime(end_date))
filtered_df = df.loc[mask]

# 필터링된 데이터 표시
st.subheader("📄 필터링된 데이터")
st.dataframe(filtered_df)

# 🌡️ 기온 그래프
if '기온(°C)' in filtered_df.columns:
    st.subheader("🌡️ 기온 추이")
    fig1, ax1 = plt.subplots()
    ax1.plot(filtered_df['일시'], filtered_df['기온(°C)'], color='tomato')
    ax1.set_xlabel("일시")
    ax1.set_ylabel("기온 (°C)")
    ax1.set_title("기온 변화 그래프")
    st.pyplot(fig1)
else:
    st.warning("⚠️ '기온(°C)' 데이터가 없습니다.")

# 🌧️ 강수량 그래프
if '강수량(mm)' in filtered_df.columns:
    st.subheader("🌧️ 강수량 추이")
    fig2, ax2 = plt.subplots()
    ax2.bar(filtered_df['일시'], filtered_df['강수량(mm)'], color='skyblue')
    ax2.set_xlabel("일시")
    ax2.set_ylabel("강수량 (mm)")
    ax2.set_title("강수량 변화 그래프")
    st.pyplot(fig2)
else:
    st.warning("⚠️ '강수량(mm)' 데이터가 없습니다.")
