# MicroPython 速查表

快速參考 Raspberry Pi Pico 常用的 MicroPython 功能。

## 基礎語法

### 匯入模組
```python
import machine
import time
from machine import Pin, ADC
```

### 延遲
```python
time.sleep(1)        # 延遲 1 秒
time.sleep_ms(500)   # 延遲 500 毫秒
time.sleep_us(100)   # 延遲 100 微秒
```

## GPIO 控制

### 數位輸出
```python
# 建立 LED 物件（Pico W 使用 "LED"）
led = Pin("LED", Pin.OUT)

# 控制 LED
led.on()             # 開啟
led.off()            # 關閉
led.toggle()         # 切換狀態
led.value(1)         # 設定為高電位
led.value(0)         # 設定為低電位
```

### 數位輸入
```python
# 建立按鈕物件（使用內部上拉電阻）
button = Pin(15, Pin.IN, Pin.PULL_UP)

# 讀取按鈕狀態
state = button.value()  # 0 或 1

# 按鈕按下檢測（使用上拉電阻時）
if button.value() == 0:
    print("按鈕被按下")
```

### 中斷處理
```python
def button_handler(pin):
    print("按鈕被按下")

# 設定中斷（下降邊緣觸發）
button.irq(trigger=Pin.IRQ_FALLING, handler=button_handler)

# 中斷觸發選項
Pin.IRQ_FALLING  # 下降邊緣（1→0）
Pin.IRQ_RISING   # 上升邊緣（0→1）
```

## 類比輸入

### ADC（類比數位轉換器）
```python
# 建立 ADC 物件（GPIO 26-28 支援 ADC）
adc = ADC(Pin(26))

# 讀取原始值（0-65535）
raw_value = adc.read_u16()

# 轉換為電壓（0-3.3V）
voltage = raw_value * 3.3 / 65535
```

### 內建溫度感測器
```python
# 建立溫度感測器物件
sensor = ADC(4)  # ADC 通道 4 是內建溫度感測器

# 讀取溫度
raw_value = sensor.read_u16()
voltage = raw_value * 3.3 / 65535
temperature = 27 - (voltage - 0.706) / 0.001721

print(f"溫度: {temperature:.1f}°C")
```

## PWM（脈衝寬度調變）

### 基本 PWM
```python
from machine import PWM

# 建立 PWM 物件
pwm = PWM(Pin(15))

# 設定頻率（Hz）
pwm.freq(1000)

# 設定占空比（0-65535）
pwm.duty_u16(32768)  # 50% 占空比

# 關閉 PWM
pwm.deinit()
```

### LED 亮度控制
```python
# 淡入淡出效果
for duty in range(0, 65536, 256):
    pwm.duty_u16(duty)
    time.sleep_ms(10)
```

## 計時器

### 軟體計時器
```python
from machine import Timer

def timer_callback(timer):
    print("計時器觸發")

# 建立計時器（每秒觸發一次）
timer = Timer()
timer.init(period=1000, mode=Timer.PERIODIC, callback=timer_callback)

# 停止計時器
timer.deinit()
```

## UART（串列通訊）

### 基本 UART
```python
from machine import UART

# 建立 UART 物件（UART0, TX=GPIO0, RX=GPIO1）
uart = UART(0, baudrate=9600)

# 發送資料
uart.write("Hello\n")

# 接收資料
if uart.any():
    data = uart.read()
    print(data.decode())
```

## I2C

### 基本 I2C
```python
from machine import I2C

# 建立 I2C 物件（I2C0, SDA=GPIO4, SCL=GPIO5）
i2c = I2C(0, scl=Pin(5), sda=Pin(4), freq=400000)

# 掃描裝置
devices = i2c.scan()
print("I2C 裝置:", [hex(d) for d in devices])

# 讀寫資料
i2c.writeto(address, data)
data = i2c.readfrom(address, num_bytes)
```

## SPI

### 基本 SPI
```python
from machine import SPI

# 建立 SPI 物件
spi = SPI(0, baudrate=1000000, polarity=0, phase=0,
          sck=Pin(2), mosi=Pin(3), miso=Pin(4))

# 發送資料
spi.write(b'\x01\x02\x03')

# 接收資料
data = spi.read(3)

# 同時發送和接收
spi.write_readinto(send_buffer, receive_buffer)
```

