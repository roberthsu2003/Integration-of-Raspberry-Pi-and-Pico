# UART/USB 通訊模組

本模組簡介 UART/USB 串列通訊，作為 MQTT 網路通訊的補充。

## 模組概覽

本模組涵蓋 Day 5 下午的課程內容，包含兩個主要單元：

### 📚 學習單元

1. **[Pico UART](pico_uart/README.md)**
   - UART 基礎概念
   - 發送和接收資料
   - 感測器資料傳輸

2. **[Pi 串列通訊](pi_serial/README.md)**
   - PySerial 使用
   - 資料接收和處理
   - 資料庫整合

## 學習目標

完成本模組後，你將能夠：

- ✅ 理解 UART 串列通訊的基本原理
- ✅ 正確連接 Pico 和 Pi 的 UART 硬體
- ✅ 在 Pico 上實作 UART 發送
- ✅ 在 Pi 上實作串列接收
- ✅ 理解 UART 和 MQTT 的差異
- ✅ 選擇適合的通訊方式

## UART 基礎

### 什麼是 UART？

UART (Universal Asynchronous Receiver/Transmitter) 是一種串列通訊協定。

**特點：**
- 全雙工：可同時發送和接收
- 非同步：不需要時鐘訊號
- 點對點：一對一通訊
- 簡單可靠：硬體實作簡單

### 硬體連接

```
┌─────────────┐         ┌─────────────┐
│    Pico     │         │     Pi      │
│             │         │             │
│  TX (GPIO0) ├────────▶│ RX          │
│  RX (GPIO1) │◀────────┤ TX          │
│  GND        ├─────────┤ GND         │
└─────────────┘         └─────────────┘
```

**重要：**
- TX 連接到對方的 RX
- RX 連接到對方的 TX
- 必須共地（GND 連接）

### 鮑率（Baudrate）

鮑率是每秒傳輸的位元數。

**常用鮑率：**
- 9600 bps（預設，適合一般應用）
- 19200 bps
- 38400 bps
- 57600 bps
- 115200 bps（高速）

**注意：** 兩端必須使用相同的鮑率！

## 快速開始

### 1. 硬體連接

使用跳線連接 Pico 和 Pi：
- Pico TX (GPIO 0) → Pi RX
- Pico RX (GPIO 1) → Pi TX
- Pico GND → Pi GND

### 2. Pico 端

```python
# 在 Thonny 中執行
import machine

uart = machine.UART(0, baudrate=9600, tx=machine.Pin(0), rx=machine.Pin(1))
uart.write("Hello from Pico\n")
```

### 3. Pi 端

```bash
# 安裝 pyserial
pip install pyserial

# 執行接收程式
python pi_serial/serial_basic.py
```

## UART vs MQTT 比較

| 特性 | UART | MQTT |
|------|------|------|
| **連接方式** | 有線（直接連接） | 無線（WiFi 網路） |
| **距離** | 短（< 15m） | 長（網路範圍） |
| **速度** | 快（直接傳輸） | 較慢（網路延遲） |
| **拓撲** | 點對點（1對1） | 多對多 |
| **複雜度** | 簡單 | 較複雜 |
| **可靠性** | 高（有線） | 中（依賴網路） |
| **功耗** | 低 | 較高（WiFi） |
| **成本** | 低（只需線材） | 中（需要網路設備） |

### 使用場景

**使用 UART 的情況：**
- ✅ 裝置直接相鄰
- ✅ 需要高速傳輸
- ✅ 需要低功耗
- ✅ 簡單的點對點通訊
- ✅ 除錯和開發

**使用 MQTT 的情況：**
- ✅ 裝置分散在不同位置
- ✅ 需要多對多通訊
- ✅ 需要靈活的拓撲
- ✅ 已有網路基礎設施
- ✅ 需要遠端監控

## 專案結構

```
04_uart_usb/
├── pico_uart/                 # Pico UART 範例
│   ├── uart_basic.py         # 基本 UART 通訊
│   ├── uart_sensor.py        # 感測器資料傳輸
│   └── README.md
├── pi_serial/                # Pi 串列通訊
│   ├── serial_basic.py       # 基本串列通訊
│   ├── serial_receiver.py    # 資料接收器
│   └── README.md
└── README.md                 # 本檔案
```

## 資料流程

```
1. Pico 讀取感測器
        ↓
2. 格式化為 JSON
        ↓
3. 透過 UART 發送
        ↓
4. Pi 串列埠接收
        ↓
5. 解析 JSON
        ↓
6. 驗證資料
        ↓
7. 儲存到資料庫
```

## 實用範例

### 範例 1：簡單通訊

