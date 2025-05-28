import pandas as pd

# Google Drive 파일 URL
url = 'https://drive.google.com/uc?export=download&id=1pwfON6doXyH5p7AOBJPfiofYlni0HVVY'

# 데이터 불러오기
df = pd.read_csv(url)

# 데이터 미리보기
print(df.head())
