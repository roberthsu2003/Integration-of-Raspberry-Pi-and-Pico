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

---

## 效能優化建議

### MongoDB 效能優化

**建立索引：**
```javascript
// 在 MongoDB shell 中執行
use iot_data
db.sensor_logs.createIndex({"device_id": 1, "timestamp": -1})
db.control_history.createIndex({"device_id": 1, "timestamp": -1})
db.alerts.createIndex({"timestamp": -1})
```

**定期清理舊資料：**
```javascript
// 刪除 30 天前的資料
db.sensor_logs.deleteMany({
  "timestamp": {
    $lt: new Date(Date.now() - 30*24*60*60*1000).toISOString()
  }
})
```

### MQTT 效能優化

**調整 QoS 等級：**
```python
# QoS 0: 最多一次（最快，可能遺失）
client.publish(topic, message, qos=0)

# QoS 1: 至少一次（較慢，保證送達）
client.publish(topic, message, qos=1)
```

**使用持久連接：**
```python
# 設定 keep_alive 時間
client = mqtt.Client()
client.connect(broker, port, keepalive=60)
```

### Pico 記憶體優化

**釋放未使用的變數：**
```python
import gc

# 執行垃圾回收
gc.collect()

# 檢查可用記憶體
print(f"可用記憶體: {gc.mem_free()} bytes")
```

**減少資料緩衝：**
```python
# 立即發送，不累積
client.publish(topic, message)
time.sleep(0.1)  # 給予發送時間
```

---

## 安全性建議

### MQTT 安全

**使用帳號密碼：**
```python
client.username_pw_set("username", "password")
```

**使用 TLS/SSL：**
```python
client.tls_set(ca_certs="ca.crt")
client.connect(broker, 8883)  # 使用 SSL 埠號
```

### MongoDB 安全

**限制網路存取：**
```yaml
# docker-compose.yml
services:
  mongodb:
    ports:
      - "127.0.0.1:27017:27017"  # 只允許本機存取
```

**使用強密碼：**
```bash
# 修改 MongoDB 密碼
docker exec -it mongodb mongosh -u admin -p password123
db.changeUserPassword("admin", "new_strong_password")
```

### API 安全

**加入 API 金鑰驗證：**
```python
from fastapi import Header, HTTPException

async def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != "your_secret_key":
        raise HTTPException(status_code=401, detail="Invalid API Key")
    return x_api_key

@app.get("/api/data", dependencies=[Depends(verify_api_key)])
async def get_data():
    # ...
```

---

## 監控和日誌

### 系統監控

**監控 CPU 和記憶體：**
```bash
# 即時監控
htop

# 檢查特定程序
ps aux | grep python3
```

**監控磁碟空間：**
```bash
df -h
du -sh /var/lib/docker
```

### 日誌管理

**設定日誌輪替：**
```python
import logging
from logging.handlers import RotatingFileHandler

handler = RotatingFileHandler(
    'app.log',
    maxBytes=10*1024*1024,  # 10MB
    backupCount=5
)
logging.basicConfig(handlers=[handler])
```

**集中日誌查看：**
```bash
# 查看所有 Python 程式的日誌
tail -f *.log

# 使用 journalctl（如果使用 systemd）
journalctl -u your_service -f
```

---

## 備份和還原

### 資料庫備份

**手動備份：**
```bash
# 備份整個資料庫
docker exec mongodb mongodump -u admin -p password123 --out /backup

# 複製備份到本機
docker cp mongodb:/backup ./mongodb_backup_$(date +%Y%m%d)
```

**自動備份腳本：**
```bash
#!/bin/bash
# backup_mongodb.sh

BACKUP_DIR="/home/pi/backups"
DATE=$(date +%Y%m%d_%H%M%S)

docker exec mongodb mongodump -u admin -p password123 --out /backup
docker cp mongodb:/backup "$BACKUP_DIR/mongodb_$DATE"

# 保留最近 7 天的備份
find "$BACKUP_DIR" -name "mongodb_*" -mtime +7 -exec rm -rf {} \;
```

