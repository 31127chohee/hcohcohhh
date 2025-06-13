import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 제목
st.title("📊 기상청 날씨 데이터 시각화")

# 데이터 불러오기
@st.cache_data
def load_data():
    df = pd.read_csv("OBS_ASOS_ANL_20250613120855.csv", encoding='euc-kr')
    df['일시'] = pd.to_datetime(df['일시'], errors='coerce')
    return df

df = load_data()

# 날짜 범위 설정
st.sidebar.header("📅 날짜 범위 선택")
start_date = st.sidebar.date_input("시작 날짜", df['일시'].min().date())
end_date = st.sidebar.date_input("종료 날짜", df['일시'].max().date())

# 데이터 필터링
mask = (df['일시'] >= pd.to_datetime(start_date)) & (df['일시'] <= pd.to_datetime(end_date))
filtered_df = df.loc[mask]

st.subheader("📄 필터링된 데이터")
st.dataframe(filtered_df)

# 기온 그래프
if '기온(°C)' in filtered_df.columns:
    st.subheader("🌡️ 기온 추이")
    fig1, ax1 = plt.subplots()
    ax1.plot(filtered_df['일시'], filtered_df['기온(°C)'], color='tomato')
    ax1.set_xlabel("일시")
    ax1.set_ylabel("기온 (°C)")
    ax1.set_title("기온 변화 그래프")
    st.pyplot(fig1)
else:
    st.warning("
