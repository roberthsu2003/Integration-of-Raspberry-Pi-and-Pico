# 資料視覺化儀表板

## 專案簡介

這是一個即時資料視覺化儀表板，提供 Web 介面顯示感測器資料圖表。使用 FastAPI 提供後端 API，搭配簡單的 HTML/JavaScript 前端實現即時資料更新。

## 功能特色

- ✅ 即時資料顯示
- ✅ 歷史資料圖表
- ✅ 多裝置支援
- ✅ 響應式設計
- ✅ 自動更新

## 系統架構

```
MongoDB ← API 服務 → Web 儀表板
                      ↓
                   Chart.js 圖表
```

## 檔案說明

- `dashboard_api.py` - 後端 API 服務
- `dashboard.html` - 前端儀表板
- `requirements.txt` - Python 套件需求

## 快速開始

### 1. 安裝依賴

```bash
cd 07_example_projects/04_dashboard
pip3 install -r requirements.txt
```

### 2. 啟動 API 服務

```bash
python3 dashboard_api.py
```

### 3. 開啟儀表板

在瀏覽器中開啟：
```
http://localhost:8000
```

## API 端點

### 取得最新資料
```
GET /api/latest?device_id=pico_001
```

### 取得歷史資料
```
GET /api/history?device_id=pico_001&hours=24
```

### 取得圖表資料
```
GET /api/chart?device_id=pico_001&hours=6
```

### 取得裝置列表
```
GET /api/devices
```

### 取得統計資訊
```
GET /api/stats?device_id=pico_001&hours=24
```
回傳：平均值、最大值、最小值、資料筆數、範圍

### 比較多個裝置
```
GET /api/compare?hours=6
```
回傳所有裝置的資料，用於多裝置比較圖表

## 客製化

### 修改更新間隔

編輯 `dashboard.html`：
```javascript
const UPDATE_INTERVAL = 5000; // 毫秒
```

### 修改圖表樣式

編輯 Chart.js 配置：
```javascript
const chartConfig = {
  type: 'line',
  options: {
    // 自訂選項
  }
};
```

### 加入新的圖表

複製現有圖表區塊並修改：
```html
<canvas id="myNewChart"></canvas>
```

## 新增功能

### 多裝置比較圖表
- 點擊「載入比較資料」按鈕可以同時顯示多個裝置的溫度趨勢
- 每個裝置使用不同顏色的線條
- 適合比較不同位置的溫度差異

### 統計資訊 API
- 提供完整的統計資訊（平均、最大、最小、範圍）
- 可以指定時間範圍
- 方便進行資料分析

## 練習題

1. ✅ 加入溫度範圍警示線（可在圖表配置中加入 annotation）
2. ✅ 實作多裝置比較圖表（已完成）
3. 加入資料匯出功能（CSV/JSON）
4. 加入溫度預測功能（使用簡單的線性回歸）
5. 實作警報閾值設定介面

## 檢核清單

- [ ] API 服務正常運作
- [ ] 儀表板可以開啟
- [ ] 圖表正常顯示
- [ ] 資料自動更新
- [ ] 多裝置切換正常
