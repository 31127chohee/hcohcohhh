import streamlit as st
import pandas as pd
import plotly.express as px

st.title("🌤️ 기상청 날씨 데이터 시각화 (2024년 6월)")

@st.cache_data
def load_data():
    df = pd.read_csv("OBS_ASOS_ANL_20250616091000.csv", encoding='euc-kr')
    df['일시'] = pd.to_datetime(df['일시'], errors='coerce')
    
    # 1970년 날짜 → 2024-01-01로 변경
    df.loc[df['일시'].dt.year == 1970, '일시'] = pd.Timestamp('2024-01-01 00:00:00')
    
    df = df.dropna(subset=['일시'])  # '일시' 없는 행 제거
    return df

df = load_data()

# 2024년 6월 데이터만 필터링
start_date = pd.Timestamp('2024-06-01')
end_date = pd.Timestamp('2024-06-30 23:59:59')
filtered_df = df[(df['일시'] >= start_date) & (df['일시'] <= end_date)]

st.sidebar.success(f"2024년 6월 데이터 필터링: {start_date.date()} ~ {end_date.date()}")
st.sidebar.write("📌 필터된 데이터 수:", len(filtered_df))

st.subheader("📄 2024년 6월 데이터")
st.dataframe(filtered_df)

# 결측값 현황 출력
st.sidebar.header("🔍 데이터 결측 현황")
if '평균기온(°C)' in df.columns and '합계 강수량(mm)' in df.columns:
    missing_counts = filtered_df[['평균기온(°C)', '합계 강수량(mm)']].isna().sum()
    st.sidebar.write("**결측값 개수 (6월 데이터 기준)**")
    st.sidebar.write(missing_counts)
else:
    st.sidebar.warning("⚠️ '평균기온(°C)' 또는 '합계 강수량(mm)' 컬럼이 데이터에 없습니다.")

# 평균 기온 그래프
if '평균기온(°C)' in filtered_df.columns and not filtered_df['평균기온(°C)'].dropna().empty:
    st.subheader("🌡️ 2024년 6월 평균 기온 변화")
    fig_temp = px.line(filtered_df, x='일시', y='평균기온(°C)', title="2024년 6월 평균 기온 추이", markers=True)
    st.plotly_chart(fig_temp)
else:
    st.warning("⚠️ '평균기온(°C)' 데이터가 없거나 비어 있습니다.")

# 합계 강수량 그래프
if '합계 강수량(mm)' in filtered_df.columns and not filtered_df['합계 강수량(mm)'].dropna().empty:
    st.subheader("🌧️ 2024년 6월 합계 강수량 변화")
    fig_rain = px.bar(filtered_df, x='일시', y='합계 강수량(mm)', title="2024년 6월 합계 강수량 추이", color='합계 강수량(mm)')
    st.plotly_chart(fig_rain)
else:
    st.warning("⚠️ '합계 강수량(mm)' 데이터가 없거나 비어 있습니다.")
