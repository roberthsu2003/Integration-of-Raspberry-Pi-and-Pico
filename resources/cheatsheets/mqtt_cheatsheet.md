# MQTT 速查表

快速參考 MQTT 協定和 Paho MQTT 客戶端的常用功能。

## MQTT 基礎概念

### 核心元件
- **Broker（代理）**: 訊息伺服器，負責接收和分發訊息
- **Publisher（發布者）**: 發送訊息的客戶端
- **Subscriber（訂閱者）**: 接收訊息的客戶端
- **Topic（主題）**: 訊息的分類標籤

### 訊息流程
```
Publisher → Topic → Broker → Topic → Subscriber
```

### QoS 等級
- **QoS 0**: 最多一次（Fire and Forget）
- **QoS 1**: 至少一次（需要確認）
- **QoS 2**: 恰好一次（四次握手）

## Mosquitto Broker

### 安裝
```bash
# Ubuntu/Debian
sudo apt-get install mosquitto mosquitto-clients

# macOS
brew install mosquitto

# Docker
docker run -d -p 1883:1883 -p 9001:9001 eclipse-mosquitto
```

### 基本指令
```bash
# 啟動 Broker
mosquitto

# 使用設定檔啟動
mosquitto -c mosquitto.conf

# 訂閱主題
mosquitto_sub -h localhost -t "test/topic"

# 發布訊息
mosquitto_pub -h localhost -t "test/topic" -m "Hello MQTT"

# 訂閱所有主題
mosquitto_sub -h localhost -t "#" -v
```

### 設定檔範例
```conf
# mosquitto.conf
listener 1883
allow_anonymous true

# 啟用 WebSocket
listener 9001
protocol websockets

# 日誌
log_dest file /var/log/mosquitto/mosquitto.log
log_type all
```

## Python - Paho MQTT

### 安裝
```bash
pip install paho-mqtt
```

### 基本發布者
```python
import paho.mqtt.client as mqtt

# 建立客戶端
client = mqtt.Client()

# 連接到 Broker
client.connect("localhost", 1883, 60)

# 發布訊息
client.publish("test/topic", "Hello MQTT")

# 斷開連接
client.disconnect()
```

### 基本訂閱者
```python
import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print(f"連接成功，返回碼: {rc}")
    client.subscribe("test/topic")

def on_message(client, userdata, msg):
    print(f"收到訊息: {msg.topic} {msg.payload.decode()}")

# 建立客戶端
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# 連接並開始循環
client.connect("localhost", 1883, 60)
client.loop_forever()
```

### 完整客戶端範例
```python
import paho.mqtt.client as mqtt
import time

class MQTTClient:
    def __init__(self, broker, port=1883, client_id=""):
        self.broker = broker
        self.port = port
        self.client = mqtt.Client(client_id)
        self.connected = False
        
        # 設定回調函式
        self.client.on_connect = self._on_connect
        self.client.on_disconnect = self._on_disconnect
        self.client.on_message = self._on_message
        self.client.on_publish = self._on_publish
    
    def _on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("連接成功")
            self.connected = True
        else:
            print(f"連接失敗，錯誤碼: {rc}")
    
    def _on_disconnect(self, client, userdata, rc):
        print("已斷開連接")
        self.connected = False
    
    def _on_message(self, client, userdata, msg):
        print(f"收到: {msg.topic} - {msg.payload.decode()}")
    
    def _on_publish(self, client, userdata, mid):
        print(f"訊息已發布 (mid: {mid})")
    
    def connect(self):
        """連接到 Broker"""
        try:
            self.client.connect(self.broker, self.port, 60)
            self.client.loop_start()
            
            # 等待連接
            timeout = 10
            while not self.connected and timeout > 0:
                time.sleep(0.5)
                timeout -= 0.5
            
            return self.connected
        except Exception as e:
            print(f"連接失敗: {e}")
            return False
    
    def disconnect(self):
        """斷開連接"""
        self.client.loop_stop()
        self.client.disconnect()
    
    def publish(self, topic, message, qos=0):
        """發布訊息"""
        if not self.connected:
            print("未連接到 Broker")
            return False
        
        result = self.client.publish(topic, message, qos)
        return result.rc == mqtt.MQTT_ERR_SUCCESS
    
    def subscribe(self, topic, qos=0):
        """訂閱主題"""
        if not self.connected:
            print("未連接到 Broker")
            return False
        
        result = self.client.subscribe(topic, qos)
        return result[0] == mqtt.MQTT_ERR_SUCCESS

# 使用範例
client = MQTTClient("localhost")
if client.connect():
    client.subscribe("sensors/#")
    client.publish("sensors/temp", "25.5")
    time.sleep(5)
    client.disconnect()
```

