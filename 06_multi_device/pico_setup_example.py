"""
Pico 多裝置設定範例
在每個 Pico 上使用不同的配置
"""

# ============================================
# Pico 1 配置
# ============================================
# 在第一個 Pico 的 wifi_config.py 中設定：

DEVICE_ID = "pico_001"
DEVICE_NAME = "Temperature Sensor 1"
LOCATION = "Classroom A"

WIFI_SSID = "your_wifi_ssid"
WIFI_PASSWORD = "your_wifi_password"

MQTT_BROKER = "192.168.1.100"  # Pi 的 IP 位址
MQTT_PORT = 1883
MQTT_TOPIC = f"sensors/{DEVICE_ID}/temperature"

# ============================================
# Pico 2 配置
# ============================================
# 在第二個 Pico 的 wifi_config.py 中設定：

DEVICE_ID = "pico_002"
DEVICE_NAME = "Temperature Sensor 2"
LOCATION = "Classroom B"

WIFI_SSID = "your_wifi_ssid"
WIFI_PASSWORD = "your_wifi_password"

MQTT_BROKER = "192.168.1.100"  # Pi 的 IP 位址
MQTT_PORT = 1883
MQTT_TOPIC = f"sensors/{DEVICE_ID}/temperature"

# ============================================
# Pico 3 配置
# ============================================
# 在第三個 Pico 的 wifi_config.py 中設定：

DEVICE_ID = "pico_003"
DEVICE_NAME = "Temperature Sensor 3"
LOCATION = "Hallway"

WIFI_SSID = "your_wifi_ssid"
WIFI_PASSWORD = "your_wifi_password"

MQTT_BROKER = "192.168.1.100"  # Pi 的 IP 位址
MQTT_PORT = 1883
MQTT_TOPIC = f"sensors/{DEVICE_ID}/temperature"

# ============================================
# 使用說明
# ============================================
"""
1. 在每個 Pico 上建立 wifi_config.py
2. 複製對應的配置到該檔案
3. 修改 WIFI_SSID、WIFI_PASSWORD 和 MQTT_BROKER
4. 確保每個 Pico 的 DEVICE_ID 都不同
5. 執行 sensor_publisher.py 開始發送資料

範例 sensor_publisher.py：

```python
from wifi_manager import WiFiManager
from mqtt_client import PicoMQTTClient
from sensor_reader import SensorReader
import wifi_config
import time
import json

# 連接 WiFi
wifi = WiFiManager(wifi_config.WIFI_SSID, wifi_config.WIFI_PASSWORD)
if not wifi.connect():
    print("WiFi 連接失敗")
    sys.exit(1)

# 連接 MQTT
mqtt = PicoMQTTClient(
    client_id=wifi_config.DEVICE_ID,
    broker=wifi_config.MQTT_BROKER,
    port=wifi_config.MQTT_PORT
)

if not mqtt.connect():
    print("MQTT 連接失敗")
    sys.exit(1)

# 建立感測器讀取器
sensor = SensorReader()

# 主迴圈
while True:
    try:
        # 讀取溫度
        temp = sensor.read_temperature()
        
        # 建立資料
        data = {
            "device_id": wifi_config.DEVICE_ID,
            "device_name": wifi_config.DEVICE_NAME,
            "location": wifi_config.LOCATION,
            "sensor_type": "temperature",
            "value": temp,
            "unit": "celsius",
            "timestamp": time.time()
        }
        
        # 發布資料
        mqtt.publish(wifi_config.MQTT_TOPIC, json.dumps(data))
        print(f"[{wifi_config.DEVICE_ID}] 發送: {temp}°C")
        
        # 等待 30 秒
        time.sleep(30)
        
    except KeyboardInterrupt:
        break
    except Exception as e:
        print(f"錯誤: {e}")
        time.sleep(5)

# 清理
mqtt.disconnect()
```
"""
