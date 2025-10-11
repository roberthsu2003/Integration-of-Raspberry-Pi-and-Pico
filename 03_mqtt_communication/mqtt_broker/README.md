# MQTT Broker 設定

本目錄包含 Mosquitto MQTT Broker 的配置檔案。

## 快速開始

### 1. 啟動 MQTT Broker

```bash
# 進入目錄
cd 03_mqtt_communication/mqtt_broker

# 建立必要的目錄
mkdir -p data log

# 啟動 Mosquitto
docker-compose up -d

# 檢查狀態
docker-compose ps
```

### 2. 測試連接

**訂閱測試：**
```bash
# 在終端 1 訂閱主題
mosquitto_sub -h localhost -t test/topic
```

**發布測試：**
```bash
# 在終端 2 發布訊息
mosquitto_pub -h localhost -t test/topic -m "Hello MQTT"
```

如果終端 1 顯示 "Hello MQTT"，表示 MQTT Broker 運作正常。

## 配置說明

### mosquitto.conf

主要配置項目：

- **listener 1883**: MQTT 連接埠
- **allow_anonymous true**: 允許匿名連接（開發用）
- **persistence true**: 啟用資料持久化
- **log_dest**: 日誌輸出位置

### 目錄結構

```
mqtt_broker/
├── mosquitto.conf       # Mosquitto 配置檔
├── docker-compose.yml   # Docker Compose 配置
├── data/               # 持久化資料（自動建立）
└── log/                # 日誌檔案（自動建立）
```

## 常用指令

### Docker 管理

```bash
# 啟動
docker-compose up -d

# 停止
docker-compose stop

# 重新啟動
docker-compose restart

# 查看日誌
docker-compose logs -f

# 停止並移除
docker-compose down
```

### MQTT 測試指令

```bash
# 訂閱主題
mosquitto_sub -h localhost -t "sensors/#" -v

# 發布訊息
mosquitto_pub -h localhost -t "sensors/temp" -m "25.5"

# 訂閱所有主題
mosquitto_sub -h localhost -t "#" -v

# 訂閱系統主題
mosquitto_sub -h localhost -t "\$SYS/#" -v
```

## 安全設定（生產環境）

### 1. 建立密碼檔

```bash
# 進入容器
docker exec -it iot_mosquitto sh

# 建立使用者
mosquitto_passwd -c /mosquitto/config/passwd username

# 新增更多使用者
mosquitto_passwd /mosquitto/config/passwd another_user
```

### 2. 修改 mosquitto.conf

```conf
# 啟用密碼驗證
password_file /mosquitto/config/passwd
allow_anonymous false
```

### 3. 重新啟動

```bash
docker-compose restart
```

### 4. 使用密碼連接

```bash
mosquitto_sub -h localhost -t test -u username -P password
```

## 故障排除

### Q: 無法連接到 Broker？

**檢查項目：**
```bash
# 檢查容器是否運行
docker ps | grep mosquitto

# 檢查連接埠
sudo netstat -tulpn | grep 1883

# 查看日誌
docker-compose logs mosquitto
```

### Q: 訊息沒有收到？

**可能原因：**
1. Topic 名稱不匹配
2. QoS 設定問題
3. 網路連接問題

**除錯方法：**
```bash
# 訂閱所有主題查看訊息
mosquitto_sub -h localhost -t "#" -v
```

### Q: 如何重置 Broker？

```bash
# 停止並移除容器和資料
docker-compose down -v

# 刪除資料目錄
rm -rf data log

# 重新建立目錄
mkdir -p data log

# 重新啟動
docker-compose up -d
```

## 效能調校

### 高負載環境

修改 mosquitto.conf：

```conf
# 增加最大連接數
max_connections 10000

# 增加訊息佇列
max_queued_messages 10000

# 調整 keepalive
keepalive_interval 30
```

### 記憶體優化

```conf
# 限制訊息大小
message_size_limit 1048576  # 1MB

# 限制佇列訊息
max_queued_messages 100
```

## 監控

### 系統主題

Mosquitto 提供系統主題用於監控：

```bash
# 查看所有系統資訊
mosquitto_sub -h localhost -t "\$SYS/#" -v

# 客戶端數量
mosquitto_sub -h localhost -t "\$SYS/broker/clients/connected"

# 訊息統計
mosquitto_sub -h localhost -t "\$SYS/broker/messages/received"
mosquitto_sub -h localhost -t "\$SYS/broker/messages/sent"
```

## 參考資源

- [Mosquitto 官方文件](https://mosquitto.org/documentation/)
- [MQTT 協定規範](https://mqtt.org/)
- [Eclipse Mosquitto Docker](https://hub.docker.com/_/eclipse-mosquitto)
