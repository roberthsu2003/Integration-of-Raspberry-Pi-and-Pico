# Pico UART 範例

本目錄包含 Pico 端的 UART 通訊範例程式。

## 檔案說明

```
pico_uart/
├── uart_basic.py           # 基本 UART 通訊
├── uart_sensor.py          # UART 感測器資料傳輸
└── README.md              # 本檔案
```

## UART 基礎

### 什麼是 UART？

UART (Universal Asynchronous Receiver/Transmitter) 是一種串列通訊協定，用於裝置間的點對點通訊。

**特點：**
- 全雙工通訊（可同時發送和接收）
- 非同步（不需要時鐘訊號）
- 簡單可靠
- 適合短距離通訊

### 硬體連接

```
┌─────────┐         ┌─────────┐
│  Pico   │         │   Pi    │
│         │         │         │
│ TX (0)  ├────────▶│ RX      │
│ RX (1)  │◀────────┤ TX      │
│ GND     ├─────────┤ GND     │
└─────────┘         └─────────┘
```

**注意：**
- TX 連接到對方的 RX
- RX 連接到對方的 TX
- 必須共地（GND 連接）

### Pico UART 腳位

Pico 有兩個 UART：

**UART 0：**
- TX: GPIO 0 或 GPIO 12 或 GPIO 16
- RX: GPIO 1 或 GPIO 13 或 GPIO 17

**UART 1：**
- TX: GPIO 4 或 GPIO 8
- RX: GPIO 5 或 GPIO 9

本範例使用 UART 0 的 GPIO 0 (TX) 和 GPIO 1 (RX)。

## 範例 1：基本 UART 通訊

### uart_basic.py

最簡單的 UART 發送和接收範例。

**功能：**
- 定時發送訊息
- 接收並顯示訊息

**使用方法：**
1. 連接硬體（Pico TX → Pi RX, Pico RX → Pi TX, GND → GND）
2. 在 Thonny 中開啟 `uart_basic.py`
3. 執行程式

**程式碼重點：**
```python
# 初始化 UART
uart = machine.UART(0, baudrate=9600, tx=machine.Pin(0), rx=machine.Pin(1))

# 發送訊息
uart.write("Hello\n")

# 接收訊息
if uart.any():
    data = uart.read()
    message = data.decode('utf-8')
```

## 範例 2：UART 感測器資料傳輸

### uart_sensor.py

透過 UART 發送感測器資料到 Pi。

**功能：**
- 讀取溫度感測器
- 格式化為 JSON
- 透過 UART 發送
- 接收命令（選用）

**使用方法：**
1. 連接硬體
2. 在 Thonny 中開啟 `uart_sensor.py`
3. 執行程式
4. 在 Pi 端執行接收程式

**資料格式：**
```json
{
    "device_id": "pico_uart_001",
    "sensor_type": "temperature",
    "value": 25.5,
    "unit": "celsius",
    "timestamp": 12345
}
```

**程式碼重點：**
```python
# 建立 UART 感測器
sensor = UARTSensor(uart_id=0, baudrate=9600)

# 讀取並發送資料
sensor.send_sensor_data()

# 接收命令
command = sensor.receive_command()
```

## 鮑率（Baudrate）

鮑率是每秒傳輸的位元數。

**常用鮑率：**
- 9600 bps（預設，適合一般應用）
- 19200 bps
- 38400 bps
- 57600 bps
- 115200 bps（高速）

**注意：**
- 發送端和接收端必須使用相同的鮑率
- 鮑率越高，傳輸速度越快，但距離越短
- 建議從 9600 開始測試

## 資料格式

### 文字格式

```python
# 發送
uart.write("Hello World\n")

# 接收
data = uart.read()
text = data.decode('utf-8')
```

### JSON 格式

```python
import json

# 發送
data = {"key": "value"}
uart.write(json.dumps(data) + '\n')

# 接收
line = uart.readline()
data = json.loads(line)
```

### 二進位格式

```python
import struct

# 發送（打包為二進位）
data = struct.pack('f', 25.5)  # float
uart.write(data)

# 接收（解包）
data = uart.read(4)  # 讀取 4 bytes
value = struct.unpack('f', data)[0]
```

## 測試步驟

### 1. 硬體連接測試

使用跳線短接 TX 和 RX（迴路測試）：

```python
import machine

uart = machine.UART(0, baudrate=9600, tx=machine.Pin(0), rx=machine.Pin(1))

# 發送
uart.write("test\n")

# 接收（應該收到 "test"）
if uart.any():
    print(uart.read())
```

### 2. 與 Pi 通訊測試

**Pico 端：**
```python
# 執行 uart_basic.py
```

