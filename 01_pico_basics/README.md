# Pico 基礎模組

歡迎來到 Raspberry Pi Pico 基礎模組！這個模組將帶你從零開始學習 Pico 的基本操作。

## 模組概覽

本模組包含三個主要單元：

### 📚 學習單元

1. **[LED 閃爍](01_led_blink/README.md)** - Day 1 上午
   - GPIO 基礎概念
   - 數位輸出控制
   - MicroPython 基礎語法
   - 時間控制

2. **[內建感測器](02_onboard_sensor/README.md)** - Day 1 下午 & Day 2 上午
   - ADC（類比數位轉換）
   - 溫度感測器讀取
   - 資料處理和平滑
   - JSON 格式化

3. **[按鈕輸入](03_button_input/README.md)** - Day 2 下午
   - 數位輸入讀取
   - 防彈跳處理
   - 中斷處理
   - 按鈕控制應用

## 學習目標

完成本模組後，你將能夠：

- ✅ 設定 Pico 開發環境
- ✅ 使用 MicroPython 編寫程式
- ✅ 控制 GPIO 進行輸入輸出
- ✅ 讀取內建感測器資料
- ✅ 處理和格式化感測器資料
- ✅ 實作按鈕輸入和控制邏輯
- ✅ 理解中斷和防彈跳技術

## 開始之前

### 硬體準備

**必要：**
- Raspberry Pi Pico W（注意：必須是 W 版本，有 WiFi）
- USB 連接線（支援資料傳輸）
- 電腦（Windows / Mac / Linux）

**選用：**
- 麵包板
- 按鈕開關
- LED 燈
- 跳線

### 軟體準備

1. **安裝 Thonny IDE**
   - 下載：https://thonny.org/
   - Raspberry Pi OS 通常已預裝

2. **安裝 MicroPython 韌體**
   - 下載 Pico W 韌體：https://micropython.org/download/rp2-pico-w/
   - 按住 BOOTSEL 按鈕，連接 USB
   - 將 .uf2 檔案拖曳到 Pico 磁碟機

3. **設定 Thonny**
   - 開啟 Thonny
   - 右下角選擇 "MicroPython (Raspberry Pi Pico)"
   - 選擇正確的 USB 連接埠

詳細設定步驟請參考：[SETUP.md](../SETUP.md)

## 學習路徑

### 第一階段：Pico 入門

**學習內容：**
- 課程介紹與環境檢查
- LED 閃爍基礎
- LED 進階練習
- MicroPython 基礎
- 按鈕輸入處理
- 總結

**學習重點：**
- 完成環境設定
- 理解 GPIO 概念
- 掌握基本程式結構

### 第二階段：感測器與資料處理

**學習內容：**
- 複習與問題解答
- 內建溫度感測器
- 資料處理與格式化
- 計時器和排程
- 錯誤處理與除錯
- 綜合練習

**學習重點：**
- ADC 和感測器讀取
- 資料平滑和格式化
- 物件導向程式設計

## 快速開始

### 1. 測試環境

執行第一個程式確認環境正常：

```python
# 在 Thonny Shell 中輸入
print("Hello, Pico!")
```

### 2. LED 閃爍

```python
import machine
import time

led = machine.Pin("LED", machine.Pin.OUT)

while True:
    led.toggle()
    time.sleep(1)
```

### 3. 讀取溫度

```python
import machine

sensor = machine.ADC(4)
adc_value = sensor.read_u16()
voltage = adc_value * (3.3 / 65535)
temperature = 27 - (voltage - 0.706) / 0.001721

print(f"溫度: {temperature:.2f}°C")
```

## 重要概念速查

### GPIO 模式

```python
import machine

# 輸出模式
led = machine.Pin(15, machine.Pin.OUT)
led.on()   # 設為 HIGH
led.off()  # 設為 LOW

# 輸入模式（上拉電阻）
button = machine.Pin(14, machine.Pin.IN, machine.Pin.PULL_UP)
state = button.value()  # 讀取狀態
```

### ADC 讀取

```python
import machine

# 初始化 ADC
adc = machine.ADC(pin_number)

# 讀取值（0-65535）
value = adc.read_u16()
```

### 時間函式

```python
import time

time.sleep(1)        # 暫停 1 秒
time.sleep_ms(100)   # 暫停 100 毫秒
time.sleep_us(10)    # 暫停 10 微秒

ms = time.ticks_ms() # 取得毫秒計時器
```

## 練習專題

完成基礎學習後，挑戰這些專題：

### 🎯 專題 1：溫度監控器

**需求：**
- 持續監控溫度
- 超過閾值時 LED 閃爍警告
- 顯示最高、最低、平均溫度

