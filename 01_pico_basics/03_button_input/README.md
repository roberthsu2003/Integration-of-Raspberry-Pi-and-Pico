# 按鈕輸入範例

## 學習目標

- 理解數位輸入的概念
- 學習讀取按鈕狀態
- 掌握防彈跳（Debounce）技術
- 理解中斷（Interrupt）處理
- 實作按鈕控制應用

## 硬體需求

- Raspberry Pi Pico / Pico W
- 按鈕開關（或使用麵包板和跳線短接測試）
- 跳線
- 麵包板（選用）

## 硬體連接

### 基本連接方式

```
按鈕連接：
┌─────────┐
│  Pico   │
│         │
│ GPIO 15 ├──┐
│         │  │  按鈕
│     GND ├──┼───┤├───┐
│         │  │        │
└─────────┘  └────────┘
```

**連接步驟：**
1. 按鈕一端連接到 GPIO 15
2. 按鈕另一端連接到 GND
3. 程式中使用內部上拉電阻

**為什麼使用上拉電阻？**
- 當按鈕未按下時，GPIO 腳位被拉到 HIGH（3.3V）
- 當按鈕按下時，GPIO 腳位連接到 GND（LOW）
- 避免浮接狀態（floating state）

## 程式說明

### 1. button.py - 基本按鈕讀取

最簡單的按鈕輸入程式。

**重要概念：**

**數位輸入：**
```python
# 初始化為輸入模式，使用內部上拉電阻
button = machine.Pin(15, machine.Pin.IN, machine.Pin.PULL_UP)

# 讀取狀態
state = button.value()  # 0 = 按下，1 = 放開
```

**上拉電阻模式：**
- `PULL_UP`：內部上拉電阻，未按下時為 HIGH
- `PULL_DOWN`：內部下拉電阻，未按下時為 LOW
- 不使用上拉/下拉會導致不穩定的讀數

**執行步驟：**
1. 連接按鈕到 GPIO 15 和 GND
2. 執行 `button.py`
3. 按下和放開按鈕，觀察 LED 和訊息

**注意：**
- 這個程式會持續輪詢按鈕狀態
- 可能會看到多次觸發（彈跳問題）

### 2. button_debounce.py - 防彈跳處理

處理按鈕的機械彈跳問題。

**什麼是彈跳（Bounce）？**

當按鈕被按下時，機械接點不會立即穩定，而是會快速震動：

```
理想狀態：
HIGH ────┐
         └──────── LOW

實際狀態（有彈跳）：
HIGH ────┐ ┌┐┌┐
         └─┘└┘└─── LOW
```

**防彈跳策略：**

1. **時間延遲法**
```python
if button_pressed:
    time.sleep(0.05)  # 等待 50ms
    if button_pressed:  # 再次確認
        # 真的被按下
```

2. **狀態追蹤法**
```python
# 只在狀態改變時觸發
if last_state == 1 and current_state == 0:
    # 偵測到按下
```

**Button 類別功能：**
- `is_pressed()`: 檢查是否被按下（有防彈跳）
- `wait_for_press()`: 等待按鈕被按下
- `wait_for_release()`: 等待按鈕被放開

**執行步驟：**
1. 執行 `button_debounce.py`
2. 快速按下按鈕多次
3. 觀察計數是否準確（應該不會重複計數）

### 3. button_interrupt.py - 中斷處理

使用中斷方式處理按鈕，更有效率。

**什麼是中斷（Interrupt）？**

中斷允許硬體事件立即通知 CPU，而不需要程式持續檢查：

```
輪詢方式（Polling）：
while True:
    if button_pressed:  # 持續檢查
        do_something()

中斷方式（Interrupt）：
button.irq(handler=button_handler)  # 設定一次
# 主程式可以做其他事
# 按鈕按下時自動呼叫 handler
```

**中斷的優點：**
- 不需要持續檢查，節省 CPU 資源
- 反應更即時
- 主程式可以執行其他任務

**中斷觸發模式：**
```python
# 下降緣觸發（HIGH → LOW）
button.irq(trigger=machine.Pin.IRQ_FALLING, handler=handler)

# 上升緣觸發（LOW → HIGH）
button.irq(trigger=machine.Pin.IRQ_RISING, handler=handler)

# 任何變化都觸發
button.irq(trigger=machine.Pin.IRQ_RISING | machine.Pin.IRQ_FALLING, handler=handler)
```

**執行步驟：**
1. 執行 `button_interrupt.py`
2. 觀察主程式持續顯示運行時間
3. 按下按鈕，中斷會立即處理

**注意事項：**
- 中斷處理函式應該盡量簡短
- 避免在中斷中使用 `time.sleep()`
- 使用全域變數或旗標與主程式溝通

### 4. button_led_control.py - 綜合應用

實作短按和長按的不同功能。

**功能設計：**
- **短按**：切換 LED 開關
- **長按**（超過 1 秒）：切換閃爍模式

**長按偵測：**
```python
press_start = time.ticks_ms()
while button_pressed:
    pass
press_duration = time.ticks_diff(time.ticks_ms(), press_start)

if press_duration > 1000:
    # 長按
else:
    # 短按
```

**執行步驟：**
1. 執行 `button_led_control.py`
2. 短按按鈕：LED 開關切換
3. 長按按鈕（超過 1 秒）：進入/離開閃爍模式

**延伸功能：**
- 雙擊偵測
- 多按鈕組合
- 按鈕序列識別

