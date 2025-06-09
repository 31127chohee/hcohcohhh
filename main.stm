from pytrends.request import TrendReq
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 한글 폰트 설정 (Mac/Windows 환경에 따라 다름)
plt.rcParams['font.family'] = 'Malgun Gothic'  # 윈도우
# plt.rcParams['font.family'] = 'AppleGothic'  # 맥

# 구글 트렌드 객체 초기화 (한국 기준)
pytrends = TrendReq(hl='ko', tz=540)

# 분석할 키워드 리스트
keywords = ["멜론", "유튜브 뮤직", "NewJeans"]

# 시간대별 검색 트렌드 가져오기 (최근 7일)
pytrends.build_payload(keywords, timeframe='now 7-d', geo='KR')
df = pytrends.interest_over_time()

# 시간 추출
df = df.reset_index()
df['hour'] = df['date'].dt.hour

# 시간대별 평균 검색량 계산
hourly_avg = df.groupby('hour')[keywords].mean()

# 네이버 가상 데이터 (하루 단위 검색량 기준, 예시용 - 실제는 사용자 수집 필요)
# 상대적 검색 비율 (1일 평균 비중으로 가정)
naver_data = {
    "hour": list(range(24)),
    "멜론": [2,1,1,1,2,3,6,8,10,11,10,9,8,7,6,5,6,8,9,10,9]()
