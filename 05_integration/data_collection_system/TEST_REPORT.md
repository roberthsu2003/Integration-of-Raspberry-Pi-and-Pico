# 端到端測試報告

## 測試目的

驗證完整的 IoT 資料收集系統，從 MQTT 發布到資料庫儲存，再到 API 查詢的整個流程。

## 測試環境

### 必要服務
- MongoDB (Docker)
- Mosquitto MQTT Broker
- FastAPI 服務 (api_server.py)
- MQTT 資料收集器 (mqtt_to_db.py)

### 測試工具
- Python 3.7+
- paho-mqtt
- pymongo
- requests

## 測試項目

### 1. 基礎連接測試

| 測試項目 | 測試內容 | 預期結果 |
|---------|---------|---------|
| MQTT Broker 連接 | 連接到 localhost:1883 | 成功連接 |
| MongoDB 連接 | 連接到 MongoDB 並執行 ping | 成功連接 |
| API 健康檢查 | GET /health | 回傳 healthy 狀態 |

### 2. 資料發布測試

| 測試項目 | 測試內容 | 預期結果 |
|---------|---------|---------|
| 發布測試資料 | 透過 MQTT 發布感測器資料 | 成功發布 |
| 資料儲存驗證 | 檢查資料是否儲存到 MongoDB | 找到對應文件 |

### 3. API 查詢測試

| 測試項目 | 測試內容 | 預期結果 |
|---------|---------|---------|
| 查詢所有資料 | GET /api/data | 回傳資料列表 |
| 查詢特定裝置 | GET /api/data/{device_id} | 回傳該裝置資料 |
| 時間範圍查詢 | GET /api/data/range?hours=1 | 回傳時間範圍內資料 |
| 統計資訊 | GET /api/stats/{device_id} | 回傳統計數據 |
| 裝置列表 | GET /api/devices | 回傳所有裝置 |

### 4. 資料完整性測試

| 測試項目 | 測試內容 | 預期結果 |
|---------|---------|---------|
| 資料一致性 | 比對 API 和資料庫的資料 | 資料完全一致 |

## 執行測試

### 前置準備

1. 啟動 MongoDB：
```bash
cd 02_pi_basics
docker-compose up -d
```

2. 啟動 MQTT Broker：
```bash
sudo systemctl start mosquitto
```

3. 啟動資料收集器（終端機 1）：
```bash
cd 05_integration/data_collection_system
python3 mqtt_to_db.py
```

4. 啟動 API 服務（終端機 2）：
```bash
cd 05_integration/data_collection_system
python3 api_server.py
```

### 執行測試腳本

在新的終端機執行：

```bash
cd 05_integration/data_collection_system
python3 test_e2e.py
```

## 測試結果範例

```
============================================================
端到端測試 - IoT 資料收集系統
============================================================

測試項目：
  1. MQTT Broker 連接
  2. MongoDB 連接
  3. API 健康檢查
  4. 發布測試資料
  5. 驗證資料已儲存
  6. API 查詢所有資料
  7. API 查詢特定裝置
  8. API 時間範圍查詢
  9. API 統計資訊
  10. API 裝置列表
  11. 資料完整性驗證

開始測試...
------------------------------------------------------------
✓ PASS - MQTT Broker 連接
✓ PASS - MongoDB 連接
✓ PASS - API 健康檢查
✓ PASS - 發布測試資料
✓ PASS - 資料儲存到資料庫
      找到文件 ID: 6529a1b2c3d4e5f6g7h8i9j0
✓ PASS - API 查詢所有資料
      取得 10 筆資料
✓ PASS - API 查詢特定裝置
      取得 1 筆資料
✓ PASS - API 時間範圍查詢
      取得 5 筆資料
✓ PASS - API 統計資訊
      總計: 1 筆, 平均: 25.5
✓ PASS - API 裝置列表
      找到 3 個裝置
✓ PASS - 資料完整性驗證
      API 和資料庫資料一致
------------------------------------------------------------

測試結果摘要：
  總測試數: 11
  通過: 11 ✓
  失敗: 0 ✗

清理測試資料: 刪除 1 筆

============================================================
```

## 常見測試失敗原因

### MQTT Broker 連接失敗
- **原因**: Mosquitto 未啟動
- **解決**: `sudo systemctl start mosquitto`

### MongoDB 連接失敗
- **原因**: Docker 容器未運行
- **解決**: `docker-compose up -d`

### API 健康檢查失敗
- **原因**: API 服務未啟動
- **解決**: 執行 `python3 api_server.py`

### 資料儲存驗證失敗
- **原因**: mqtt_to_db.py 未運行
- **解決**: 在另一個終端機執行資料收集器

### 資料完整性驗證失敗
- **原因**: 資料格式不一致或時間延遲
- **解決**: 檢查資料格式，增加等待時間

## 測試資料清理

測試腳本會自動清理測試資料（device_id: test_pico_e2e）。

如需手動清理：

```bash
# 進入 MongoDB Shell
docker exec -it mongodb mongosh

# 刪除測試資料
use iot_data
db.sensor_readings.deleteMany({"device_id": "test_pico_e2e"})
```

## 效能測試

### 測試場景 1：高頻率資料發布

測試 Pico 每秒發布一次資料，持續 1 小時：
- 預期：3600 筆資料
- 驗證：資料完整性、無遺失

### 測試場景 2：多裝置同時發布

測試 10 個裝置同時發布資料：
- 預期：所有資料正確儲存
- 驗證：裝置識別正確、無資料混淆

### 測試場景 3：大量資料查詢

測試查詢 10000 筆資料的效能：
- 預期：回應時間 < 1 秒
- 驗證：分頁功能正常

## 持續整合建議

將測試腳本整合到 CI/CD 流程：

```yaml
# .github/workflows/test.yml
name: E2E Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Start services
        run: |
          docker-compose up -d
          sudo systemctl start mosquitto
      - name: Run tests
        run: python3 test_e2e.py
```

## 結論

端到端測試確保整個系統的各個組件正確整合，能夠：
- 驗證資料流程完整性
- 及早發現整合問題
- 確保系統可靠性
- 提供回歸測試基礎

建議在每次程式碼變更後執行完整測試。
