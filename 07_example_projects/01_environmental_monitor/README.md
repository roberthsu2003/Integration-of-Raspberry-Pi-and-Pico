# 環境監測系統

## 專案簡介

這是一個完整的環境監測系統，使用 Pico 收集溫度資料，透過 MQTT 傳送到 Pi，儲存到 MongoDB，並提供 API 查詢歷史資料和統計分析。

## 功能特色

- ✅ 即時溫度監測
- ✅ 歷史資料記錄
- ✅ 溫度趨勢分析
- ✅ 異常值檢測
- ✅ RESTful API 查詢

## 系統架構

```
Pico (溫度感測器) 
    ↓ MQTT
MQTT Broker
    ↓ Subscribe
環境監測服務
    ↓ 儲存
MongoDB
    ↓ 查詢
API 服務
```

## 檔案說明

- `pico_sensor.py` - Pico 端溫度感測器程式
- `monitor_service.py` - Pi 端監測服務
- `api_server.py` - API 查詢服務
- `requirements.txt` - Python 套件需求
- `config.py` - 配置檔案

## 快速開始

### 1. 安裝依賴

```bash
cd 07_example_projects/01_environmental_monitor
pip3 install -r requirements.txt
```

### 2. 啟動 MongoDB

```bash
cd ../../02_pi_basics
docker-compose up -d
```

### 3. 啟動 MQTT Broker

```bash
sudo systemctl start mosquitto
```

### 4. 啟動監測服務

```bash
python3 monitor_service.py
```

### 5. 啟動 API 服務（新終端機）

```bash
python3 api_server.py
```

### 6. 上傳 Pico 程式

1. 修改 `pico_sensor.py` 中的 WiFi 和 MQTT 設定
2. 使用 Thonny 上傳到 Pico
3. 執行程式

## API 使用

### 查詢最新資料

```bash
curl http://localhost:8000/api/latest
```

### 查詢歷史資料

```bash
# 查詢最近 24 小時
curl http://localhost:8000/api/history?hours=24

# 查詢特定時間範圍
curl "http://localhost:8000/api/history?start=2025-10-11T00:00:00&end=2025-10-11T23:59:59"
```

### 查詢統計資訊

```bash
curl http://localhost:8000/api/stats?hours=24
```

回應範例：
```json
{
  "period": "24 hours",
  "count": 288,
  "average": 25.3,
  "min": 23.1,
  "max": 27.8,
  "std_dev": 1.2
}
```

### 查詢溫度趨勢

```bash
curl http://localhost:8000/api/trend?hours=24
```

## 功能說明

### 1. 即時監測

Pico 每 5 分鐘讀取一次溫度並發送到 MQTT Broker。

### 2. 資料儲存

監測服務訂閱 MQTT 主題，接收資料後驗證並儲存到 MongoDB。

### 3. 異常檢測

系統會檢測以下異常：
- 溫度超出正常範圍（15-35°C）
- 溫度變化過快（>5°C/小時）
- 感測器無回應（>15 分鐘）

### 4. 趨勢分析

API 提供溫度趨勢分析：
- 上升趨勢
- 下降趨勢
- 穩定
- 波動

## 資料格式

### MQTT 訊息格式

```json
{
  "device_id": "pico_env_001",
  "sensor_type": "temperature",
  "value": 25.3,
  "unit": "celsius",
  "timestamp": "2025-10-11T10:30:00Z",
  "location": "classroom_a"
}
```

### MongoDB 文件格式

```json
{
  "_id": "ObjectId(...)",
  "device_id": "pico_env_001",
  "sensor_type": "temperature",
  "value": 25.3,
  "unit": "celsius",
  "timestamp": "2025-10-11T10:30:00Z",
  "location": "classroom_a",
  "created_at": "2025-10-11T10:30:05Z"
}
```

## 客製化

### 修改監測間隔

編輯 `pico_sensor.py`：

```python
PUBLISH_INTERVAL = 300  # 改為你想要的秒數
```

### 修改異常閾值

編輯 `config.py`：

```python
TEMP_MIN = 15  # 最低溫度
TEMP_MAX = 35  # 最高溫度
TEMP_CHANGE_THRESHOLD = 5  # 溫度變化閾值
```

### 加入其他感測器

1. 在 Pico 端加入感測器讀取
2. 修改 MQTT 訊息格式
3. 更新監測服務的資料處理邏輯

## 故障排除

### Pico 無法連接 WiFi

1. 檢查 WiFi SSID 和密碼
2. 確認 WiFi 訊號強度
3. 檢查 Pico 是否支援該 WiFi 頻段（2.4GHz）

### MQTT 連接失敗

```bash
# 檢查 Mosquitto 狀態
sudo systemctl status mosquitto

# 測試 MQTT 連接
mosquitto_sub -h localhost -t "sensors/#" -v
```

### 資料未儲存

1. 檢查 MongoDB 是否運行
2. 檢查監測服務日誌
3. 驗證 MQTT 訊息格式

### API 查詢無資料

1. 確認資料已儲存到資料庫
2. 檢查時間範圍參數
3. 驗證 device_id

## 練習題

### 基礎練習

1. 修改監測間隔為 1 分鐘
2. 查詢最近 1 小時的資料
3. 計算平均溫度

### 進階練習

1. 加入濕度感測器（模擬）
2. 實作溫度警報功能
3. 建立每日溫度報告

### 挑戰題

1. 實作多地點監測（多個 Pico）
2. 加入資料視覺化圖表
3. 實作預測性維護（溫度異常預警）

## 延伸應用

- 🌡️ 多房間溫度監控
- 📊 溫度資料匯出和分析
- 🔔 溫度異常即時通知
- 📱 手機 App 整合
- 🤖 自動化空調控制

## 檢核清單

- [ ] Pico 成功連接 WiFi
- [ ] MQTT 訊息正常發送
- [ ] 監測服務正常接收資料
- [ ] 資料成功儲存到 MongoDB
- [ ] API 可以查詢歷史資料
- [ ] 統計功能正常運作
- [ ] 異常檢測功能正常

## 參考資源

- [MicroPython 溫度感測器文件](https://docs.micropython.org/en/latest/library/machine.ADC.html)
- [MQTT 協定說明](../03_mqtt_communication/README.md)
- [FastAPI 文件](https://fastapi.tiangolo.com/)
- [MongoDB 查詢語法](https://docs.mongodb.com/manual/tutorial/query-documents/)
