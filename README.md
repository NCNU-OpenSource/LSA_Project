# 1091 LSA 期末專題 - 當兵模擬器

## 器材
- 麥克風*1
- 螢幕*1
- Raspberry Pi*1

## 安裝步驟
### 麥克風
PI 接到螢幕上 輸入 alsamixer 確認有沒有抓到 mic(SSH無法使用這方法)
如果沒有
先確認 usb 有沒有偵測到
```
cat /proc/asound/cards
```
![](https://i.imgur.com/Vnko99V.png)

MIC有在2號

```
sudo vim /usr/share/alsa/alsa.conf
```

把
```
defaults.ctl.card 0
defaults.pcm.card 0
```
改成
```
defaults.ctl.card 2
defaults.pcm.card 2
```

再次去alsamixer看應該就有了

### 播音軟體
本次使用 mpg321 作為播放音樂的軟體
安裝:
```
sudo apt install mpg321
```

### 資料庫
- 安裝
```
sudo apt-get install mariadb-server
```
- 設定
```
sudo mysql -u root -p //進入資料庫
```
```sql=
create database tableName; //創建table
CREATE USER 'user'@localhost IDENTIFIED BY 'passwd'; //創建使用者
GRANT ALL PRIVILEGES ON tableName.* TO 'user'@localhost; //給予使用者剛才創造的table權限
```
離開資料庫
- 匯入資料
```
sudo mysql -u root -p tableName < user.sql
```

### python套件
- 先安裝 pip
```
sudo apt install python3-pip
```
- 再來安裝套件
```
pip3 install telepot //連結telegram的
pip3 install pymysql //連結資料庫的
pip3 install requests //爬蟲用
pip3 install SpeechRecognition //語音辨識
pip3 install schedule //語音辨識
```
### telegram BOT
- 到 telegram 搜尋 @BotFather
![]https://i.imgur.com/Hep0M8H.png
- 然後按 /start
![]https://i.imgur.com/I3ASL0B.png
- 創造機器人 /newbot
- 輸入機器人的名字
- 輸入機器人的username
- 成功後即可獲得機器人的連結&token
![](https://i.imgur.com/ira9u05.png)
- token要丟到 `solider.py` 裡面的 bot = telepot.Bot('Your_Bot_Key')
- 接下來輸入 /mybots
- 然後選擇剛才創造的bot
- Edit bot -> Edit Commands
- 輸入以下
```
new - 創造新的軍職生涯
suicide - 這個軍職生涯我不想要了
status - 查看現在的狀態
activity - 進行活動
drink - 喝水
shop - 購買點心
```
### 執行
```
python3 solider.py
```
### 分工
- 遊戲設計 : 陳柏瑋 60% 楊筱彤 15% 蘇庭玉 15% 徐芳沂 10%
- 網路爬蟲 : 楊筱彤 40% 蘇庭玉 40% 徐芳沂 10% 陳柏瑋 10%
- 語音辨識 : 楊筱彤 45% 蘇庭玉 45% 陳柏瑋 10%
- bot設計 : 徐芳沂 70% 陳柏瑋 30%