# 範例專案故障排除指南

本文件提供所有範例專案的常見問題和解決方案。

## 通用問題

### MongoDB 連接失敗

**症狀：** `pymongo.errors.ServerSelectionTimeoutError`

**解決方案：**
```bash
# 檢查 MongoDB 是否運行
docker ps

# 如果沒有運行，啟動 MongoDB
cd 02_pi_basics
docker-compose up -d

# 檢查連接
docker exec -it mongodb mongosh -u admin -p password123
```

### MQTT 連接失敗

**症狀：** `Connection refused` 或 `Timeout`

**解決方案：**
```bash
# 檢查 Mosquitto 狀態
sudo systemctl status mosquitto

# 啟動 Mosquitto
sudo systemctl start mosquitto

# 測試連接
mosquitto_sub -h localhost -t "test" -v
```

### Pico WiFi 連接失敗

**症狀：** Pico 無法連接到 WiFi

**解決方案：**
1. 確認 WiFi SSID 和密碼正確
2. 確認 WiFi 是 2.4GHz（Pico W 不支援 5GHz）
3. 檢查 WiFi 訊號強度
4. 重新啟動 Pico

---

## 專案 1：環境監測系統

### 問題 1：資料未儲存到資料庫

**檢查步驟：**
```bash
# 1. 檢查監測服務是否運行
ps aux | grep monitor_service

# 2. 檢查日誌
tail -f data_logger.log

# 3. 手動測試 MQTT
mosquitto_pub -h localhost -t "sensors/environment/temperature" \
  -m '{"device_id":"test","sensor_type":"temperature","value":25,"timestamp":"2025-10-11T12:00:00"}'

# 4. 檢查資料庫
docker exec -it mongodb mongosh -u admin -p password123
use iot_data
db.environmental_data.find().limit(5)
```

### 問題 2：API 查詢無資料

**解決方案：**
1. 確認資料已儲存到資料庫
2. 檢查時間範圍參數
3. 驗證 device_id 是否正確

```bash
# 測試 API
curl http://localhost:8000/api/latest
curl http://localhost:8000/api/history?hours=24
```

### 問題 3：異常檢測未觸發

**檢查配置：**
```python
# 編輯 config.py
TEMP_MIN = 15  # 調整閾值
TEMP_MAX = 35
```

---

## 專案 2：資料記錄器

### 問題 1：匯出檔案過大

**解決方案：**
```bash
# 分批匯出
python3 export_data.py --format csv --days 1 --output day1.csv
python3 export_data.py --format csv --days 2 --output day2.csv

# 或使用壓縮
gzip data.json
```

### 問題 2：備份失敗

**檢查磁碟空間：**
```bash
df -h

# 清理舊備份
cd backups
ls -lh
rm old_backup_*.json
```

### 問題 3：CSV 格式錯誤

**解決方案：**
- 確認資料中沒有特殊字元
- 使用 JSON 格式作為替代
- 檢查欄位名稱是否一致

---

## 專案 3：警報系統

### 問題 1：警報未觸發

**檢查步驟：**
```bash
# 1. 檢查規則配置
cat alert_config.json

# 2. 測試條件
python3 -c "
value = 32
print('Condition result:', value > 30)
"

# 3. 發送測試資料
mosquitto_pub -h localhost -t "sensors/test/temperature" \
  -m '{"device_id":"test","sensor_type":"temperature","value":35,"timestamp":"2025-10-11T12:00:00"}'
```

### 問題 2：重複警報

**調整冷卻時間：**
```json
{
  "name": "high_temperature",
  "cooldown": 600
}
```

### 問題 3：警報歷史查詢失敗

**檢查資料庫：**
```bash
docker exec -it mongodb mongosh -u admin -p password123
use iot_data
db.alerts.find().limit(5)
```

---

## 專案 4：資料視覺化儀表板

### 問題 1：儀表板無法開啟

**解決方案：**
```bash
# 檢查 API 服務是否運行
ps aux | grep dashboard_api

# 重新啟動服務
python3 dashboard_api.py

# 檢查埠號是否被佔用
lsof -i :8000
```