**Pico：**
```python
import machine
uart = machine.UART(0, 9600, tx=machine.Pin(0), rx=machine.Pin(1))
uart.write("Hello\n")
```

**Pi：**
```python
import serial
ser = serial.Serial('/dev/ttyACM0', 9600)
print(ser.readline())
```

### 範例 2：感測器資料

**Pico：**
```python
import json
data = {
    "device_id": "pico_001",
    "temperature": 25.5
}
uart.write(json.dumps(data) + '\n')
```

**Pi：**
```python
line = ser.readline()
data = json.loads(line)
print(f"溫度: {data['temperature']}°C")
```

## 常見問題

### Q: 為什麼需要學習 UART？

**原因：**
1. **基礎知識**：UART 是最基本的通訊方式
2. **除錯工具**：開發時用於除錯
3. **備用方案**：網路不可用時的替代方案
4. **理解差異**：了解不同通訊方式的優缺點

### Q: 實際專案中會用 UART 嗎？

**答案：** 視情況而定

**適合使用 UART：**
- 開發和除錯階段
- 裝置直接連接的場景
- 需要低功耗的應用
- 簡單的資料傳輸

**不適合使用 UART：**
- 裝置距離遠
- 需要多裝置通訊
- 需要靈活的拓撲
- 已有網路基礎設施

### Q: UART 和 USB 有什麼關係？

**說明：**
- Pico 透過 USB 連接到 Pi 時，實際上是使用 USB CDC (Communication Device Class)
- USB CDC 模擬串列埠，在 Pi 上顯示為 `/dev/ttyACM0`
- 從程式角度看，使用方式與 UART 相同
- 這就是為什麼模組名稱是 "UART/USB"

### Q: 如何選擇通訊方式？

**決策流程：**

```
需要多裝置通訊？
├─ 是 → 使用 MQTT
└─ 否 → 裝置距離遠？
    ├─ 是 → 使用 MQTT
    └─ 否 → 需要高速傳輸？
        ├─ 是 → 使用 UART
        └─ 否 → 兩者皆可，建議 MQTT（更靈活）
```

## 測試步驟

### 1. 硬體測試

```python
# Pico 迴路測試（短接 TX 和 RX）
import machine
uart = machine.UART(0, 9600, tx=machine.Pin(0), rx=machine.Pin(1))
uart.write("test")
print(uart.read())  # 應該顯示 "test"
```

### 2. 基本通訊測試

**Pico：**
```python
# 執行 pico_uart/uart_basic.py
```

**Pi：**
```bash
python pi_serial/serial_basic.py
```

### 3. 感測器資料測試

**Pico：**
```python
# 執行 pico_uart/uart_sensor.py
```

**Pi：**
```bash
python pi_serial/serial_receiver.py
```

## 故障排除

### 問題 1：找不到串列埠

```bash
# 列出所有串列埠
ls /dev/tty*

# 查看連接訊息
dmesg | grep tty
```

### 問題 2：權限被拒

```bash
# 加入 dialout 群組
sudo usermod -a -G dialout $USER

# 或臨時修改權限
sudo chmod 666 /dev/ttyACM0
```

### 問題 3：收到亂碼

**檢查：**
- 鮑率是否一致
- 硬體連接是否正確
- GND 是否連接

## 練習題

### 🟢 練習 1：雙向通訊

實作 Pico 和 Pi 的雙向通訊：
- Pi 發送命令
- Pico 執行並回應
- 顯示通訊狀態

### 🟡 練習 2：資料壓縮

實作資料壓縮傳輸：
- 使用二進位格式
- 減少資料大小
- 比較傳輸效率

### 🔴 練習 3：混合通訊

實作混合通訊系統：
- UART 用於本地除錯
- MQTT 用於遠端監控
- 自動切換通訊方式

## 檢核清單

完成本模組前，確認：

- [ ] 理解 UART 的基本原理
- [ ] 正確連接硬體
- [ ] 能夠發送和接收資料
- [ ] 理解鮑率的概念
- [ ] 能夠處理 JSON 資料
- [ ] 理解 UART 和 MQTT 的差異
- [ ] 能夠選擇適合的通訊方式

## 下一步

完成 UART/USB 模組後，繼續學習：

- **[整合應用](../05_integration/README.md)** - 建立完整系統
- **[多裝置管理](../06_multi_device/README.md)** - 管理多個裝置

## 參考資源

- [UART 協定說明](https://en.wikipedia.org/wiki/Universal_asynchronous_receiver-transmitter)
- [PySerial 文件](https://pyserial.readthedocs.io/)
- [MicroPython UART](https://docs.micropython.org/en/latest/library/machine.UART.html)
- [Serial Programming Guide](https://tldp.org/HOWTO/Serial-Programming-HOWTO/)

祝學習愉快！🚀
