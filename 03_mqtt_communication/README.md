# MQTT 通訊模組

歡迎來到 MQTT 通訊模組！本模組將教你如何使用 MQTT 協定實現 Pico 和 Pi 之間的通訊。

## 模組概覽

本模組包含四個主要單元：

### 📚 學習單元

1. **[MQTT Broker](mqtt_broker/README.md)**
   - MQTT 基本概念
   - Mosquitto Broker 設定
   - 測試和驗證

2. **[Pico 發布者](pico_publisher/README.md)**
   - WiFi 連接管理
   - MQTT 客戶端實作
   - 感測器資料發布

3. **[Pi 訂閱者](pi_subscriber/README.md)**
   - MQTT 訂閱實作
   - 資料處理和驗證
   - 資料庫整合

4. **[測試工具](mqtt_test_tools/README.md)**
   - 訊息監控工具
   - 測試發布工具
   - 除錯技巧

## 學習目標

完成本模組後，你將能夠：

- ✅ 理解 MQTT 協定的基本概念
- ✅ 設定和管理 MQTT Broker
- ✅ 在 Pico 上實作 MQTT 發布者
- ✅ 在 Pi 上實作 MQTT 訂閱者
- ✅ 設計合理的主題結構
- ✅ 處理連接中斷和重連
- ✅ 測試和除錯 MQTT 通訊
- ✅ 整合 MQTT 和資料庫

## MQTT 基礎概念

### 什麼是 MQTT？

MQTT (Message Queuing Telemetry Transport) 是一個輕量級的訊息傳輸協定，特別適合物聯網應用。

**特點：**
- 輕量級：適合資源受限的裝置
- 低頻寬：訊息開銷小
- 可靠性：支援不同的 QoS 等級
- 雙向通訊：支援發布和訂閱

### MQTT 架構

```
┌─────────┐         ┌─────────┐         ┌─────────┐
│ Pico 1  │────────▶│  MQTT   │◀────────│   Pi    │
│發布者   │         │ Broker  │         │訂閱者   │
└─────────┘         └─────────┘         └─────────┘
                         ▲
                         │
                    ┌────┴────┐
                    │ Pico 2  │
                    │發布者   │
                    └─────────┘
```

**角色說明：**
- **Broker（代理）**：訊息中轉站，負責接收和分發訊息
- **Publisher（發布者）**：發送訊息的客戶端（如 Pico）
- **Subscriber（訂閱者）**：接收訊息的客戶端（如 Pi）

### 主題（Topic）

主題是 MQTT 訊息的路由機制，類似檔案路徑。

**範例：**
```
sensors/pico_001/temperature
sensors/pico_001/humidity
sensors/pico_002/temperature
alerts/high_temperature
```

**萬用字元：**
- `+`：單層萬用字元
  - `sensors/+/temperature` 匹配所有裝置的溫度
- `#`：多層萬用字元
  - `sensors/#` 匹配 sensors 下的所有主題

### QoS（服務品質）

MQTT 提供三種 QoS 等級：

| QoS | 說明 | 使用場景 |
|-----|------|----------|
| 0 | 最多一次（At most once） | 不重要的資料 |
| 1 | 至少一次（At least once） | 一般資料 |
| 2 | 恰好一次（Exactly once） | 重要資料 |

## 快速開始

### 1. 啟動 MQTT Broker

```bash
cd mqtt_broker
docker-compose up -d
```

### 2. 測試 Broker

```bash
# 終端 1：訂閱
mosquitto_sub -h localhost -t test

# 終端 2：發布
mosquitto_pub -h localhost -t test -m "Hello MQTT"
```

### 3. 設定 Pico

1. 修改 `pico_publisher/wifi_config.py`
2. 上傳檔案到 Pico
3. 執行 `sensor_publisher.py`

### 4. 啟動 Pi 訂閱者

```bash
cd pi_subscriber
python subscriber.py
```

### 5. 監控訊息

```bash
cd mqtt_test_tools
python mqtt_monitor.py --topics "sensors/#"
```

## 專案結構

```
03_mqtt_communication/
├── mqtt_broker/                # MQTT Broker 設定
│   ├── mosquitto.conf         # Mosquitto 配置
│   ├── docker-compose.yml     # Docker 配置
│   └── README.md
├── pico_publisher/            # Pico 發布者
│   ├── wifi_config.py         # WiFi 配置
│   ├── wifi_manager.py        # WiFi 管理
│   ├── mqtt_client.py         # MQTT 客戶端
│   ├── sensor_publisher.py    # 主程式
│   └── README.md
├── pi_subscriber/             # Pi 訂閱者
│   ├── mqtt_client.py         # MQTT 客戶端
│   ├── data_handler.py        # 資料處理
│   ├── subscriber.py          # 主程式
│   └── README.md
├── mqtt_test_tools/           # 測試工具
│   ├── mqtt_monitor.py        # 監控工具
│   ├── mqtt_publisher.py      # 發布工具
│   └── README.md
└── README.md                  # 本檔案
```

## 資料流程

完整的資料流程：

```
1. Pico 讀取感測器
        ↓
2. 格式化為 JSON
        ↓
3. 透過 WiFi 連接到 Broker
        ↓
4. 發布到 MQTT 主題
        ↓
5. Broker 轉發訊息
        ↓
6. Pi 訂閱者接收
        ↓
7. 驗證和處理資料
        ↓
8. 儲存到 MongoDB
```

## 主題設計

### 推薦的主題結構

```
sensors/{device_id}/{sensor_type}
alerts/{alert_type}
status/{device_id}
commands/{device_id}/{command}
```

### 範例

**感測器資料：**
```
sensors/pico_001/temperature
sensors/pico_001/humidity
sensors/pico_002/temperature
```

