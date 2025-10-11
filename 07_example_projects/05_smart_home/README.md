# 智慧家居控制系統

## 專案簡介

這是一個智慧家居控制系統，根據感測器資料自動執行控制動作。使用規則引擎實現自動化邏輯，支援雙向 MQTT 通訊（感測器資料上傳 + 控制命令下發）。

## 功能特色

- ✅ 自動化規則引擎
- ✅ 雙向 MQTT 通訊
- ✅ 手動控制介面
- ✅ 規則配置管理
- ✅ 控制歷史記錄

## 系統架構

```
Pico (感測器 + 控制器)
    ↕ MQTT (雙向)
自動化控制服務
    ├─ 規則引擎
    ├─ 控制邏輯
    └─ 歷史記錄
```

## 檔案說明

- `automation_service.py` - 自動化控制服務
- `pico_controller.py` - Pico 控制器程式
- `automation_rules.json` - 自動化規則配置
- `manual_control.py` - 手動控制工具
- `requirements.txt` - Python 套件需求

## 快速開始

### 1. 安裝依賴

```bash
cd 07_example_projects/05_smart_home
pip3 install -r requirements.txt
```

### 2. 配置自動化規則

編輯 `automation_rules.json`

### 3. 啟動自動化服務

```bash
python3 automation_service.py
```

### 4. 上傳 Pico 程式

上傳 `pico_controller.py` 到 Pico

### 5. 手動控制（選填）

```bash
python3 manual_control.py --device pico_001 --action led_on
```

## 自動化規則範例

```json
{
  "rules": [
    {
      "name": "auto_cooling",
      "condition": "temperature > 28",
      "action": "fan_on",
      "description": "溫度過高時開啟風扇"
    },
    {
      "name": "auto_heating",
      "condition": "temperature < 20",
      "action": "heater_on",
      "description": "溫度過低時開啟加熱器"
    }
  ]
}
```

## 支援的控制動作

- `led_on` / `led_off` - LED 控制
- `fan_on` / `fan_off` - 風扇控制（模擬）
- `heater_on` / `heater_off` - 加熱器控制（模擬）

## 控制歷史查詢

### 查看最近的控制記錄
```bash
python3 control_history.py --hours 24 --limit 20
```

### 查看特定裝置的記錄
```bash
python3 control_history.py --device pico_001 --hours 12
```

### 查看統計資訊
```bash
python3 control_history.py --stats --hours 24
```

### 匯出歷史記錄
```bash
python3 control_history.py --export history.json --hours 48
```

## 練習題

1. ✅ 建立溫度自動控制規則（已完成）
2. ✅ 實作手動控制功能（已完成）
3. ✅ 加入控制歷史查詢（已完成）
4. 加入排程控制（例如：每天 22:00 關閉所有設備）
5. 實作多條件規則（例如：溫度 > 28 且濕度 > 70）
6. 建立 Web 控制介面

## 檢核清單

- [ ] 自動化服務正常運作
- [ ] Pico 可以接收控制命令
- [ ] 規則引擎正常觸發
- [ ] 手動控制功能正常
- [ ] 控制歷史正常記錄
