import requests
import schedule
import time
import datetime

# 더미 appkey, appsecret
appkey = "Xt7Aq2Ks9Ld3Mw5Nz6Oy8Pv4Qr1Sw2Tx3Uv4Wz5"
appsecret = "Xt7Aq2Ks9Ld3Mw5Nz6Oy8Pv4Qr1Sw2Tx3Uv4Wz5Xt7Aq2Ks9Ld3Mw5Nz6Oy8Pv4Qr1Sw2Tx3Uv4Wz5Xt7Aq2Ks9Ld3Mw5Nz6Oy8Pv4Qr1Sw2Tx3Uv4Wz5"

def get_token(appkey, appsecret):
    domain = "https://openapivts.koreainvestment.com:29443"
    url = "/oauth2/tokenP"
    
    headers = {"Content-Type": "application/json"}
    body = {
        "grant_type": "client_credentials",
        "appkey": appkey,
        "appsecret": appsecret
    }

    try:
        response = requests.post(f"{domain}{url}", headers=headers, json=body)
        response.raise_for_status()  # 응답 상태 코드가 200이 아닐 경우 예외 발생
        return response.json()
    except Exception as e:
        print("Error getting token:", e)
        return

token_json = get_token(appkey, appsecret)
app_token = token_json["access_token"]

def trade(signal, token):
    domain = "https://openapivts.koreainvestment.com:29443"
    url = "/uapi/domestic-stock/v1/trading/order-cash"
    
    tr_id = "VTTC0802U" if signal == "buy" else "VTTC0801U" if signal == "sell" else None
    if tr_id is None:
        print("Error: Invalid signal")
        return
    
    headers = {
        "Content-Type": "application/json",
        "authorization": f"Bearer {token}",
        "appkey": appkey,
        "appsecret": appsecret,
        "tr_id": tr_id
    }

    body = {
        "CANO": "ABCJDERD",  # 더미 데이터
        "ACNT_PRDT_CD": "TR",  # 더미 데이터
        "PDNO": "005930",
        "ORD_DVSN": "01",
        "ORD_QTY": "1",  # 매수 수량 설정 (예시)
        "ORD_UNPR": "100000"  # 매수 가격 설정 (예시)
    }

    try:
        response = requests.post(f"{domain}{url}", headers=headers, json=body)
        response.raise_for_status()  # 응답 상태 코드가 200이 아닐 경우 예외 발생
        print("Trade successful:", response.json())
    except Exception as e:
        print("Error in trade:", e)

def decision(response):
    data = []
    output = response.get("output2", [])  # "output2" 키가 없을 경우 빈 리스트 반환
    
    # 주가 데이터 로드
    for item in output:
        data.append(item['stck_prpr'])
    
    if len(data) < 61:
        print("Need more data!")
        return
    
    # ma20, ma60 계산
    ma20_prev = sum(data[-21:-1]) / 20
    ma20 = sum(data[-20:]) / 20
    ma60_prev = sum(data[-61:-1]) / 60
    ma60 = sum(data[-60:]) / 60
    
    # 골든 크로스 및 데드 크로스 신호 확인
    if (ma20_prev < ma60_prev) and (ma20 > ma60):
        trade("buy", app_token)
    elif (ma20_prev > ma60_prev) and (ma20 < ma60):
        trade("sell", app_token)

def tracking(token):
    domain = "https://openapivts.koreainvestment.com:29443"
    url = "/uapi/domestic-stock/v1/quotations/inquire-time-itemchartprice"
    
    current_time = datetime.datetime.now().strftime("%H%M%S")
    
    headers = {
        "Content-Type": "application/json",
        "authorization": f"Bearer {token}",
        "appkey": appkey,
        "appsecret": appsecret,
        "tr_id": "FHKST03010200",
        "custtype": "P"
    }

    body = {
        "FID_ETC_CLS_CODE": "",
        "FID_COND_MRKT_DIV_CODE": "J",
        "FID_INPUT_ISCD": "005930",
        "FID_INPUT_HOUR_1": current_time,
        "FID_PW_DATA_INCU_YN": "Y",
    }

    try:
        response = requests.get(f"{domain}{url}", headers=headers, params=body)
        response.raise_for_status()  # 응답 상태 코드가 200이 아닐 경우 예외 발생
        decision(response.json())
    except Exception as e:
        print("Error in tracking:", e)

schedule.every(1).minutes.do(tracking, app_token)

while True:
    schedule.run_pending()
    time.sleep(1)
