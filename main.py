import streamlit as st
import pandas as pd
import plotly.express as px

# 앱 제목
st.title("🌤️ 기상청 날씨 데이터 시각화")

# 데이터 로드 (캐싱)
@st.cache_data
def load_data():
    df = pd.read_csv("OBS_ASOS_ANL_20250613120855.csv", encoding='euc-kr')
    df['일시'] = pd.to_datetime(df['일시'], errors='coerce')  # 날짜 형식 변환
    return df

df = load_data()

# 날짜 필터
st.sidebar.header("📅 날짜 범위 선택")
start_date = st.sidebar.date_input("시작 날짜", df['일시'].min().date())
end_date = st.sidebar.date_input("종료 날짜", df['일시'].max().date())

mask = (df['일시'] >= pd.to_datetime(start_date)) & (df['일시'] <= pd.to_datetime(end_date))
filtered_df = df.loc[mask]

# 필터링된 데이터 표시
st.subheader("📄 필터링된 데이터")
st.dataframe(filtered_df)

# 기온 그래프
if '기온(°C)' in filtered_df.columns:
    st.subheader("🌡️ 기온 변화 그래프")
    fig_temp = px.line(filtered_df, x='일시', y='기온(°C)', title="기온 추이", markers=True)
    st.plotly_chart(fig_temp)
else:
    st.warning("⚠️ '기온(°C)' 데이터가 없습니다.")

# 강수량 그래프
if '강수량(mm)' in filtered_df.columns:
    st.subheader("🌧️ 강수량 변화 그래프")
    fig_rain = px.bar(filtered_df, x='일시', y='강수량(mm)', title="강수량 추이", color='강수량(mm)')
    st.plotly_chart(fig_rain)
else:
    st.warning("⚠️ '강수량(mm)' 데이터가 없습니다.")
