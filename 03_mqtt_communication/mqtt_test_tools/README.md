# MQTT 測試工具

本目錄包含用於測試和除錯 MQTT 通訊的工具。

## 工具列表

```
mqtt_test_tools/
├── mqtt_monitor.py         # 訊息監控工具
├── mqtt_publisher.py       # 測試發布工具
└── README.md              # 本檔案
```

## 1. MQTT 監控工具 (mqtt_monitor.py)

即時監控和顯示 MQTT 訊息。

### 基本使用

```bash
# 監控所有主題
python mqtt_monitor.py

# 監控特定主題
python mqtt_monitor.py --topics "sensors/#"

# 監控多個主題
python mqtt_monitor.py --topics "sensors/#" "alerts/#"

# 指定 Broker
python mqtt_monitor.py --broker 192.168.1.100 --port 1883
```

### 輸出範例

```
======================================================================
✓ 已連接到 MQTT Broker
======================================================================
📡 訂閱主題: sensors/#
======================================================================
開始監控訊息...
按 Ctrl+C 停止
======================================================================

┌─ [1] 10:30:15 ────────────────────────────────────────────────────
│ 主題: sensors/pico_001/temperature
│ 內容:
│   {
│     "device_id": "pico_001",
│     "sensor_type": "temperature",
│     "value": 28.5,
│     "unit": "celsius"
│   }
└────────────────────────────────────────────────────────────────────

┌─ [2] 10:30:20 ────────────────────────────────────────────────────
│ 主題: sensors/pico_002/temperature
│ 內容:
│   {
│     "device_id": "pico_002",
│     "sensor_type": "temperature",
│     "value": 26.2,
│     "unit": "celsius"
│   }
└────────────────────────────────────────────────────────────────────
```

### 停止監控

按 `Ctrl+C` 停止，會顯示統計資訊：

```
監控已停止

======================================================================
統計資訊
======================================================================
運行時間: 120.5 秒
總訊息數: 24
訊息速率: 0.20 則/秒

各主題訊息數:
  sensors/pico_001/temperature: 12
  sensors/pico_002/temperature: 12
======================================================================
```

## 2. MQTT 發布工具 (mqtt_publisher.py)

用於測試 MQTT 訊息發布。

### 單次發布

```bash
# 發布簡單訊息
python mqtt_publisher.py publish "test/topic" "Hello MQTT"

# 發布 JSON 訊息
python mqtt_publisher.py publish "test/topic" '{"key":"value"}'
```

### 模擬感測器

```bash
# 模擬溫度感測器（預設 10 次，間隔 1 秒）
python mqtt_publisher.py simulate

# 自訂參數
python mqtt_publisher.py simulate \
  --device-id pico_test \
  --count 20 \
  --interval 0.5

# 指定 Broker
python mqtt_publisher.py --broker 192.168.1.100 simulate
```

輸出範例：

```
✓ 已連接到 localhost:1883

模擬溫度感測器: test_device
發布 10 次，間隔 1.0 秒
--------------------------------------------------
✓ [1/10] 溫度: 27.34°C
✓ [2/10] 溫度: 23.12°C
✓ [3/10] 溫度: 28.91°C
...
--------------------------------------------------
完成！成功: 10, 失敗: 0
```

### 壓力測試

```bash
# 壓力測試（預設 100 則訊息）
python mqtt_publisher.py stress

# 自訂參數
python mqtt_publisher.py stress \
  --topic test/stress \
  --count 1000 \
  --delay 0.001

# 高速測試（每秒 1000 則）
python mqtt_publisher.py stress --count 10000 --delay 0.001
```

輸出範例：

```
壓力測試
主題: test/stress
訊息數: 100
間隔: 0.01 秒
--------------------------------------------------
已發布 10/100 則訊息
已發布 20/100 則訊息
...
--------------------------------------------------
完成！
總時間: 1.23 秒
速率: 81.30 則/秒
成功: 100, 失敗: 0
```

## 使用場景

### 場景 1：測試 MQTT Broker

```bash
# 終端 1：啟動監控
python mqtt_monitor.py

# 終端 2：發布測試訊息
python mqtt_publisher.py publish "test/topic" "Hello"
```

### 場景 2：測試訂閱者

```bash
# 終端 1：啟動訂閱者
cd ../pi_subscriber
python subscriber.py

# 終端 2：模擬 Pico 發送資料
cd ../mqtt_test_tools
python mqtt_publisher.py simulate --device-id pico_001 --count 5
```

### 場景 3：除錯 Pico 發布

