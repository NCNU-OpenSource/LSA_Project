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