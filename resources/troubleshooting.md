# 故障排除指南

常見問題和解決方案。

## Pico 相關問題

### Thonny 找不到 Pico
**症狀：** Thonny 右下角沒有顯示 Pico
**解決方法：**
1. 檢查 USB 線是否支援資料傳輸
2. 重新安裝 MicroPython 韌體
3. 重新啟動 Thonny
4. 嘗試不同的 USB 連接埠

### LED 不會亮
**症狀：** 執行 LED 程式但 LED 不亮
**解決方法：**
1. 確認使用 Pico W（不是一般 Pico）
2. 使用 `"LED"` 字串而非數字 25
3. 檢查程式是否有錯誤訊息

### WiFi 無法連接
**症狀：** Pico 無法連接 WiFi
**解決方法：**
1. 確認 SSID 和密碼正確
2. 確認是 2.4GHz WiFi（不支援 5GHz）
3. 檢查訊號強度
4. 嘗試重新啟動 Pico

## Pi 相關問題

### Docker 權限被拒
**症狀：** `permission denied while trying to connect to the Docker daemon`
**解決方法：**
```bash
sudo usermod -aG docker $USER
newgrp docker
```

### MongoDB 無法啟動
**症狀：** MongoDB 容器無法啟動
**解決方法：**
```bash
# 檢查連接埠是否被佔用
sudo netstat -tulpn | grep 27017

# 查看容器日誌
docker logs iot_mongodb

# 重新啟動
docker-compose down
docker-compose up -d
```

### API 無法訪問
**症狀：** 無法訪問 FastAPI
**解決方法：**
1. 檢查程式是否正在運行
2. 確認連接埠 8000 未被佔用
3. 檢查防火牆設定
4. 使用 `curl http://localhost:8000/api/health` 測試

## MQTT 相關問題

### MQTT Broker 無法啟動
**症狀：** Mosquitto 容器無法啟動
**解決方法：**
```bash
# 檢查連接埠
sudo netstat -tulpn | grep 1883

# 查看日誌
docker logs iot_mosquitto

# 重新啟動
cd 03_mqtt_communication/mqtt_broker
docker-compose restart
```

### Pico 無法連接 MQTT
**症狀：** MQTT 連接逾時
**解決方法：**
1. 確認 Broker IP 位址正確
2. 確認 Broker 正在運行
3. 檢查防火牆設定
4. 測試連接：`mosquitto_sub -h localhost -t test`

### 訊息沒有收到
**症狀：** 發布訊息但訂閱者沒收到
**解決方法：**
1. 檢查主題是否匹配
2. 使用監控工具查看：`python mqtt_monitor.py`
3. 確認 QoS 設定
4. 檢查網路連接

## UART 相關問題

### 找不到串列埠
**症狀：** `/dev/ttyACM0` 不存在
**解決方法：**
```bash
# 列出所有串列埠
ls /dev/tty*

# 查看連接訊息
dmesg | grep tty

# 可能是 ttyUSB0 或其他
```

### 串列埠權限被拒
**症狀：** `Permission denied: '/dev/ttyACM0'`
**解決方法：**
```bash
# 永久解決
sudo usermod -aG dialout $USER
# 登出後重新登入

# 臨時解決
sudo chmod 666 /dev/ttyACM0
```

### 收到亂碼
**症狀：** 接收到的資料是亂碼
**解決方法：**
1. 確認鮑率一致（兩端都是 9600）
2. 檢查硬體連接（TX→RX, RX→TX）
3. 確認 GND 已連接

## 資料庫相關問題

### 資料沒有儲存
**症狀：** 資料沒有出現在資料庫中
**解決方法：**
1. 檢查 MongoDB 是否運行
2. 檢查連接字串是否正確
3. 查看訂閱者日誌的錯誤訊息
4. 驗證資料格式是否正確

### 無法查詢資料
**症狀：** API 查詢返回空結果
**解決方法：**
```bash
# 直接查詢 MongoDB
docker exec -it iot_mongodb mongosh -u admin -p password123
> use iot_data
> db.sensor_data.find().limit(5)
```

## 整合問題

### 完整流程不通
**症狀：** 資料無法從 Pico 到資料庫
**解決方法：**
1. 逐步檢查每個環節：
   - Pico 是否發布？（用監控工具查看）
   - Broker 是否收到？（用 mosquitto_sub 測試）
   - Pi 是否訂閱？（查看訂閱者日誌）
   - 資料庫是否儲存？（直接查詢 MongoDB）

2. 使用測試工具：
```bash
# 測試 MQTT
python mqtt_test_tools/mqtt_publisher.py simulate

# 監控訊息
python mqtt_test_tools/mqtt_monitor.py

# 檢查 API
curl http://localhost:8000/api/data
```

## 效能問題

### 系統變慢
**症狀：** 系統反應變慢
**解決方法：**
1. 檢查 CPU 和記憶體使用：`htop`
2. 檢查 Docker 容器資源：`docker stats`
3. 清理舊資料
4. 調整發布頻率

### 資料遺失
**症狀：** 部分資料沒有儲存
**解決方法：**
1. 檢查網路穩定性
2. 增加 MQTT QoS 等級
3. 加入重試機制
4. 檢查資料庫容量

## 除錯技巧

### 使用日誌
```python
# 加入詳細日誌
import logging
logging.basicConfig(level=logging.DEBUG)
```

### 使用監控工具
```bash
# MQTT 監控
python mqtt_monitor.py --topics "#"

# 系統監控
htop
docker stats
```

### 逐步測試
1. 先測試單一元件
2. 再測試兩個元件的連接
3. 最後測試完整流程

## 尋求協助

如果問題仍未解決：
1. 查看相關模組的 README
2. 檢查錯誤訊息
3. 搜尋類似問題
4. 詢問講師或同學
5. 在論壇發問

記住：錯誤訊息是你的朋友，仔細閱讀它！
