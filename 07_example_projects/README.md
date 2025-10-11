# 範例專案

5 個完整的物聯網應用專案範例，每個專案都包含完整的程式碼、文件和故障排除指南。

## 專案列表

### 1. 環境監測系統 ⭐⭐☆☆☆

**目錄：** `01_environmental_monitor/`

**功能：**
- 即時溫度監測
- 歷史資料記錄
- 溫度趨勢分析
- 異常值檢測
- RESTful API 查詢

**技術：** Pico 溫度感測器 + MQTT + MongoDB + FastAPI

**檔案：**
- `pico_sensor.py` - Pico 端感測器程式
- `monitor_service.py` - Pi 端監測服務
- `api_server.py` - API 查詢服務
- `config.py` - 配置檔案

**快速開始：**
```bash
cd 01_environmental_monitor
pip3 install -r requirements.txt
python3 monitor_service.py  # 終端機 1
python3 api_server.py       # 終端機 2
```

---

### 2. 資料記錄器 ⭐⭐☆☆☆

**目錄：** `02_data_logger/`

**功能：**
- 連續資料記錄
- 多格式匯出（CSV、JSON）
- 自動資料備份
- 資料完整性驗證

**技術：** 持續資料收集 + 檔案匯出 + 備份管理

**檔案：**
- `logger_service.py` - 資料記錄服務
- `export_data.py` - 資料匯出工具
- `backup_manager.py` - 備份管理工具

**快速開始：**
```bash
cd 02_data_logger
pip3 install -r requirements.txt
python3 logger_service.py

# 匯出資料
python3 export_data.py --format csv --output data.csv

# 建立備份
python3 backup_manager.py --backup
```

---

### 3. 警報系統 ⭐⭐⭐☆☆

**目錄：** `03_alert_system/`

**功能：**
- 多種警報條件（閾值、變化率）
- 可配置的警報規則
- 警報歷史記錄
- 多種通知方式
- 警報統計分析

**技術：** 閾值監控 + 規則引擎 + 警報通知

**檔案：**
- `alert_service.py` - 警報監控服務
- `alert_config.json` - 警報規則配置
- `alert_history.py` - 警報歷史查詢工具

**快速開始：**
```bash
cd 03_alert_system
pip3 install -r requirements.txt
python3 alert_service.py

# 查詢警報歷史
python3 alert_history.py --list
python3 alert_history.py --stats
```

---

### 4. 資料視覺化儀表板 ⭐⭐⭐⭐☆

**目錄：** `04_dashboard/`

**功能：**
- 即時資料顯示
- 歷史資料圖表
- 多裝置支援
- 響應式設計
- 自動更新

**技術：** FastAPI + HTML/JavaScript + Chart.js

**檔案：**
- `dashboard_api.py` - 後端 API 服務
- `dashboard.html` - 前端儀表板

**快速開始：**
```bash
cd 04_dashboard
pip3 install -r requirements.txt
python3 dashboard_api.py

# 開啟瀏覽器
# http://localhost:8000
```

---

### 5. 智慧家居控制 ⭐⭐⭐⭐⭐

**目錄：** `05_smart_home/`

**功能：**
- 自動化規則引擎
- 雙向 MQTT 通訊
- 手動控制介面
- 規則配置管理
- 控制歷史記錄

**技術：** 自動化規則 + 雙向通訊 + 控制邏輯

**檔案：**
- `automation_service.py` - 自動化控制服務
- `pico_controller.py` - Pico 控制器程式
- `automation_rules.json` - 自動化規則配置
- `manual_control.py` - 手動控制工具

**快速開始：**
```bash
cd 05_smart_home
pip3 install -r requirements.txt
python3 automation_service.py

# 手動控制
python3 manual_control.py --device pico_001 --action led_on
```

---

## 故障排除

所有專案的常見問題和解決方案請參考：[TROUBLESHOOTING.md](TROUBLESHOOTING.md)

## 專題建議

### 選擇專題
- 根據興趣和難度選擇合適的專案
- 可以從簡單的專案開始，逐步進階
- 可以組合多個專案的功能

### 客製化建議
- 加入自己的創意和想法
- 使用不同類型的感測器
- 設計獨特的功能和介面
- 優化效能和使用者體驗

### 展示準備
- 準備展示影片或投影片
- 說明設計理念和技術架構
- 展示實際運作和功能
- 分享遇到的挑戰和解決方案

## 評分標準

- **功能完整性（40%）** - 核心功能是否實現且運作正常
- **程式碼品質（30%）** - 程式碼結構、註解、錯誤處理
- **創新性（20%）** - 獨特的想法和創意實作
- **文件完整性（10%）** - README、使用說明、註解

## 學習路徑

建議按照以下順序學習專案：

1. **環境監測系統** - 學習基本的資料收集和 API 查詢
2. **資料記錄器** - 學習資料匯出和備份管理
3. **警報系統** - 學習規則引擎和事件處理
4. **資料視覺化** - 學習前端整合和圖表顯示
5. **智慧家居控制** - 學習雙向通訊和自動化控制

## 延伸挑戰

完成基本功能後，可以嘗試：

- 🌡️ 加入多種感測器（濕度、光線、壓力）
- 📊 實作更複雜的資料分析功能
- 🔔 加入多種通知方式（Email、LINE、Telegram）
- 📱 建立手機 App 介面
- 🤖 使用機器學習進行預測和異常檢測
- ☁️ 整合雲端服務（AWS IoT、Azure IoT）

## 參考資源

### 基礎模組
- Pico 基礎：`../01_pico_basics/`
- Pi 基礎：`../02_pi_basics/`
- MQTT 通訊：`../03_mqtt_communication/`
- 整合應用：`../05_integration/`

### 文件資源
- [MicroPython 文件](https://docs.micropython.org/)
- [FastAPI 文件](https://fastapi.tiangolo.com/)
- [MongoDB 文件](https://docs.mongodb.com/)
- [Chart.js 文件](https://www.chartjs.org/)

## 下一步

完成範例專案後，繼續：[綜合專題](../08_final_project/README.md)