## WiFi（Pico W）

### 連接 WiFi
```python
import network

# 建立 WLAN 物件
wlan = network.WLAN(network.STA_IF)
wlan.active(True)

# 連接到 WiFi
wlan.connect('SSID', 'PASSWORD')

# 等待連接
while not wlan.isconnected():
    time.sleep(1)

# 取得網路資訊
print("IP 位址:", wlan.ifconfig()[0])
```

### 檢查連接狀態
```python
if wlan.isconnected():
    print("已連接")
    print("IP:", wlan.ifconfig()[0])
else:
    print("未連接")
```

## 檔案系統

### 檔案操作
```python
# 寫入檔案
with open('data.txt', 'w') as f:
    f.write('Hello, World!\n')

# 讀取檔案
with open('data.txt', 'r') as f:
    content = f.read()
    print(content)

# 附加到檔案
with open('data.txt', 'a') as f:
    f.write('New line\n')
```

### 列出檔案
```python
import os

# 列出目錄內容
files = os.listdir('/')
print(files)

# 刪除檔案
os.remove('data.txt')
```

## JSON 處理

### JSON 編碼/解碼
```python
import json

# Python 物件轉 JSON
data = {'temperature': 25.5, 'humidity': 60}
json_str = json.dumps(data)

# JSON 轉 Python 物件
data = json.loads(json_str)
print(data['temperature'])
```

## 常用函式

### 系統資訊
```python
import sys
import machine

# Python 版本
print(sys.version)

# 系統頻率
print(machine.freq())

# 重置裝置
machine.reset()

# 軟重置
machine.soft_reset()
```

### 記憶體管理
```python
import gc

# 執行垃圾回收
gc.collect()

# 查看可用記憶體
print(gc.mem_free())
```

## 錯誤處理

### Try-Except
```python
try:
    # 可能出錯的程式碼
    value = sensor.read()
except Exception as e:
    print(f"錯誤: {e}")
finally:
    # 清理程式碼
    pass
```

## 實用技巧

### 防彈跳
```python
def read_button_debounced(button, delay_ms=50):
    """讀取按鈕狀態（含防彈跳）"""
    if button.value() == 0:
        time.sleep_ms(delay_ms)
        if button.value() == 0:
            return True
    return False
```

### 非阻塞延遲
```python
class NonBlockingDelay:
    """非阻塞延遲類別"""
    def __init__(self, interval_ms):
        self.interval = interval_ms
        self.last_time = time.ticks_ms()
    
    def is_ready(self):
        current_time = time.ticks_ms()
        if time.ticks_diff(current_time, self.last_time) >= self.interval:
            self.last_time = current_time
            return True
        return False

# 使用範例
delay = NonBlockingDelay(1000)
while True:
    if delay.is_ready():
        print("1 秒到了")
    # 可以執行其他程式碼
```

### 平均濾波
```python
def moving_average(values, new_value, window_size=10):
    """移動平均濾波"""
    values.append(new_value)
    if len(values) > window_size:
        values.pop(0)
    return sum(values) / len(values)

# 使用範例
readings = []
filtered_value = moving_average(readings, sensor.read())
```

## 常見問題

### Q: 如何讓程式開機自動執行？
A: 將程式儲存為 `main.py`，Pico 開機時會自動執行。

### Q: 如何停止執行中的程式？
A: 在 Thonny 中按 Ctrl+C 或點擊停止按鈕。

### Q: 如何查看錯誤訊息？
A: 錯誤訊息會顯示在 Thonny 的 Shell 視窗中。

### Q: Pico W 的 LED 為什麼要用 "LED" 而不是數字？
A: Pico W 的 LED 連接到 WiFi 晶片，需要使用字串 "LED" 來控制。

## 參考資源

- [MicroPython 官方文件](https://docs.micropython.org/)
- [Pico MicroPython SDK](https://datasheets.raspberrypi.com/pico/raspberry-pi-pico-python-sdk.pdf)
- [Pico 腳位圖](https://datasheets.raspberrypi.com/pico/Pico-R3-A4-Pinout.pdf)
