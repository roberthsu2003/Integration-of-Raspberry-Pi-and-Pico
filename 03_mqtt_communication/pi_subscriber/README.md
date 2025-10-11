# Pi MQTT 訂閱者

本目錄包含 Raspberry Pi 端的 MQTT 訂閱者程式，用於接收 Pico 發送的感測器資料並儲存到資料庫。

## 檔案說明

```
pi_subscriber/
├── mqtt_client.py          # MQTT 客戶端類別
├── data_handler.py         # 資料處理和儲存
├── subscriber.py           # 主程式
└── README.md              # 本檔案
```

## 快速開始

### 1. 安裝依賴套件

```bash
pip install paho-mqtt pymongo
```

### 2. 確保服務運行

**啟動 MongoDB：**
```bash
cd 02_pi_basics
docker-compose up -d
```

**啟動 MQTT Broker：**
```bash
cd 03_mqtt_communication/mqtt_broker
docker-compose up -d
```

### 3. 執行訂閱者

```bash
cd 03_mqtt_communication/pi_subscriber
python subscriber.py
```

預期輸出：
```
============================================================
MQTT 訂閱者啟動中...
============================================================

連接到 MQTT Broker: localhost:1883
✓ MQTT 連接成功
  訂閱主題: sensors/#

============================================================
設定完成！開始接收資料...
============================================================

提示：
  - 按 Ctrl+C 停止程式
  - 按 Ctrl+\ 顯示統計資訊

--------------------------------------------------
📨 收到訊息 [1]
主題: sensors/pico_001/temperature
裝置: pico_001
類型: temperature
數值: 28.5 celsius
位置: classroom_a
時間: 2025-01-11 10:30:00
--------------------------------------------------
✓ 插入感測器資料: 507f1f77bcf86cd799439011
```

## 命令列選項

```bash
# 基本使用
python subscriber.py

# 指定 Broker 位址
python subscriber.py --broker 192.168.1.100

# 指定連接埠
python subscriber.py --port 1883

# 自訂客戶端 ID
python subscriber.py --client-id my_subscriber

# 不使用資料庫（僅顯示資料）
python subscriber.py --no-db

# 組合使用
python subscriber.py --broker 192.168.1.100 --port 1883 --no-db
```

## 模組說明

### PiMQTTClient

MQTT 客戶端類別，處理連接和訊息接收。

**主要方法：**
```python
# 建立客戶端
client = PiMQTTClient(
    client_id="pi_subscriber",
    broker="localhost",
    port=1883
)

# 連接到 Broker
client.connect()

# 訂閱主題
def callback(topic, data):
    print(f"收到: {topic} - {data}")

client.subscribe("sensors/#", callback)

# 取得統計資訊
stats = client.get_statistics()
```

**支援的萬用字元：**
- `+` : 單層萬用字元
  - `sensors/+/temperature` 匹配 `sensors/pico_001/temperature`
- `#` : 多層萬用字元
  - `sensors/#` 匹配 `sensors/pico_001/temperature` 和 `sensors/pico_001/humidity`

### DataHandler

資料處理器類別，驗證和儲存資料。

**主要方法：**
```python
# 建立處理器
handler = DataHandler(db_manager)

# 處理訊息
handler.handle_message(topic, data)

# 取得統計資訊
stats = handler.get_statistics()

# 查看最近的資料
recent = handler.get_recent_data(count=5)
```

**資料驗證：**
- 檢查必填欄位
- 驗證資料型別
- 格式化時間戳記
- 四捨五入數值

### MQTTSubscriber

整合訂閱者類別，組合 MQTT 客戶端和資料處理器。

**主要方法：**
```python
# 建立訂閱者
subscriber = MQTTSubscriber(
    client_id="pi_subscriber",
    broker="localhost",
    port=1883,
    use_database=True
)

# 執行
subscriber.run()
```

## 資料流程

```
Pico 發布 MQTT 訊息
        ↓
MQTT Broker 轉發
        ↓
Pi 訂閱者接收
        ↓
資料驗證和格式化
        ↓
儲存到 MongoDB
        ↓
顯示統計資訊
```

## 訂閱主題

預設訂閱 `sensors/#`，匹配所有感測器主題：

- `sensors/pico_001/temperature`
- `sensors/pico_002/temperature`
- `sensors/pico_001/humidity`
- 等等...

## 資料格式

接收的 JSON 資料格式：

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

## 測試

### 1. 測試 MQTT 客戶端

```python
from mqtt_client import PiMQTTClient

def on_message(topic, data):
    print(f"收到: {topic} - {data}")

client = PiMQTTClient("test_client", "localhost", 1883)
if client.connect():
    client.subscribe("test/#", on_message)
    
    import time
    time.sleep(60)  # 等待 60 秒
    
    client.disconnect()
```

### 2. 測試資料處理器

```python
from data_handler import DataHandler

handler = DataHandler()

test_data = {
    "device_id": "pico_test",
    "sensor_type": "temperature",
    "value": 25.5,
    "unit": "celsius"
}

handler.handle_message("sensors/pico_test/temperature", test_data)
handler.print_statistics()
```

