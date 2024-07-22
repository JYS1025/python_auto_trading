import requests
import schedule, time, datetime
#dumy appkey, appsecret
appkey = "Xt7Aq2Ks9Ld3Mw5Nz6Oy8Pv4Qr1Sw2Tx3Uv4Wz5"
appsecret = "Xt7Aq2Ks9Ld3Mw5Nz6Oy8Pv4Qr1Sw2Tx3Uv4Wz5Xt7Aq2Ks9Ld3Mw5Nz6Oy8Pv4Qr1Sw2Tx3Uv4Wz5Xt7Aq2Ks9Ld3Mw5Nz6Oy8Pv4Qr1Sw2Tx3Uv4Wz5"

#1minute chart data
data = []
def get_token(appkey, appsecret):
    domain = "https://openapivts.koreainvestment.com:29443"
    url = "/oauth2/tokenP"

    content = {"Content-Type":"application/json"}
    content.json()

    body = {
        "grant_type" : "client_credentials",
        "appkey" : appkey,
        "appsecret" : appsecret 
    }.json()

    try:
        response = request.post(f"{domain}{url}", headers=content, data=body).json()
        return response
    except Exception as e:
        print(e)
        return

token_json = get_token(appkey, appsecret)
app_token = token_json["access_token"]

def decision(response):
    #make empty list to stack stock-price data
    data = []
    ma20 = []
    ma60 = []
    output = response[output2]
    
    #Load stock-price data
    for item in output:
        data.append(item['stck_prpr'])
    
    #Compute ma20, ma60 data
    for i in range(60, len(data)):
        ma20.append(sum(data[i-20:i])/20)
    for i in range(60, len(data)):
        ma60.append(sum(data[i-60:i])/60)

    # **Prob** : Why we should compute all data? we just need current result so it more adapt on backtest
    for i in range(1, len(data)-60):
        #Golden cross test
        if (ma20[i-1] < ma60[i-1]) and (ma20[i] > ma60[i]): 
            print("매수")
            #전체 매수
        #Dead cross test
        elif (ma20[i-1] > ma60[i-1]) and (ma20[i] < ma60[i]): 
            print("매도")
            #전체 매도
    return


def tracking(token):
    #API domain, url
    domain = "https://openapivts.koreainvestment.com:29443"
    url = "/uapi/domestic-stock/v1/quotations/inquire-time-itemchartprice"
    
    #get current time
    current_time = datetime.datetime.now().strftime("%H%M%S")
    
    #request-headers
    content = {
        "Content-Type":"application/json",
        "authorization":f"Bearer {token}",
        "appkey":appkey,
        "appsecret":appsecret,  
        "tr_id":"FHKST03010200",
        "custtype":"P"
    }
    content.json()

    #request-body
    body = {
        "FID_ETC_CLS_CODE" : "",
        "FID_COND_MRKT_DIV_CODE" : "J",
        "FID_INPUT_ISCD" : "005930",
        "FID_INPUT_HOUR_1" : current_time,
        "FID_PW_DATA_INCU_YN" : "Y",
    }
    try:
        response = request.get(f"{domain}{url}",headers = content, params = body).json()
        decision(response)
        return response
    except Exception as e:
        print(e)
        return



schedule.every(1).minutes.do(tracking)
