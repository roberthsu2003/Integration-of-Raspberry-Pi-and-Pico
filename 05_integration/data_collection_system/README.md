# 資料收集系統

這個範例展示如何整合 MQTT 訂閱和 MongoDB，自動將 Pico 發送的感測器資料儲存到資料庫。

## 📋 學習目標

- 學習如何整合 MQTT 和 MongoDB
- 掌握資料驗證的重要性
- 理解自動化資料收集流程
- 學習錯誤處理和統計追蹤

## 🔧 前置需求

### 硬體
- Raspberry Pi Pico W（執行發布者程式）
- Raspberry Pi（執行資料收集系統）

### 軟體
- MongoDB（透過 Docker 運行）
- Mosquitto MQTT Broker
- Python 3.7+

## 📁 檔案說明

```
data_collection_system/
├── README.md              # 本說明文件
├── mqtt_to_db.py          # MQTT 到 MongoDB 資料收集程式
└── requirements.txt       # Python 套件需求
```

## 🚀 使用步驟

### 步驟 1：啟動 MongoDB

使用 Docker Compose 啟動 MongoDB：

```bash
cd 02_pi_basics
docker-compose up -d
```

驗證 MongoDB 運作：

```bash
docker ps
# 應該看到 mongodb 容器正在運行
```

### 步驟 2：安裝 Python 套件

```bash
cd 05_integration/data_collection_system
pip3 install -r requirements.txt
```

### 步驟 3：啟動資料收集系統

```bash
python3 mqtt_to_db.py
```

你應該會看到：

```
============================================================
資料收集系統 - MQTT 到 MongoDB
============================================================

✓ 成功連接到 MongoDB: iot_data.sensor_readings
資料庫現有記錄: 0 筆

正在連接到 MQTT Broker: localhost:1883...
✓ 成功連接到 MQTT Broker
✓ 訂閱主題: sensors/#

等待接收資料...
按 Ctrl+C 停止
```

### 步驟 4：啟動 Pico 發布者

使用前一個範例的 `pico_publisher.py` 或任何 MQTT 發布程式。

### 步驟 5：觀察資料儲存

當 Pico 發布資料時，你會看到：

```
[2025-10-11 10:30:15] ✓ 資料已儲存
  裝置: pico_001
  感測器: temperature
  數值: 25.5 celsius
  文件 ID: 6529a1b2c3d4e5f6g7h8i9j0
  總計: 1 筆
------------------------------------------------------------
```

## 📊 系統架構

```
┌─────────────┐
│ Pico Sensor │
└──────┬──────┘
       │ MQTT Publish
       ▼
┌─────────────┐
│ MQTT Broker │
└──────┬──────┘
       │ Subscribe
       ▼
┌─────────────────────┐
│ mqtt_to_db.py       │
│ - 接收 MQTT 訊息    │
│ - 驗證資料格式      │
│ - 儲存到 MongoDB    │
└──────┬──────────────┘
       │
       ▼
┌─────────────┐
│  MongoDB    │
│  (Docker)   │
└─────────────┘
```

## 🔍 程式碼重點說明

### 資料庫管理類別

```python
class DatabaseManager:
    def __init__(self, uri, db_name, collection_name):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]
    
    def insert_data(self, data):
        data['stored_at'] = datetime.now()
        result = self.collection.insert_one(data)
        return str(result.inserted_id)
```

### 資料驗證

```python
def validate_sensor_data(data):
    # 檢查必要欄位
    required_fields = ['device_id', 'sensor_type', 'value']
    for field in required_fields:
        if field not in data:
            return False, f"缺少必要欄位: {field}"
    
    # 檢查數值類型
    if not isinstance(data['value'], (int, float)):
        return False, "value 必須是數字"
    
    # 檢查溫度範圍
    if data['sensor_type'] == 'temperature':
        if data['value'] < -50 or data['value'] > 100:
            return False, f"溫度值超出合理範圍"
    
    return True, "驗證通過"
```

### MQTT 訊息處理

```python
def on_message(client, userdata, msg):
    # 解析 JSON
    data = json.loads(msg.payload.decode('utf-8'))
    
    # 驗證資料
    is_valid, message = validate_sensor_data(data)
    if not is_valid:
        print(f"驗證失敗: {message}")
        return
    
    # 儲存到資料庫
    doc_id = db_manager.insert_data(data)
```