### 3. 使用 mosquitto_pub 發送測試訊息

```bash
# 發送測試訊息
mosquitto_pub -h localhost -t "sensors/pico_test/temperature" \
  -m '{"device_id":"pico_test","sensor_type":"temperature","value":25.5,"unit":"celsius"}'

# 發送多則訊息
for i in {1..10}; do
  mosquitto_pub -h localhost -t "sensors/pico_001/temperature" \
    -m "{\"device_id\":\"pico_001\",\"sensor_type\":\"temperature\",\"value\":$((25 + RANDOM % 5)).$((RANDOM % 10)),\"unit\":\"celsius\"}"
  sleep 1
done
```

## 常見問題

### Q: 無法連接到 MQTT Broker？

**檢查項目：**
```bash
# 檢查 Broker 是否運行
docker ps | grep mosquitto

# 測試連接
mosquitto_sub -h localhost -t test

# 檢查連接埠
sudo netstat -tulpn | grep 1883
```

### Q: 無法連接到資料庫？

**檢查項目：**
```bash
# 檢查 MongoDB 是否運行
docker ps | grep mongodb

# 測試連接
python -c "from pymongo import MongoClient; client = MongoClient('mongodb://admin:password123@localhost:27017/'); print('OK')"
```

### Q: 收不到訊息？

**除錯步驟：**
1. 確認 Pico 正在發布訊息
2. 使用 mosquitto_sub 測試：
```bash
mosquitto_sub -h localhost -t "sensors/#" -v
```
3. 檢查主題是否匹配
4. 查看訂閱者的錯誤訊息

### Q: 資料沒有儲存到資料庫？

**可能原因：**
1. 資料庫連接失敗
2. 資料驗證失敗
3. 權限問題

**除錯方法：**
```python
# 執行時加入 --no-db 選項，查看資料是否正確接收
python subscriber.py --no-db

# 檢查資料庫
docker exec -it iot_mongodb mongosh -u admin -p password123
> use iot_data
> db.sensor_data.find().limit(5)
```

## 進階功能

### 1. 自訂訊息處理

```python
class CustomDataHandler(DataHandler):
    def handle_message(self, topic, data):
        # 自訂處理邏輯
        if data.get('value') > 30:
            print("⚠ 溫度過高警報！")
        
        # 呼叫父類別方法
        super().handle_message(topic, data)
```

### 2. 多主題訂閱

```python
# 訂閱多個主題
client.subscribe("sensors/+/temperature", on_temperature)
client.subscribe("sensors/+/humidity", on_humidity)
client.subscribe("alerts/#", on_alert)
```

### 3. 訊息過濾

```python
def on_sensor_data(topic, data):
    # 只處理特定裝置
    if data.get('device_id') in ['pico_001', 'pico_002']:
        handler.handle_message(topic, data)
```

### 4. 資料聚合

```python
class AggregatingHandler(DataHandler):
    def __init__(self, db_manager, batch_size=10):
        super().__init__(db_manager)
        self.batch = []
        self.batch_size = batch_size
    
    def handle_message(self, topic, data):
        self.batch.append(data)
        
        if len(self.batch) >= self.batch_size:
            # 批次儲存
            for item in self.batch:
                self.save_to_database(item)
            self.batch = []
```

## 監控和日誌

### 查看統計資訊

執行中按 `Ctrl+\` 顯示統計資訊：

```
============================================================
統計資訊
============================================================

MQTT 客戶端:
  連接狀態: 已連接
  接收訊息: 150 則
  發生錯誤: 2 次

資料處理:
  處理訊息: 150 則
  成功儲存: 148 則
  發生錯誤: 2 次
  成功率: 98.7%
============================================================
```

### 日誌記錄

```python
import logging

# 設定日誌
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('subscriber.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)
logger.info("訂閱者啟動")
```

## 效能優化

### 1. 使用批次插入

```python
# 累積資料後批次插入
batch = []
for data in incoming_data:
    batch.append(data)
    if len(batch) >= 100:
        db.sensor_data.insert_many(batch)
        batch = []
```

### 2. 使用非同步處理

```python
import asyncio
from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor(max_workers=4)

def handle_message_async(topic, data):
    executor.submit(handler.handle_message, topic, data)
```

## 檢核清單

完成本單元前，確認：

- [ ] 成功連接到 MQTT Broker
- [ ] 能夠接收 Pico 發送的訊息
- [ ] 資料能夠儲存到 MongoDB
- [ ] 理解訂閱主題和萬用字元
- [ ] 能夠查看統計資訊
- [ ] 能夠處理連接中斷
- [ ] 理解資料驗證流程

## 下一步

完成 Pi 訂閱者後，繼續學習：
- [MQTT 測試工具](../mqtt_test_tools/README.md) - 測試和除錯
- [整合應用](../../05_integration/README.md) - 完整的系統整合

## 參考資源

- [Paho MQTT Python 文件](https://www.eclipse.org/paho/index.php?page=clients/python/docs/index.php)
- [MQTT 協定規範](https://mqtt.org/mqtt-specification/)
- [MongoDB Python 驅動程式](https://pymongo.readthedocs.io/)
