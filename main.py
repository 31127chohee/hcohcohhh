import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 제목
st.title("기상청 날씨 데이터 시각화")

# CSV 파일 불러오기
@st.cache_data
def load_data():
    df = pd.read_csv("OBS_ASOS_ANL_20250613120855.csv", encoding='euc-kr')
    return df

df = load_data()

# 날짜 형식 변환
df['일시'] = pd.to_datetime(df['일시'], errors='coerce')

# 사이드바: 날짜 필터링
st.sidebar.header("필터 설정")
start_date = st.sidebar.date_input("시작 날짜", df['일시'].min())
end_date = st.sidebar.date_input("끝 날짜", df['일시'].max())

# 필터링
mask = (df['일시'] >= pd.to_datetime(start_date)) & (df['일시'] <= pd.to_datetime(end_date))
filtered_df = df.loc[mask]

# 메인 화면
st.subheader("필터링된 데이터")
st.dataframe(filtered_df)

# 기온 시각화
if '기온(°C)' in df.columns:
    st.subheader("기온 추이")
    fig, ax = plt.subplots()
    ax.plot(filtered_df['일시'], filtered_df['기온(°C)'], color='red')
    ax.set_xlabel("날짜")
    ax.set_ylabel("기온 (°C)")
    ax.set_title("기온 변화")
    st.pyplot(fig)

# 강수량 시각화
if '강수량(mm)' in df.columns:
    st.subheader("강수량 추이")
    fig2, ax2 = plt.subplots()
    ax2.bar(filtered_df['일시'], filtered_df['강수량(mm)'], color='blue')
    ax2.set_xlabel("날짜")
    ax2.set_ylabel("강수량 (mm)")
    ax2.set_title("강수량 변화")
    st.pyplot(fig2)