## MicroPython - MQTT

### 基本發布者（Pico W）
```python
from umqtt.simple import MQTTClient
import time

# 建立客戶端
client = MQTTClient(
    client_id="pico_001",
    server="192.168.1.100",
    port=1883
)

# 連接
client.connect()

# 發布訊息
client.publish("sensors/temp", "25.5")

# 斷開連接
client.disconnect()
```

### 基本訂閱者（Pico W）
```python
from umqtt.simple import MQTTClient

def on_message(topic, msg):
    print(f"收到: {topic.decode()} - {msg.decode()}")

# 建立客戶端
client = MQTTClient(
    client_id="pico_002",
    server="192.168.1.100",
    port=1883
)

# 設定回調
client.set_callback(on_message)

# 連接並訂閱
client.connect()
client.subscribe("commands/#")

# 持續監聽
while True:
    client.check_msg()
    time.sleep(0.1)
```

### 完整 Pico 客戶端
```python
from umqtt.simple import MQTTClient
import time

class PicoMQTTClient:
    def __init__(self, client_id, broker, port=1883):
        self.client_id = client_id
        self.broker = broker
        self.port = port
        self.client = None
        self.connected = False
    
    def connect(self, retry=3):
        """連接到 Broker（含重試）"""
        for attempt in range(retry):
            try:
                self.client = MQTTClient(
                    self.client_id,
                    self.broker,
                    self.port
                )
                self.client.connect()
                self.connected = True
                print(f"連接成功: {self.broker}")
                return True
            except Exception as e:
                print(f"連接失敗 (嘗試 {attempt + 1}/{retry}): {e}")
                time.sleep(2)
        
        return False
    
    def disconnect(self):
        """斷開連接"""
        if self.client:
            try:
                self.client.disconnect()
                self.connected = False
                print("已斷開連接")
            except:
                pass
    
    def publish(self, topic, message, qos=0):
        """發布訊息"""
        if not self.connected:
            print("未連接到 Broker")
            return False
        
        try:
            self.client.publish(topic, message, qos=qos)
            return True
        except Exception as e:
            print(f"發布失敗: {e}")
            self.connected = False
            return False
    
    def subscribe(self, topic, callback):
        """訂閱主題"""
        if not self.connected:
            print("未連接到 Broker")
            return False
        
        try:
            self.client.set_callback(callback)
            self.client.subscribe(topic)
            return True
        except Exception as e:
            print(f"訂閱失敗: {e}")
            return False
    
    def check_msg(self):
        """檢查新訊息（非阻塞）"""
        if self.connected:
            try:
                self.client.check_msg()
            except Exception as e:
                print(f"檢查訊息失敗: {e}")
                self.connected = False

# 使用範例
client = PicoMQTTClient("pico_001", "192.168.1.100")
if client.connect():
    client.publish("sensors/temp", "25.5")
    client.disconnect()
```

## 主題命名規範

### 最佳實踐
```
# 良好的主題結構
sensors/device_001/temperature
sensors/device_001/humidity
home/living_room/light/status
home/bedroom/temperature

# 避免
sensor_data          # 太籠統
/sensors/temp        # 不要以 / 開頭
sensors/temp/        # 不要以 / 結尾
sensors//temp        # 不要有空層級
```

### 萬用字元
```python
# + 匹配單一層級
"sensors/+/temperature"  # 匹配 sensors/device1/temperature
                         # 匹配 sensors/device2/temperature

# # 匹配多層級（必須在最後）
"sensors/#"              # 匹配 sensors/device1/temperature
                         # 匹配 sensors/device1/humidity
                         # 匹配 sensors/device2/light/status
```

## 訊息格式

### JSON 格式（推薦）
```python
import json

# 發布
data = {
    "device_id": "pico_001",
    "temperature": 25.5,
    "timestamp": "2025-10-11T10:30:00Z"
}
client.publish("sensors/data", json.dumps(data))

# 接收
def on_message(client, userdata, msg):
    data = json.loads(msg.payload.decode())
    print(f"溫度: {data['temperature']}")
```

