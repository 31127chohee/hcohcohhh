import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# 구글 스프레드시트 CSV URL 생성
sheet_url = "https://docs.google.com/spreadsheets/d/1b-yJdvtLL-gEvUzyTY-EYnVn0c7Z2ZwVMnp-z3i7Kq0/edit#gid=1414820323"
csv_url = sheet_url.replace('/edit#gid=', '/export?format=csv&gid=')

@st.cache_data
def load_data(url):
    return pd.read_csv(url)

df = load_data(csv_url)

st.title("K-means 군집화 및 시각화")

st.write("데이터 미리보기:")
st.dataframe(df)

# 군집화에 사용할 컬럼 선택 (숫자형 컬럼 필터링)
numeric_cols = df.select_dtypes(include='number').columns.tolist()

if len(numeric_cols) < 2:
    st.error("숫자형 컬럼이 2개 이상 필요합니다.")
else:
    st.sidebar.header("군집화 설정")
    selected_features = st.sidebar.multiselect("군집화에 사용할 피처 선택", numeric_cols, default=numeric_cols)
    n_clusters = st.sidebar.slider("군집 개수 선택", min_value=2, max_value=10, value=3)

    if len(selected_features) < 2:
        st.warning("적어도 2개의 피처를 선택해주세요.")
    else:
        X = df[selected_features]

        # 데이터 표준화
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        # K-means 클러스터링
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        cluster_labels = kmeans.fit_predict(X_scaled)

        df['cluster'] = cluster_labels.astype(str)  # 군집 라벨을 문자열로 변환(Plotly 색상 구분용)

        # 2D 산점도 시각화 (첫 두 선택된 피처 기준)
        fig = px.scatter(
            df,
            x=selected_features[0],
            y=selected_features[1],
            color='cluster',
            title=f"K-means Clustering (K={n_clusters})",
            labels={'cluster': 'Cluster'},
            hover_data=df.columns
        )
        st.plotly_chart(fig)
