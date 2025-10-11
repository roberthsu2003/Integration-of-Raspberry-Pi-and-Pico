# Pi 串列通訊範例

本目錄包含 Raspberry Pi 端的串列通訊程式，用於接收 Pico 透過 UART 發送的資料。

## 檔案說明

```
pi_serial/
├── serial_basic.py         # 基本串列通訊
├── serial_receiver.py      # 感測器資料接收器
└── README.md              # 本檔案
```

## 安裝依賴

```bash
pip install pyserial
```

## 找到串列埠

### 方法 1：列出所有串列埠

```bash
ls /dev/tty*
```

常見的串列埠：
- `/dev/ttyACM0` - USB CDC (Pico 預設)
- `/dev/ttyUSB0` - USB-Serial 轉接器
- `/dev/serial0` - GPIO UART

### 方法 2：查看連接訊息

```bash
# 連接 Pico 後執行
dmesg | tail

# 輸出範例：
# [12345.678] usb 1-1: new full-speed USB device
# [12345.789] cdc_acm 1-1:1.0: ttyACM0: USB ACM device
```

### 方法 3：使用 Python

```python
import serial.tools.list_ports

ports = serial.tools.list_ports.comports()
for port in ports:
    print(f"{port.device}: {port.description}")
```

## 範例 1：基本串列通訊

### serial_basic.py

簡單的串列通訊程式，接收訊息並發送回應。

**使用方法：**
```bash
# 使用預設設定
python serial_basic.py

# 指定串列埠
python serial_basic.py --port /dev/ttyACM0

# 指定鮑率
python serial_basic.py --baudrate 115200
```

**功能：**
- 接收 Pico 發送的訊息
- 發送回應（Echo）
- 顯示通訊狀態

## 範例 2：感測器資料接收器

### serial_receiver.py

接收 Pico 發送的 JSON 格式感測器資料並儲存到資料庫。

**使用方法：**
```bash
# 使用預設設定（含資料庫）
python serial_receiver.py

# 不使用資料庫
python serial_receiver.py --no-db

# 自訂設定
python serial_receiver.py --port /dev/ttyACM0 --baudrate 9600
```

**功能：**
- 接收 JSON 格式資料
- 驗證資料格式
- 儲存到 MongoDB
- 顯示統計資訊

## 測試步驟

### 1. 測試串列埠

```bash
# 使用 screen 測試
screen /dev/ttyACM0 9600

# 或使用 minicom
minicom -D /dev/ttyACM0 -b 9600

# 按 Ctrl+A 然後 K 退出 screen
# 按 Ctrl+A 然後 X 退出 minicom
```

### 2. 測試基本通訊

**終端 1（Pi）：**
```bash
python serial_basic.py
```

**終端 2（Pico）：**
```python
# 在 Thonny 中執行 uart_basic.py
```

### 3. 測試感測器資料

**終端 1（Pi）：**
```bash
python serial_receiver.py
```

**終端 2（Pico）：**
```python
# 在 Thonny 中執行 uart_sensor.py
```

## 權限設定

如果遇到權限問題：

```bash
# 將使用者加入 dialout 群組
sudo usermod -a -G dialout $USER

# 登出後重新登入使變更生效
# 或執行
newgrp dialout

# 或直接修改權限（臨時）
sudo chmod 666 /dev/ttyACM0
```

## 常見問題

### Q: 找不到串列埠？

**檢查步驟：**
```bash
# 1. 確認 Pico 已連接
lsusb

# 2. 檢查核心訊息
dmesg | grep tty

# 3. 檢查裝置檔案
ls -l /dev/ttyACM*
```

### Q: 權限被拒？

**錯誤訊息：**
```
PermissionError: [Errno 13] Permission denied: '/dev/ttyACM0'
```

**解決方法：**
```bash
# 方法 1：加入群組（永久）
sudo usermod -a -G dialout $USER
# 登出後重新登入

# 方法 2：修改權限（臨時）
sudo chmod 666 /dev/ttyACM0
```

### Q: 串列埠被佔用？

**錯誤訊息：**
```
SerialException: [Errno 16] Device or resource busy
```

**解決方法：**
```bash
# 查看哪個程式在使用
sudo lsof /dev/ttyACM0

# 關閉佔用的程式
# 或重新連接 Pico
```

### Q: 收到亂碼？

**可能原因：**
1. 鮑率不一致
2. 編碼問題

**解決方法：**
```python
# 確認鮑率一致
# Pico: baudrate=9600
# Pi: baudrate=9600

# 使用正確的編碼
data.decode('utf-8', errors='ignore')
```

## 進階功能

### 1. 非阻塞讀取

```python
import serial

ser = serial.Serial('/dev/ttyACM0', 9600, timeout=0)

while True:
    if ser.in_waiting > 0:
        data = ser.read(ser.in_waiting)
        print(data)
```

### 2. 二進位資料

```python
import struct

# 接收二進位資料
data = ser.read(8)  # 讀取 8 bytes
temp, humidity = struct.unpack('ff', data)
```

### 3. 資料緩衝

```python
buffer = b''

while True:
    if ser.in_waiting > 0:
        buffer += ser.read(ser.in_waiting)
        
        # 處理完整的訊息（以換行符號分隔）
        while b'\n' in buffer:
            line, buffer = buffer.split(b'\n', 1)
            process_message(line.decode())
```

## 效能優化

### 1. 調整緩衝區大小

```python
# 增加接收緩衝區
ser = serial.Serial(
    '/dev/ttyACM0',
    9600,
    timeout=1,
    rtscts=False,
    dsrdtr=False
)
```

### 2. 批次處理

```python
batch = []
batch_size = 10

while True:
    if ser.in_waiting > 0:
        data = ser.readline()
        batch.append(data)
        
        if len(batch) >= batch_size:
            process_batch(batch)
            batch = []
```

## 檢核清單

完成本單元前，確認：

- [ ] 成功安裝 pyserial
- [ ] 能夠找到串列埠
- [ ] 解決權限問題
- [ ] 能夠接收文字訊息
- [ ] 能夠接收 JSON 資料
- [ ] 理解鮑率設定
- [ ] 能夠除錯常見問題

## 下一步

完成 Pi 串列通訊後，繼續學習：
- [整合應用](../../05_integration/README.md) - 完整系統整合
- [多裝置管理](../../06_multi_device/README.md) - 管理多個裝置

## 參考資源

- [PySerial 文件](https://pyserial.readthedocs.io/)
- [Serial Programming Guide](https://tldp.org/HOWTO/Serial-Programming-HOWTO/)
- [Linux Serial Console](https://www.kernel.org/doc/html/latest/admin-guide/serial-console.html)
