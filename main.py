import requests
import base64

client_id = "YOUR_CLIENT_ID"
client_secret = "YOUR_CLIENT_SECRET"

auth_url = "https://accounts.spotify.com/api/token"
auth_header = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()

headers = {
    "Authorization": f"Basic {auth_header}",
    "Content-Type": "application/x-www-form-urlencoded"
}
data = {
    "grant_type": "client_credentials"
}

auth_response = requests.post(auth_url, headers=headers, data=data)

# 오류 출력
print(auth_response.status_code)
print(auth_response.text)

# 에러 없이 토큰 추출
if auth_response.status_code == 200:
    access_token = auth_response.json()["access_token"]
    print("Access Token:", access_token)
else:
    print("인증 실패: 응답 확인 필요")