## 重要概念

### 輪詢 vs 中斷

**輪詢（Polling）：**
```python
while True:
    if button.value() == 0:
        handle_button()
    time.sleep(0.01)
```

優點：
- 簡單易懂
- 容易除錯

缺點：
- 浪費 CPU 資源
- 可能錯過快速事件

**中斷（Interrupt）：**
```python
button.irq(trigger=machine.Pin.IRQ_FALLING, handler=handle_button)
while True:
    do_other_things()
```

優點：
- 節省 CPU 資源
- 反應即時
- 不會錯過事件

缺點：
- 較複雜
- 需要注意競爭條件（race condition）

### 防彈跳技術

**硬體防彈跳：**
- 使用電容濾波
- 使用施密特觸發器（Schmitt Trigger）

**軟體防彈跳：**
1. **延遲法**：等待一段時間後再讀取
2. **計數法**：連續讀取多次，多數決定
3. **狀態機法**：追蹤狀態變化

### 時間函式

**MicroPython 時間函式：**
```python
import time

# 秒級延遲
time.sleep(1)

# 毫秒級延遲
time.sleep_ms(100)

# 微秒級延遲
time.sleep_us(10)

# 取得毫秒計時器
ms = time.ticks_ms()

# 計算時間差（處理溢位）
diff = time.ticks_diff(time.ticks_ms(), start_time)
```

## 實用技巧

### 多按鈕處理

```python
buttons = {
    'up': machine.Pin(14, machine.Pin.IN, machine.Pin.PULL_UP),
    'down': machine.Pin(15, machine.Pin.IN, machine.Pin.PULL_UP),
    'select': machine.Pin(16, machine.Pin.IN, machine.Pin.PULL_UP)
}

for name, button in buttons.items():
    if button.value() == 0:
        print(f"{name} 按鈕被按下")
```

### 按鈕組合

```python
if button1.value() == 0 and button2.value() == 0:
    print("兩個按鈕同時按下")
```

### 雙擊偵測

```python
def detect_double_click(max_interval=500):
    """偵測雙擊（兩次按下間隔小於 500ms）"""
    if button.is_pressed():
        first_time = time.ticks_ms()
        time.sleep(0.05)  # 防彈跳
        
        # 等待第二次按下
        timeout = first_time + max_interval
        while time.ticks_ms() < timeout:
            if button.is_pressed():
                return True
            time.sleep(0.01)
    
    return False
```

## 常見問題

### Q: 按鈕沒有反應？

**檢查項目：**
1. 確認硬體連接正確
2. 檢查 GPIO 腳位編號
3. 確認使用了上拉電阻
4. 測試按鈕是否正常（用三用電表）

### Q: 一次按下觸發多次？

**原因：彈跳問題**

解決方法：
1. 使用防彈跳程式碼
2. 加入適當的延遲
3. 使用中斷配合防彈跳

### Q: 中斷不會觸發？

**可能原因：**
1. 觸發模式設定錯誤
2. 中斷處理函式有錯誤
3. 硬體連接問題

**除錯方法：**
```python
def handler(pin):
    print("中斷觸發！")  # 加入除錯訊息
```

### Q: 如何測試沒有實體按鈕？

**方法 1：使用跳線**
- 用跳線短接 GPIO 15 和 GND 模擬按鈕

**方法 2：修改程式**
```python
# 使用另一個 GPIO 模擬按鈕
test_pin = machine.Pin(14, machine.Pin.OUT)
test_pin.value(0)  # 模擬按下
```

## 練習題

### 練習 1：計數器

實作一個計數器：
- 按鈕 1：加 1
- 按鈕 2：減 1
- 按鈕 3：重置為 0
- 在 Shell 顯示當前數值

### 練習 2：選單系統

實作簡單的選單系統：
- 按鈕 1：上一個選項
- 按鈕 2：下一個選項
- 按鈕 3：確認選擇
- 顯示當前選項

### 練習 3：密碼鎖

實作密碼鎖系統：
- 定義一個按鈕序列作為密碼（如：短-長-短）
- 使用者輸入序列
- 正確時 LED 亮綠燈，錯誤時閃紅燈

### 練習 4：反應測試遊戲

實作反應速度測試：
- LED 隨機時間後亮起
- 測量使用者按下按鈕的反應時間
- 顯示反應時間（毫秒）

## 檢核清單

完成本單元後，你應該能夠：

- [ ] 理解數位輸入的概念
- [ ] 正確連接按鈕到 Pico
- [ ] 使用上拉/下拉電阻
- [ ] 讀取按鈕狀態
- [ ] 實作防彈跳處理
- [ ] 使用中斷處理按鈕
- [ ] 偵測短按和長按
- [ ] 整合按鈕和 LED 控制

## 下一步

完成按鈕輸入後，你已經掌握了 Pico 的基礎操作！

繼續學習：
- [Pi 基礎](../../02_pi_basics/README.md) - 學習 Raspberry Pi 和資料庫
- [MQTT 通訊](../../03_mqtt_communication/README.md) - 裝置間通訊

## 參考資源

- [MicroPython Pin 類別](https://docs.micropython.org/en/latest/library/machine.Pin.html)
- [按鈕防彈跳技術](https://www.arduino.cc/en/Tutorial/BuiltInExamples/Debounce)
- [中斷處理最佳實踐](https://docs.micropython.org/en/latest/reference/isr_rules.html)
