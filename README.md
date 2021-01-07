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

### python套件
```
pip3 install telepot
pip3 install pymysql
pip3 install requests
pip3 install SpeechRecognition-3.7.1-py2.py3-none-any.whl
```

### 分工
- 遊戲設計 : 陳柏瑋 60% 楊筱彤 15% 蘇庭玉 15% 徐芳沂 10%
- 網路爬蟲 : 楊筱彤 40% 蘇庭玉 40% 徐芳沂 10% 陳柏瑋 10%
- 語音辨識 : 楊筱彤 45% 蘇庭玉 45% 陳柏瑋 10%
- bot設計 : 徐芳沂 70% 陳柏瑋 30%