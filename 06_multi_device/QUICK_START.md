# 多裝置管理 - 快速開始指南

## 🚀 5 分鐘快速啟動

### 前置需求
- ✅ MongoDB 正在執行
- ✅ MQTT Broker 正在執行
- ✅ 已安裝 Python 依賴

### 步驟 1：安裝依賴
```bash
cd 06_multi_device/device_manager
pip install -r requirements.txt
```

### 步驟 2：一鍵啟動所有服務
```bash
./start_all.sh
```

這會自動啟動：
- 多裝置訂閱器
- 裝置監控系統
- 儀表板 API

### 步驟 3：開啟 Web 儀表板
```bash
open dashboard.html
```

或在瀏覽器中開啟：`file:///path/to/06_multi_device/device_manager/dashboard.html`

### 步驟 4：設定 Pico 裝置

在每個 Pico 的 `wifi_config.py` 中：
```python
DEVICE_ID = "pico_001"  # 每個 Pico 使用不同的 ID
DEVICE_NAME = "Temperature Sensor 1"
LOCATION = "Classroom A"
```

### 步驟 5：啟動 Pico
在每個 Pico 上執行感測器發布程式。

## 📊 查看結果

### Web 儀表板
瀏覽器開啟 `dashboard.html`，可以看到：
- 裝置總數、線上/離線狀態
- 每個裝置的即時資訊
- 自動每 30 秒更新

### API 文件
瀏覽器開啟：http://localhost:8001/docs

### 命令列工具

```bash
# 查看所有裝置
python device_manager.py list

# 查看裝置狀態
python device_monitor.py check

# 查看警報
python device_monitor.py alerts
```

## 🛑 停止服務

```bash
./stop_all.sh
```

## 📝 常用命令

### 裝置管理
```bash
# 註冊裝置
python device_manager.py register pico_001 "感測器1" "教室A"

# 查看裝置狀態
python device_manager.py status pico_001

# 查看線上裝置
python device_manager.py online
```

### API 測試
```bash
# 儀表板摘要
curl http://localhost:8001/api/dashboard

# 裝置列表
curl http://localhost:8001/api/devices

# 比較裝置
curl "http://localhost:8001/api/comparison?device_ids=pico_001,pico_002&hours=24"
```

## 🔧 故障排除

### 問題：無法連接 MongoDB
```bash
# 檢查 MongoDB 是否執行
docker ps | grep mongo

# 啟動 MongoDB
cd ../../02_pi_basics
docker-compose up -d
```

### 問題：無法連接 MQTT
```bash
# 檢查 MQTT Broker
mosquitto -v

# 或使用 Docker
cd ../../03_mqtt_communication/mqtt_broker
docker-compose up -d
```

### 問題：API 無法啟動
```bash
# 檢查端口是否被佔用
lsof -i :8001

# 查看 API 日誌
tail -f logs/api.log
```

## 📚 更多資訊

詳細文件請參考：[README.md](README.md)
