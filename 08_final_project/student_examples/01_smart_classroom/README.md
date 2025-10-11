# 智慧教室監控系統

## 專題簡介

這是一個智慧教室環境監控系統，能夠即時監測教室的溫度，並根據溫度自動控制空調（使用 LED 模擬）。系統會記錄所有歷史資料，並提供 API 查詢功能。

## 功能列表

- [x] 即時監測教室溫度
- [x] 溫度資料透過 MQTT 傳送到 Pi
- [x] 自動儲存資料到 MongoDB
- [x] 溫度過高時自動開啟空調（LED 亮起）
- [x] 提供 API 查詢歷史資料
- [x] 顯示當前教室狀態

## 系統架構

### 硬體架構
- Raspberry Pi Pico W × 1（溫度感測器）
- Raspberry Pi × 1（資料收集和處理）
- LED × 1（模擬空調）

### 軟體架構
```
Pico (溫度感測)
  ↓ MQTT
MQTT Broker
  ↓
Pi (資料處理)
  ├─ MongoDB (資料儲存)
  └─ FastAPI (API 服務)
```

## 技術選擇

- **通訊協定：** MQTT
- **資料庫：** MongoDB
- **API 框架：** FastAPI
- **感測器：** Pico 內建溫度感測器

## 安裝與設定

### 1. 環境需求
- Raspberry Pi 已安裝 Python 3.9+
- Docker 和 Docker Compose
- Raspberry Pi Pico W 已安裝 MicroPython
- MQTT Broker (Mosquitto)

### 2. Pi 端設定

```bash
# 進入專案目錄
cd pi/

# 複製環境變數檔案
cp .env.example .env

# 修改 .env 中的設定（如需要）

# 安裝相依套件
pip install -r requirements.txt

# 啟動 MongoDB
docker-compose up -d

# 啟動服務
python main.py
```

### 3. Pico 端設定

```bash
# 1. 將 pico/ 目錄下的所有檔案複製到 Pico
# 2. 修改 config.py 中的設定：
#    - WIFI_SSID: 你的 WiFi 名稱
#    - WIFI_PASSWORD: 你的 WiFi 密碼
#    - MQTT_BROKER: Pi 的 IP 位址
#    - TEMP_THRESHOLD: 溫度閾值（預設 26°C）
# 3. 重新啟動 Pico
```

## 使用方法

### 啟動系統

1. **啟動 Pi 端服務**
   ```bash
   cd pi/
   python main.py
   ```
   看到 "API 服務運行於..." 表示啟動成功

2. **啟動 Pico**
   - 連接 Pico 到電源
   - Pico 會自動連接 WiFi 和 MQTT
   - LED 閃爍 3 次表示連接成功

3. **檢查系統狀態**
   ```bash
   curl http://localhost:8000/health
   ```

### 查看資料

#### 使用 API 查詢

```bash
# 查看所有資料
curl http://localhost:8000/api/data

# 查看特定裝置資料
curl http://localhost:8000/api/data/classroom_temp_01

# 查看裝置列表
curl http://localhost:8000/api/devices

# 查看當前教室狀態
curl http://localhost:8000/api/classroom/status
```

#### 使用瀏覽器

開啟瀏覽器訪問：
- API 文件：`http://[Pi_IP]:8000/docs`
- 健康檢查：`http://[Pi_IP]:8000/health`

### 測試功能

```bash
# 測試溫度警報
# 用手握住 Pico 讓溫度上升
# 觀察 LED 是否亮起（模擬空調開啟）

# 測試資料記錄
# 等待幾分鐘後查詢資料
curl http://localhost:8000/api/data/classroom_temp_01
```

## 專題展示

### 功能演示流程

1. **展示即時監測**（1 分鐘）
   - 顯示 Pico 正在運作
   - 說明溫度感測原理

2. **展示自動控制**（2 分鐘）
   - 用手握住 Pico 提高溫度
   - 觀察 LED 自動亮起
   - 說明控制邏輯

3. **展示資料查詢**（2 分鐘）
   - 使用 API 查詢歷史資料
   - 展示資料格式
   - 說明資料儲存機制

4. **問題討論**（1 分鐘）
   - 回答評審問題
   - 說明技術選擇

### 展示截圖

#### 系統運作畫面
```
Pico 輸出：
正在連接到 MQTT Broker: 192.168.1.100:1883
MQTT 連接成功
已發布資料: {'device_id': 'classroom_temp_01', 'temperature': 25.5, 'ac_status': 'off'}
```

#### API 查詢結果
```json
{
  "status": "success",
  "device_id": "classroom_temp_01",
  "count": 50,
  "data": [
    {
      "device_id": "classroom_temp_01",
      "timestamp": 1696000000.0,
      "temperature": 25.5,
      "ac_status": "off"
    }
  ]
}
```

## 遇到的挑戰與解決方案

### 挑戰 1：溫度感測不穩定
**問題：** Pico 內建溫度感測器讀取值波動較大

**解決方案：** 
- 實作移動平均濾波器
- 取 5 次讀取的平均值
- 減少誤觸發

### 挑戰 2：MQTT 連接不穩定
**問題：** WiFi 訊號弱時 MQTT 容易斷線

**解決方案：**
- 加入自動重連機制
- 設定 keep-alive 時間
- 使用 QoS 1 確保訊息送達

### 挑戰 3：溫度閾值設定
**問題：** 不同教室的舒適溫度不同

**解決方案：**
- 將閾值設定為可配置參數
- 提供 API 動態調整閾值
- 記錄閾值變更歷史

## 創新特色

1. **智慧控制邏輯**
   - 不只是簡單的開關控制
   - 考慮溫度變化趨勢
   - 避免頻繁開關

2. **資料分析功能**
   - 計算平均溫度
   - 統計空調使用時間
   - 提供節能建議

3. **擴展性設計**
   - 易於加入更多感測器
   - 支援多個教室監控
   - 可整合其他系統

## 未來改進方向

- [ ] 加入濕度感測器
- [ ] 實作溫度預測功能
- [ ] 加入網頁儀表板
- [ ] 支援手機 App 控制
- [ ] 整合課表自動調整
- [ ] 加入能源消耗統計
- [ ] 實作異常警報通知

## 程式碼亮點

### 移動平均濾波器
```python
class TemperatureFilter:
    def __init__(self, window_size=5):
        self.window = []
        self.window_size = window_size
    
    def add_reading(self, value):
        self.window.append(value)
        if len(self.window) > self.window_size:
            self.window.pop(0)
        return sum(self.window) / len(self.window)
```

### 智慧控制邏輯
```python
def should_turn_on_ac(current_temp, threshold, trend):
    # 溫度超過閾值且持續上升
    if current_temp > threshold and trend > 0:
        return True
    # 溫度遠超閾值
    if current_temp > threshold + 2:
        return True
    return False
```

## 參考資源

- [Pico 溫度感測器文件](https://datasheets.raspberrypi.com/pico/raspberry-pi-pico-python-sdk.pdf)
- [MQTT 協定說明](https://mqtt.org/)
- [FastAPI 官方文件](https://fastapi.tiangolo.com/)
- [MongoDB Python 驅動](https://pymongo.readthedocs.io/)

## 作者

- 姓名：學生範例
- 日期：2025-10-11
- 課程：Raspberry Pi & Pico 物聯網整合課程
