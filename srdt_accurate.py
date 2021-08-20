# -*- coding: utf-8 -*-
"""
Created on Fri Jan 29 18:12:57 2021

@author: XTian
"""


from io import BytesIO
import pyttsx3
import pyautogui
import time
import keyboard
import random
import win32api, win32con
import base64
import requests
import json
import searchsql




#点1 X745:  Y:259
#点2 X:1168 Y:742
# x1=740
# y1=237    #挑战答题
s=requests.Session()
#x1=730
#y1=336  #双人答题(模拟器)
x1=773
y1=310  #双人答题(MIUI+)
host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=fzXwd3nVTXW2cgXfrEsClG4O&client_secret=mQjIVMCPYjQiT0jqkGQkx19I5ztaLfs5'
#host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=U7Z6NnsQNOLkdTWITItGgf1w&client_secret=9cRLl0ZMWQCEkFxQeb73zC4feFsCry4e'
response = s.get(host)
if response:
    print(response.json())
    print(response.json()['access_token'])
def click(x,y):
    vmx=477
    vmy=500
    miuix=380
    miuiy=410
    print(x)
    print(y)
    if x>x1+miuix:
        x=x1+miuix
    if y>y1+miuiy:  
        y=y1+miuiy
    win32api.SetCursorPos((x,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(0.01)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)


def getfromapi():
    import time
    
    ss=pyautogui.screenshot(region=(x1,y1,477,500))
    pic = BytesIO()
    ss.save(pic,format="jpeg")
    base64_data = base64.b64encode(pic.getvalue())
    #print(base64_data)

    time1=time.time()
    url = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate?access_token="+response.json()['access_token']
    payload={"image":"data:image/jpeg;base64,"+str(base64_data, encoding = "utf-8")}
    #payload={"image":str(base64_data, encoding = "utf-8")}
    #print(payload)
    headers = {
	'Content-Type': 'application/x-www-form-urlencoded',
	'Host': 'aip.baidubce.com'
	}
    response1 = s.request("POST", url, headers=headers, data=payload)
    print(response1.text)
    print(time.time()-time1)
    temp=json.loads(response1.text)

    # savepic(temp)  //保存图片
    print('时间为：'+str(time.time()-time1))
    
    #print(temp['words_result'][0]['words'])
    if len(temp['words_result'])<1:
        print('超范围')
        return(1)
    zqcx=0
    position=temp['words_result'][0]['words'].find('词语的正确')
    if position >0:
        if len(temp['words_result'])<2:
            print('选择正确词语等答案出现再点击！！')
            return 0
        zqcx=1 #选择词语的正确词形
    position=temp['words_result'][0]['words'].find('。')
    if len(temp['words_result'])>=2:
        plus=1
    else:
        plus=0
    print("句号位置",position)
    if position!=-1:
        keyword0=temp['words_result'][zqcx]['words'][2:(position-1)]
        keyword1=temp['words_result'][zqcx+plus]['words'][2:(position-1)]
    else:
        keyword0=temp['words_result'][zqcx]['words'][2:len(temp['words_result'][zqcx]['words'])]
        keyword1=temp['words_result'][zqcx+plus]['words'][2:]#len(temp['words_result'][zqcx]['words'])
    # results=searchsql.main(keyword0.replace(',','，').replace('“','"').replace('”','"').replace(':','：'),'')
    # results2=searchsql.main(keyword0.replace(',','，').replace('“','"').replace('”','"').replace(':','：'),keyword1.replace(',','，').replace('“','"').replace('”','"').replace(':','：'))
    # results3=searchsql.main('',keyword1.replace(',','，').replace('“','"').replace('”','"').replace(':','：'))
    results=searchsql.main(keyword0.replace(',','').replace('，','').replace('“','').replace('*','').replace('”','').replace(':','').replace('·','').replace('_','').replace('(','').replace(')','').replace('（','').replace('）','').replace('?','').replace('？',''),'')
    results2=searchsql.main(keyword0.replace(',','').replace('，','').replace('“','').replace('*','').replace('”','').replace(':','').replace('·','').replace('_','').replace('(','').replace(')','').replace('（','').replace('）','').replace('?','').replace('？',''),keyword1.replace(',','').replace('，','').replace('“','').replace('*','').replace('”','').replace(':','').replace('·','').replace('_','').replace('(','').replace(')','').replace('（','').replace('）','').replace('?','').replace('？',''))
    results3=searchsql.main('',keyword1.replace(',','').replace('，','').replace('“','').replace('*','').replace('”','').replace(':','').replace('·','').replace('_','').replace('(','').replace(')','').replace('（','').replace('）','').replace('?','').replace('？',''))
    #print(keyword1.replace(',','，'))


    #if len(results2)==0:
        #results2=results
    if len(results2)==0:
        results2=results
    if len(results2)==0:
        results2=results3
    if len(results2)==0 and len(temp['words_result'])>=2:        #没查到再多查询一行
        results2=searchsql.main(temp['words_result'][zqcx]['words'][2:len(temp['words_result'][zqcx]['words'])].replace(',','').replace('，','').replace('“','').replace('*','').replace('”','').replace(':','').replace('·','').replace('_','').replace('(','').replace(')','').replace('（','').replace('）','').replace('?','').replace('？',''),'')
    print(results2)
    print(keyword0,keyword1)

    #click(750,500)
     #   print(x1+random.randint(10,22)+temp['words_result'][len(temp['words_result'])-2]['location']['top'])
        # if response.text[position+1] == "A" or "B" or "C" or "D":   #去掉ABCD
        #     position=position+1                                     #双人答题不需要去掉ABCD
    no=1
    time=0
    if len(results2)==0:
        engine = pyttsx3.init()
        print('请随意点击，查询失败')
        engine.say('随意点击，查询失败')
        # 等待语音播报完毕
        engine.runAndWait()
        return 0

    for r in range(len(results2)):
        for i in range(len(temp['words_result'])):

            if results2[r]['number'][0]==temp['words_result'][i]['words'][0]:
                no=0
                time=r
                #print(response.text[position+1],'==',temp['words_result'][i]['words'][0])
                click(x1+random.randint(20,360)+temp['words_result'][i]['location']['left'],y1+random.randint(10,22)+temp['words_result'][i]['location']['top'])
                # click(x1+random.randint(20,360)+temp['words_result'][i]['location']['left'],y1+random.randint(10,22)+temp['words_result'][i]['location']['top'])
                return 1
            print(results2[r]['number'][1:],"!=",temp['words_result'][i]['words'][:len(results2[r]['number'][1:])])
        if no:
            if results2[r]['number'][0]=='A':
                time=r
                click(x1+random.randint(20,300)+temp['words_result'][len(temp['words_result'])-1]['location']['left'],y1+random.randint(75,95)+temp['words_result'][len(temp['words_result'])-1]['location']['top'])
                return 1
            if results2[r]['number'][0]=='B':
                time=r
                click(x1+random.randint(20,300)+temp['words_result'][len(temp['words_result'])-1]['location']['left'],y1+random.randint(140,160)+temp['words_result'][len(temp['words_result'])-1]['location']['top'])
                return 1
            if results2[r]['number'][0]=='C':
                time=r
                click(x1+random.randint(20,300)+temp['words_result'][len(temp['words_result'])-1]['location']['left'],y1+random.randint(205,225)+temp['words_result'][len(temp['words_result'])-1]['location']['top'])
                return 1
            if results2[r]['number'][0]=='D':
                time=r
                click(x1+random.randint(20,300)+temp['words_result'][len(temp['words_result'])-1]['location']['left'],y1+random.randint(270,290)+temp['words_result'][len(temp['words_result'])-1]['location']['top'])
                return 1
				##10,320模拟器 50 100  125 175 200 250 275 325 
    engine = pyttsx3.init()
    print('准备开始语音播报...')
    engine.say(results2[time]['number'][:8])
    # 等待语音播报完毕
    engine.runAndWait()
        # if response.text[position+1] == "A":
        #     print(response.text[position+1:position2])
        #     click(x1+random.randint(10,22)+temp['words_result'][len(temp['words_result'])-4]['location']['left'],y1+random.randint(10,22)+temp['words_result'][len(temp['words_result'])-4]['location']['top'])
        # if response.text[position+1] == "B":
        #     print(response.text[position+1:position2])
        #     click(x1+random.randint(10,22)+temp['words_result'][len(temp['words_result'])-3]['location']['left'],y1+random.randint(10,22)+temp['words_result'][len(temp['words_result'])-3]['location']['top'])
        # if response.text[position+1] == "C":
        #     print(response.text[position+1:position2])
        #     click(x1+random.randint(10,22)+temp['words_result'][len(temp['words_result'])-2]['location']['left'],y1+random.randint(10,22)+temp['words_result'][len(temp['words_result'])-2]['location']['top'])
        # if response.text[position+1] == "D":
        #     print(response.text[position+1:position2])
        #     click(x1+random.randint(10,22)+temp['words_result'][len(temp['words_result'])-1]['location']['left'],y1+random.randint(10,22)+temp['words_result'][len(temp['words_result'])-1]['location']['top'])
    
if keyboard.is_pressed('q') == False:
    while keyboard.is_pressed('s') == False:
        time.sleep(0.01)
        if keyboard.is_pressed('q') == True:
            getfromapi()
    print('答题结束！祝你有美好的一天。')
