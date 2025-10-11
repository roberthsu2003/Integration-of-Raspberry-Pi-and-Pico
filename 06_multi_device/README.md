# 多裝置管理模組

管理多個 Pico 裝置，實現並發資料收集和監控。

## 核心概念

### 裝置識別
每個 Pico 使用唯一的 device_id：
- pico_001, pico_002, pico_003...
- 透過 MQTT 主題區分：`sensors/{device_id}/temperature`

### 並發處理
Pi 同時接收多個 Pico 的資料：
- 使用 MQTT 訂閱 `sensors/#`
- 資料庫自動處理並發寫入

## 快速開始

### 1. 設定多個 Pico

在每個 Pico 的 `wifi_config.py` 中設定不同的 device_id：
```python
DEVICE_ID = "pico_001"  # 第一個 Pico
DEVICE_ID = "pico_002"  # 第二個 Pico
DEVICE_ID = "pico_003"  # 第三個 Pico
```

### 2. 啟動所有 Pico

在每個 Pico 上執行 `sensor_publisher.py`

### 3. 監控所有裝置

```bash
# 監控所有裝置
python 03_mqtt_communication/mqtt_test_tools/mqtt_monitor.py --topics "sensors/#"

# 查詢所有裝置資料
curl http://localhost:8000/api/devices
```

## 裝置管理功能

### 查詢裝置列表
```bash
curl http://localhost:8000/api/devices
```

### 查詢特定裝置
```bash
curl http://localhost:8000/api/devices/pico_001
```

### 查詢裝置資料
```bash
curl http://localhost:8000/api/data/pico_001?limit=10
```

## 檢核清單

- [ ] 每個 Pico 有唯一的 device_id
- [ ] 所有 Pico 成功連接 WiFi
- [ ] 所有 Pico 正常發布資料
- [ ] Pi 正確接收所有裝置資料
- [ ] 資料庫正確儲存並區分裝置
- [ ] 可以查詢各裝置的資料

完成後繼續：[範例專案](../07_example_projects/README.md)