**提示：**
- 使用 SensorReader 類別
- 實作閾值檢查
- 記錄歷史資料

### 🎯 專題 2：互動式選單

**需求：**
- 使用按鈕導航選單
- 顯示不同的 LED 模式
- 支援選項選擇和確認

**提示：**
- 使用狀態機設計
- 實作防彈跳
- 清晰的使用者回饋

### 🎯 專題 3：資料記錄器

**需求：**
- 定時記錄溫度資料
- 儲存到檔案（JSON 格式）
- 按鈕控制開始/停止記錄

**提示：**
- 使用 DataFormatter
- 檔案 I/O 操作
- 時間戳記管理

## 常見問題

### Q: Thonny 找不到 Pico？

**解決步驟：**
1. 確認 USB 線支援資料傳輸
2. 重新安裝 MicroPython 韌體
3. 檢查 USB 連接埠權限
4. 重新啟動 Thonny

### Q: 程式執行後沒有反應？

**檢查項目：**
1. 確認程式沒有語法錯誤
2. 檢查縮排是否正確（Python 對縮排敏感）
3. 查看 Shell 視窗的錯誤訊息
4. 確認 GPIO 腳位編號正確

### Q: LED 不會亮？

**可能原因：**
1. Pico W 使用 `"LED"` 字串，不是數字
2. 一般 Pico 使用 `25`
3. 確認你的硬體型號

### Q: 溫度讀數異常？

**說明：**
- 這是晶片溫度，不是環境溫度
- 正常範圍 25-35°C
- USB 供電會導致溫度上升
- 程式執行會產生熱量

## 除錯技巧

### 1. 使用 print() 除錯

```python
print("程式開始")
print(f"變數值: {variable}")
print("到達這裡")
```

### 2. 檢查變數型別

```python
print(type(variable))
```

### 3. 捕捉錯誤

```python
try:
    # 可能出錯的程式碼
    result = risky_operation()
except Exception as e:
    print(f"錯誤: {e}")
```

### 4. 使用 LED 指示

```python
led.on()   # 到達這個位置
# 執行某些操作
led.off()  # 操作完成
```

## 學習資源

### 官方文件

- [MicroPython 官方文件](https://docs.micropython.org/)
- [Raspberry Pi Pico 文件](https://www.raspberrypi.com/documentation/microcontrollers/)
- [RP2040 資料手冊](https://datasheets.raspberrypi.com/rp2040/rp2040-datasheet.pdf)

### 教學資源

- [MicroPython 教學](https://docs.micropython.org/en/latest/rp2/quickref.html)
- [Pico 入門指南](https://projects.raspberrypi.org/en/projects/getting-started-with-the-pico)

### 社群資源

- [MicroPython 論壇](https://forum.micropython.org/)
- [Raspberry Pi 論壇](https://forums.raspberrypi.com/)

## 檢核清單

完成本模組前，確認你已經：

### 環境設定
- [ ] 安裝 Thonny IDE
- [ ] 安裝 MicroPython 韌體
- [ ] 成功連接 Pico
- [ ] 執行 Hello World 程式

### LED 控制
- [ ] 理解 GPIO 概念
- [ ] 控制 LED 開關
- [ ] 實作 LED 閃爍
- [ ] 完成 SOS 訊號

### 感測器讀取
- [ ] 理解 ADC 原理
- [ ] 讀取溫度感測器
- [ ] 實作資料平滑
- [ ] 格式化為 JSON

### 按鈕輸入
- [ ] 讀取按鈕狀態
- [ ] 實作防彈跳
- [ ] 使用中斷處理
- [ ] 偵測短按和長按

### 程式設計
- [ ] 使用函式組織程式碼
- [ ] 建立類別封裝功能
- [ ] 處理錯誤和例外
- [ ] 撰寫清晰的註解

## 下一步

恭喜完成 Pico 基礎模組！🎉

你現在已經掌握了：
- Pico 的基本操作
- GPIO 輸入輸出
- 感測器資料讀取
- 基本的程式設計技巧

**繼續學習：**

1. **[Pi 基礎模組](../02_pi_basics/README.md)**
   - 學習 Raspberry Pi
   - Docker 和 MongoDB
   - FastAPI 建立 API

2. **[MQTT 通訊模組](../03_mqtt_communication/README.md)**
   - 裝置間通訊
   - MQTT 協定
   - 網路連接

## 需要協助？

如果遇到問題：

1. 查看各單元的 README 文件
2. 參考 [故障排除指南](../resources/troubleshooting.md)
3. 查看 [常見問題](../resources/faq.md)
4. 向講師或同學尋求協助

**記住：**
- 錯誤是學習的一部分
- 多嘗試、多實驗
- 不要害怕問問題
- 享受學習的過程！

祝學習愉快！🚀
