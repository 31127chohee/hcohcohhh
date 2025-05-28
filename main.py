import streamlit as st
import pandas as pd
import plotly.express as px

# 페이지 제목
st.title("🩺 당뇨병 증상 데이터 시각화")

# Google Drive CSV 다운로드 URL
url = 'https://drive.google.com/uc?export=download&id=1pwfON6doXyH5p7AOBJPfiofYlni0HVVY'

# 데이터 불러오기
@st.cache_data
def load_data():
    df = pd.read_csv(url)
    return df

df = load_data()

# 데이터 미리보기
st.subheader("📋 데이터 미리보기")
st.dataframe(df.head())

# 컬럼 정보 출력
st.write("컬럼 목록:", df.columns.tolist())

# 📊 class 분포 시각화
st.subheader("🧪 당뇨병 여부(class) 분포")
fig_class = px.histogram(df, x='class', color='class', title='당뇨병 여부 분포')
st.plotly_chart(fig_class)

# 📊 증상 선택 시각화
st.subheader("🧬 증상별 당뇨병 분포 보기")

symptom = st.selectbox("👇 증상을 선택하세요", df.columns[:-1])

# 그룹화 및 시각화
grouped = df.groupby([symptom, 'class']).size().reset_index(name='count')
fig_symptom = px.bar(grouped,
                     x=symptom,
                     y='count',
                     color='class',
                     barmode='group',
                     title=f"{symptom} 여부에 따른 당뇨병 분포")
st.plotly_chart(fig_symptom)
