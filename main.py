from pytrends.request import TrendReq
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 한글 폰트 설정 (Windows용, Mac은 AppleGothic)
plt.rcParams['font.family'] = 'Malgun Gothic'

# 구글 트렌드 초기화 (한국 기준 시간대)
pytrends = TrendReq(hl='ko', tz=540)

# 분석할 키워드 리스트
keywords = ["멜론", "유튜브 뮤직", "NewJeans"]

# 구글 트렌드 데이터 요청 (최근 7일간, 한국 지역)
pytrends.build_payload(keywords, timeframe='now 7-d', geo='KR')

# 시간대별 관심도 데이터 수집
df = pytrends.interest_over_time()

# 시간 추출 및 그룹화
df = df.reset_index()
df['hour'] = df['date'].dt.hour
hourly_avg = df.groupby('hour')[keywords].mean()

# 시각화
plt.figure(figsize=(12, 6))
for keyword in keywords:
    sns.lineplot(x=hourly_avg.index, y=hourly_avg[keyword], label=keyword)

plt.title("구글 트렌드 기준 시간대별 검색 관심도 (최근 7일)")
plt.xlabel("시간대 (0~23시)")
plt.ylabel("관심도 (0~100 상대값)")
plt.xticks(range(0, 24))
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
