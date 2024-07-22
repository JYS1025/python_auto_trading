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

def init_data():

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
        return response
    except Exception as e:
        print(e)
        return

schedule.every(1).minutes.do(tracking)