### 純文字格式
```python
# 簡單數值
client.publish("sensors/temp", "25.5")

# CSV 格式
client.publish("sensors/data", "25.5,60.2,1013.25")
```

## 進階功能

### 遺囑訊息（Last Will）
```python
# Python
client = mqtt.Client()
client.will_set("status/device_001", "offline", qos=1, retain=True)
client.connect("localhost", 1883, 60)

# MicroPython
client = MQTTClient(
    "pico_001",
    "192.168.1.100",
    keepalive=60
)
# 注意: umqtt.simple 不支援遺囑訊息
# 需要使用 umqtt.robust 或其他函式庫
```

### 保留訊息（Retained）
```python
# 發布保留訊息
client.publish("status/device_001", "online", retain=True)

# 新訂閱者會立即收到最後的保留訊息
```

### 持久會話
```python
# Python
client = mqtt.Client(client_id="device_001", clean_session=False)

# MicroPython
client = MQTTClient("pico_001", "192.168.1.100", keepalive=60)
# clean_session 預設為 True
```

### 認證
```python
# Python
client = mqtt.Client()
client.username_pw_set("username", "password")
client.connect("localhost", 1883, 60)

# MicroPython
client = MQTTClient(
    "pico_001",
    "192.168.1.100",
    user="username",
    password="password"
)
```

### TLS/SSL
```python
# Python
import ssl

client = mqtt.Client()
client.tls_set(
    ca_certs="ca.crt",
    certfile="client.crt",
    keyfile="client.key",
    cert_reqs=ssl.CERT_REQUIRED
)
client.connect("localhost", 8883, 60)
```

## 錯誤處理

### 連接錯誤碼
```python
# 0: 連接成功
# 1: 協定版本不正確
# 2: 客戶端 ID 無效
# 3: 伺服器不可用
# 4: 使用者名稱或密碼錯誤
# 5: 未授權

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("連接成功")
    elif rc == 1:
        print("協定版本不正確")
    elif rc == 2:
        print("客戶端 ID 無效")
    elif rc == 3:
        print("伺服器不可用")
    elif rc == 4:
        print("使用者名稱或密碼錯誤")
    elif rc == 5:
        print("未授權")
```

### 重連機制
```python
def connect_with_retry(client, broker, port, max_retries=5):
    """帶重試的連接函式"""
    for attempt in range(max_retries):
        try:
            client.connect(broker, port, 60)
            return True
        except Exception as e:
            print(f"連接失敗 (嘗試 {attempt + 1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)  # 指數退避
    return False
```

## 測試工具

### MQTT Explorer
- GUI 工具，可視化 MQTT 訊息
- 下載: http://mqtt-explorer.com/

### mosquitto_sub/pub
```bash
# 監控所有訊息
mosquitto_sub -h localhost -t "#" -v

# 發布測試訊息
mosquitto_pub -h localhost -t "test" -m "Hello"

# 使用 QoS 1
mosquitto_pub -h localhost -t "test" -m "Hello" -q 1

# 保留訊息
mosquitto_pub -h localhost -t "status" -m "online" -r
```

## 效能優化

### 批次發布
```python
# 使用 loop_start() 進行非阻塞發布
client.loop_start()
for i in range(100):
    client.publish(f"sensors/device_{i}", f"value_{i}")
client.loop_stop()
```

### 訊息壓縮
```python
import gzip
import json

# 壓縮大型 JSON
data = {"large": "data" * 1000}
compressed = gzip.compress(json.dumps(data).encode())
client.publish("data/compressed", compressed)
```

## 常見問題

### Q: 訊息沒有收到？
A: 檢查：
1. Broker 是否運行
2. 主題是否匹配
3. QoS 設定
4. 網路連接

### Q: 如何確保訊息送達？
A: 使用 QoS 1 或 2，並檢查發布結果

### Q: 如何處理大量訊息？
A: 使用適當的 QoS、批次處理、訊息壓縮

### Q: Pico 斷線後如何重連？
A: 實作重連機制，定期檢查連接狀態

## 參考資源

- [MQTT 官方網站](https://mqtt.org/)
- [Paho MQTT Python 文件](https://www.eclipse.org/paho/index.php?page=clients/python/docs/index.php)
- [Mosquitto 文件](https://mosquitto.org/documentation/)
- [MQTT 規範](https://docs.oasis-open.org/mqtt/mqtt/v5.0/mqtt-v5.0.html)
