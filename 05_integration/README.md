# 整合應用模組

本模組展示如何整合所有學過的技術，建立完整的物聯網資料收集系統。

## 完整資料流程

```
Pico 感測器 → MQTT 發布 → MQTT Broker → Pi 訂閱 → 資料驗證 → MongoDB 儲存 → FastAPI 查詢
```

## 快速開始

### 1. 啟動所有服務

```bash
# 啟動 MongoDB
cd 02_pi_basics
docker-compose up -d

# 啟動 MQTT Broker
cd ../03_mqtt_communication/mqtt_broker
docker-compose up -d

# 啟動 FastAPI（選用）
cd ../../02_pi_basics/fastapi_app
python main.py &
```

### 2. 啟動 Pi 訂閱者

```bash
cd 03_mqtt_communication/pi_subscriber
python subscriber.py
```

### 3. 啟動 Pico 發布者

在 Thonny 中執行：
```python
# 03_mqtt_communication/pico_publisher/sensor_publisher.py
```

### 4. 驗證資料流程

```bash
# 查看 MQTT 訊息
cd 03_mqtt_communication/mqtt_test_tools
python mqtt_monitor.py --topics "sensors/#"

# 查看資料庫
docker exec -it iot_mongodb mongosh -u admin -p password123
> use iot_data
> db.sensor_data.find().limit(5)

# 查看 API
curl http://localhost:8000/api/data?limit=5
```

## 故障排除

### 問題：Pico 無法連接 WiFi
- 檢查 SSID 和密碼
- 確認是 2.4GHz WiFi
- 檢查訊號強度

### 問題：MQTT 連接失敗
- 確認 Broker 正在運行：`docker ps | grep mosquitto`
- 檢查 IP 位址是否正確
- 測試連接：`mosquitto_sub -h localhost -t test`

### 問題：資料沒有儲存
- 檢查 MongoDB：`docker ps | grep mongodb`
- 檢查訂閱者日誌
- 驗證資料格式

## 檢核清單

- [ ] 所有服務正常運行
- [ ] Pico 成功連接 WiFi
- [ ] MQTT 訊息正常發布
- [ ] Pi 成功接收訊息
- [ ] 資料正確儲存到資料庫
- [ ] API 可以查詢資料

## 下一步

完成整合後，繼續學習：
- [多裝置管理](../06_multi_device/README.md)
- [範例專案](../07_example_projects/README.md)
