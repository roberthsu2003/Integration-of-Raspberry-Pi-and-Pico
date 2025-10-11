# 資料記錄器

## 專案簡介

這是一個連續資料記錄系統，可以長時間收集感測器資料並提供多種格式的資料匯出功能（CSV、JSON）。適合用於科學實驗、環境監測等需要長期資料記錄的場景。

## 功能特色

- ✅ 連續資料記錄
- ✅ 自動資料備份
- ✅ 多格式匯出（CSV、JSON）
- ✅ 資料完整性驗證
- ✅ 記錄統計報告

## 系統架構

```
Pico 感測器
    ↓ MQTT
資料記錄服務
    ↓ 儲存
MongoDB
    ↓ 匯出
CSV/JSON 檔案
```

## 檔案說明

- `logger_service.py` - 資料記錄服務
- `export_data.py` - 資料匯出工具
- `backup_manager.py` - 備份管理工具
- `requirements.txt` - Python 套件需求

## 快速開始

### 1. 安裝依賴

```bash
cd 07_example_projects/02_data_logger
pip3 install -r requirements.txt
```

### 2. 啟動資料記錄服務

```bash
python3 logger_service.py
```

### 3. 匯出資料

```bash
# 匯出為 JSON
python3 export_data.py --format json --output data.json

# 匯出為 CSV
python3 export_data.py --format csv --output data.csv

# 匯出特定時間範圍
python3 export_data.py --format csv --start "2025-10-11" --end "2025-10-12" --output data.csv

# 匯出特定裝置
python3 export_data.py --format json --device pico_001 --output pico_001.json
```

### 4. 建立備份

```bash
# 手動備份
python3 backup_manager.py --backup

# 還原備份
python3 backup_manager.py --restore backup_20251011_120000.json
```

## 資料格式

### JSON 格式

```json
[
  {
    "device_id": "pico_001",
    "sensor_type": "temperature",
    "value": 25.3,
    "unit": "celsius",
    "timestamp": "2025-10-11T10:30:00",
    "location": "classroom_a"
  }
]
```

### CSV 格式

```csv
device_id,sensor_type,value,unit,timestamp,location
pico_001,temperature,25.3,celsius,2025-10-11T10:30:00,classroom_a
pico_001,temperature,25.5,celsius,2025-10-11T10:35:00,classroom_a
```

## 功能說明

### 1. 連續記錄

服務會持續監聽 MQTT 訊息並自動儲存到資料庫，無需人工介入。

### 2. 資料匯出

支援多種匯出選項：
- 格式：JSON、CSV
- 時間範圍：指定開始和結束時間
- 裝置篩選：匯出特定裝置的資料
- 感測器類型：匯出特定類型的感測器資料

### 3. 自動備份

系統會定期建立資料備份：
- 每日自動備份
- 備份檔案包含時間戳記
- 支援手動備份和還原

### 4. 資料完整性

記錄服務會驗證資料完整性：
- 檢查必要欄位
- 驗證資料格式
- 記錄錯誤和警告

## 使用場景

### 科學實驗

```bash
# 開始實驗前啟動記錄
python3 logger_service.py

# 實驗結束後匯出資料
python3 export_data.py --format csv --start "2025-10-11 09:00" --end "2025-10-11 17:00" --output experiment_data.csv
```

### 長期監測

```bash
# 設定為系統服務，開機自動啟動
sudo systemctl enable data-logger
sudo systemctl start data-logger

# 定期匯出週報
python3 export_data.py --format csv --days 7 --output weekly_report.csv
```

### 資料分析

```bash
# 匯出 JSON 格式供 Python 分析
python3 export_data.py --format json --output analysis_data.json

# 使用 pandas 分析
python3 -c "
import pandas as pd
import json

with open('analysis_data.json') as f:
    data = json.load(f)

df = pd.DataFrame(data)
print(df.describe())
"
```

## 進階功能

### 自訂匯出格式

編輯 `export_data.py` 加入自訂格式：

```python
def export_custom(data, output_file):
    # 自訂匯出邏輯
    pass
```

### 資料壓縮

匯出大量資料時自動壓縮：

```bash
python3 export_data.py --format json --compress --output data.json.gz
```

### 增量備份

只備份新增的資料：

```bash
python3 backup_manager.py --incremental
```

## 故障排除

### 匯出檔案過大

```bash
# 分批匯出
python3 export_data.py --format csv --limit 10000 --offset 0 --output part1.csv
python3 export_data.py --format csv --limit 10000 --offset 10000 --output part2.csv
```

### 記憶體不足

修改 `export_data.py` 使用串流處理：

```python
# 使用游標逐筆處理，不一次載入全部資料
cursor = collection.find(query).batch_size(100)
```

### 備份失敗

檢查磁碟空間：

```bash
df -h
```

## 練習題

### 基礎練習

1. 記錄 1 小時的資料並匯出為 CSV
2. 比較 JSON 和 CSV 檔案大小
3. 建立手動備份

### 進階練習

1. 實作自動每日備份腳本
2. 加入資料壓縮功能
3. 建立資料統計報告

### 挑戰題

1. 實作即時資料串流匯出
2. 加入資料加密功能
3. 建立 Web 介面供下載資料

## 檢核清單

- [ ] 資料記錄服務正常運作
- [ ] 可以匯出 JSON 格式
- [ ] 可以匯出 CSV 格式
- [ ] 時間範圍篩選正常
- [ ] 裝置篩選正常
- [ ] 備份功能正常
- [ ] 還原功能正常

## 參考資源

- [MongoDB 匯出工具](https://docs.mongodb.com/database-tools/mongoexport/)
- [Python CSV 模組](https://docs.python.org/3/library/csv.html)
- [Pandas 資料分析](https://pandas.pydata.org/)
