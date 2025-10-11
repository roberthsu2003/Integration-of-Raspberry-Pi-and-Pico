# [專題名稱]

## 專題簡介

[在此描述你的專題目的和功能]

## 功能列表

- [ ] 功能 1：[描述]
- [ ] 功能 2：[描述]
- [ ] 功能 3：[描述]

## 系統架構

### 硬體架構
- Raspberry Pi Pico W × [數量]
- Raspberry Pi × 1
- 感測器：[列出使用的感測器]

### 軟體架構
```
Pico (MicroPython)
  ↓ [MQTT/UART]
MQTT Broker / Serial
  ↓
Pi (Python)
  ↓
MongoDB
  ↓
FastAPI
```

## 技術選擇

- **通訊協定：** MQTT / UART
- **資料庫：** MongoDB
- **API 框架：** FastAPI
- **其他工具：** [列出其他使用的工具]

## 安裝與設定

### 1. 環境需求
- Raspberry Pi 已安裝 Python 3.9+
- Docker 和 Docker Compose
- Raspberry Pi Pico W 已安裝 MicroPython

### 2. Pi 端設定
```bash
# 安裝相依套件
cd pi/
pip install -r requirements.txt

# 啟動 MongoDB
docker-compose up -d

# 啟動服務
python main.py
```

### 3. Pico 端設定
```bash
# 上傳程式到 Pico
# 1. 將 pico/ 目錄下的所有檔案複製到 Pico
# 2. 修改 config.py 中的 WiFi 和 MQTT 設定
# 3. 重新啟動 Pico
```

## 使用方法

### 啟動系統
1. 啟動 Pi 端服務
2. 啟動 Pico 裝置
3. 檢查連接狀態

### 查看資料
- API 端點：`http://[Pi_IP]:8000/api/data`
- 儀表板：`http://[Pi_IP]:8000/dashboard`

### 測試功能
```bash
# 測試 API
python test_api.py

# 查看 MQTT 訊息
python monitor_mqtt.py
```

## 專題展示

### 功能演示
[描述如何展示各項功能]

### 展示影片/截圖
[放置展示影片連結或截圖]

## 遇到的挑戰與解決方案

### 挑戰 1：[描述問題]
**解決方案：** [描述如何解決]

### 挑戰 2：[描述問題]
**解決方案：** [描述如何解決]

## 未來改進方向

- [ ] 改進項目 1
- [ ] 改進項目 2
- [ ] 改進項目 3

## 參考資源

- [列出參考的文件、教學或專案]

## 作者

- 姓名：[你的名字]
- 日期：[完成日期]
- 聯絡方式：[選填]
