# Pico MQTT 發布者

本目錄包含 Pico 端的 MQTT 客戶端程式，用於發布感測器資料到 MQTT Broker。

## 檔案說明

```
pico_publisher/
├── wifi_config.py          # WiFi 和 MQTT 配置（需要修改）
├── wifi_manager.py         # WiFi 連接管理
├── mqtt_client.py          # MQTT 客戶端
├── sensor_publisher.py     # 感測器資料發布程式
└── README.md              # 本檔案
```

## 快速開始

### 1. 修改配置

編輯 `wifi_config.py`，填入你的 WiFi 和 MQTT 設定：

```python
# WiFi 設定
WIFI_SSID = "your_wifi_ssid"
WIFI_PASSWORD = "your_wifi_password"

# MQTT Broker 設定
MQTT_BROKER = "192.168.1.100"  # Raspberry Pi 的 IP
MQTT_PORT = 1883
MQTT_CLIENT_ID = "pico_001"

# 裝置資訊
DEVICE_ID = "pico_001"
DEVICE_NAME = "Temperature Sensor 1"
DEVICE_LOCATION = "classroom_a"
```

### 2. 安裝 MQTT 函式庫

在 Thonny 中：
1. 點擊 "Tools" > "Manage packages"
2. 搜尋 "umqtt.simple"
3. 點擊安裝

或在 Pico 的 REPL 中執行：
```python
import upip
upip.install('umqtt.simple')
```

### 3. 上傳檔案到 Pico

使用 Thonny 將以下檔案上傳到 Pico：
- `wifi_config.py`
- `wifi_manager.py`
- `mqtt_client.py`
- `sensor_publisher.py`

### 4. 執行程式

在 Thonny 中開啟 `sensor_publisher.py` 並執行。

預期輸出：
```
==================================================
感測器發布者啟動中...
==================================================

[1/2] 連接 WiFi...
正在連接到 WiFi: your_wifi_ssid
WiFi 連接成功！
========================================
網路資訊:
  IP 位址: 192.168.1.101
  ...
========================================
✓ WiFi 連接成功

[2/2] 連接 MQTT Broker...
正在連接到 MQTT Broker: 192.168.1.100:1883
MQTT 連接成功！
✓ MQTT 連接成功

==================================================
設定完成！開始發布資料...
==================================================

✓ 發布訊息到 sensors/pico_001/temperature
[1] 溫度: 28.50°C
✓ 發布訊息到 sensors/pico_001/temperature
[2] 溫度: 28.52°C
...
```

## 模組說明

### WiFiManager

管理 WiFi 連接的類別。

**主要方法：**
```python
wifi = WiFiManager(ssid, password)

# 連接 WiFi
wifi.connect()

# 檢查連接狀態
if wifi.is_connected():
    print("已連接")

# 取得 IP 位址
ip = wifi.get_ip()

# 自動重連
wifi.reconnect_if_needed()
```

### PicoMQTTClient

MQTT 客戶端類別。

**主要方法：**
```python
mqtt = PicoMQTTClient(client_id, broker, port)

# 連接到 Broker
mqtt.connect()

# 發布訊息
mqtt.publish(topic, message)

# 發布感測器資料（便利方法）
mqtt.publish_sensor_data(
    device_id="pico_001",
    sensor_type="temperature",
    value=25.5,
    unit="celsius"
)
```

### SensorPublisher

整合感測器讀取和 MQTT 發布的類別。

**主要方法：**
```python
publisher = SensorPublisher(
    device_id="pico_001",
    location="classroom_a",
    publish_interval=5
)

# 執行發布者
publisher.run()
```

## MQTT 主題結構

發布的訊息使用以下主題結構：

```
sensors/{device_id}/{sensor_type}
```

範例：
- `sensors/pico_001/temperature`
- `sensors/pico_002/temperature`

## 訊息格式

發布的 JSON 訊息格式：

```json
{
    "device_id": "pico_001",
    "device_type": "pico_w",
    "sensor_type": "temperature",
    "value": 25.5,
    "unit": "celsius",
    "timestamp": 1704974422,
    "location": "classroom_a"
}
```

## 測試步驟

### 1. 測試 WiFi 連接

```python
from wifi_manager import WiFiManager
from wifi_config import WIFI_SSID, WIFI_PASSWORD

wifi = WiFiManager(WIFI_SSID, WIFI_PASSWORD)
if wifi.connect():
    print(f"IP: {wifi.get_ip()}")
```

### 2. 測試 MQTT 連接

```python
from mqtt_client import PicoMQTTClient
from wifi_config import MQTT_BROKER, MQTT_PORT

mqtt = PicoMQTTClient("test_client", MQTT_BROKER, MQTT_PORT)
if mqtt.connect():
    mqtt.publish("test/topic", "Hello MQTT")
```