## 💾 資料庫結構

### Collection: sensor_readings

每筆記錄包含以下欄位：

```json
{
  "_id": "6529a1b2c3d4e5f6g7h8i9j0",
  "device_id": "pico_001",
  "device_type": "pico_w",
  "sensor_type": "temperature",
  "value": 25.5,
  "unit": "celsius",
  "timestamp": 1696147815,
  "mqtt_topic": "sensors/pico_001/temperature",
  "stored_at": "2025-10-11T10:30:15.123456"
}
```

### 查詢資料

使用 MongoDB Shell 或 Python 查詢：

```bash
# 進入 MongoDB Shell
docker exec -it mongodb mongosh

# 切換到資料庫
use iot_data

# 查詢所有資料
db.sensor_readings.find()

# 查詢特定裝置
db.sensor_readings.find({"device_id": "pico_001"})

# 查詢最新 10 筆
db.sensor_readings.find().sort({"stored_at": -1}).limit(10)

# 統計資料筆數
db.sensor_readings.countDocuments()
```

## 🐛 常見問題排除

### 問題 1：無法連接 MongoDB

**症狀：** `MongoDB 連接失敗`

**解決方法：**
```bash
# 檢查 Docker 容器狀態
docker ps

# 如果沒有運行，啟動它
cd 02_pi_basics
docker-compose up -d

# 檢查 MongoDB 日誌
docker logs mongodb
```

### 問題 2：資料驗證失敗

**症狀：** `資料驗證失敗: 缺少必要欄位`

**解決方法：**
1. 檢查 Pico 發送的資料格式
2. 確認包含所有必要欄位：`device_id`, `sensor_type`, `value`
3. 使用 `mosquitto_sub` 查看原始資料：
   ```bash
   mosquitto_sub -h localhost -t "sensors/#" -v
   ```

### 問題 3：資料未儲存

**症狀：** 收到訊息但沒有儲存到資料庫

**解決方法：**
1. 檢查程式輸出的錯誤訊息
2. 驗證 MongoDB 連接
3. 檢查資料格式是否正確

## 📝 練習題

### 練習 1：查詢統計資訊

在 `DatabaseManager` 類別中加入方法，計算：
- 每個裝置的資料筆數
- 平均溫度
- 最高/最低溫度

```python
def get_device_stats(self, device_id):
    pipeline = [
        {"$match": {"device_id": device_id}},
        {"$group": {
            "_id": "$device_id",
            "count": {"$sum": 1},
            "avg_value": {"$avg": "$value"},
            "max_value": {"$max": "$value"},
            "min_value": {"$min": "$value"}
        }}
    ]
    return list(self.collection.aggregate(pipeline))
```

### 練習 2：資料清理

實作一個功能，刪除超過 7 天的舊資料：

```python
def cleanup_old_data(self, days=7):
    cutoff_date = datetime.now() - timedelta(days=days)
    result = self.collection.delete_many({
        "stored_at": {"$lt": cutoff_date}
    })
    return result.deleted_count
```

### 練習 3：異常偵測

加入異常值偵測，當溫度變化過大時發出警告：

```python
def check_anomaly(self, device_id, current_value):
    # 取得最近 10 筆資料
    recent_data = self.collection.find(
        {"device_id": device_id}
    ).sort("stored_at", -1).limit(10)
    
    # 計算平均值和標準差
    # 如果當前值偏離過大，回傳 True
```

### 練習 4：批次插入

修改程式支援批次插入，提升效能：

```python
def insert_batch(self, data_list):
    if data_list:
        result = self.collection.insert_many(data_list)
        return len(result.inserted_ids)
    return 0
```

## 🎯 檢核清單

完成以下項目後，你就掌握了資料收集系統：

- [ ] MongoDB 成功啟動並運行
- [ ] 資料收集程式成功連接 MQTT 和 MongoDB
- [ ] 能夠接收並儲存感測器資料
- [ ] 資料驗證功能正常運作
- [ ] 能夠查詢和分析儲存的資料
- [ ] 理解錯誤處理機制
- [ ] 能夠監控系統統計資訊

