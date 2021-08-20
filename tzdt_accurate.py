# -*- coding: utf-8 -*-
"""
Created on Tue Jan 19 16:08:16 2021

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

s=requests.Session()

x1=745    #挑战答题
y1=223    #挑战答题

host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=&client_secret='#修改为自己的AK
response = s.get(host)
if response:
    print(response.json())
    print(response.json()['access_token'])
#x1=1560
#y1=541    #挑战4k

# x1=737  #双人答题
# y1=406  #双人答题
def click(x,y):

    win32api.SetCursorPos((x,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(0.01)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)

    
def getfromapi():
    ss=pyautogui.screenshot(region=(x1,y1,477,650))
    pic = BytesIO()
    ss.save(pic,format="jpeg")
    time1=time.time()
    base64_data = base64.b64encode(pic.getvalue())
    url = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate?access_token="+response.json()['access_token']
    payload={"image":"data:image/jpeg;base64,"+str(base64_data, encoding = "utf-8")}
	#print(payload)
    headers = {
	'Content-Type': 'application/x-www-form-urlencoded',
	'Host': 'aip.baidubce.com'
	}
    response1 = s.request("POST", url, headers=headers, data=payload)
    #print(response1.text)
    temp=json.loads(response1.text)
    print(temp)
    print(time.time()-time1)
    #print(temp['words_result'][0]['words'])
    if len(temp['words_result'])<1:
        print('超范围')
        return(1)
    zqcx=0
    position=temp['words_result'][0]['words'].find('词语的正确')
    if position >0 and len(temp['words_result'])<2:
        print('选择正确词语等答案出现再点击！！')
        return 0
        zqcx=1 #选择词语的正确词形
    position=temp['words_result'][0]['words'].find('。')
    if len(temp['words_result'])>=1:
        plus=1
    else:
        plus=0
    print("句号位置",position)
    if position!=-1:
        keyword0=temp['words_result'][zqcx]['words'][0:(position-1)]
        keyword1=temp['words_result'][zqcx+plus]['words'][0:(position-1)]
    else:
        keyword0=temp['words_result'][zqcx]['words'][0:len(temp['words_result'][zqcx]['words'])]
        keyword1=temp['words_result'][zqcx+plus]['words'][0:len(temp['words_result'][zqcx]['words'])]
    results=searchsql.main(keyword0.replace(',','').replace('，','').replace('“','').replace('*','').replace('”','').replace(':','').replace('·','').replace('_','').replace('(','').replace(')','').replace('（','').replace('）','').replace('?','').replace('？',''),'')
    results2=searchsql.main(keyword0.replace(',','').replace('，','').replace('“','').replace('*','').replace('”','').replace(':','').replace('·','').replace('_','').replace('(','').replace(')','').replace('（','').replace('）','').replace('?','').replace('？',''),keyword1.replace(',','').replace('，','').replace('“','').replace('*','').replace('”','').replace(':','').replace('·','').replace('_','').replace('(','').replace(')','').replace('（','').replace('）','').replace('?','').replace('？',''))
    results3=searchsql.main('',keyword1.replace(',','').replace('，','').replace('“','').replace('*','').replace('”','').replace(':','').replace('·','').replace('_','').replace('(','').replace(')','').replace('（','').replace('）','').replace('?','').replace('？',''))
    if len(results2)==0:
        results2=results
    if len(results2)==0:
        results2=results3
    if len(results2)==0 and len(temp['words_result'])>=2:        #没查到再多查询一行
        results2=searchsql.main(temp['words_result'][zqcx]['words'][2:len(temp['words_result'][zqcx]['words'])].replace(',','').replace('，','').replace('“','').replace('*','').replace('”','').replace(':','').replace('·','').replace('_','').replace('(','').replace(')','').replace('（','').replace('）','').replace('?','').replace('？',''),'')
    print(results2)
    for r in range(len(results2)):
        for i in range(len(temp['words_result'])):
    
            if results2[r]['number'][1:21].replace(',','').replace('，','').replace('“','').replace('*','').replace('”','').replace(':','').replace('·','').replace('_','').replace('(','').replace(')','').replace('（','').replace('）','').replace('?','').replace('？','')==temp['words_result'][i]['words'][:len(results2[r]['number'][1:21])].replace(',','').replace('，','').replace('“','').replace('*','').replace('”','').replace(':','').replace('·','').replace('_','').replace('(','').replace(')','').replace('（','').replace('）','').replace('?','').replace('？',''):
                click(x1+random.randint(10,320)+temp['words_result'][i]['location']['left'],y1+random.randint(10,22)+temp['words_result'][i]['location']['top'])
                engine = pyttsx3.init() 
                print('准备开始语音播报...')
                engine.say(results2[r]['number'][:8])
                # 等待语音播报完毕 
                engine.runAndWait() 
                return 1
            print(results2[r]['number'][1:21],"!=",temp['words_result'][i]['words'][:len(results2[r]['number'][1:21])].replace(',','').replace('，','').replace('*','').replace('“','').replace('”','').replace(':',''))

if keyboard.is_pressed('q') == False:
    while keyboard.is_pressed('s') == False:
        time.sleep(0.05)
        if keyboard.is_pressed('q') == True:
            getfromapi()
    print('Done!!!')