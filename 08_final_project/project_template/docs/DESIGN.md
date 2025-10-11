# 專題設計文件

## 系統架構

### 整體架構圖

```
┌─────────────────────┐
│  Raspberry Pi Pico  │
│  ┌───────────────┐  │
│  │ 感測器讀取    │  │
│  └───────┬───────┘  │
│          │          │
│  ┌───────▼───────┐  │
│  │ MQTT 發布     │  │
│  └───────────────┘  │
└──────────┬──────────┘
           │ WiFi/MQTT
           │
┌──────────▼──────────┐
│   MQTT Broker       │
│   (Mosquitto)       │
└──────────┬──────────┘
           │
┌──────────▼──────────┐
│  Raspberry Pi       │
│  ┌───────────────┐  │
│  │ MQTT 訂閱     │  │
│  └───────┬───────┘  │
│          │          │
│  ┌───────▼───────┐  │
│  │ 資料處理      │  │
│  └───────┬───────┘  │
│          │          │
│  ┌───────▼───────┐  │
│  │ MongoDB       │  │
│  └───────┬───────┘  │
│          │          │
│  ┌───────▼───────┐  │
│  │ FastAPI       │  │
│  └───────────────┘  │
└─────────────────────┘
```

## 資料流程

### 1. 資料收集流程

```
感測器 → Pico 讀取 → 格式化 → MQTT 發布 → Broker → Pi 訂閱 → 儲存到 DB
```

### 2. 資料查詢流程

```
使用者 → HTTP 請求 → FastAPI → 查詢 MongoDB → 回傳 JSON → 使用者
```

## 模組設計

### Pico 端模組

#### 1. main.py
- 主程式進入點
- 初始化所有模組
- 主迴圈控制

#### 2. sensor_reader.py
- 感測器讀取邏輯
- 資料格式化
- 錯誤處理

#### 3. mqtt_client.py
- MQTT 連接管理
- 訊息發布
- 重連機制

#### 4. config.py
- 配置參數
- WiFi 設定
- MQTT 設定

### Pi 端模組

#### 1. main.py
- FastAPI 應用程式
- API 端點定義
- 啟動/關閉邏輯

#### 2. mqtt_subscriber.py
- MQTT 訂閱管理
- 訊息接收處理
- 背景執行緒

#### 3. database.py
- MongoDB 連接
- CRUD 操作
- 查詢方法

#### 4. models.py
- 資料模型定義
- 驗證規則

#### 5. config.py
- 環境變數載入
- 配置管理

## 資料模型

### 感測器資料格式

```json
{
  "device_id": "pico_student_01",
  "timestamp": 1696000000.0,
  "data": {
    "temperature": 25.5,
    "humidity": 60.0
  }
}
```

### MongoDB 文件結構

```json
{
  "_id": ObjectId("..."),
  "device_id": "pico_student_01",
  "timestamp": 1696000000.0,
  "data": {
    "temperature": 25.5
  },
  "saved_at": ISODate("2025-10-11T10:30:00Z")
}
```

## API 設計

### 端點列表

| 方法 | 路徑 | 說明 |
|------|------|------|
| GET | / | 根端點，顯示 API 資訊 |
| GET | /health | 健康檢查 |
| GET | /api/data | 取得所有資料 |
| GET | /api/data/{device_id} | 取得特定裝置資料 |
| GET | /api/devices | 取得裝置列表 |
| DELETE | /api/data | 清除所有資料 |

### API 回應格式

#### 成功回應
```json
{
  "status": "success",
  "data": [...],
  "count": 100
}
```

#### 錯誤回應
```json
{
  "detail": "錯誤訊息"
}
```

## 通訊協定

### MQTT 主題結構

```
student/sensors/{device_id}
```

範例：
- `student/sensors/pico_student_01`
- `student/sensors/pico_student_02`

### MQTT 訊息格式

```json
{
  "device_id": "pico_student_01",
  "timestamp": 1696000000.0,
  "data": {
    "temperature": 25.5
  }
}
```

## 錯誤處理

### Pico 端

1. **感測器讀取失敗**
   - 回傳 None 或預設值
   - 記錄錯誤訊息
   - 繼續執行

2. **MQTT 連接失敗**
   - 重試連接（最多 3 次）
   - 延遲重試（5 秒）
   - 閃爍 LED 指示錯誤

### Pi 端

1. **資料庫連接失敗**
   - 拋出 HTTPException (503)
   - 記錄錯誤日誌
   - 自動重連

2. **MQTT 訂閱失敗**
   - 記錄錯誤
   - 嘗試重新訂閱
   - 通知管理員

## 擴展性考量

### 支援多裝置

- 使用 device_id 識別不同裝置
- MQTT 主題包含 device_id
- 資料庫索引優化查詢

### 支援多種感測器

- sensor_reader.py 模組化設計
- 動態載入感測器驅動
- 統一的資料格式

### 效能優化

- MongoDB 索引優化
- API 分頁查詢
- MQTT QoS 設定

## 安全性考量

### 基本安全措施

1. **MQTT 認證**（選用）
   - 使用者名稱/密碼
   - TLS 加密

2. **API 安全**（選用）
   - API Key 驗證
   - CORS 設定
   - 速率限制

3. **資料驗證**
   - Pydantic 模型驗證
   - 輸入清理
   - 範圍檢查

## 測試策略

### 單元測試

- 感測器讀取功能
- 資料庫操作
- API 端點

### 整合測試

- 端到端資料流程
- MQTT 通訊
- 錯誤處理

### 手動測試

- 實際硬體測試
- 網路中斷測試
- 壓力測試

## 部署建議

### 開發環境

- 本地 MongoDB
- 本地 MQTT Broker
- 開發模式 API

### 生產環境（選用）

- Docker 容器化
- 雲端 MQTT Broker
- 反向代理（Nginx）
- HTTPS 加密
