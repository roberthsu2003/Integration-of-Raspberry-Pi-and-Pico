# 警報系統

## 專案簡介

這是一個智慧警報系統，可以監控感測器資料並在超過設定閾值時自動發出警報。支援多種警報條件和通知方式，適合用於環境監控、安全監控等場景。

## 功能特色

- ✅ 多種警報條件（閾值、變化率、異常值）
- ✅ 可配置的警報規則
- ✅ 警報歷史記錄
- ✅ 多種通知方式（終端、日誌、MQTT）
- ✅ 警報統計分析

## 系統架構

```
Pico 感測器
    ↓ MQTT
警報監控服務
    ├─ 規則引擎
    ├─ 警報觸發
    └─ 通知發送
        ↓
MongoDB (警報記錄)
```

## 檔案說明

- `alert_service.py` - 警報監控服務
- `alert_rules.py` - 警報規則定義
- `alert_config.json` - 警報配置檔案
- `alert_history.py` - 警報歷史查詢工具
- `requirements.txt` - Python 套件需求

## 快速開始

### 1. 安裝依賴

```bash
cd 07_example_projects/03_alert_system
pip3 install -r requirements.txt
```

### 2. 配置警報規則

編輯 `alert_config.json`：

```json
{
  "rules": [
    {
      "name": "high_temperature",
      "condition": "value > 30",
      "sensor_type": "temperature",
      "severity": "warning",
      "message": "溫度過高"
    }
  ]
}
```

### 3. 啟動警報服務

```bash
python3 alert_service.py
```

### 4. 查詢警報歷史

```bash
# 查詢所有警報
python3 alert_history.py --list

# 查詢特定裝置的警報
python3 alert_history.py --device pico_001

# 查詢最近 24 小時的警報
python3 alert_history.py --hours 24
```

## 警報規則

### 規則類型

#### 1. 閾值警報

溫度、濕度等數值超過設定範圍：

```json
{
  "name": "high_temperature",
  "condition": "value > 30",
  "sensor_type": "temperature",
  "severity": "warning"
}
```

#### 2. 變化率警報

數值變化過快：

```json
{
  "name": "rapid_change",
  "condition": "change_rate > 5",
  "sensor_type": "temperature",
  "severity": "critical"
}
```

#### 3. 範圍警報

數值超出正常範圍：

```json
{
  "name": "out_of_range",
  "condition": "value < 15 or value > 35",
  "sensor_type": "temperature",
  "severity": "warning"
}
```

#### 4. 無回應警報

感測器長時間無資料：

```json
{
  "name": "sensor_timeout",
  "condition": "no_data_for > 600",
  "severity": "critical"
}
```

### 嚴重程度

- `info` - 資訊性警報
- `warning` - 警告
- `critical` - 嚴重警報

## 通知方式

### 1. 終端輸出

直接在終端顯示警報訊息（預設啟用）

### 2. 日誌記錄

寫入日誌檔案 `alerts.log`

### 3. MQTT 發布

發布警報到 MQTT 主題 `alerts/{device_id}`

```json
{
  "alert_id": "alert_20251011_120000",
  "device_id": "pico_001",
  "rule_name": "high_temperature",
  "severity": "warning",
  "message": "溫度過高: 32.5°C",
  "timestamp": "2025-10-11T12:00:00",
  "value": 32.5
}
```

### 4. 電子郵件（選配）

發送警報郵件到指定信箱

## 使用範例

### 基本監控

```bash
# 啟動服務，使用預設配置
python3 alert_service.py
```

### 自訂配置

```bash
# 使用自訂配置檔案
python3 alert_service.py --config my_config.json
```

### 測試警報

```bash
# 發送測試資料觸發警報
mosquitto_pub -h localhost -t "sensors/test/temperature" \
  -m '{"device_id":"test","sensor_type":"temperature","value":35,"timestamp":"2025-10-11T12:00:00"}'
```

## 警報配置範例

### 完整配置檔案

```json
{
  "mqtt": {
    "broker": "localhost",
    "port": 1883,
    "topic": "sensors/#"
  },
  "database": {
    "uri": "mongodb://admin:password123@localhost:27017/",
    "db": "iot_data",
    "collection": "alerts"
  },
  "notifications": {
    "terminal": true,
    "log_file": true,
    "mqtt": true,
    "email": false
  },
  "rules": [
    {
      "name": "high_temperature",
      "condition": "value > 30",
      "sensor_type": "temperature",
      "severity": "warning",
      "message": "溫度過高: {value}°C",
      "cooldown": 300
    },
    {
      "name": "low_temperature",
      "condition": "value < 15",
      "sensor_type": "temperature",
      "severity": "warning",
      "message": "溫度過低: {value}°C",
      "cooldown": 300
    },
    {
      "name": "critical_temperature",
      "condition": "value > 35",
      "sensor_type": "temperature",
      "severity": "critical",
      "message": "溫度嚴重過高: {value}°C",
      "cooldown": 60
    }
  ]
}
```

### 規則說明

- `name` - 規則名稱（唯一識別）
- `condition` - 觸發條件（Python 表達式）
- `sensor_type` - 感測器類型（選填）
- `severity` - 嚴重程度
- `message` - 警報訊息（支援變數替換）
- `cooldown` - 冷卻時間（秒），避免重複警報

## 警報統計

查詢警報統計資訊：

```bash
python3 alert_history.py --stats
```

輸出範例：

```
警報統計 (最近 24 小時)
========================
總警報數: 15
  - warning: 12
  - critical: 3

最常觸發的規則:
  1. high_temperature: 8 次
  2. rapid_change: 4 次
  3. critical_temperature: 3 次

受影響的裝置:
  - pico_001: 10 次
  - pico_002: 5 次
```

## 故障排除

### 警報未觸發

1. 檢查規則配置是否正確
2. 驗證感測器資料格式
3. 查看服務日誌

### 重複警報

調整 `cooldown` 時間：

```json
{
  "name": "high_temperature",
  "cooldown": 600
}
```

### 誤報過多

調整閾值或加入條件：

```json
{
  "name": "high_temperature",
  "condition": "value > 30 and value < 50"
}
```

## 練習題

### 基礎練習

1. 建立溫度過高警報規則
2. 測試警報觸發
3. 查詢警報歷史

### 進階練習

1. 建立多個警報規則
2. 實作警報冷卻機制
3. 加入警報統計功能

### 挑戰題

1. 實作電子郵件通知
2. 建立警報儀表板
3. 實作智慧警報（機器學習異常檢測）

## 檢核清單

- [ ] 警報服務正常運作
- [ ] 可以觸發警報
- [ ] 警報記錄到資料庫
- [ ] 可以查詢警報歷史
- [ ] 通知功能正常
- [ ] 冷卻機制正常
- [ ] 統計功能正常

## 參考資源

- [警報系統設計模式](https://en.wikipedia.org/wiki/Alarm_management)
- [Python 表達式求值](https://docs.python.org/3/library/functions.html#eval)
- [MQTT 警報最佳實踐](https://www.hivemq.com/blog/mqtt-essentials-part-5-mqtt-topics-best-practices/)
