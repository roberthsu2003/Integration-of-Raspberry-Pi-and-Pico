# LED 閃爍範例

## 學習目標

- 理解 GPIO（通用輸入輸出）的基本概念
- 學習如何控制數位輸出
- 使用 MicroPython 控制 LED
- 理解程式流程控制

## 硬體需求

- Raspberry Pi Pico W
- USB 連接線
- 電腦（安裝 Thonny IDE）

## 程式說明

### 1. hello.py - Hello World

這是你的第一個 MicroPython 程式，用來驗證環境設定是否正確。

**執行步驟：**
1. 在 Thonny 中開啟 `hello.py`
2. 確認右下角顯示 "MicroPython (Raspberry Pi Pico)"
3. 點擊執行按鈕（綠色三角形）或按 F5
4. 在 Shell 視窗中查看輸出

**預期輸出：**
```
Hello, Pico!
歡迎來到 MicroPython 的世界！
Python 版本: 3.4.0
Pico 唯一 ID: e66118605b3c5628
程式執行完成！
```

### 2. blink.py - 基本 LED 閃爍

讓 Pico W 的內建 LED 以 1 秒間隔閃爍。

**程式碼重點：**
```python
import machine
import time

# 初始化 LED（Pico W 使用 "LED" 腳位）
led = machine.Pin("LED", machine.Pin.OUT)

# 控制 LED
led.on()   # 開啟
led.off()  # 關閉
```

**執行步驟：**
1. 在 Thonny 中開啟 `blink.py`
2. 點擊執行
3. 觀察 Pico W 上的 LED（綠色）閃爍
4. 按 Ctrl+C 停止程式

**觀察重點：**
- LED 每秒開關一次
- Shell 視窗顯示 "LED 開啟" 和 "LED 關閉"

### 3. blink_fast.py - 調整閃爍頻率

練習修改程式參數來改變 LED 閃爍速度。

**練習任務：**
1. 執行原始程式，觀察閃爍速度
2. 修改 `delay_time` 變數：
   - 試試 `0.1`（更快）
   - 試試 `2.0`（更慢）
   - 試試 `0.05`（非常快）
3. 每次修改後重新執行，觀察變化

**思考問題：**
- 最小的延遲時間是多少？
- 延遲時間太小會發生什麼？
- 如何讓 LED 看起來像是持續亮著？

### 4. sos_signal.py - SOS 訊號

實作摩斯密碼 SOS 求救訊號。

**摩斯密碼規則：**
- S = `...` (三個短訊號)
- O = `---` (三個長訊號)
- SOS = `... --- ...`

**程式特色：**
- 使用函式封裝功能
- 定義時間常數
- 模組化設計

**執行步驟：**
1. 執行程式
2. 觀察 LED 閃爍模式
3. 對照 Shell 輸出確認訊號正確

**延伸挑戰：**
1. 實作其他字母的摩斯密碼（如 A = `.-`）
2. 讓程式可以發送自訂訊息
3. 加入聲音輸出（如果有蜂鳴器）

## 重要概念

### GPIO（General Purpose Input/Output）

GPIO 是微控制器上可以程式化控制的腳位，可以設定為：
- **輸出模式**：控制 LED、馬達等
- **輸入模式**：讀取按鈕、感測器等

### 數位輸出

數位輸出只有兩種狀態：
- **HIGH (1)**：輸出高電位（3.3V）- LED 亮
- **LOW (0)**：輸出低電位（0V）- LED 滅

### machine 模組

MicroPython 的 `machine` 模組提供硬體控制功能：
```python
import machine

# Pin 類別用於控制 GPIO
pin = machine.Pin(pin_number, mode)

# 常用方法
pin.on()    # 設為 HIGH
pin.off()   # 設為 LOW
pin.value(1)  # 設定值（0 或 1）
pin.value()   # 讀取當前值
```

### time 模組

用於時間相關操作：
```python
import time

time.sleep(1)      # 暫停 1 秒
time.sleep_ms(500) # 暫停 500 毫秒
time.sleep_us(100) # 暫停 100 微秒
```

## 常見問題

### Q: LED 不會閃爍？

**可能原因：**
1. 確認使用的是 Pico W（有 WiFi 的版本）
2. 檢查程式是否正確執行（沒有錯誤訊息）
3. 確認 USB 連接穩定

### Q: 出現 "Pin not found" 錯誤？

**解決方法：**
- Pico W 使用 `"LED"` 字串
- 一般 Pico 使用 `25` 數字
- 確認你的硬體型號

### Q: 如何停止程式？

**方法：**
1. 在 Thonny 中按 Ctrl+C
2. 點擊 Thonny 的停止按鈕（紅色方塊）
3. 重新連接 Pico

### Q: 程式執行後 LED 一直亮著？

**原因：**
- 程式可能在 `led.on()` 後就結束了
- 確保有 `while True:` 迴圈
- 檢查縮排是否正確

## 練習題

### 練習 1：呼吸燈效果

修改程式讓 LED 產生呼吸燈效果（漸亮漸暗）。

**提示：**
- 使用 PWM（脈衝寬度調變）
- 參考 `machine.PWM` 類別

### 練習 2：交通號誌

如果有外接 LED（紅、黃、綠），實作交通號誌邏輯：
- 綠燈 5 秒
- 黃燈 2 秒
- 紅燈 5 秒
- 重複

### 練習 3：自訂摩斯密碼

擴展 SOS 程式，讓它可以發送任意文字的摩斯密碼。

**摩斯密碼對照表：**
```
A .-    B -...  C -.-.  D -..   E .
F ..-.  G --.   H ....  I ..    J .---
K -.-   L .-..  M --    N -.    O ---
P .--.  Q --.-  R .-.   S ...   T -
U ..-   V ...-  W .--   X -..-  Y -.--
Z --..
```

## 檢核清單

完成本單元後，你應該能夠：

- [ ] 成功執行 Hello World 程式
- [ ] 理解 GPIO 和數位輸出的概念
- [ ] 使用 `machine.Pin` 控制 LED
- [ ] 使用 `time.sleep()` 控制時序
- [ ] 修改程式參數改變行為
- [ ] 使用函式組織程式碼
- [ ] 實作 SOS 訊號
- [ ] 能夠除錯簡單的程式問題

## 下一步

完成 LED 控制後，繼續學習：
- [內建感測器](../02_onboard_sensor/README.md) - 讀取溫度資料
- [按鈕輸入](../03_button_input/README.md) - 處理使用者輸入

## 參考資源

- [MicroPython 官方文件](https://docs.micropython.org/)
- [Raspberry Pi Pico Python SDK](https://datasheets.raspberrypi.com/pico/raspberry-pi-pico-python-sdk.pdf)
- [machine 模組參考](https://docs.micropython.org/en/latest/library/machine.html)
