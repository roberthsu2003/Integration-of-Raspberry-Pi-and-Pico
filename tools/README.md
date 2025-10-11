# 輔助工具說明

本目錄包含課程使用的輔助工具，用於驗證環境設定、測試 MQTT 連接和檢查 API 服務。

## 工具列表

### 1. verify_setup.py - 環境驗證工具

檢查課程所需的所有軟體和服務是否正確安裝。

**功能：**
- 檢查 Python 版本
- 檢查 Docker 和 Docker Compose
- 檢查必要的 Python 套件
- 檢查 Docker 服務（MongoDB、Mosquitto）

**使用方法：**
```bash
python tools/verify_setup.py
```

**輸出範例：**
```
============================================================
 環境驗證工具
============================================================

============================================================
 Python 環境
============================================================
✓ Python 3.11.0

============================================================
 系統工具
============================================================
✓ Docker: Docker version 24.0.0
✓ Docker Compose: Docker Compose version v2.20.0
✓ Git: git version 2.40.0

============================================================
 Python 套件
============================================================
✓ fastapi
✓ uvicorn
✓ pymongo
✓ paho-mqtt
✓ pyserial

============================================================
 驗證結果
============================================================

通過: 5/5

🎉 所有檢查通過！環境設定完成。
```

---

### 2. test_mqtt.py - MQTT 測試工具

測試 MQTT Broker 的連接、發布和訂閱功能。

**功能：**
- 測試 Broker 連接
- 測試訊息發布
- 測試訊息訂閱
- 測試完整的發布訂閱流程

**使用方法：**

#### 測試連接
```bash
python tools/test_mqtt.py --broker localhost connection
```

#### 測試發布
```bash
python tools/test_mqtt.py --broker localhost publish \
  --topic test/topic \
  --message "Hello MQTT"
```

#### 測試訂閱（監聽 10 秒）
```bash
python tools/test_mqtt.py --broker localhost subscribe \
  --topic test/# \
  --duration 10
```

#### 完整測試（發布並驗證接收）
```bash
python tools/test_mqtt.py --broker localhost pubsub \
  --topic test/demo \
  --message "Test message"
```

**參數說明：**
- `--broker`: MQTT Broker 位址（預設: localhost）
- `--port`: MQTT Broker 連接埠（預設: 1883）
- `--timeout`: 連接逾時時間（秒，預設: 10）
- `--topic`: 主題名稱
- `--message`: 訊息內容
- `--qos`: QoS 等級（0, 1, 2，預設: 0）
- `--duration`: 監聽時間（秒）

**輸出範例：**
```
============================================================
 測試發布訂閱流程
============================================================
1. 啟動訂閱者...
✓ 訂閱者已就緒

2. 發布測試訊息...
✓ 訊息已發布

3. 等待接收訊息...

📨 收到訊息:
   主題: test/demo
   內容: {"message": "Test message", "timestamp": "2025-10-11T10:30:00", "test": true}
   QoS: 0

============================================================
 測試結果
============================================================
✓ 成功接收 1 則訊息
✓ 發布訂閱流程正常
```

---

### 3. check_api.py - API 檢查工具

驗證 FastAPI 服務的所有端點是否正常運作。

**功能：**
- 測試基本端點（健康檢查、根路徑、文件）
- 測試資料端點（發布、查詢）
- 測試錯誤處理
- 生成測試報告

**使用方法：**

#### 基本測試
```bash
python tools/check_api.py --url http://localhost:8000
```

#### 完整測試
```bash
python tools/check_api.py --url http://localhost:8000 --full
```

#### 只測試資料端點
```bash
python tools/check_api.py --url http://localhost:8000 --data
```

#### 測試並儲存報告
```bash
python tools/check_api.py --url http://localhost:8000 --full --save
```

**參數說明：**
- `--url`: API 基礎 URL（預設: http://localhost:8000）
- `--timeout`: 請求逾時時間（秒，預設: 10）
- `--basic`: 只測試基本端點
- `--data`: 只測試資料端點
- `--error`: 只測試錯誤處理
- `--full`: 執行完整測試
- `--save`: 儲存測試報告到 JSON 檔案

