import time
import telepot
from telepot.loop import MessageLoop
import random
import pymysql
import speech_recognition
import os
import pyaudio
import datetime
import requests
import schedule
import threading
from playsound import playsound

def getWeather():
    global weather , temperature
    url = "https://www.cwb.gov.tw/V8/C/W/Observe/MOD/24hr/C0H89.html?559"
    r = requests.get(url)
    data = r.text.split("span")
    # print(data[1][-6:-2])
    temperature = float(data[1][-6:-2])
    a = data[4].split(">")
    if a[3][-3:-1][0] == '"':
        weather = a[3][-3:-1][1]
        # print(a[3][-3:-1][1])
    else:
        weather = a[3][-3:-1]
        # print(a[3][-3:-1])
    conn = pymysql.connect(host='localhost', user='PLRO',passwd='23094740', db='delsa')
    c = conn.cursor()
    c.execute("Select cId from `user` where 1;")
    tmp = c.fetchall()
    for i in tmp:
        print(list(i))
        bot.sendMessage(int(list(i)[0]), '今天的天氣是:' + weather + '\n今天的溫度是:' + str(temperature))
    boardcast()
    c.execute("UPDATE `user` set `money` = `money` + 50 where 1;")
    
    conn.commit()
    conn.close()
def recover():
    conn = pymysql.connect(host='localhost', user='PLRO',passwd='23094740', db='delsa')
    c = conn.cursor()
    c.execute("UPDATE `user` set `canDo` = 1 where 1;")
    conn.commit()
    conn.close()
def sleep():
    conn = pymysql.connect(host='localhost', user='PLRO',passwd='23094740', db='delsa')
    c = conn.cursor()
    c.execute("UPDATE `user` set `HP` = `HP` + 30 where 1;")
    conn.commit()
    conn.close()
def boardcast():
    global todayCMD
    todayCMD = random.randint(0,7)
    conn = pymysql.connect(host='localhost', user='PLRO',passwd='23094740', db='delsa')
    c = conn.cursor()
    c.execute("Select cId from `user` where 1;")
    tmp = c.fetchall()
    for i in tmp:
        bot.sendMessage(int(list(i)[0]), '今天的口令是:' + cmd1[todayCMD] + cmd2[todayCMD] + cmd3[todayCMD])
    conn.close()
def checkStatus(chat_id):
    conn = pymysql.connect(host='localhost', user='PLRO',passwd='23094740', db='delsa')
    c = conn.cursor()
    c.execute("Select water , kimoji from `user` where cId = "+ str(chat_id) +";")
    tmp = list(c.fetchall())
    c.execute("UPDATE `user` set `HP` = 100 where `HP` > 100;")
    c.execute("UPDATE `user` set `kimoji` = 100 where `kimoji` > 100;")
    conn.commit()
    print(tmp)
    if len(tmp) > 0:
        print(tmp[0][0])
        if tmp[0][0] <= 0:
            bot.sendMessage(chat_id,"你渴死了......" )
            deleteAccount(chat_id)
            return True
        elif tmp[0][1] <= 0:
            bot.sendMessage(chat_id,"你心情不好，毅然決然的...逃兵了" )
            deleteAccount(chat_id)
            return True
    conn.close()
    

def Voice_To_Text():
    rr = speech_recognition
    r = rr.Recognizer()
    with speech_recognition.Microphone() as source: 
     ## 介紹一下 with XXX as XX 這個指令
     ## XXX 是一個函數或動作 然後我們把他 的output 放在 XX 裡
     ## with 是在設定一個範圍 讓本來的 source 不會一直進行
     ## 簡單的應用，可以參考
     ## https://blog.gtwang.org/programming/python-with-context-manager-tutorial/
        print("請開始說話:")                               # print 一個提示 提醒你可以講話了
        r.adjust_for_ambient_noise(source)     # 函數調整麥克風的噪音:
        audio = r.listen(source)
     ## with 的功能結束 source 會不見 
     ## 接下來我們只會用到 audio 的結果
    try:
        Text = r.recognize_google(audio, language="zh-TW")     
              ##將剛說的話轉成  zh-TW 繁體中文 的 字串
              ## recognize_google 指得是使用 google 的api 
              ## 也就是用google 網站看到的語音辨識啦~~
              ## 雖然有其他選擇  但人家是大公司哩 當然優先用他的囉
    except rr.UnknownValueError:
        Text = "無法翻譯"
        os.system('mpg321 WTM.mp3 &')
        time.sleep(2)
    except rr.RequestError as e:
        Text = "無法翻譯{0}".format(e)
              # 兩個 except 是當語音辨識不出來的時候 防呆用的 
    return Text
def checkCanDo(chat_id):
    conn = pymysql.connect(host='localhost', user='PLRO',passwd='23094740', db='delsa')
    c = conn.cursor()
    c.execute("Select `canDo` from `user` where `cId` = '" + str(chat_id) + "';")
    result = list(c.fetchall())
    conn.close()
    if(result[0][0] == 0):
        return False
    else:
        return True
def HPEnough(chat_id):
    conn = pymysql.connect(host='localhost', user='PLRO',passwd='23094740', db='delsa')
    c = conn.cursor()
    c.execute("Select `HP` from `user` where `cId` = '" + str(chat_id) + "';")
    result = list(c.fetchall())
    conn.close()
    if(result[0][0] < 10):
        bot.sendMessage(chat_id,"已經沒體力了" )
        return False
    else:
        return True
