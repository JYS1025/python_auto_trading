import json

budget = 1000000
sample = None
with open("sample.json", "r") as f:
    sample = json.load(f)

data = []
ma20 = []
ma60 = []
output = sample[output2]

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