### 還原資料庫

```bash
# 還原備份
docker cp ./mongodb_backup mongodb:/restore
docker exec mongodb mongorestore -u admin -p password123 /restore
```

---

## 常見錯誤代碼

### HTTP 狀態碼

- `200 OK` - 請求成功
- `400 Bad Request` - 請求格式錯誤
- `401 Unauthorized` - 未授權
- `404 Not Found` - 資源不存在
- `500 Internal Server Error` - 伺服器錯誤
- `503 Service Unavailable` - 服務暫時無法使用

### MQTT 連接代碼

- `0` - 連接成功
- `1` - 協議版本錯誤
- `2` - 客戶端 ID 無效
- `3` - 伺服器無法使用
- `4` - 帳號密碼錯誤
- `5` - 未授權

### MongoDB 錯誤

- `ServerSelectionTimeoutError` - 無法連接到伺服器
- `DuplicateKeyError` - 重複的鍵值
- `WriteError` - 寫入錯誤
- `NetworkTimeout` - 網路逾時

---

## 快速診斷檢查表

### 系統啟動檢查

- [ ] MongoDB 容器正在運行
- [ ] Mosquitto 服務正在運行
- [ ] Python 虛擬環境已啟動
- [ ] 所有必要的套件已安裝
- [ ] Pico 已連接到 WiFi
- [ ] Pico 可以連接到 MQTT Broker

### 資料流程檢查

- [ ] Pico 可以讀取感測器資料
- [ ] Pico 可以發布 MQTT 訊息
- [ ] Pi 可以接收 MQTT 訊息
- [ ] 資料可以儲存到 MongoDB
- [ ] API 可以查詢資料
- [ ] 儀表板可以顯示資料

### 控制流程檢查

- [ ] 自動化服務正在運行
- [ ] 規則引擎可以評估條件
- [ ] 控制命令可以發送
- [ ] Pico 可以接收控制命令
- [ ] LED 可以正常控制
- [ ] 控制歷史有記錄

---

## 取得協助

如果以上方法都無法解決問題：

1. **檢查日誌檔案** - 查看詳細的錯誤訊息
2. **查看錯誤堆疊追蹤** - 找出問題發生的位置
3. **搜尋錯誤訊息** - 在 Google 或 Stack Overflow 搜尋
4. **檢查版本相容性** - 確認套件版本是否相容
5. **詢問講師或同學** - 描述問題和已嘗試的解決方法
6. **參考官方文件** - 查看最新的文件和範例

### 提問技巧

好的問題應該包含：
- 你想要達成什麼目標
- 你做了什麼操作
- 發生了什麼錯誤（完整的錯誤訊息）
- 你已經嘗試過哪些解決方法
- 你的環境資訊（作業系統、Python 版本等）

---

## 參考資源

### 官方文件

- [MicroPython 文件](https://docs.micropython.org/)
- [Raspberry Pi Pico 文件](https://www.raspberrypi.com/documentation/microcontrollers/)
- [FastAPI 文件](https://fastapi.tiangolo.com/)
- [MongoDB 文件](https://docs.mongodb.com/)
- [MQTT 文件](https://mqtt.org/)
- [Paho MQTT Python](https://www.eclipse.org/paho/index.php?page=clients/python/index.php)

### 社群資源

- [MicroPython 論壇](https://forum.micropython.org/)
- [Raspberry Pi 論壇](https://forums.raspberrypi.com/)
- [Stack Overflow](https://stackoverflow.com/)
- [GitHub Issues](https://github.com/)

### 學習資源

- [MicroPython 教學](https://docs.micropython.org/en/latest/esp8266/tutorial/index.html)
- [FastAPI 教學](https://fastapi.tiangolo.com/tutorial/)
- [MongoDB 大學](https://university.mongodb.com/)
- [MQTT 入門](https://www.hivemq.com/mqtt-essentials/)

---

**最後更新：** 2025-10-11  
**版本：** 2.0