### 3. 測試感測器讀取

```python
import machine

sensor = machine.ADC(4)
adc_value = sensor.read_u16()
voltage = adc_value * (3.3 / 65535)
temperature = 27 - (voltage - 0.706) / 0.001721
print(f"溫度: {temperature:.2f}°C")
```

## 常見問題

### Q: WiFi 無法連接？

**檢查項目：**
1. SSID 和密碼是否正確
2. WiFi 是否為 2.4GHz（Pico W 不支援 5GHz）
3. 訊號強度是否足夠
4. 路由器是否允許新裝置連接

**除錯方法：**
```python
# 掃描可用的 WiFi 網路
import network
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
networks = wlan.scan()
for net in networks:
    print(net[0].decode())  # 顯示 SSID
```

### Q: MQTT 連接失敗？

**檢查項目：**
1. MQTT Broker 是否正在運行
2. IP 位址是否正確
3. 連接埠是否正確（預設 1883）
4. 防火牆是否阻擋連接

**測試 Broker：**
```bash
# 在 Pi 上測試
mosquitto_sub -h localhost -t test
```

### Q: 訊息沒有發布成功？

**除錯步驟：**
1. 檢查 MQTT 連接狀態
2. 在 Pi 上訂閱主題查看：
```bash
mosquitto_sub -h localhost -t "sensors/#" -v
```
3. 查看 Pico 的錯誤訊息
4. 檢查訊息格式是否正確

### Q: 連接經常中斷？

**可能原因：**
1. WiFi 訊號不穩定
2. 電源供應不足
3. keepalive 時間設定不當

**解決方法：**
```python
# 調整 keepalive 時間
mqtt = PicoMQTTClient(
    client_id="pico_001",
    broker=MQTT_BROKER,
    keepalive=30  # 減少到 30 秒
)

# 定期 ping
mqtt.ping()
```

## 進階功能

### 1. 發布多種感測器資料

```python
# 溫度
mqtt.publish_sensor_data(
    device_id=DEVICE_ID,
    sensor_type="temperature",
    value=25.5,
    unit="celsius"
)

# 濕度（如果有外接感測器）
mqtt.publish_sensor_data(
    device_id=DEVICE_ID,
    sensor_type="humidity",
    value=60.0,
    unit="percent"
)
```

### 2. 自訂發布間隔

```python
# 快速發布（每秒一次）
publisher = SensorPublisher(
    device_id=DEVICE_ID,
    publish_interval=1
)

# 慢速發布（每分鐘一次）
publisher = SensorPublisher(
    device_id=DEVICE_ID,
    publish_interval=60
)
```

### 3. 條件式發布

```python
def publish_if_changed(self, threshold=0.5):
    """只在溫度變化超過閾值時發布"""
    current_temp = self.read_temperature()
    
    if abs(current_temp - self.last_temp) > threshold:
        self.mqtt.publish_sensor_data(...)
        self.last_temp = current_temp
```

### 4. 批次發布

```python
def publish_batch(self, readings):
    """批次發布多筆資料"""
    data = {
        "device_id": DEVICE_ID,
        "readings": readings,
        "count": len(readings)
    }
    self.mqtt.publish("sensors/batch", data)
```

## 效能優化

### 減少記憶體使用

```python
# 使用 gc 模組進行垃圾回收
import gc

while True:
    publish_sensor_data()
    gc.collect()  # 手動觸發垃圾回收
    time.sleep(5)
```

### 降低功耗

```python
import machine

# 使用輕度睡眠
machine.lightsleep(5000)  # 睡眠 5 秒

# 使用深度睡眠（會重新啟動）
machine.deepsleep(60000)  # 睡眠 60 秒
```

## 檢核清單

完成本單元前，確認：

- [ ] 已修改 wifi_config.py 的設定
- [ ] 已安裝 umqtt.simple 函式庫
- [ ] WiFi 能夠成功連接
- [ ] MQTT 能夠成功連接
- [ ] 能夠發布測試訊息
- [ ] 能夠發布感測器資料
- [ ] 理解主題結構和訊息格式
- [ ] 能夠處理連接中斷

## 下一步

完成 Pico 發布者後，繼續學習：
- [Pi 訂閱者](../pi_subscriber/README.md) - 接收和處理資料
- [整合應用](../../05_integration/README.md) - 完整的資料流程

## 參考資源

- [umqtt 文件](https://github.com/micropython/micropython-lib/tree/master/micropython/umqtt.simple)
- [MQTT 協定](https://mqtt.org/)
- [Pico W 網路功能](https://datasheets.raspberrypi.com/picow/connecting-to-the-internet-with-pico-w.pdf)
