# Raspberry Pi 與 Pico 物聯網整合課程

## 課程簡介

這是一個為期 9 天（54 小時）的實作導向課程，教導學生如何使用 Raspberry Pi 和 Raspberry Pi Pico 建立完整的物聯網應用系統。課程採用循序漸進的方式，從單一裝置的基礎操作開始，逐步進階到多裝置整合應用。

## 學習目標

完成本課程後，學生將能夠：

- 使用 MicroPython 控制 Raspberry Pi Pico 和讀取內建感測器
- 使用 FastAPI 建立 RESTful API 服務
- 使用 Docker 部署 MongoDB 資料庫
- 透過 MQTT 協定實現裝置間的網路通訊
- 整合 Pi 和 Pico 建立完整的資料收集系統
- 管理多個 Pico 裝置並處理並發資料流
- 設計和實作實用的物聯網專案

## 技術架構

### 硬體需求

- **Raspberry Pi**（建議 Pi 4 或更新版本）
  - 至少 2GB RAM
  - microSD 卡（至少 16GB）
  - 電源供應器
  
- **Raspberry Pi Pico W**（至少 2 個）
  - 內建 WiFi 功能
  - USB 連接線
  
- **網路環境**
  - WiFi 路由器或網路交換器
  - 穩定的網路連接

### 軟體技術棧

**Raspberry Pi：**
- 作業系統：Raspberry Pi OS
- Python 3.9+
- FastAPI - Web 框架
- Docker & Docker Compose
- MongoDB - NoSQL 資料庫
- Mosquitto - MQTT Broker
- Paho MQTT - Python MQTT 客戶端

**Raspberry Pi Pico：**
- MicroPython 韌體
- umqtt.simple - MQTT 客戶端函式庫
- 內建感測器（溫度感測器）

## 課程結構

課程分為三個主要階段，共 9 天：

### 第一階段：基礎操作（Day 1-3）

**Day 1-2：Pico 基礎**
- 開發環境設定
- MicroPython 程式設計基礎
- LED 控制和按鈕輸入
- 內建感測器使用

**Day 3：Pi 基礎**
- Docker 和 MongoDB 設定
- FastAPI 入門
- RESTful API 設計
- 資料庫 CRUD 操作

### 第二階段：通訊整合（Day 4-6）

**Day 4-5：MQTT 通訊**
- MQTT 協定概念
- Mosquitto Broker 設定
- Pico MQTT 客戶端
- Pi MQTT 客戶端
- UART/USB 通訊簡介

**Day 6：Pi-Pico 整合**
- 整合架構設計
- 資料收集流程
- 資料儲存和查詢
- 端到端測試

### 第三階段：進階應用（Day 7-9）

**Day 7：多裝置管理**
- 裝置識別和註冊
- 多裝置資料收集
- 裝置狀態監控
- 並發處理

**Day 8：範例專案**
- 環境監測系統
- 資料記錄器
- 警報系統
- 資料視覺化儀表板
- 智慧家居控制

**Day 9：綜合專題**
- 專題設計和實作
- 成果展示
- 課程總結
- 後續學習建議

## 快速開始

### 1. 環境設定

請參考 [SETUP.md](SETUP.md) 進行完整的環境設定。

### 2. 驗證安裝

```bash
# 驗證環境配置
python tools/verify_setup.py

# 測試 MQTT 連接
python tools/test_mqtt.py --broker localhost --port 1883

# 檢查 API 服務
python tools/check_api.py --url http://localhost:8000
```

### 3. 開始學習

按照課程順序學習各個模組：

1. [Pico 基礎](01_pico_basics/README.md)
2. [Pi 基礎](02_pi_basics/README.md)
3. [MQTT 通訊](03_mqtt_communication/README.md)
4. [UART/USB 通訊](04_uart_usb/README.md)
5. [整合應用](05_integration/README.md)
6. [多裝置管理](06_multi_device/README.md)
7. [範例專案](07_example_projects/README.md)
8. [綜合專題](08_final_project/README.md)

## 專案結構

```
pi-pico-integration/
├── README.md                          # 本檔案
├── SETUP.md                           # 環境設定指南
├── SCHEDULE.md                        # 詳細課程表
├── 01_pico_basics/                    # Pico 基礎模組
├── 02_pi_basics/                      # Pi 基礎模組
├── 03_mqtt_communication/             # MQTT 通訊模組
├── 04_uart_usb/                       # UART/USB 通訊模組
├── 05_integration/                    # 整合應用模組
├── 06_multi_device/                   # 多裝置管理模組
├── 07_example_projects/               # 範例專案
├── 08_final_project/                  # 綜合專題
├── tools/                             # 輔助工具
│   ├── verify_setup.py               # 環境驗證工具
│   ├── test_mqtt.py                  # MQTT 測試工具
│   └── check_api.py                  # API 檢查工具
└── resources/                         # 學習資源
    ├── cheatsheets/                  # 速查表
    ├── troubleshooting.md            # 故障排除指南
    └── references.md                 # 參考資源
```

## 教學資源

### 給學生

- 每個模組都包含完整的程式碼範例和說明
- 所有程式碼都有詳細的中文註解
- 提供練習題和檢核清單
- 包含常見問題和解決方案

### 給講師

- 詳細的教學指引和時間分配建議
- 每日教學重點和注意事項
- 學生能力評量標準
- 課程調整建議

詳見 [resources/teacher_guide.md](resources/teacher_guide.md)

## 學習建議

1. **按順序學習**：課程設計為循序漸進，建議按照順序完成每個模組
2. **動手實作**：每個概念都配有實作範例，務必親自執行程式碼
3. **完成練習**：每個模組的練習題能幫助鞏固學習成果
4. **記錄問題**：遇到問題時記錄下來，參考故障排除指南或詢問講師
5. **延伸學習**：完成基礎內容後，嘗試延伸挑戰題和自己的創意專案

## 常見問題

### Q: 我需要有程式設計經驗嗎？

A: 建議具備基礎的 Python 程式設計知識，但課程會從基礎開始教學。

### Q: 可以使用其他型號的 Raspberry Pi 嗎？

A: 可以，但建議使用 Pi 3 或更新的型號以確保效能。

### Q: Pico 和 Pico W 有什麼差別？

A: Pico W 內建 WiFi 功能，是本課程必需的。一般的 Pico 沒有 WiFi 無法進行網路通訊。

### Q: 我可以在 Windows/Mac 上開發嗎？

A: Pi 端的開發建議在 Raspberry Pi OS 上進行。Pico 的開發可以在任何作業系統上使用 Thonny IDE。

更多問題請參考 [resources/troubleshooting.md](resources/troubleshooting.md)

## 授權

本課程材料採用 MIT 授權。詳見 [LICENSE](LICENSE) 檔案。

## 貢獻

歡迎提出問題、建議或貢獻程式碼。請參考 [CONTRIBUTING.md](CONTRIBUTING.md)。

## 聯絡方式

如有任何問題或建議，請透過以下方式聯絡：

- 提交 Issue
- 發送 Pull Request
- 電子郵件：[your-email@example.com]

## 致謝

感謝所有為本課程提供建議和回饋的學生和講師。

---

**祝學習愉快！** 🚀