**警報：**
```
alerts/high_temperature
alerts/low_battery
alerts/connection_lost
```

**狀態：**
```
status/pico_001
status/pico_002
```

**命令：**
```
commands/pico_001/led
commands/pico_001/reset
```

## 訊息格式

### 感測器資料

```json
{
    "device_id": "pico_001",
    "device_type": "pico_w",
    "sensor_type": "temperature",
    "value": 25.5,
    "unit": "celsius",
    "timestamp": 1704974422,
    "location": "classroom_a"
}
```

### 狀態訊息

```json
{
    "device_id": "pico_001",
    "status": "online",
    "uptime": 3600,
    "wifi_rssi": -45,
    "timestamp": 1704974422
}
```

### 警報訊息

```json
{
    "device_id": "pico_001",
    "alert_type": "high_temperature",
    "severity": "warning",
    "value": 35.5,
    "threshold": 30.0,
    "timestamp": 1704974422
}
```

## 實用範例

### 範例 1：基本發布訂閱

**Pico 發布：**
```python
from mqtt_client import PicoMQTTClient

mqtt = PicoMQTTClient("pico_001", "192.168.1.100")
mqtt.connect()
mqtt.publish_sensor_data(
    device_id="pico_001",
    sensor_type="temperature",
    value=25.5,
    unit="celsius"
)
```

**Pi 訂閱：**
```python
from mqtt_client import PiMQTTClient

def on_message(topic, data):
    print(f"收到: {data}")

mqtt = PiMQTTClient("pi_sub", "localhost")
mqtt.connect()
mqtt.subscribe("sensors/#", on_message)
```

### 範例 2：多裝置管理

```python
# 訂閱所有裝置的溫度
mqtt.subscribe("sensors/+/temperature", on_temperature)

# 訂閱特定裝置的所有感測器
mqtt.subscribe("sensors/pico_001/#", on_pico_001)

# 訂閱所有警報
mqtt.subscribe("alerts/#", on_alert)
```

### 範例 3：雙向通訊

**Pi 發送命令：**
```python
command = {
    "command": "led_on",
    "duration": 5
}
mqtt.publish("commands/pico_001/led", command)
```

**Pico 接收命令：**
```python
def on_command(topic, data):
    if data['command'] == 'led_on':
        led.on()
        time.sleep(data['duration'])
        led.off()

mqtt.subscribe("commands/pico_001/#", on_command)
```

## 常見問題

### Q: MQTT 和 HTTP 有什麼差別？

**MQTT：**
- 推送模式（Push）
- 持續連接
- 低延遲
- 適合即時資料

**HTTP：**
- 拉取模式（Pull）
- 請求-回應
- 較高延遲
- 適合按需查詢

### Q: 何時使用 MQTT vs UART？

**使用 MQTT：**
- 裝置之間有網路連接
- 需要多對多通訊
- 距離較遠
- 需要可靠性

**使用 UART：**
- 裝置直接連接
- 點對點通訊
- 距離很近
- 需要高速傳輸

### Q: 如何確保訊息可靠性？

**方法：**
1. 使用 QoS 1 或 2
2. 實作重連機制
3. 加入訊息確認
4. 記錄失敗訊息

### Q: 如何優化效能？

**建議：**
1. 使用合適的 QoS 等級
2. 批次發送訊息
3. 壓縮大型訊息
4. 調整 keepalive 時間
5. 使用持久會話

## 練習題

### 🟢 練習 1：基本通訊

建立簡單的發布訂閱系統：
- Pico 每秒發布溫度
- Pi 接收並顯示
- 記錄最高和最低溫度

### 🟡 練習 2：多感測器

擴展系統支援多種感測器：
- 溫度、濕度、光線
- 使用不同的主題
- 實作資料聚合

### 🔴 練習 3：雙向控制

實作雙向通訊系統：
- Pi 發送控制命令
- Pico 執行並回報狀態
- 實作命令佇列

### 🔴 練習 4：警報系統

建立智慧警報系統：
- 監控多個閾值
- 發送警報訊息
- 實作警報升級機制

## 檢核清單

完成本模組前，確認你已經：

### MQTT 基礎
- [ ] 理解 MQTT 的基本概念
- [ ] 了解 Broker、Publisher、Subscriber 的角色
- [ ] 掌握主題和萬用字元的使用
- [ ] 理解 QoS 等級的差異

### Broker 設定
- [ ] 成功啟動 Mosquitto Broker
- [ ] 能夠使用 mosquitto_pub/sub 測試
- [ ] 理解 Broker 配置選項
- [ ] 能夠查看 Broker 日誌

### Pico 發布
- [ ] 實作 WiFi 連接管理
- [ ] 實作 MQTT 客戶端
- [ ] 能夠發布感測器資料
- [ ] 處理連接中斷和重連

### Pi 訂閱
- [ ] 實作 MQTT 訂閱者
- [ ] 處理接收到的訊息
- [ ] 整合資料庫儲存
- [ ] 實作錯誤處理

### 測試和除錯
- [ ] 使用監控工具觀察訊息
- [ ] 使用發布工具測試
- [ ] 能夠除錯連接問題
- [ ] 理解訊息流程

## 下一步

完成 MQTT 通訊模組後，繼續學習：

- **[UART/USB 通訊](../04_uart_usb/README.md)** - 學習串列通訊
- **[整合應用](../05_integration/README.md)** - 建立完整系統

## 參考資源

- [MQTT 官方網站](https://mqtt.org/)
- [Mosquitto 文件](https://mosquitto.org/documentation/)
- [Paho MQTT Python](https://www.eclipse.org/paho/index.php?page=clients/python/docs/index.php)
- [MQTT 最佳實踐](https://www.hivemq.com/mqtt-essentials/)

祝學習愉快！🚀
