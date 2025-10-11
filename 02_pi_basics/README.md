# Pi 基礎模組

歡迎來到 Raspberry Pi 基礎模組！本模組將教你如何使用 Raspberry Pi 建立 API 服務和資料庫系統。

## 模組概覽

本模組學習如何：
- 使用 Docker 部署 MongoDB 資料庫
- 建立 FastAPI RESTful API 服務
- 實作資料庫 CRUD 操作
- 測試和除錯 API

## 學習目標

完成本模組後，你將能夠：

- ✅ 使用 Docker Compose 部署 MongoDB
- ✅ 理解 NoSQL 資料庫概念
- ✅ 建立 FastAPI 應用程式
- ✅ 設計 RESTful API 端點
- ✅ 實作資料驗證和錯誤處理
- ✅ 使用 MongoDB 進行 CRUD 操作
- ✅ 測試 API 功能

## 專案結構

```
02_pi_basics/
├── docker-compose.yml          # Docker Compose 配置
├── init-mongo.js              # MongoDB 初始化腳本
├── .env.example               # 環境變數範例
├── test_api.py                # API 測試腳本
├── fastapi_app/               # FastAPI 應用程式
│   ├── main.py               # 主程式和 API 端點
│   ├── models.py             # 資料模型
│   ├── database.py           # 資料庫操作
│   └── requirements.txt      # Python 套件依賴
└── README.md                  # 本檔案
```

## 快速開始

### 1. 安裝 Docker

如果還沒安裝 Docker，請參考 [SETUP.md](../SETUP.md)。

驗證安裝：
```bash
docker --version
docker-compose --version
```

### 2. 啟動 MongoDB

```bash
# 進入專案目錄
cd 02_pi_basics

# 啟動 MongoDB 容器
docker-compose up -d

# 檢查容器狀態
docker-compose ps
```

預期輸出：
```
NAME                IMAGE               STATUS
iot_mongodb         mongo:latest        Up
iot_mongo_express   mongo-express       Up
```

### 3. 安裝 Python 套件

```bash
# 建立虛擬環境（建議）
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows

# 安裝套件
cd fastapi_app
pip install -r requirements.txt
```

### 4. 啟動 FastAPI 應用程式

```bash
# 在 fastapi_app 目錄中
python main.py
```

或使用 uvicorn：
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 5. 測試 API

開啟瀏覽器訪問：
- API 文件：http://localhost:8000/docs
- 健康檢查：http://localhost:8000/api/health

或執行測試腳本：
```bash
# 在 02_pi_basics 目錄中
python test_api.py
```

## Docker Compose 說明

### docker-compose.yml

這個檔案定義了兩個服務：

**1. MongoDB 資料庫**
```yaml
mongodb:
  image: mongo:latest
  ports:
    - "27017:27017"
  environment:
    MONGO_INITDB_ROOT_USERNAME: admin
    MONGO_INITDB_ROOT_PASSWORD: password123
  volumes:
    - ./mongodb_data:/data/db
```

**2. Mongo Express（網頁管理介面）**
```yaml
mongo-express:
  image: mongo-express:latest
  ports:
    - "8081:8081"
  depends_on:
    - mongodb
```

### 常用 Docker Compose 指令

```bash
# 啟動服務（背景執行）
docker-compose up -d

# 查看服務狀態
docker-compose ps

# 查看日誌
docker-compose logs
docker-compose logs mongodb  # 只看 MongoDB 日誌

# 停止服務
docker-compose stop

# 停止並移除容器
docker-compose down

# 停止並移除容器和資料卷
docker-compose down -v
```

## MongoDB 基礎

### 連接 MongoDB

**使用 mongosh（MongoDB Shell）：**
```bash
docker exec -it iot_mongodb mongosh -u admin -p password123
```

**使用 Mongo Express（網頁介面）：**
- 訪問：http://localhost:8081
- 帳號：admin
- 密碼：admin123

### 基本操作

```javascript
// 切換到 iot_data 資料庫
use iot_data

// 查看所有集合
show collections

// 查詢資料
db.sensor_data.find().limit(5)

// 插入資料
db.sensor_data.insertOne({
  device_id: "pico_001",
  sensor_type: "temperature",
  value: 25.5,
  unit: "celsius",
  timestamp: new Date()
})

// 查詢特定裝置
db.sensor_data.find({device_id: "pico_001"})

// 計數
db.sensor_data.countDocuments()

// 刪除資料
db.sensor_data.deleteMany({device_id: "pico_test"})
```

## FastAPI 應用程式

### 專案結構

**main.py** - 主應用程式
- 定義 API 端點
- 處理 HTTP 請求
- 錯誤處理

**models.py** - 資料模型
- 使用 Pydantic 定義資料結構
- 自動資料驗證
- API 文件生成

**database.py** - 資料庫操作
- MongoDB 連接管理
- CRUD 操作
- 查詢和篩選

### API 端點

#### 健康檢查

```bash
# GET /api/health
curl http://localhost:8000/api/health
```

#### 建立感測器資料

```bash
# POST /api/data
curl -X POST http://localhost:8000/api/data \
  -H "Content-Type: application/json" \
  -d '{
    "device_id": "pico_001",
    "sensor_type": "temperature",
    "value": 25.5,
    "unit": "celsius"
  }'
```