def happy(chat_id):
    conn = pymysql.connect(host='localhost', user='PLRO',passwd='23094740', db='delsa')
    c = conn.cursor()
    kimoji = random.randint(10,30)
    c.execute("Select `money` from `user` where `cId` = '" + str(chat_id) + "';")
    result = list(c.fetchall())
    if(result[0][0] >= 30):
        c.execute("UPDATE `user` set `money` = `money` - 30 , `kimoji` = `kimoji` +"+ str(kimoji) +" where `cId` = '" + str(chat_id) + "';")
        conn.commit()
        food = ["泡麵","冰棒","飲料"]
        bot.sendMessage(chat_id,"買了"+ food[random.randint(0,2)]+"吃，心情上升"+str(kimoji))
    else:
        bot.sendMessage(chat_id,"窮鬼，你根本沒有錢")
    
    
    conn.close()
def canAct(chat_id):
    # ttmp = datetime.datetime.now()
    # nowtime = (int(ttmp.strftime("%H")) + 8) % 24
    print(nowtime)
    stmp = "現在可以進行的活動有:\n"
    if nowtime == 6:
        bot.sendMessage(chat_id,stmp + "朝會\n掃地\n運動" )
        nowCmd[str(chat_id)] = "/act6"
    elif nowtime == 7:
        bot.sendMessage(chat_id,stmp + "吃飯" )
        nowCmd[str(chat_id)] = "/act7"
    elif nowtime == 8:
        bot.sendMessage(chat_id,stmp + "上課\n掃地\n出公差\n運動" )
        nowCmd[str(chat_id)] = "/act8"
    elif nowtime == 9:
        bot.sendMessage(chat_id,stmp + "上課\n掃地\n出公差\n運動" )
        nowCmd[str(chat_id)] = "/act9"
    elif nowtime == 10:
        bot.sendMessage(chat_id,stmp + "上課\n掃地\n出公差\n運動" )
        nowCmd[str(chat_id)] = "/act10"
    elif nowtime == 11:
        bot.sendMessage(chat_id,stmp + "上課\n掃地\n出公差\n運動" )
        nowCmd[str(chat_id)] = "/act11"
    elif nowtime == 12:
        bot.sendMessage(chat_id,stmp + "吃飯" )
        nowCmd[str(chat_id)] = "/act12"
    elif nowtime == 13:
        bot.sendMessage(chat_id,stmp + "睡覺\n讀書" )
        nowCmd[str(chat_id)] = "/act13"
    elif nowtime == 14:
        bot.sendMessage(chat_id,stmp + "上課\n掃地\n出公差\n運動" )
        nowCmd[str(chat_id)] = "/act14"
    elif nowtime == 15:
        bot.sendMessage(chat_id,stmp + "上課\n掃地\n出公差\n運動" )
        nowCmd[str(chat_id)] = "/act15"
    elif nowtime == 16:
        bot.sendMessage(chat_id,stmp + "上課\n掃地\n出公差\n運動" )
        nowCmd[str(chat_id)] = "/act16"
    elif nowtime == 17:
        bot.sendMessage(chat_id,stmp + "上課\n掃地\n出公差\n運動" )
        nowCmd[str(chat_id)] = "/act17"
    elif nowtime == 18:
        bot.sendMessage(chat_id,stmp + "吃飯" )
        nowCmd[str(chat_id)] = "/act18"
    elif nowtime == 19:
        bot.sendMessage(chat_id,stmp + "洗澡" )
        nowCmd[str(chat_id)] = "/act19"
    elif nowtime == 20:
        bot.sendMessage(chat_id,stmp + "滑手機" )
        nowCmd[str(chat_id)] = "/act20"
    else:
        bot.sendMessage(chat_id,"現在應該是要躺平囉" )


def decreaseWaterPeriod():
    conn = pymysql.connect(host='localhost', user='PLRO',passwd='23094740', db='delsa')
    c = conn.cursor()
    inttmp = 0
    inttmpwater = 0
    if temperature > 26:
        inttmp = inttmp + 1
    if temperature > 30:
        inttmp = inttmp + 1
    if weather == "晴":
        inttmp = inttmp + 1
    c.execute("Select * from `user` where 1;")
    result = list(c.fetchall())
    # print(result)
    
    for i in result:
        inttmp = inttmp + random.randint(5,10)
        inttmpwater = inttmpwater + random.randint(1,3)
        # print(list(i))
        c.execute("UPDATE `user` set `water` = `water` - " +str(inttmp)+ " where `cId` = "+ list(i)[1] +";")
        c.execute("UPDATE `user` set `kimoji` = `kimoji` - " +str(inttmpwater)+ " where `cId` = "+ list(i)[1] +";")
        c.execute("UPDATE `user` set `water` = 0 where `water` < 0 and `cId` = "+ list(i)[1] +";")
        conn.commit()
    conn.close()

def drinkWater(chat_id):
    conn = pymysql.connect(host='localhost', user='PLRO',passwd='23094740', db='delsa')
    c = conn.cursor()
    c.execute("UPDATE `user` set `water` = `water` + 10 where `cId` = "+ str(chat_id) +";")
    conn.commit()
    c.execute("UPDATE `user` set `water` = 100 where `cId` = "+ str(chat_id) +" and `water` > 100;")
    conn.commit()
    c.execute("UPDATE `user` set `water` = 0 where `cId` = "+ str(chat_id) +" and `water` < 0;")
    conn.commit()
    conn.close()
    bot.sendMessage(chat_id, '咕嚕咕嚕咕嚕，水份回復了')

def deleteAccount(chat_id):
    conn = pymysql.connect(host='localhost', user='PLRO',passwd='23094740', db='delsa')
    c = conn.cursor()
    c.execute("delete from `user` where `cId` = "+ str(chat_id) +";")
    conn.commit()
    conn.close()
