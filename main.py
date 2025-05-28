# streamlit_app.py
import streamlit as st
import pandas as pd
import plotly.express as px

# 데이터 불러오기
url = 'https://drive.google.com/uc?export=download&id=1pwfON6doXyH5p7AOBJPfiofYlni0HVVY'
df = pd.read_csv(url)

# Streamlit UI
st.title("데이터 시각화 웹앱")
st.write("Google Drive에서 불러온 데이터를 Plotly로 시각화합니다.")

# Plotly 그래프
fig = px.line(df, x='date', y='value', title='시간에 따른 변화')
st.plotly_chart(fig)

