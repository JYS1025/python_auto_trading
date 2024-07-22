import requests

#dumy appkey, appsecret
appkey = "Xt7Aq2Ks9Ld3Mw5Nz6Oy8Pv4Qr1Sw2Tx3Uv4Wz5"
appsecret = "Xt7Aq2Ks9Ld3Mw5Nz6Oy8Pv4Qr1Sw2Tx3Uv4Wz5Xt7Aq2Ks9Ld3Mw5Nz6Oy8Pv4Qr1Sw2Tx3Uv4Wz5Xt7Aq2Ks9Ld3Mw5Nz6Oy8Pv4Qr1Sw2Tx3Uv4Wz5"

def get_token(appkey, appsecret):
    domain = "https://openapivts.koreainvestment.com:29443"
    url = "/oauth2/tokenP"

    content = {"Content-Type":"json"}
    content.json()

    body = {
        "grant_type" : "client_credentials",
        "appkey" : appkey,
        "appsecret" : appsecret 
    }.json()


    response = request.post(f"{domain}{url}", headers=content, data=body)
    return response