**輸出範例：**
```
============================================================
 API 檢查工具
============================================================
目標 URL: http://localhost:8000
逾時時間: 10秒

============================================================
 測試基本端點
============================================================

✓ GET /api/health
   描述: 健康檢查端點
   狀態碼: 200
   回應時間: 0.015秒
   回應: {
  "status": "healthy",
  "timestamp": "2025-10-11T10:30:00"
}

============================================================
 測試資料端點
============================================================

✓ POST /api/data
   描述: 發布感測器資料
   狀態碼: 200
   回應時間: 0.023秒

✓ GET /api/data
   描述: 查詢所有資料
   狀態碼: 200
   回應時間: 0.018秒

============================================================
 測試報告
============================================================

總測試數: 5
通過: 5
失敗: 0
成功率: 100.0%

平均回應時間: 0.019秒

✓ 所有測試通過
```

---

## 常見使用場景

### 場景 1：課程開始前檢查環境
```bash
# 1. 驗證環境設定
python tools/verify_setup.py

# 2. 測試 MQTT Broker
python tools/test_mqtt.py --broker localhost connection

# 3. 測試 API 服務
python tools/check_api.py --url http://localhost:8000 --basic
```

### 場景 2：除錯 MQTT 通訊問題
```bash
# 1. 測試 Broker 連接
python tools/test_mqtt.py --broker localhost connection

# 2. 監聽所有訊息
python tools/test_mqtt.py --broker localhost subscribe --topic "#" --duration 30

# 3. 發布測試訊息
python tools/test_mqtt.py --broker localhost publish --topic test/debug --message "Debug message"
```

### 場景 3：驗證整合系統
```bash
# 1. 檢查 API 服務
python tools/check_api.py --url http://localhost:8000 --full

# 2. 測試 MQTT 發布訂閱
python tools/test_mqtt.py --broker localhost pubsub --topic sensors/test

# 3. 驗證資料流程（手動）
# - 使用 Pico 發布資料
# - 使用 test_mqtt.py 監聽
# - 使用 check_api.py 查詢資料庫
```

### 場景 4：學生自我檢測
```bash
# 完整檢測腳本
python tools/verify_setup.py && \
python tools/test_mqtt.py --broker localhost connection && \
python tools/check_api.py --url http://localhost:8000 --basic
```

---

## 故障排除

### 工具無法執行

**問題：** `ModuleNotFoundError: No module named 'paho'`

**解決方法：**
```bash
pip install paho-mqtt requests
```

### MQTT 連接失敗

**問題：** `✗ 連接失敗: [Errno 111] Connection refused`

**解決方法：**
1. 確認 Mosquitto 正在運行：
   ```bash
   docker ps | grep mosquitto
   ```
2. 如果沒有運行，啟動它：
   ```bash
   cd 03_mqtt_communication/mqtt_broker
   docker-compose up -d
   ```

### API 連接失敗

**問題：** `✗ 無法連接到 http://localhost:8000`

**解決方法：**
1. 確認 FastAPI 服務正在運行
2. 檢查連接埠是否正確
3. 嘗試訪問：http://localhost:8000/docs

---

## 進階使用

### 自訂測試腳本

你可以匯入這些工具的類別來建立自訂測試：

```python
from tools.test_mqtt import MQTTTester
from tools.check_api import APIChecker

# MQTT 測試
mqtt = MQTTTester("localhost")
mqtt.test_connection()
mqtt.test_publish("test/topic", "Hello")

# API 測試
api = APIChecker("http://localhost:8000")
api.test_basic_endpoints()
api.generate_report()
```

### 持續整合

在 CI/CD 流程中使用這些工具：

```yaml
# .github/workflows/test.yml
- name: Verify Setup
  run: python tools/verify_setup.py

- name: Test MQTT
  run: python tools/test_mqtt.py --broker localhost connection

- name: Test API
  run: python tools/check_api.py --url http://localhost:8000 --full
```

---

## 相關資源

- [故障排除指南](../resources/troubleshooting.md)
- [MQTT 速查表](../resources/cheatsheets/mqtt_cheatsheet.md)
- [FastAPI 速查表](../resources/cheatsheets/fastapi_cheatsheet.md)

---

## 回饋與改進

如果你發現工具有任何問題或有改進建議，請：
1. 查看 [CONTRIBUTING.md](../CONTRIBUTING.md)
2. 提交 Issue 或 Pull Request
3. 聯絡課程講師

---

**提示：** 建議在每次課程開始前執行 `verify_setup.py`，確保環境正常運作。