def createAccount(chat_id):
    conn = pymysql.connect(host='localhost', user='PLRO',passwd='23094740', db='delsa')
    c = conn.cursor()
    c.execute("INSERT INTO `user` (`id`, `cId`, `nickname`, `HP`, `water` ,`kimoji`, `strength` , `dexterity` , `intelligent`, `money`, `level` , `canDo`) VALUES (NULL, '"+ str(chat_id) +"', '"+ str(nowNew[str(chat_id)]) +"', '100', '100','100' , '"+ str(newS[str(chat_id)]) +"', '"+ str(newD[str(chat_id)]) +"', '"+ str(newI[str(chat_id)]) +"', '0', '二兵','1');")
    conn.commit()
    conn.close()

def checkHasAccount(chat_id):
    conn = pymysql.connect(host='localhost', user='PLRO',passwd='23094740', db='delsa')
    c = conn.cursor()
    c.execute("Select `cId` from `user` where `cId` = '" + str(chat_id) + "';")
    result = list(c.fetchall())
    conn.close()
    if(len(result) == 0):
        return False
    else:
        return True


def showStatus(chat_id):
    conn = pymysql.connect(host='localhost', user='PLRO',passwd='23094740', db='delsa')
    c = conn.cursor()
    c.execute("Select * from `user` where `cId` = '" + str(chat_id) + "';")
    tmp = c.fetchall()
    if len(tmp) > 0:
        # print(tmp)
        result = [list(i) for i in list(tmp)][0]
        strtmp ="你的ID : " + str(result[1]) + "\n你的暱稱 : " + str(result[2]) + "\n你的體力 : "
        strtmp = strtmp + '♥'*(result[3]//10) + '♡'*(10-result[3]//10) +"\n你的水份 : " + '♥'*(result[4]//10) + '♡'*(10-result[4]//10) +"\n你的心情 : " + '♥'*(result[5]//10) + '♡'*(10-result[5]//10) 
        strtmp = strtmp +"\n你的力量 : " + str(result[6]) + "\n你的敏捷 : " + str(result[7]) + "\n你的智慧 : " + str(result[8]) + "\n你的錢錢 : " + str(result[9]) + "\n你的職階 : " + str(result[10])
        # print(result)
        bot.sendMessage(chat_id, strtmp)
    else:
        bot.sendMessage(chat_id, '還不趕快加入國軍')

    conn.close()

def clean(chat_id):
    conn = pymysql.connect(host='localhost', user='PLRO',passwd='23094740', db='delsa')
    c = conn.cursor()
    c.execute("Select `dexterity` from `user` where `cId` = '" + str(chat_id) + "';")
    result = list(c.fetchall())
    per = int(result[0][0]) // 10 + random.randint(1,100)
    HP = random.randint(1,10)
    DEX = random.randint(1,3)
    kimoji = 0
    if per <= 10:
        HP = HP + 10
        kimoji = kimoji - random.randint(1,5)
        bot.sendMessage(chat_id, '掃地摸魚摸到大白鯊了...\n體力減少'+ str(HP) +'\n心情下降'+ str(kimoji*-1) +'\n敏捷增加'+str(DEX))
    elif per <= 20:
        HP = HP + 5
        bot.sendMessage(chat_id, '在班長的監督下掃完了\n體力減少'+ str(HP) +'\n敏捷增加'+str(DEX))
    elif per <= 50:
        DEX = DEX + 1
        bot.sendMessage(chat_id, '隨便掃掃\n體力減少'+ str(HP) +'\n敏捷增加'+str(DEX))
    elif per <= 80:
        DEX = DEX + random.randint(1,3)
        bot.sendMessage(chat_id, '快速地掃了掃\n體力減少'+ str(HP) +'\n敏捷增加'+str(DEX))
    elif per <= 90:
        HP = 0
        DEX = DEX + random.randint(1,3)
        bot.sendMessage(chat_id, '摸魚沒被抓到\n敏捷增加'+str(DEX))
    else:
        HP = random.randint(1,10)
        kimoji = random.randint(1,5)
        bot.sendMessage(chat_id, '掃完地，長官請吃東西\n體力增加'+str(HP)+'\n敏捷增加'+str(DEX) + '\n心情上升' + str(kimoji))
        HP = HP * -1
    c.execute("UPDATE `user` set `HP` = `HP` - "+ str(HP) +" ,`dexterity` = `dexterity` + " + str(DEX)+ ",`kimoji` = `kimoji` + " + str(kimoji) +" where `cId` = "+ str(chat_id) +";")
    c.execute("UPDATE `user` set `canDo` = 0 where `cId` = '" + str(chat_id) + "';")
    conn.commit()
    
    conn.close()
def eat(chat_id):
    conn = pymysql.connect(host='localhost', user='PLRO',passwd='23094740', db='delsa')
    c = conn.cursor()
    c.execute("Select `strength`,`dexterity`,`intelligent` from `user` where `cId` = '" + str(chat_id) + "';")
    result = list(c.fetchall())
    per = (int(result[0][0]) + int(result[0][1]) + int(result[0][2])) // 30 + random.randint(1,100)
    HP = 20
    kimoji = 0
    if per <= 10:
        kimoji = kimoji - random.randint(1,5)
        bot.sendMessage(chat_id, '今天的餐點真難吃...\n體力增加'+ str(HP) +'\n心情下降'+ str(kimoji*-1))
    elif per <= 50:
        HP = HP + random.randint(1,10)
        bot.sendMessage(chat_id, '今天的餐點還能接受\n體力增加'+ str(HP))
    elif per <= 90:
        HP = HP +random.randint(10,20)
        bot.sendMessage(chat_id, '今天的餐點真好吃\n體力增加'+str(HP))
    else:
        HP = HP +random.randint(10,30)
        kimoji = random.randint(1,5)
        bot.sendMessage(chat_id, '好久沒吃這麼好了\n體力增加' + str(HP) + '\n心情上升' + str(kimoji))
    c.execute("UPDATE `user` set `HP` = `HP` + "+ str(HP) +",`kimoji` = `kimoji` + " + str(kimoji) +" where `cId` = "+ str(chat_id) +";")
    c.execute("UPDATE `user` set `canDo` = 0 where `cId` = '" + str(chat_id) + "';")
    conn.commit()
    
    conn.close()
def tolerance(chat_id):
    conn = pymysql.connect(host='localhost', user='PLRO',passwd='23094740', db='delsa')
    c = conn.cursor()
    c.execute("Select `strength`,`dexterity`,`intelligent` from `user` where `cId` = '" + str(chat_id) + "';")
    result = list(c.fetchall())
    per = (int(result[0][0]) + int(result[0][1]) + int(result[0][2])) // 30 + random.randint(1,100)
    HP = 20
    kimoji = 0
    money = 10
    if per <= 10:
        kimoji = kimoji - random.randint(1,5)
        money = money + random.randint(1,5)
        bot.sendMessage(chat_id, '今天出的公差超累...\n體力減少'+ str(HP) +'\n心情下降'+ str(kimoji*-1) + '\n錢錢增加' + str(money))
    elif per <= 50:
        HP = HP - random.randint(1,10)
        money = money + random.randint(1,10)
        bot.sendMessage(chat_id, '今天出的公差好忙\n體力減少'+ str(HP)+ '\n錢錢增加' + str(money))
    elif per <= 90:
        HP = HP - random.randint(10,20)
        money = money + random.randint(1,10)
        bot.sendMessage(chat_id, '今天公差沒什麼事情\n體力減少'+str(HP)+ '\n錢錢增加' + str(money))
    else:
        HP = HP -random.randint(10,20)
        kimoji = random.randint(1,5)
        money = money + random.randint(1,10)
        bot.sendMessage(chat_id, '今天出到爽差好開心唷\n體力減少' + str(HP) + '\n心情上升' + str(kimoji)+ '\n錢錢增加' + str(money))
    c.execute("UPDATE `user` set `HP` = `HP` - "+ str(HP) +",`kimoji` = `kimoji` + " + str(kimoji)+",`money` = `money` + " + str(money) +" where `cId` = "+ str(chat_id) +";")
    c.execute("UPDATE `user` set `canDo` = 0 where `cId` = '" + str(chat_id) + "';")
    conn.commit()
    
    conn.close()

def sport(chat_id):
    conn = pymysql.connect(host='localhost', user='PLRO',passwd='23094740', db='delsa')
    c = conn.cursor()
    c.execute("Select `strength` from `user` where `cId` = '" + str(chat_id) + "';")
    result = list(c.fetchall())
    per = int(result[0][0]) // 10 + random.randint(1,100)
    HP = random.randint(1,10)
    STR = random.randint(1,3)
    kimoji = 0
    if per <= 10:
        HP = HP + 10
        kimoji = kimoji - random.randint(1,5)
        bot.sendMessage(chat_id, '跑了五千公尺好累喔...\n體力減少'+ str(HP) +'\n心情下降'+ str(kimoji*-1) +'\n力量增加'+str(STR))
    elif per <= 20:
        HP = HP + 5
        bot.sendMessage(chat_id, '行軍真累\n體力減少'+ str(HP) +'\n力量增加'+str(STR))
    elif per <= 50:
        STR = STR + 1
        bot.sendMessage(chat_id, '今天行軍只走一點點路\n體力減少'+ str(HP) +'\n力量增加'+str(STR))
    elif per <= 80:
        STR = STR + random.randint(1,3)
        bot.sendMessage(chat_id, '今天只有跑一點點步\n體力減少'+ str(HP) +'\n力量增加'+str(STR))
    elif per <= 90:
        HP = 0
        STR = STR + random.randint(1,3)
        bot.sendMessage(chat_id, '打躲避球YA\n力量增加'+str(STR))
    else:
        HP = random.randint(1,10)
        kimoji = random.randint(1,5)
        bot.sendMessage(chat_id, '因為跟長官去踢足球，還踢得不錯，可以跟長官一起吃東西\n體力增加'+str(HP)+'\n力量增加'+str(STR) + '\n心情上升' + str(kimoji))
        HP = HP * -1
    c.execute("UPDATE `user` set `HP` = `HP` - "+ str(HP) +" ,`strength` = `strength` + " + str(STR)+ ",`kimoji` = `kimoji` + " + str(kimoji) +" where `cId` = "+ str(chat_id) +";")
    c.execute("UPDATE `user` set `canDo` = 0 where `cId` = '" + str(chat_id) + "';")
    conn.commit()
    
    conn.close()

def learn(chat_id):
    conn = pymysql.connect(host='localhost', user='PLRO',passwd='23094740', db='delsa')
    c = conn.cursor()
    c.execute("Select `intelligent` from `user` where `cId` = '" + str(chat_id) + "';")
    result = list(c.fetchall())
    per = int(result[0][0]) // 10 + random.randint(1,100)
    HP = random.randint(1,10)
    INT = random.randint(1,3)
    kimoji = 0
    if per <= 10:
        HP = HP + 10
        kimoji = kimoji - random.randint(1,5)
        bot.sendMessage(chat_id, '背誦單兵作戰的口訣真困難呀...\n體力減少'+ str(HP) +'\n心情下降'+ str(kimoji*-1) +'\n智力增加'+str(INT))
    elif per <= 20:
        HP = HP + 5
        bot.sendMessage(chat_id, '背誦槍枝資訊真麻煩\n體力減少'+ str(HP) +'\n智力增加'+str(INT))
    elif per <= 50:
        INT = INT + 1
        bot.sendMessage(chat_id, '軍歌沒有很好記啊\n體力減少'+ str(HP) +'\n智力增加'+str(INT))
    elif per <= 80:
        INT = INT + random.randint(1,3)
        bot.sendMessage(chat_id, '槍枝拆解真輕鬆\n體力減少'+ str(HP) +'\n智力增加'+str(INT))
    elif per <= 90:
        HP = 0
        INT = INT + random.randint(1,3)
        bot.sendMessage(chat_id, '沒要上課，無聊看看書\n智力增加'+str(INT))
    else:
        HP = random.randint(1,10)
        kimoji = random.randint(1,5)
        bot.sendMessage(chat_id, '在教室內看書\n體力增加'+str(HP)+'\n智力增加'+str(INT) + '\n心情上升' + str(kimoji))
        HP = HP * -1
    c.execute("UPDATE `user` set `HP` = `HP` - "+ str(HP) +" ,`intelligent` = `intelligent` + " + str(INT)+ ",`kimoji` = `kimoji` + " + str(kimoji) +" where `cId` = "+ str(chat_id) +";")
    c.execute("UPDATE `user` set `canDo` = 0 where `cId` = '" + str(chat_id) + "';")
    conn.commit()
    
    conn.close()

def morning(chat_id):
    conn = pymysql.connect(host='localhost', user='PLRO',passwd='23094740', db='delsa')
    c = conn.cursor()
    c.execute("Select `intelligent` from `user` where `cId` = '" + str(chat_id) + "';")
    result = list(c.fetchall())
    per = int(result[0][0]) // 10 + random.randint(1,100)
    HP = random.randint(1,10)
    INT = random.randint(1,3)
    kimoji = 0
    if per <= 10:
        HP = HP + 10
        kimoji = kimoji - random.randint(1,5)
        bot.sendMessage(chat_id, '被一堆蚊子叮，真煩\n體力減少'+ str(HP) +'\n心情下降'+ str(kimoji*-1) +'\n智力增加'+str(INT))
    elif per <= 50:
        INT = INT + 1
        bot.sendMessage(chat_id, '做白日夢...\n體力減少'+ str(HP) +'\n智力增加'+str(INT))
    elif per <= 80:
        INT = INT + random.randint(1,3)
        bot.sendMessage(chat_id, '東想想西想想\n體力減少'+ str(HP) +'\n智力增加'+str(INT))
    else:
        HP = random.randint(1,10)
        kimoji = random.randint(1,5)
        bot.sendMessage(chat_id, '朝會一下子就結束了\n體力增加'+str(HP)+'\n智力增加'+str(INT) + '\n心情上升' + str(kimoji))
        HP = HP * -1
    c.execute("UPDATE `user` set `HP` = `HP` - "+ str(HP) +" ,`intelligent` = `intelligent` + " + str(INT)+ ",`kimoji` = `kimoji` + " + str(kimoji) +" where `cId` = "+ str(chat_id) +";")
    c.execute("UPDATE `user` set `canDo` = 0 where `cId` = '" + str(chat_id) + "';")
    conn.commit()
    
    conn.close()

def takeBreak(chat_id):
    conn = pymysql.connect(host='localhost', user='PLRO',passwd='23094740', db='delsa')
    c = conn.cursor()
    HP = str(random.randint(10,30))
    bot.sendMessage(chat_id, 'Zzzz....\n體力增加'+str(HP))
    c.execute("UPDATE `user` set `HP` = `HP` + "+ str(HP) +" where `cId` = "+ str(chat_id) +";")
    c.execute("UPDATE `user` set `canDo` = 0 where `cId` = '" + str(chat_id) + "';")
    conn.commit()
    conn.close()

def read(chat_id):
    conn = pymysql.connect(host='localhost', user='PLRO',passwd='23094740', db='delsa')
    c = conn.cursor()
    INT = random.randint(1,5)
    bot.sendMessage(chat_id, '看書中...\n智力增加'+str(INT))
    c.execute("UPDATE `user` set `intelligent` = `intelligent` + "+ str(INT) +" where `cId` = "+ str(chat_id) +";")
    c.execute("UPDATE `user` set `canDo` = 0 where `cId` = '" + str(chat_id) + "';")
    conn.commit()
    conn.close()

def shower(chat_id):
    conn = pymysql.connect(host='localhost', user='PLRO',passwd='23094740', db='delsa')
    c = conn.cursor()
    c.execute("Select `strength`,`dexterity`,`intelligent` from `user` where `cId` = '" + str(chat_id) + "';")
    result = list(c.fetchall())
    per = (int(result[0][0]) + int(result[0][1]) + int(result[0][2])) // 30 + random.randint(1,100)
    HP = 10
    kimoji = 0
    if per <= 10:
        HP = HP - random.randint(1,10)
        kimoji = kimoji - random.randint(1,5)
        bot.sendMessage(chat_id, '哇...剛洗完澡就被叫去搬東西...\n體力增加'+ str(HP) +'\n心情下降'+ str(kimoji*-1))
    elif per <= 50:
        HP = HP + random.randint(1,5)
        bot.sendMessage(chat_id, '洗澡的隊伍有點長...\n體力增加'+ str(HP))
    else:
        HP = HP +random.randint(5,10)
        bot.sendMessage(chat_id, '很快就輪到洗澡了\n體力增加'+str(HP))
    c.execute("UPDATE `user` set `HP` = `HP` + "+ str(HP) +",`kimoji` = `kimoji` + " + str(kimoji) +" where `cId` = "+ str(chat_id) +";")
    c.execute("UPDATE `user` set `canDo` = 0 where `cId` = '" + str(chat_id) + "';")
    conn.commit()
    
    conn.close()

def phone(chat_id):
    conn = pymysql.connect(host='localhost', user='PLRO',passwd='23094740', db='delsa')
    c = conn.cursor()
    HP = random.randint(10,20)
    bot.sendMessage(chat_id, '摸到久違的手機了\n體力增加'+str(HP))
    c.execute("UPDATE `user` set `HP` = `HP` + "+ str(HP) +" where `cId` = "+ str(chat_id) +";")
    c.execute("UPDATE `user` set `canDo` = 0 where `cId` = '" + str(chat_id) + "';")
    conn.commit()
    conn.close()


# content of the automatic reply
def handle(msg):
    global cmd, nowCmd, conn, nowNew, newS, newD, newI , nowtime ,weather
    content_type, chat_type, chat_id = telepot.glance(msg)
    print(type(chat_id))
    cmd_id = str(chat_id)
    print(msg)
    if checkStatus(chat_id):
        return
    AClist = ['/new','/suicide','/activity','/status','/drink','/guard','/start','/shop']
    if not cmd_id in nowCmd.keys():
        nowCmd[cmd_id] = ''
    print(nowCmd[cmd_id])
    if nowCmd[cmd_id] in ['/new1','/new2'] and msg['text'] in AClist:
        nowCmd[cmd_id] = ''
        nowNew[cmd_id] = ''
        bot.sendMessage(chat_id, '創角失敗')
    if nowCmd[cmd_id] == '/suicide' and msg['text'] in AClist:
        nowCmd[cmd_id] = ''
        bot.sendMessage(chat_id, '停止自殺')
    if nowCmd[cmd_id] in ['/drinkT','/drinkB','/drinkD','/drinkDD'] and msg['text'] in AClist:
        nowCmd[cmd_id] = ''
        bot.sendMessage(chat_id, '連喝水都不會，你還會做什麼啊')
    if nowCmd[cmd_id][:4] == "/act" and msg['text'] in AClist:
        nowCmd[cmd_id] = ''
        bot.sendMessage(chat_id, '啊你怎麼跑去做別的事情了呀')
    if nowCmd[cmd_id] == "/shop" and msg['text'] in AClist:
        nowCmd[cmd_id] = ''
        bot.sendMessage(chat_id, '不買快樂了唷?')
        
    if msg['text'] == '/start':
        bot.sendMessage(chat_id, '歡迎來到當兵模擬器')
        nowCmd[cmd_id] = ''
    elif nowCmd[cmd_id] == '/new1':
        nowNew[cmd_id] = msg['text']
        nowCmd[cmd_id] = '/new2'
        newS[cmd_id] = random.randint(1,6)
        newD[cmd_id] = random.randint(1,6)
        newI[cmd_id] = random.randint(1,6)
        bot.sendMessage(chat_id, '以下為你的能力值，請問滿意嗎?(都是隨機1~6)\n力量 : ' + str(newS[cmd_id]) + '\n敏捷 : ' + str(newD[cmd_id]) + '\n智力 : ' + str(newI[cmd_id]))
        bot.sendMessage(chat_id, '不滿意請輸入N，滿意請輸入Y')

    elif nowCmd[cmd_id] == '/new2':
        if(msg['text'] == 'Y' or msg['text'] == 'y'):
            nowCmd[cmd_id] = ''
            createAccount(chat_id)
            bot.sendMessage(chat_id, '加入迷彩，人生精彩')

        elif(msg['text'] == 'N' or msg['text'] == 'n'):
            newS[cmd_id] = random.randint(1,6)
            newD[cmd_id] = random.randint(1,6)
            newI[cmd_id] = random.randint(1,6)
            bot.sendMessage(chat_id, '以下為你的能力值，請問滿意嗎?(都是隨機1~6)\n力量 : ' + str(newS[cmd_id]) + '\n敏捷 : ' + str(newD[cmd_id]) + '\n智力 : ' + str(newI[cmd_id]))
            bot.sendMessage(chat_id, '不滿意請輸入N，滿意請輸入Y')
    
    elif nowCmd[cmd_id] == '/suicide' :
        if(msg['text'] == 'Y' or msg['text'] == 'y'):
            deleteAccount(chat_id)
            nowCmd[cmd_id] = ''
            bot.sendMessage(chat_id, '人生五十年，如夢似幻；一度得生者，豈有不滅者乎?')

        elif(msg['text'] == 'N' or msg['text'] == 'n'):
            bot.sendMessage(chat_id, '再努力掙扎一下吧騷年')
            nowCmd[cmd_id] = ''
            
    elif nowCmd[cmd_id] == '/drinkT':
        if(msg['text'] == '取出水壺'):
            bot.sendMessage(chat_id, '打開瓶蓋')
            nowCmd[cmd_id] = '/drinkB'
    elif nowCmd[cmd_id] == '/drinkB':
        if(msg['text'] == '打開瓶蓋'):
            bot.sendMessage(chat_id, '操課前飲水500cc')
            nowCmd[cmd_id] = '/drinkD'
    elif nowCmd[cmd_id] == '/drinkD':
        if(msg['text'] == '操課前飲水500cc'):
            bot.sendMessage(chat_id, '喝水')
            nowCmd[cmd_id] = '/drinkDD'
    elif nowCmd[cmd_id] == '/drinkDD':
            drinkWater(chat_id)
            nowCmd[cmd_id] = ''
    elif nowCmd[cmd_id][0:4] == '/act':

        print(nowtime,nowCmd[cmd_id][4:])
        if nowCmd[cmd_id][4:] == str(nowtime):
            if msg['text'] == '掃地' and nowCmd[cmd_id][4:] in ['6','8','9','10','11','14','15','16','17'] and HPEnough(chat_id):
                clean(chat_id)
                nowCmd[cmd_id] = ''
            elif msg['text'] == '吃飯' and nowCmd[cmd_id][4:] in ['7','12','18']:
                eat(chat_id)
                nowCmd[cmd_id] = ''
            elif msg['text'] == '運動' and nowCmd[cmd_id][4:] in ['6','8','9','10','11','14','15','16','17'] and HPEnough(chat_id):
                if "雨" in weather:
                    bot.sendMessage(chat_id, '下雨天不能運動')
                elif temperature > 30:
                    bot.sendMessage(chat_id, '太熱了，不能運動')
                else:
                    sport(chat_id)
                    nowCmd[cmd_id] = ''
            elif msg['text'] == '上課' and nowCmd[cmd_id][4:] in ['8','9','10','11','14','15','16','17'] and HPEnough(chat_id):
                learn(chat_id)
                nowCmd[cmd_id] = ''
            elif msg['text'] == '出公差' and nowCmd[cmd_id][4:] in ['8','9','10','11','14','15','16','17'] and HPEnough(chat_id):
                tolerance(chat_id)
                nowCmd[cmd_id] = ''
            elif msg['text'] == '朝會' and nowCmd[cmd_id][4:] in ['6'] and HPEnough(chat_id):
                if "雨" in weather:
                    bot.sendMessage(chat_id, '下雨天沒有朝會')
                else:
                    morning(chat_id)
                    nowCmd[cmd_id] = ''
            elif msg['text'] == '睡覺' and nowCmd[cmd_id][4:] in ['13']:
                takeBreak(chat_id)
                nowCmd[cmd_id] = ''
            elif msg['text'] == '讀書' and nowCmd[cmd_id][4:] in ['13']:
                read(chat_id)
                nowCmd[cmd_id] = ''
            elif msg['text'] == '洗澡' and nowCmd[cmd_id][4:] in ['19']:
                shower(chat_id)
                nowCmd[cmd_id] = ''
            elif msg['text'] == '滑手機' and nowCmd[cmd_id][4:] in ['20']:
                phone(chat_id)
                nowCmd[cmd_id] = ''
            else:
                bot.sendMessage(chat_id, '現在沒有這個選項')
        else:
            bot.sendMessage(chat_id, '指令已過時，請再次下/activity')
    elif nowCmd[cmd_id] == '/shop' :
        if(msg['text'] == 'Y' or msg['text'] == 'y'):
            happy(chat_id)
            nowCmd[cmd_id] = ''

        elif(msg['text'] == 'N' or msg['text'] == 'n'):
            bot.sendMessage(chat_id, '你很快就會回來的')
            nowCmd[cmd_id] = ''
    elif nowCmd[cmd_id] == '/settime' :
        nowCmd[cmd_id] = ''
        nowtime = int(msg['text'])
    elif nowCmd[cmd_id] == '/setweather' :
        nowCmd[cmd_id] = ''
        weather = msg['text']


            
    else:
        if msg['text'] == '/new':
            if(checkHasAccount(chat_id)):
                bot.sendMessage(chat_id, '你已經是軍人了')
            else:
                # createAccount(chat_id)
                bot.sendMessage(chat_id, '開始登記資料')
                bot.sendMessage(chat_id, '請輸入你想要的稱呼')
                nowNew[cmd_id]=""
                nowCmd[cmd_id]="/new1"
                
        elif msg['text'] == '/suicide':
            if(checkHasAccount(chat_id)):
                bot.sendMessage(chat_id, "你真的想不開嗎?")
                bot.sendMessage(chat_id, "如果是請輸入Y，如果還想活請輸入N")
                nowCmd[cmd_id]="/suicide"
            else:
                bot.sendMessage(chat_id, "你根本沒有開始遊戲")
        elif msg['text'] == '/status':
            showStatus(chat_id)
        elif msg['text'] == '/activity':
            if(checkHasAccount(chat_id)):
                if checkCanDo(chat_id):
                    canAct(chat_id)
                else:
                    bot.sendMessage(chat_id, "你已經行動過了，每個整點、15分、30分、45分可以再行動一次")
            else:
                bot.sendMessage(chat_id, "你根本沒有開始遊戲")
            

        elif msg['text'] == '/drink':
            if(checkHasAccount(chat_id)):
                bot.sendMessage(chat_id, "單兵注意，操課前飲水500cc(接下來請跟著複誦)")
                bot.sendMessage(chat_id, "取出水壺")
                nowCmd[cmd_id] = '/drinkT'
            else:
                bot.sendMessage(chat_id, "你根本沒有開始遊戲")
        elif msg['text'] == '/shop':
            if(checkHasAccount(chat_id)):
                bot.sendMessage(chat_id, "確定要30$買快樂?")
                bot.sendMessage(chat_id, "如果是請輸入Y，如果沒有請輸入N")
                nowCmd[cmd_id] = '/shop'
            else:
                bot.sendMessage(chat_id, "你根本沒有開始遊戲")
        elif msg['text'] == '/guard' and (chat_id == 662368163 or chat_id == 684335853 or chat_id == 648113869 or chat_id == 611594121):
            os.system('mpg321 stop.mp3 &')
            TEXT1 = Voice_To_Text()
            print(TEXT1)
            print(type(TEXT1))
            os.system('mpg321 where.mp3 &')
            TEXT2 = Voice_To_Text()
            print(TEXT2)
            os.system('mpg321 what.mp3 &')
            TEXT3 = Voice_To_Text()
            print(TEXT3)
            a = open("test.txt","w+")
            a.write(TEXT1+TEXT2+TEXT3)
            if(str(TEXT1) == cmd1[todayCMD] and str(TEXT2) == cmd2[todayCMD] and str(TEXT3) == cmd3[todayCMD]):
                os.system('mpg321 NMDNNJ.mp3 &')
                print("bingo")
            else:
                print(TEXT1 == cmd1[todayCMD])
                print(TEXT2 == cmd2[todayCMD])
                print(TEXT3 == cmd3[todayCMD])
                print("tingnizaipe")
                os.system('mpg321 pee.mp3 &')
            print(cmd1[todayCMD] + cmd2[todayCMD] + cmd3[todayCMD])
            bot.sendMessage(648113869, TEXT1+TEXT2+TEXT3)
        elif msg['text'] == '/settime' and (chat_id == 662368163 or chat_id == 684335853 or chat_id == 648113869 or chat_id == 611594121):
            bot.sendMessage(chat_id, "請輸入欲調整時間")
            nowCmd[cmd_id] = '/settime'
        elif msg['text'] == '/setweather' and (chat_id == 662368163 or chat_id == 684335853 or chat_id == 648113869 or chat_id == 611594121):
            bot.sendMessage(chat_id, "請輸入欲調整天氣")
            nowCmd[cmd_id] = '/setweather'
        elif msg['text'] == '/recover' and (chat_id == 662368163 or chat_id == 684335853 or chat_id == 648113869 or chat_id == 611594121):
            recover()
            bot.sendMessage(chat_id, "已重置canDo")


global cmd1 , cmd2 , cmd3 ,todayCMD , nowtime
cmd1 = ["黃曉明","周杰倫","陳水扁","大雄","韓國瑜","亂太郎","小紅帽","小叮噹"]
cmd2 = ["在廁所","房間","廚房","海邊","浴室","陽台","森林","鞋櫃"]
cmd3 = ["喝水","唱歌","打電動","做日光浴","摔倒","打嗝","打獵","刷牙"]
todayCMD = 0
nowCmd = {}
nowNew = {}
newS = {}
newD = {}
newI = {}
nowtime = 6
weather = ""
temperature = 20
bot = telepot.Bot('1426207270:AAGjUG2tc40VF0YTMt211N0vWT-ptWZLMJM')
MessageLoop(bot, handle).run_as_thread()
getWeather()
# boardcast()
schedule.every().day.at("22:00").do(recover)
schedule.every().day.at("22:15").do(recover)
schedule.every().day.at("22:30").do(recover)
schedule.every().day.at("22:45").do(recover)
schedule.every().day.at("23:00").do(recover)
schedule.every().day.at("23:15").do(recover)
schedule.every().day.at("23:30").do(recover)
schedule.every().day.at("23:45").do(recover)
schedule.every().day.at("00:00").do(getWeather)
schedule.every().day.at("00:00").do(recover)
schedule.every().day.at("00:15").do(recover)
schedule.every().day.at("00:30").do(recover)
schedule.every().day.at("00:45").do(recover)
# schedule.every().day.at("00:00").do(boardcast)
schedule.every().day.at("01:00").do(recover)
schedule.every().day.at("01:15").do(recover)
schedule.every().day.at("01:30").do(recover)
schedule.every().day.at("01:45").do(recover)
schedule.every().day.at("02:00").do(recover)
schedule.every().day.at("02:15").do(recover)
schedule.every().day.at("02:30").do(recover)
schedule.every().day.at("02:45").do(recover)
schedule.every().day.at("03:00").do(recover)
schedule.every().day.at("03:15").do(recover)
schedule.every().day.at("03:30").do(recover)
schedule.every().day.at("03:45").do(recover)
schedule.every().day.at("04:00").do(recover)
schedule.every().day.at("04:15").do(recover)
schedule.every().day.at("04:30").do(recover)
schedule.every().day.at("04:45").do(recover)
schedule.every().day.at("05:00").do(recover)
schedule.every().day.at("05:15").do(recover)
schedule.every().day.at("05:30").do(recover)
schedule.every().day.at("05:45").do(recover)
schedule.every().day.at("06:00").do(recover)
schedule.every().day.at("06:15").do(recover)
schedule.every().day.at("06:30").do(recover)
schedule.every().day.at("06:45").do(recover)
schedule.every().day.at("07:00").do(recover)
schedule.every().day.at("07:15").do(recover)
schedule.every().day.at("07:30").do(recover)
schedule.every().day.at("07:45").do(recover)
schedule.every().day.at("08:00").do(recover)
schedule.every().day.at("08:15").do(recover)
schedule.every().day.at("08:30").do(recover)
schedule.every().day.at("08:45").do(recover)
schedule.every().day.at("09:00").do(recover)
schedule.every().day.at("09:15").do(recover)
schedule.every().day.at("09:30").do(recover)
schedule.every().day.at("09:45").do(recover)
schedule.every().day.at("10:00").do(recover)
schedule.every().day.at("10:15").do(recover)
schedule.every().day.at("10:30").do(recover)
schedule.every().day.at("10:45").do(recover)
schedule.every().day.at("11:00").do(recover)
schedule.every().day.at("11:15").do(recover)
schedule.every().day.at("11:30").do(recover)
schedule.every().day.at("11:45").do(recover)
schedule.every().day.at("12:00").do(recover)
schedule.every().day.at("12:15").do(recover)
schedule.every().day.at("12:30").do(recover)
schedule.every().day.at("12:45").do(recover)
schedule.every().day.at("13:00").do(recover)
schedule.every().day.at("13:00").do(sleep)
schedule.every(1).minutes.do(decreaseWaterPeriod)
schedule.every(1).minutes.do(recover)
print ('Listening ...')

# Keep the program running.
while 1:
    schedule.run_pending()
    time.sleep(10)