```bash
# 啟動監控，查看 Pico 發送的訊息
python mqtt_monitor.py --topics "sensors/#"

# 在 Pico 上執行發布程式
# 觀察監控工具的輸出
```

### 場景 4：效能測試

```bash
# 終端 1：啟動監控
python mqtt_monitor.py

# 終端 2：壓力測試
python mqtt_publisher.py stress --count 1000 --delay 0.01

# 觀察訊息速率和系統負載
```

## 常用命令組合

### 測試完整流程

```bash
# 1. 啟動 MQTT Broker
cd ../mqtt_broker
docker-compose up -d

# 2. 啟動監控
cd ../mqtt_test_tools
python mqtt_monitor.py --topics "sensors/#" &

# 3. 啟動訂閱者
cd ../pi_subscriber
python subscriber.py &

# 4. 模擬資料發送
cd ../mqtt_test_tools
python mqtt_publisher.py simulate --count 10

# 5. 查看結果
# 監控工具會顯示訊息
# 訂閱者會儲存到資料庫
```

### 除錯連接問題

```bash
# 測試 Broker 是否運行
python mqtt_publisher.py publish "test" "hello"

# 如果失敗，檢查 Broker
docker ps | grep mosquitto

# 查看 Broker 日誌
docker logs iot_mosquitto
```

### 驗證資料格式

```bash
# 監控特定主題
python mqtt_monitor.py --topics "sensors/pico_001/#"

# 發送測試資料
python mqtt_publisher.py simulate --device-id pico_001 --count 1

# 檢查輸出的 JSON 格式是否正確
```

## 進階使用

### 自訂監控過濾

修改 `mqtt_monitor.py`，加入過濾邏輯：

```python
def _on_message(self, client, userdata, msg):
    # 只顯示特定裝置的訊息
    try:
        data = json.loads(msg.payload.decode())
        if data.get('device_id') in ['pico_001', 'pico_002']:
            self._print_message(msg.topic, msg.payload.decode())
    except:
        pass
```

### 自訂發布資料

修改 `mqtt_publisher.py`，加入自訂資料生成：

```python
def publish_custom_data(self):
    """發布自訂資料"""
    data = {
        "device_id": "custom_device",
        "custom_field": "custom_value",
        "timestamp": time.time()
    }
    self.publish("custom/topic", data)
```

### 記錄訊息到檔案

```bash
# 將監控輸出記錄到檔案
python mqtt_monitor.py --topics "sensors/#" > mqtt_log.txt 2>&1

# 或使用 tee 同時顯示和記錄
python mqtt_monitor.py --topics "sensors/#" | tee mqtt_log.txt
```

## 故障排除

### Q: 無法連接到 Broker？

**檢查步驟：**
```bash
# 1. 檢查 Broker 是否運行
docker ps | grep mosquitto

# 2. 檢查連接埠
sudo netstat -tulpn | grep 1883

# 3. 測試連接
mosquitto_sub -h localhost -t test

# 4. 查看防火牆
sudo ufw status
```

### Q: 監控工具沒有顯示訊息？

**可能原因：**
1. 主題不匹配
2. 沒有訊息發布
3. QoS 設定問題

**解決方法：**
```bash
# 使用萬用字元訂閱所有主題
python mqtt_monitor.py --topics "#"

# 發送測試訊息
mosquitto_pub -h localhost -t test -m "hello"
```

### Q: 發布工具報錯？

**檢查項目：**
1. Python 套件是否安裝：`pip install paho-mqtt`
2. Broker 位址是否正確
3. 網路連接是否正常

## 效能基準

在標準配置下的效能參考：

| 測試項目 | 結果 |
|---------|------|
| 單次發布延遲 | < 10ms |
| 持續發布速率 | 100-1000 則/秒 |
| 訂閱延遲 | < 5ms |
| 記憶體使用 | < 50MB |

## 最佳實踐

1. **測試前準備**
   - 確保 Broker 正在運行
   - 清理舊的測試資料
   - 記錄測試參數

2. **監控建議**
   - 使用特定主題而非 `#`
   - 定期檢查統計資訊
   - 記錄異常訊息

3. **壓力測試**
   - 從小量開始
   - 逐步增加負載
   - 監控系統資源

4. **除錯技巧**
   - 使用監控工具觀察訊息
   - 檢查訊息格式
   - 驗證主題結構

## 參考資源

- [MQTT 協定規範](https://mqtt.org/)
- [Paho MQTT Python](https://www.eclipse.org/paho/index.php?page=clients/python/docs/index.php)
- [Mosquitto 文件](https://mosquitto.org/documentation/)
