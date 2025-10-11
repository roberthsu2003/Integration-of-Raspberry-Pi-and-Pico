# 範例專案

5 個完整的物聯網應用專案範例。

## 專案列表

### 1. 環境監測系統
**功能：** 監控教室溫度並記錄歷史資料
**技術：** Pico 溫度感測器 + MQTT + MongoDB + FastAPI
**難度：** ⭐⭐☆☆☆

**實作步驟：**
1. 使用現有的 `sensor_publisher.py`
2. 設定 5 秒發布間隔
3. 使用 API 查詢歷史資料
4. 分析溫度趨勢

### 2. 資料記錄器
**功能：** 連續記錄感測器資料並匯出
**技術：** 持續資料收集 + 檔案匯出
**難度：** ⭐⭐☆☆☆

**實作步驟：**
1. 啟動訂閱者持續收集資料
2. 使用 MongoDB 查詢匯出資料
3. 轉換為 CSV 或 JSON 格式

**匯出資料：**
```python
import pymongo
import json

client = pymongo.MongoClient('mongodb://admin:password123@localhost:27017/')
db = client['iot_data']
data = list(db.sensor_data.find({}, {'_id': 0}))

with open('export.json', 'w') as f:
    json.dump(data, f, indent=2, default=str)
```

### 3. 警報系統
**功能：** 溫度超過閾值時發出警報
**技術：** 閾值監控 + 警報通知
**難度：** ⭐⭐⭐☆☆

**實作步驟：**
1. 修改 `data_handler.py` 加入閾值檢查
2. 超過閾值時發布警報訊息
3. 記錄警報事件

**範例程式碼：**
```python
def handle_message(self, topic, data):
    # 原有處理...
    
    # 檢查閾值
    if data.get('sensor_type') == 'temperature':
        if data['value'] > 30:
            self.send_alert(data['device_id'], data['value'])

def send_alert(self, device_id, value):
    alert = {
        'device_id': device_id,
        'alert_type': 'high_temperature',
        'value': value,
        'timestamp': datetime.now()
    }
    # 發布警報或發送通知
    print(f"⚠️ 警報：{device_id} 溫度過高 {value}°C")
```

### 4. 資料視覺化儀表板
**功能：** 即時顯示感測器資料圖表
**技術：** FastAPI + 簡單 HTML 前端
**難度：** ⭐⭐⭐⭐☆

**實作步驟：**
1. 建立 API 端點提供圖表資料
2. 建立簡單的 HTML 頁面
3. 使用 Chart.js 繪製圖表

**API 端點：**
```python
@app.get("/api/chart/temperature")
async def get_temperature_chart(device_id: str, hours: int = 24):
    # 查詢最近 N 小時的資料
    data = db.query_recent_data(device_id, hours)
    return {
        'labels': [d['timestamp'] for d in data],
        'values': [d['value'] for d in data]
    }
```

### 5. 智慧家居控制
**功能：** 根據溫度自動控制（模擬）
**技術：** 自動化規則 + 雙向通訊
**難度：** ⭐⭐⭐⭐⭐

**實作步驟：**
1. 定義自動化規則
2. Pi 監控溫度並發送控制命令
3. Pico 接收命令並執行（LED 模擬）

**規則範例：**
```python
rules = {
    'cooling': {'condition': lambda t: t > 28, 'action': 'fan_on'},
    'heating': {'condition': lambda t: t < 20, 'action': 'heater_on'},
}
```

## 專題建議

### 選擇專題
- 根據興趣選擇
- 考慮難度和時間
- 可以組合多個功能

### 客製化
- 加入自己的創意
- 使用不同的感測器
- 設計獨特的功能

### 展示
- 準備展示影片或投影片
- 說明設計理念
- 展示實際運作

## 評分標準

- **功能完整性（40%）** - 核心功能是否實現
- **程式碼品質（30%）** - 程式碼結構和註解
- **創新性（20%）** - 獨特的想法和實作
- **文件完整性（10%）** - README 和說明

## 資源

所有專案都可以使用現有的程式碼：
- Pico 發布者：`03_mqtt_communication/pico_publisher/`
- Pi 訂閱者：`03_mqtt_communication/pi_subscriber/`
- API 服務：`02_pi_basics/fastapi_app/`
- 測試工具：`03_mqtt_communication/mqtt_test_tools/`

完成後繼續：[綜合專題](../08_final_project/README.md)
