# 快速參考指南

本文件提供常用命令和程式碼片段的快速參考。

## 目錄

- [MongoDB 命令](#mongodb-命令)
- [MQTT 命令](#mqtt-命令)
- [Docker 命令](#docker-命令)
- [Python 程式碼片段](#python-程式碼片段)
- [MicroPython 程式碼片段](#micropython-程式碼片段)

---

## MongoDB 命令

### 連接到 MongoDB

```bash
docker exec -it mongodb mongosh -u admin -p password123
```

### 常用查詢

```javascript
// 切換資料庫
use iot_data

// 查看所有集合
show collections

// 查詢所有資料
db.sensor_logs.find()

// 查詢最新 10 筆
db.sensor_logs.find().sort({timestamp: -1}).limit(10)

// 查詢特定裝置
db.sensor_logs.find({device_id: "pico_001"})

// 計數
db.sensor_logs.countDocuments()

// 刪除所有資料
db.sensor_logs.deleteMany({})

// 刪除特定資料
db.sensor_logs.deleteMany({device_id: "pico_001"})

// 建立索引
db.sensor_logs.createIndex({device_id: 1, timestamp: -1})

// 查看索引
db.sensor_logs.getIndexes()

// 聚合查詢（平均值）
db.sensor_logs.aggregate([
  {$match: {device_id: "pico_001"}},
  {$group: {_id: null, avg: {$avg: "$value"}}}
])
```

---

## MQTT 命令

### 訂閱主題

```bash
# 訂閱單一主題
mosquitto_sub -h localhost -t "sensors/temperature" -v

# 訂閱所有主題
mosquitto_sub -h localhost -t "#" -v

# 訂閱特定層級
mosquitto_sub -h localhost -t "sensors/#" -v

# 使用帳號密碼
mosquitto_sub -h localhost -t "sensors/#" -u username -P password -v
```

### 發布訊息

```bash
# 發布簡單訊息
mosquitto_pub -h localhost -t "test" -m "Hello"

# 發布 JSON 訊息
mosquitto_pub -h localhost -t "sensors/temperature" \
  -m '{"device_id":"test","value":25,"timestamp":"2025-10-11T12:00:00"}'

# 使用帳號密碼
mosquitto_pub -h localhost -t "test" -m "Hello" -u username -P password

# 設定 QoS
mosquitto_pub -h localhost -t "test" -m "Hello" -q 1
```

### 檢查 Mosquitto 狀態

```bash
# 檢查服務狀態
sudo systemctl status mosquitto

# 啟動服務
sudo systemctl start mosquitto

# 停止服務
sudo systemctl stop mosquitto

# 重新啟動服務
sudo systemctl restart mosquitto

# 查看日誌
sudo journalctl -u mosquitto -f
```

---

## Docker 命令

### 容器管理

```bash
# 查看運行中的容器
docker ps

# 查看所有容器
docker ps -a

# 啟動容器
docker start mongodb

# 停止容器
docker stop mongodb

# 重新啟動容器
docker restart mongodb

# 刪除容器
docker rm mongodb

# 查看容器日誌
docker logs mongodb
docker logs -f mongodb  # 持續顯示

# 進入容器
docker exec -it mongodb bash
```

### Docker Compose

```bash
# 啟動服務
docker-compose up -d

# 停止服務
docker-compose down

# 查看日誌
docker-compose logs -f

# 重新啟動服務
docker-compose restart

# 查看服務狀態
docker-compose ps
```

### 清理

```bash
# 刪除未使用的容器
docker container prune

# 刪除未使用的映像
docker image prune

# 刪除未使用的卷
docker volume prune

# 清理所有未使用的資源
docker system prune -a
```

---

## Python 程式碼片段

### MQTT 客戶端

```python
import paho.mqtt.client as mqtt
import json

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("已連接")
        client.subscribe("sensors/#")

def on_message(client, userdata, msg):
    data = json.loads(msg.payload.decode('utf-8'))
    print(f"收到: {data}")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("localhost", 1883, 60)
client.loop_forever()
```

### MongoDB 操作

```python
import pymongo
from datetime import datetime

# 連接
client = pymongo.MongoClient("mongodb://admin:password123@localhost:27017/")
db = client["iot_data"]
collection = db["sensor_logs"]

# 插入資料
data = {
    "device_id": "pico_001",
    "sensor_type": "temperature",
    "value": 25.5,
    "timestamp": datetime.now().isoformat()
}
collection.insert_one(data)

# 查詢資料
results = collection.find({"device_id": "pico_001"})
for doc in results:
    print(doc)

# 更新資料
collection.update_one(
    {"device_id": "pico_001"},
    {"$set": {"value": 26.0}}
)

# 刪除資料
collection.delete_many({"device_id": "pico_001"})

# 關閉連接
client.close()
```

### FastAPI 基本範例

```python
from fastapi import FastAPI, Query
from pydantic import BaseModel

app = FastAPI()

class SensorData(BaseModel):
    device_id: str
    value: float
    timestamp: str

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/api/data")
async def get_data(device_id: str = Query("pico_001")):
    # 查詢資料庫
    return {"device_id": device_id, "data": []}

@app.post("/api/data")
async def post_data(data: SensorData):
    # 儲存到資料庫
    return {"status": "success"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### 日誌設定

```python
import logging

# 基本設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# 使用
logger.info("資訊訊息")
logger.warning("警告訊息")
logger.error("錯誤訊息")

# 輸出到檔案
logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
```

---

## MicroPython 程式碼片段

### WiFi 連接

```python
import network
import time

def connect_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    
    if not wlan.isconnected():
        print(f"連接 WiFi: {ssid}")
        wlan.connect(ssid, password)
        
        timeout = 10
        while not wlan.isconnected() and timeout > 0:
            time.sleep(1)
            timeout -= 1
        
        if wlan.isconnected():
            print(f"已連接: {wlan.ifconfig()[0]}")
            return True
        else:
            print("連接失敗")
            return False
    
    return True
```

### MQTT 發布

```python
from umqtt.simple import MQTTClient
import json
import time

def publish_data(client, topic, data):
    message = json.dumps(data)
    client.publish(topic, message)
    print(f"已發布: {message}")

# 建立客戶端
client = MQTTClient("pico_001", "192.168.1.100", 1883)
client.connect()

# 發布資料
data = {
    "device_id": "pico_001",
    "value": 25.5,
    "timestamp": time.time()
}
publish_data(client, "sensors/temperature", data)

client.disconnect()
```

### 讀取溫度感測器

```python
import machine
import time

def read_temperature():
    sensor_temp = machine.ADC(4)
    reading = sensor_temp.read_u16() * (3.3 / 65535)
    temperature = 27 - (reading - 0.706) / 0.001721
    return round(temperature, 2)

# 持續讀取
while True:
    temp = read_temperature()
    print(f"溫度: {temp}°C")
    time.sleep(5)
```

### LED 控制

```python
import machine
import time

# 初始化 LED
led = machine.Pin("LED", machine.Pin.OUT)

# 開啟
led.on()

# 關閉
led.off()

# 閃爍
def blink(times=5, delay=0.5):
    for _ in range(times):
        led.on()
        time.sleep(delay)
        led.off()
        time.sleep(delay)

blink()
```

### 按鈕輸入

```python
import machine
import time

# 初始化按鈕（使用內部上拉電阻）
button = machine.Pin(15, machine.Pin.IN, machine.Pin.PULL_UP)

# 讀取狀態
while True:
    if button.value() == 0:  # 按下時為 0
        print("按鈕被按下")
        time.sleep(0.3)  # 防彈跳
```

### 錯誤處理

```python
import time

def safe_operation():
    try:
        # 可能會失敗的操作
        result = risky_function()
        return result
    except Exception as e:
        print(f"錯誤: {e}")
        return None

# 重試機制
def retry_operation(func, max_retries=3):
    for i in range(max_retries):
        try:
            return func()
        except Exception as e:
            print(f"嘗試 {i+1} 失敗: {e}")
            if i < max_retries - 1:
                time.sleep(2)
            else:
                raise
```

---

## 常用主題命名規範

### 感測器資料

```
sensors/{location}/{sensor_type}
sensors/living_room/temperature
sensors/bedroom/humidity
sensors/outdoor/light
```

### 控制命令

```
control/{device_id}
control/pico_001
control/pico_002
```

### 狀態更新

```
status/{device_id}
status/pico_001/online
status/pico_001/battery
```

### 警報

```
alerts/{severity}/{type}
alerts/critical/temperature
alerts/warning/battery
```

---

## 資料格式範例

### 感測器資料

```json
{
  "device_id": "pico_001",
  "sensor_type": "temperature",
  "value": 25.5,
  "unit": "celsius",
  "timestamp": "2025-10-11T12:00:00",
  "location": "living_room"
}
```

### 控制命令

```json
{
  "action": "led_on",
  "timestamp": "2025-10-11T12:00:00",
  "source": "automation"
}
```

### 警報訊息

```json
{
  "alert_id": "alert_001",
  "device_id": "pico_001",
  "alert_type": "high_temperature",
  "severity": "warning",
  "value": 32.5,
  "threshold": 30.0,
  "message": "溫度過高",
  "timestamp": "2025-10-11T12:00:00"
}
```

---

## 環境變數範例

### .env 檔案

```bash
# MongoDB
MONGO_HOST=localhost
MONGO_PORT=27017
MONGO_USER=admin
MONGO_PASSWORD=password123
MONGO_DB=iot_data

# MQTT
MQTT_BROKER=localhost
MQTT_PORT=1883
MQTT_USERNAME=
MQTT_PASSWORD=

# API
API_HOST=0.0.0.0
API_PORT=8000
API_KEY=your_secret_key

# Pico
WIFI_SSID=your_wifi_ssid
WIFI_PASSWORD=your_wifi_password
DEVICE_ID=pico_001
```

### 在 Python 中使用

```python
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_HOST = os.getenv("MONGO_HOST", "localhost")
MONGO_PORT = int(os.getenv("MONGO_PORT", 27017))
MQTT_BROKER = os.getenv("MQTT_BROKER", "localhost")
```

---

## 測試命令

### 測試 MongoDB 連接

```bash
docker exec mongodb mongosh -u admin -p password123 --eval "db.adminCommand('ping')"
```

### 測試 MQTT 連接

```bash
# 終端 1：訂閱
mosquitto_sub -h localhost -t "test" -v

# 終端 2：發布
mosquitto_pub -h localhost -t "test" -m "Hello"
```

### 測試 API

```bash
# 健康檢查
curl http://localhost:8000/

# GET 請求
curl http://localhost:8000/api/data?device_id=pico_001

# POST 請求
curl -X POST http://localhost:8000/api/data \
  -H "Content-Type: application/json" \
  -d '{"device_id":"pico_001","value":25.5,"timestamp":"2025-10-11T12:00:00"}'
```

### 測試 Pico 連接

```python
# 在 MicroPython REPL 中執行
import network
wlan = network.WLAN(network.STA_IF)
print(wlan.isconnected())
print(wlan.ifconfig())
```

---

**最後更新：** 2025-10-11  
**版本：** 1.0
