import streamlit as st
import pandas as pd
import plotly.express as px

st.title("🌤️ 기상청 날씨 데이터 시각화")

# CSV 파일 자동 로드
@st.cache_data
def load_data():
    df = pd.read_csv("OBS_ASOS_ANL_20250616091000.csv", encoding='euc-kr')
    df['일시'] = pd.to_datetime(df['일시'], errors='coerce')
    df = df.dropna(subset=['일시'])  # '일시'가 없는 행 제거
    return df

df = load_data()

# 🔍 컬럼명 확인용 (디버깅용)
# st.write(df.columns)

# 날짜 필터
st.sidebar.header("📅 날짜 범위 선택")
start_date = st.sidebar.date_input("시작 날짜", df['일시'].min().date())
end_date = st.sidebar.date_input("종료 날짜", df['일시'].max().date())

mask = (df['일시'] >= pd.to_datetime(start_date)) & (df['일시'] <= pd.to_datetime(end_date))
filtered_df = df.loc[mask]

st.subheader("📄 필터링된 데이터")
st.dataframe(filtered_df)

# 결측값 현황 출력
st.sidebar.header("🔍 데이터 결측 현황")
if '평균기온(°C)' in df.columns and '합계 강수량(mm)' in df.columns:
    missing_counts = df[['평균기온(°C)', '합계 강수량(mm)']].isna().sum()
    st.sidebar.write("**전체 데이터에서 결측값 개수**:")
    st.sidebar.write(missing_counts)
else:
    st.sidebar.warning("⚠️ '평균기온(°C)' 또는 '합계 강수량(mm)' 컬럼이 데이터에 없습니다.")

# 시각화 - 평균 기온
if '평균기온(°C)' in filtered_df.columns and not filtered_df['평균기온(°C)'].dropna().empty:
    st.subheader("🌡️ 평균 기온 변화 그래프")
    fig_temp = px.line(filtered_df, x='일시', y='평균기온(°C)', title="평균 기온 추이", markers=True)
    st.plotly_chart(fig_temp)
else:
    st.warning("⚠️ '평균기온(°C)' 데이터가 없거나 모든 값이 비어 있습니다.")

# 시각화 - 합계 강수량
if '합계 강수량(mm)' in filtered_df.columns and not filtered_df['합계 강수량(mm)'].dropna().empty:
    st.subheader("🌧️ 합계 강수량 변화 그래프")
    fig_rain = px.bar(filtered_df, x='일시', y='합계 강수량(mm)', title="합계 강수량 추이", color='합계 강수량(mm)')
    st.plotly_chart(fig_rain)
else:
    st.warning("⚠️ '합계 강수량(mm)' 데이터가 없거나 모든 값이 비어 있습니다.")
