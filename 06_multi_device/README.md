# Day 7：多裝置管理模組

學習如何管理多個 Pico 裝置，實現並發資料收集、狀態監控和資料視覺化。

## 📚 學習目標

完成本模組後，你將能夠：
- ✅ 管理多個 Pico 裝置的註冊和識別
- ✅ 實作裝置狀態監控和心跳檢測
- ✅ 建立多裝置資料收集系統
- ✅ 使用儀表板 API 進行資料分析和比較
- ✅ 建立簡單的 Web 儀表板

## 🎯 核心概念

### 1. 裝置識別
每個 Pico 使用唯一的 device_id：
- 命名規則：`pico_001`, `pico_002`, `pico_003`...
- MQTT 主題結構：`sensors/{device_id}/temperature`
- 資料庫中使用 device_id 區分不同裝置

### 2. 並發處理
Pi 同時接收多個 Pico 的資料：
- 使用 MQTT 萬用字元訂閱：`sensors/#`
- MongoDB 自動處理並發寫入
- 每個裝置的資料獨立儲存和查詢

### 3. 狀態監控
追蹤裝置的線上/離線狀態：
- 心跳檢測：根據最後資料時間判斷狀態
- 離線警報：裝置超過閾值時間未回報
- 狀態變化通知：記錄裝置上線/離線事件

## 🚀 快速開始

### 步驟 1：設定多個 Pico

在每個 Pico 的 `wifi_config.py` 中設定不同的 device_id：

```python
# Pico 1
DEVICE_ID = "pico_001"
DEVICE_NAME = "Temperature Sensor 1"

# Pico 2
DEVICE_ID = "pico_002"
DEVICE_NAME = "Temperature Sensor 2"

# Pico 3
DEVICE_ID = "pico_003"
DEVICE_NAME = "Temperature Sensor 3"
```

### 步驟 2：啟動多裝置訂閱器

```bash
cd 06_multi_device/device_manager
python multi_device_subscriber.py
```

這會訂閱所有裝置的資料並自動儲存到資料庫。

### 步驟 3：啟動所有 Pico

在每個 Pico 上執行感測器發布程式：
```python
# 在 Pico 上執行
import sensor_publisher
```

### 步驟 4：使用裝置管理工具

```bash
# 註冊新裝置
python device_manager.py register pico_001 "溫度感測器1" "教室A"

# 查看所有裝置
python device_manager.py list

# 查看裝置狀態
python device_manager.py status pico_001

# 查看線上裝置
python device_manager.py online
```

## 🔍 裝置狀態監控

### 啟動監控系統

```bash
cd 06_multi_device/device_manager
python device_monitor.py start
```

監控系統會：
- 每 30 秒檢查所有裝置狀態
- 偵測裝置離線（超過 5 分鐘無資料）
- 自動記錄警報事件
- 顯示即時狀態統計

### 查看監控資訊

```bash
# 檢查所有裝置狀態
python device_monitor.py check

# 查看警報記錄
python device_monitor.py alerts

# 查看特定裝置的警報
python device_monitor.py alerts pico_001

# 查看裝置統計資訊
python device_monitor.py stats pico_001
```

## 📊 儀表板 API

### 啟動儀表板 API 伺服器

```bash
cd 06_multi_device/device_manager
python dashboard_api.py
```

API 會在 `http://localhost:8001` 啟動。

### API 端點說明

#### 1. 儀表板摘要
```bash
curl http://localhost:8001/api/dashboard
```
回傳：總裝置數、線上/離線數量、24小時讀數統計

#### 2. 裝置列表
```bash
curl http://localhost:8001/api/devices
```
回傳：所有裝置的列表及其狀態

#### 3. 裝置詳細資訊
```bash
curl http://localhost:8001/api/devices/pico_001
```
回傳：特定裝置的詳細資訊和統計

#### 4. 裝置比較
```bash
curl "http://localhost:8001/api/comparison?device_ids=pico_001,pico_002,pico_003&hours=24"
```
回傳：多個裝置的資料比較（平均值、最大值、最小值）

#### 5. 統計資訊
```bash
# 所有裝置的統計
curl "http://localhost:8001/api/statistics?hours=24"

# 特定裝置的統計
curl "http://localhost:8001/api/statistics?device_id=pico_001&hours=24"
```

#### 6. 時間序列資料
```bash
curl "http://localhost:8001/api/timeseries?device_id=pico_001&hours=24&interval_minutes=60"
```
回傳：用於繪製圖表的時間序列資料

#### 7. 警報記錄
```bash
# 所有警報
curl http://localhost:8001/api/alerts

# 特定裝置的警報
curl "http://localhost:8001/api/alerts?device_id=pico_001"
```

### 查看 API 文件

瀏覽器開啟：`http://localhost:8001/docs`

這會顯示互動式 API 文件（Swagger UI），可以直接測試所有端點。

## 🌐 Web 儀表板

### 啟動 Web 儀表板

1. 確保儀表板 API 正在執行
2. 用瀏覽器開啟 `dashboard.html`：
   ```bash
   open 06_multi_device/device_manager/dashboard.html
   ```

### 儀表板功能

- 📊 即時顯示裝置統計（總數、線上、離線）
- 📱 裝置卡片顯示每個裝置的狀態
- 🔄 自動每 30 秒重新整理
- 🎨 美觀的視覺化介面