### 問題 2：圖表不顯示

**檢查瀏覽器控制台：**
1. 按 F12 開啟開發者工具
2. 查看 Console 標籤的錯誤訊息
3. 檢查 Network 標籤的 API 請求

**常見原因：**
- API 回傳資料格式錯誤
- Chart.js 載入失敗
- 資料庫中沒有資料

### 問題 3：資料不更新

**檢查：**
```javascript
// 在瀏覽器控制台執行
console.log('Update interval:', UPDATE_INTERVAL);

// 手動觸發更新
updateData();
```

---

## 專案 5：智慧家居控制

### 問題 1：Pico 未接收控制命令

**檢查步驟：**
```bash
# 1. 測試 MQTT 訂閱
mosquitto_sub -h localhost -t "control/#" -v

# 2. 手動發送命令
python3 manual_control.py --device pico_001 --action led_on

# 3. 檢查 Pico 程式
# 確認 CONTROL_TOPIC 設定正確
# 確認 client.check_msg() 有被呼叫
```

### 問題 2：自動化規則未觸發

**檢查配置：**
```json
{
  "condition": "temperature > 28",
  "action": "fan_on",
  "cooldown": 300
}
```

**測試規則：**
```python
# 測試條件評估
temperature = 30
result = eval("temperature > 28", {"__builtins__": {}}, {"temperature": temperature})
print(f"Rule triggered: {result}")
```

### 問題 3：LED 不亮

**檢查 Pico 程式：**
```python
# 測試 LED
led = machine.Pin("LED", machine.Pin.OUT)
led.on()
time.sleep(1)
led.off()
```

---

## 除錯技巧

### 1. 啟用詳細日誌

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### 2. 使用 MQTT 監控工具

```bash
# 監控所有主題
mosquitto_sub -h localhost -t "#" -v

# 監控特定主題
mosquitto_sub -h localhost -t "sensors/#" -v
```

### 3. 檢查資料庫內容

```bash
docker exec -it mongodb mongosh -u admin -p password123
use iot_data
db.getCollectionNames()
db.sensor_logs.find().limit(5).pretty()
```

### 4. 測試 API 端點

```bash
# 使用 curl
curl -X GET http://localhost:8000/api/latest

# 使用 Python
python3 -c "
import requests
r = requests.get('http://localhost:8000/api/latest')
print(r.json())
"
```

### 5. 檢查網路連接

```bash
# 檢查 Pi 的 IP
hostname -I

# 從 Pico 測試連接（在 MicroPython REPL）
import network
wlan = network.WLAN(network.STA_IF)
print(wlan.ifconfig())
```

---

## 延伸挑戰

完成基本功能後，可以嘗試以下挑戰：

### 環境監測系統
- [ ] 加入多個感測器（濕度、光線）
- [ ] 實作資料匯出功能
- [ ] 建立每日報告

### 資料記錄器
- [ ] 實作自動備份排程
- [ ] 加入資料壓縮
- [ ] 建立 Web 下載介面

### 警報系統
- [ ] 實作電子郵件通知
- [ ] 加入警報儀表板
- [ ] 實作智慧警報（機器學習）

### 資料視覺化
- [ ] 加入多種圖表類型
- [ ] 實作資料比較功能
- [ ] 加入匯出圖表功能

### 智慧家居
- [ ] 加入更多控制裝置
- [ ] 實作排程控制
- [ ] 建立手機 App 介面

---

## 取得協助

如果以上方法都無法解決問題：

1. 檢查日誌檔案
2. 查看錯誤訊息的完整堆疊追蹤
3. 搜尋相關錯誤訊息
4. 詢問講師或同學
5. 參考官方文件

## 參考資源

- [MicroPython 文件](https://docs.micropython.org/)
- [FastAPI 文件](https://fastapi.tiangolo.com/)
- [MongoDB 文件](https://docs.mongodb.com/)
- [MQTT 文件](https://mqtt.org/)
- [Paho MQTT Python](https://www.eclipse.org/paho/index.php?page=clients/python/index.php)