## 📚 延伸學習

- 實作資料備份機制
- 加入資料壓縮功能
- 探索 MongoDB 索引優化
- 實作即時資料分析
- 加入資料視覺化功能

## 🔗 相關資源

- [MongoDB 官方文件](https://docs.mongodb.com/)
- [PyMongo 教學](https://pymongo.readthedocs.io/)
- [MQTT 協定說明](../../03_mqtt_communication/README.md)


---

## 🌐 查詢 API 端點

資料收集系統包含 FastAPI 服務，提供 RESTful API 查詢儲存的資料。

### 啟動 API 服務

```bash
python3 api_server.py
```

服務啟動後，可以透過以下網址存取：
- API 文件（Swagger UI）: http://localhost:8000/docs
- API 根端點: http://localhost:8000/

### API 端點說明

#### 1. 健康檢查
```
GET /health
```

回應範例：
```json
{
  "status": "healthy",
  "database": "connected",
  "timestamp": "2025-10-11T10:30:15.123456"
}
```

#### 2. 取得所有資料（分頁）
```
GET /api/data?limit=100&skip=0
```

參數：
- `limit`: 最多回傳筆數（1-1000，預設 100）
- `skip`: 跳過筆數，用於分頁（預設 0）

#### 3. 取得特定裝置資料
```
GET /api/data/{device_id}?limit=100
```

範例：
```bash
curl http://localhost:8000/api/data/pico_001?limit=10
```

#### 4. 依時間範圍查詢
```
GET /api/data/range?device_id=pico_001&hours=24&limit=1000
```

參數：
- `device_id`: 裝置 ID（選填）
- `hours`: 最近 N 小時（1-168）
- `start_time`: 開始時間（ISO 格式，選填）
- `end_time`: 結束時間（ISO 格式，選填）
- `limit`: 最多回傳筆數

範例：
```bash
# 查詢最近 24 小時的資料
curl "http://localhost:8000/api/data/range?hours=24"

# 查詢特定時間範圍
curl "http://localhost:8000/api/data/range?start_time=2025-10-11T00:00:00&end_time=2025-10-11T23:59:59"
```

#### 5. 取得裝置統計資訊
```
GET /api/stats/{device_id}
```

回應範例：
```json
{
  "status": "success",
  "device_id": "pico_001",
  "total_records": 1234,
  "avg_value": 25.5,
  "max_value": 32.1,
  "min_value": 18.3,
  "first_reading": "2025-10-01T10:00:00",
  "last_reading": "2025-10-11T10:30:00"
}
```

#### 6. 取得所有裝置列表
```
GET /api/devices
```

回應範例：
```json
{
  "status": "success",
  "count": 3,
  "devices": [
    {
      "device_id": "pico_001",
      "device_type": "pico_w",
      "sensor_type": "temperature",
      "last_value": 25.5,
      "unit": "celsius",
      "last_seen": "2025-10-11T10:30:00"
    }
  ]
}
```

### 使用測試腳本

提供了自動化測試腳本：

```bash
chmod +x test_api.sh
./test_api.sh
```

### 在 Python 中使用 API

```python
import requests

# 取得所有裝置
response = requests.get("http://localhost:8000/api/devices")
devices = response.json()
print(f"找到 {devices['count']} 個裝置")

# 取得特定裝置的最新資料
response = requests.get("http://localhost:8000/api/data/pico_001?limit=10")
data = response.json()
for reading in data['data']:
    print(f"{reading['device_id']}: {reading['value']} {reading['unit']}")

# 取得統計資訊
response = requests.get("http://localhost:8000/api/stats/pico_001")
stats = response.json()
print(f"平均值: {stats['avg_value']}")
print(f"最大值: {stats['max_value']}")
print(f"最小值: {stats['min_value']}")
```

### 整合運行

完整的資料收集和查詢系統需要同時運行兩個程式：

**終端機 1：資料收集**
```bash
python3 mqtt_to_db.py
```

**終端機 2：API 服務**
```bash
python3 api_server.py
```

這樣就建立了完整的資料流程：
```
Pico → MQTT → mqtt_to_db.py → MongoDB ← api_server.py ← 使用者查詢
```