**Pi 端：**
```bash
# 使用 minicom 或 screen
screen /dev/ttyACM0 9600

# 或使用 Python
python ../pi_serial/serial_basic.py
```

### 3. 感測器資料測試

**Pico 端：**
```python
# 執行 uart_sensor.py
```

**Pi 端：**
```python
# 執行 serial_receiver.py
python ../pi_serial/serial_receiver.py
```

## 常見問題

### Q: 沒有收到資料？

**檢查項目：**
1. 硬體連接是否正確（TX → RX, RX → TX）
2. 鮑率是否一致
3. GND 是否連接
4. USB 線是否支援資料傳輸

**除錯方法：**
```python
# 檢查 UART 是否初始化
print(uart)

# 檢查是否有資料
print(uart.any())

# 迴路測試
uart.write("test")
time.sleep(0.1)
print(uart.read())
```

### Q: 收到亂碼？

**可能原因：**
1. 鮑率不一致
2. 資料格式錯誤
3. 編碼問題

**解決方法：**
```python
# 確認鮑率
uart = machine.UART(0, baudrate=9600)  # 兩端都用 9600

# 使用正確的編碼
data = uart.read()
text = data.decode('utf-8', errors='ignore')
```

### Q: 資料遺失？

**可能原因：**
1. 緩衝區溢位
2. 發送速度太快
3. 沒有流量控制

**解決方法：**
```python
# 加入延遲
uart.write("data")
time.sleep(0.01)

# 檢查緩衝區
if uart.any() > 0:
    data = uart.read()

# 使用較大的緩衝區
uart = machine.UART(0, baudrate=9600, rxbuf=1024)
```

### Q: 如何找到 Pi 的串列埠？

**在 Pi 上執行：**
```bash
# 列出所有串列埠
ls /dev/tty*

# 通常是以下之一：
# /dev/ttyACM0  (USB CDC)
# /dev/ttyUSB0  (USB-Serial 轉接器)
# /dev/serial0  (GPIO UART)

# 查看詳細資訊
dmesg | grep tty
```

## UART vs MQTT 比較

| 特性 | UART | MQTT |
|------|------|------|
| 連接方式 | 有線（直接連接） | 無線（網路） |
| 距離 | 短（< 15m） | 長（網路範圍） |
| 速度 | 快（直接傳輸） | 較慢（網路延遲） |
| 拓撲 | 點對點 | 多對多 |
| 複雜度 | 簡單 | 較複雜 |
| 可靠性 | 高（有線） | 中（依賴網路） |
| 功耗 | 低 | 較高（WiFi） |

**使用建議：**
- **使用 UART**：裝置直接連接、需要高速傳輸、低功耗
- **使用 MQTT**：多裝置、遠距離、需要靈活性

## 進階功能

### 1. 流量控制

```python
# 使用 RTS/CTS 流量控制
uart = machine.UART(
    0,
    baudrate=9600,
    tx=machine.Pin(0),
    rx=machine.Pin(1),
    rts=machine.Pin(2),
    cts=machine.Pin(3)
)
```

### 2. 中斷接收

```python
def uart_callback(uart):
    """UART 接收中斷"""
    if uart.any():
        data = uart.read()
        print(f"收到: {data}")

# 設定中斷
uart.irq(trigger=machine.UART.IRQ_RXIDLE, handler=uart_callback)
```

### 3. 二進位協定

```python
import struct

def send_binary_data(temp, humidity):
    """發送二進位資料"""
    # 打包：2 個 float
    data = struct.pack('ff', temp, humidity)
    uart.write(data)

def receive_binary_data():
    """接收二進位資料"""
    if uart.any() >= 8:  # 2 個 float = 8 bytes
        data = uart.read(8)
        temp, humidity = struct.unpack('ff', data)
        return temp, humidity
```

## 檢核清單

完成本單元前，確認：

- [ ] 理解 UART 的基本原理
- [ ] 正確連接硬體（TX → RX, RX → TX, GND）
- [ ] 能夠發送和接收文字訊息
- [ ] 能夠發送 JSON 格式資料
- [ ] 理解鮑率的概念
- [ ] 能夠除錯常見問題
- [ ] 理解 UART 和 MQTT 的差異

## 下一步

完成 Pico UART 範例後，繼續學習：
- [Pi 串列通訊](../pi_serial/README.md) - Pi 端的接收程式
- [整合應用](../../05_integration/README.md) - 完整系統整合

## 參考資源

- [Pico 資料手冊](https://datasheets.raspberrypi.com/pico/pico-datasheet.pdf)
- [MicroPython UART 文件](https://docs.micropython.org/en/latest/library/machine.UART.html)
- [UART 協定說明](https://en.wikipedia.org/wiki/Universal_asynchronous_receiver-transmitter)