## 💡 實作範例

### 範例 1：註冊並監控 3 個裝置

```bash
# 1. 註冊裝置
python device_manager.py register pico_001 "溫度感測器1" "教室A"
python device_manager.py register pico_002 "溫度感測器2" "教室B"
python device_manager.py register pico_003 "溫度感測器3" "走廊"

# 2. 啟動訂閱器
python multi_device_subscriber.py &

# 3. 啟動監控
python device_monitor.py start &

# 4. 啟動儀表板 API
python dashboard_api.py &

# 5. 開啟 Web 儀表板
open dashboard.html
```

### 範例 2：比較多個裝置的溫度

```python
import requests

# 比較三個裝置的溫度
response = requests.get(
    "http://localhost:8001/api/comparison",
    params={
        "device_ids": "pico_001,pico_002,pico_003",
        "hours": 24
    }
)

data = response.json()
for device in data['devices']:
    print(f"{device['device_id']}: 平均 {device['average_value']}°C")
```

### 範例 3：取得時間序列資料並繪圖

```python
import requests
import matplotlib.pyplot as plt
from datetime import datetime

# 取得時間序列資料
response = requests.get(
    "http://localhost:8001/api/timeseries",
    params={
        "device_id": "pico_001",
        "hours": 24,
        "interval_minutes": 60
    }
)

data = response.json()
timestamps = [datetime.fromisoformat(d['timestamp']) for d in data['data_points']]
values = [d['value'] for d in data['data_points']]

# 繪製圖表
plt.figure(figsize=(12, 6))
plt.plot(timestamps, values, marker='o')
plt.title('24 小時溫度變化')
plt.xlabel('時間')
plt.ylabel('溫度 (°C)')
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
```

## 🔧 故障排除

### 問題 1：裝置顯示離線但實際在運作

**可能原因：**
- 時間同步問題
- 網路延遲
- 離線閾值設定太短

**解決方案：**
```python
# 調整離線閾值（在 device_monitor.py 中）
monitor = DeviceMonitor(offline_threshold_minutes=10)  # 改為 10 分鐘
```

### 問題 2：API 無法連接

**檢查步驟：**
```bash
# 1. 確認 API 是否執行
curl http://localhost:8001/health

# 2. 檢查 MongoDB 連接
python -c "from pymongo import MongoClient; MongoClient().admin.command('ping'); print('OK')"

# 3. 查看 API 日誌
python dashboard_api.py
```

### 問題 3：儀表板無法顯示資料

**檢查步驟：**
1. 開啟瀏覽器開發者工具（F12）
2. 查看 Console 是否有錯誤
3. 確認 API URL 是否正確（`dashboard.html` 中的 `API_URL`）
4. 檢查 CORS 設定

## 📝 練習題

### 練習 1：基礎操作
1. 註冊 3 個裝置
2. 啟動多裝置訂閱器
3. 讓所有 Pico 發送資料
4. 使用 CLI 工具查看裝置狀態

### 練習 2：監控系統
1. 啟動裝置監控
2. 關閉一個 Pico
3. 觀察離線警報
4. 重新啟動 Pico
5. 觀察重新上線通知

### 練習 3：API 使用
1. 啟動儀表板 API
2. 使用 curl 測試所有端點
3. 比較多個裝置的資料
4. 取得時間序列資料

### 練習 4：Web 儀表板
1. 開啟 Web 儀表板
2. 觀察即時更新
3. 嘗試修改 HTML 加入新功能
4. 加入圖表顯示（使用 Chart.js）

## 🎓 進階挑戰

1. **自訂警報規則**
   - 溫度超過閾值時發送警報
   - 裝置資料異常時通知
   - 整合 Email 或 LINE 通知

2. **資料分析功能**
   - 計算裝置間的相關性
   - 預測裝置故障
   - 異常值偵測

3. **進階儀表板**
   - 使用 Chart.js 加入圖表
   - 即時更新（WebSocket）
   - 響應式設計（手機版）

4. **效能優化**
   - 資料庫索引優化
   - API 快取機制
   - 批次處理資料

## 📦 安裝依賴

```bash
cd 06_multi_device/device_manager
pip install -r requirements.txt
```

## 🔗 相關資源

- [FastAPI 文件](https://fastapi.tiangolo.com/)
- [MongoDB 聚合管道](https://docs.mongodb.com/manual/aggregation/)
- [Chart.js 圖表庫](https://www.chartjs.org/)

## ✅ 檢核清單

完成以下項目後，你就掌握了多裝置管理：

- [ ] 成功註冊多個裝置
- [ ] 多裝置訂閱器正常運作
- [ ] 裝置監控系統正常運作
- [ ] 能夠查看裝置狀態和警報
- [ ] 儀表板 API 正常運作
- [ ] 能夠使用所有 API 端點
- [ ] Web 儀表板正常顯示
- [ ] 能夠比較多個裝置的資料
- [ ] 理解時間序列資料的應用
- [ ] 完成所有練習題

## 📖 下一步

完成本模組後，繼續學習：
- [範例專案](../07_example_projects/README.md) - 實用的完整專案範例
- [綜合專題](../08_final_project/README.md) - 設計你自己的物聯網專案