#### 查詢所有資料

```bash
# GET /api/data
curl http://localhost:8000/api/data?limit=10
```

#### 查詢特定裝置

```bash
# GET /api/data/{device_id}
curl http://localhost:8000/api/data/pico_001
```

#### 查詢所有裝置

```bash
# GET /api/devices
curl http://localhost:8000/api/devices
```

### 使用 Python 呼叫 API

```python
import requests

# 建立資料
data = {
    "device_id": "pico_001",
    "sensor_type": "temperature",
    "value": 25.5,
    "unit": "celsius"
}

response = requests.post(
    "http://localhost:8000/api/data",
    json=data
)

print(response.json())

# 查詢資料
response = requests.get("http://localhost:8000/api/data/pico_001")
print(response.json())
```

## 資料模型

### SensorData

```python
{
    "device_id": "pico_001",        # 裝置 ID（必填）
    "device_type": "pico_w",        # 裝置類型
    "timestamp": "2025-01-11T10:30:00",  # 時間戳記
    "sensor_type": "temperature",   # 感測器類型（必填）
    "value": 25.5,                  # 數值（必填）
    "unit": "celsius",              # 單位（必填）
    "location": "classroom_a"       # 位置（選用）
}
```

### Device

```python
{
    "device_id": "pico_001",        # 裝置 ID（必填）
    "device_name": "Sensor 1",      # 裝置名稱（必填）
    "device_type": "pico_w",        # 裝置類型
    "location": "classroom_a",      # 位置
    "status": "active",             # 狀態
    "created_at": "2025-01-11T09:00:00",  # 建立時間
    "last_seen": "2025-01-11T10:30:00"    # 最後上線時間
}
```

## 測試

### 自動化測試

執行測試腳本：
```bash
python test_api.py
```

### 手動測試

**使用 curl：**
```bash
# 健康檢查
curl http://localhost:8000/api/health

# 建立資料
curl -X POST http://localhost:8000/api/data \
  -H "Content-Type: application/json" \
  -d '{"device_id":"pico_001","sensor_type":"temperature","value":25.5,"unit":"celsius"}'

# 查詢資料
curl http://localhost:8000/api/data
```

**使用 Swagger UI：**
1. 訪問 http://localhost:8000/docs
2. 點擊端點展開
3. 點擊 "Try it out"
4. 輸入參數
5. 點擊 "Execute"

## 常見問題

### Q: Docker 容器無法啟動？

**檢查項目：**
```bash
# 檢查連接埠是否被佔用
sudo netstat -tulpn | grep 27017
sudo netstat -tulpn | grep 8081

# 查看容器日誌
docker-compose logs mongodb

# 重新啟動
docker-compose down
docker-compose up -d
```

### Q: FastAPI 無法連接 MongoDB？

**解決方法：**
1. 確認 MongoDB 容器正在運行
2. 檢查連接字串是否正確
3. 測試連接：
```python
from pymongo import MongoClient
client = MongoClient('mongodb://admin:password123@localhost:27017/')
client.admin.command('ping')
```

### Q: API 回傳 422 錯誤？

**原因：** 資料驗證失敗

**解決方法：**
- 檢查必填欄位是否都有提供
- 確認資料型別正確
- 查看錯誤訊息中的詳細資訊

### Q: 如何重置資料庫？

```bash
# 停止並移除容器和資料
docker-compose down -v

# 刪除資料目錄
rm -rf mongodb_data

# 重新啟動
docker-compose up -d
```

## 練習題

### 🟢 練習 1：新增 API 端點

新增一個端點取得資料統計：
- 路徑：`GET /api/stats/{device_id}`
- 返回：平均值、最大值、最小值、資料筆數

### 🟡 練習 2：實作分頁

改進查詢端點，加入分頁功能：
- 參數：`page`（頁碼）、`page_size`（每頁筆數）
- 返回：資料、總頁數、當前頁碼

### 🔴 練習 3：時間範圍查詢

實作時間範圍查詢：
- 參數：`start_time`、`end_time`
- 支援不同的時間格式
- 加入時區處理

## 檢核清單

完成本模組前，確認你已經：

- [ ] 成功啟動 MongoDB 容器
- [ ] 能夠使用 mongosh 連接資料庫
- [ ] 執行基本的 MongoDB 操作
- [ ] 啟動 FastAPI 應用程式
- [ ] 訪問 API 文件頁面
- [ ] 測試所有 API 端點
- [ ] 理解資料模型和驗證
- [ ] 能夠除錯常見問題

## 下一步

完成 Pi 基礎模組後，繼續學習：

- **[MQTT 通訊模組](../03_mqtt_communication/README.md)** - 學習裝置間通訊
- **[整合應用模組](../05_integration/README.md)** - 整合 Pi 和 Pico

## 參考資源

- [FastAPI 官方文件](https://fastapi.tiangolo.com/)
- [MongoDB 官方文件](https://docs.mongodb.com/)
- [Docker 官方文件](https://docs.docker.com/)
- [Pydantic 文件](https://docs.pydantic.dev/)

祝學習愉快！🚀
