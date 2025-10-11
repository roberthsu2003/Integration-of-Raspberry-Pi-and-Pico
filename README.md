# Raspberry Pi 與 Pico 物聯網整合課程

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](CHANGELOG.md)
[![Status](https://img.shields.io/badge/status-ready-green.svg)](PROJECT_OVERVIEW.md)

> 📘 **快速導覽：** [專案總覽](PROJECT_OVERVIEW.md) | [環境設定](SETUP.md) | [課程表](SCHEDULE.md) | [更新日誌](CHANGELOG.md)

## 📖 課程簡介

這是一個實作導向的物聯網課程，教導學生如何使用 Raspberry Pi 和 Raspberry Pi Pico 建立完整的物聯網應用系統。課程採用循序漸進的方式，從單一裝置的基礎操作開始，逐步進階到多裝置整合應用。

## 🎯 學習目標

完成本課程後，你將能夠：

- 使用 MicroPython 控制 Raspberry Pi Pico 和讀取感測器
- 使用 FastAPI 建立 RESTful API 服務
- 使用 Docker 部署 MongoDB 資料庫
- 透過 MQTT 協定實現裝置間的網路通訊
- 整合 Pi 和 Pico 建立完整的資料收集系統
- 管理多個 Pico 裝置並處理並發資料流
- 設計和實作實用的物聯網專案

## 🛠️ 技術架構

### 硬體需求

**Raspberry Pi**（建議 Pi 4 或更新版本）
- 至少 2GB RAM
- microSD 卡（至少 16GB）
- 電源供應器

**Raspberry Pi Pico W**（至少 2 個）
- 內建 WiFi 功能
- USB 連接線

**網路環境**
- WiFi 路由器
- 穩定的網路連接

### 軟體技術棧

**Raspberry Pi 端：**
- Raspberry Pi OS
- Python 3.9+
- FastAPI - Web 框架
- Docker & Docker Compose
- MongoDB - NoSQL 資料庫
- Mosquitto - MQTT Broker
- Paho MQTT - Python MQTT 客戶端

**Raspberry Pi Pico 端：**
- MicroPython 韌體
- umqtt.simple - MQTT 客戶端
- 內建感測器（溫度感測器）

## 📚 課程模組

### 第一階段：基礎操作

**[模組 1-2：Pico 基礎](01_pico_basics/)**
- 開發環境設定
- MicroPython 程式設計
- LED 控制和按鈕輸入
- 內建感測器使用

**[模組 3：Pi 基礎](02_pi_basics/)**
- Docker 和 MongoDB 設定
- FastAPI 入門
- RESTful API 設計
- 資料庫 CRUD 操作

### 第二階段：通訊整合

**[模組 4-5：MQTT 通訊](03_mqtt_communication/)**
- MQTT 協定概念
- Mosquitto Broker 設定
- Pico MQTT 客戶端
- Pi MQTT 客戶端

**[模組 5：UART/USB 通訊](04_uart_usb/)**
- 串列通訊原理
- UART 基礎範例
- 通訊方式比較

**[模組 6：Pi-Pico 整合](05_integration/)**
- 整合架構設計
- 資料收集流程
- 資料儲存和查詢
- 端到端測試

### 第三階段：進階應用

**[模組 7：多裝置管理](06_multi_device/)**
- 裝置識別和註冊
- 多裝置資料收集
- 裝置狀態監控
- 並發處理

**[模組 8：範例專案](07_example_projects/)**
- 環境監測系統
- 資料記錄器
- 警報系統
- 資料視覺化儀表板
- 智慧家居控制

**[模組 9：綜合專題](08_final_project/)**
- 專題設計和實作
- 成果展示
- 課程總結

## 🚀 快速開始

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

1. [Pico 基礎](01_pico_basics/README.md) - MicroPython 和基礎 GPIO
2. [Pi 基礎](02_pi_basics/README.md) - FastAPI 和 MongoDB
3. [MQTT 通訊](03_mqtt_communication/README.md) - 無線通訊協定
4. [UART/USB 通訊](04_uart_usb/README.md) - 串列通訊
5. [整合應用](05_integration/README.md) - 端到端整合
6. [多裝置管理](06_multi_device/README.md) - 裝置管理
7. [範例專案](07_example_projects/README.md) - 實用專案
8. [綜合專題](08_final_project/README.md) - 學生專題

## 📁 專案結構

```
pi-pico-integration/
├── 01_pico_basics/              # Pico 基礎模組
├── 02_pi_basics/                # Pi 基礎模組
├── 03_mqtt_communication/       # MQTT 通訊模組
├── 04_uart_usb/                 # UART/USB 通訊模組
├── 05_integration/              # 整合應用模組
├── 06_multi_device/             # 多裝置管理模組
├── 07_example_projects/         # 範例專案
├── 08_final_project/            # 綜合專題
├── tools/                       # 輔助工具
│   ├── verify_setup.py         # 環境驗證
│   ├── test_mqtt.py            # MQTT 測試
│   └── check_api.py            # API 檢查
├── resources/                   # 學習資源
│   ├── cheatsheets/            # 速查表
│   ├── troubleshooting.md      # 故障排除
│   ├── teacher_guide.md        # 教師指引
│   └── references.md           # 參考資源
├── README.md                    # 本檔案
├── SETUP.md                     # 環境設定指南
├── SCHEDULE.md                  # 詳細課程表
├── CHANGELOG.md                 # 版本更新日誌
├── CONTRIBUTING.md              # 貢獻指南
├── DISTRIBUTION.md              # 課程分發指南
├── FEEDBACK.md                  # 回饋機制
└── LICENSE                      # MIT 授權
```

## 💡 學習建議

1. **按順序學習** - 課程設計為循序漸進，建議按照順序完成
2. **動手實作** - 每個概念都配有實作範例，務必親自執行
3. **完成練習** - 練習題能幫助鞏固學習成果
4. **記錄問題** - 遇到問題時記錄下來，參考故障排除指南
5. **延伸學習** - 完成基礎內容後，嘗試自己的創意專案

## 📖 教學資源

- [詳細課程表](SCHEDULE.md) - 完整的教學時程規劃
- [教師指引](resources/teacher_guide.md) - 教學建議和常見問題
- [故障排除](resources/troubleshooting.md) - 常見問題解決方案
- [速查表](resources/cheatsheets/) - MicroPython、MQTT、FastAPI 速查表
- [參考資源](resources/references.md) - 延伸學習資源

## ❓ 常見問題

**Q: 我需要有程式設計經驗嗎？**  
A: 建議具備基礎的 Python 程式設計知識，但課程會從基礎開始教學。

**Q: 可以使用其他型號的 Raspberry Pi 嗎？**  
A: 可以，但建議使用 Pi 3 或更新的型號以確保效能。

**Q: Pico 和 Pico W 有什麼差別？**  
A: Pico W 內建 WiFi 功能，是本課程必需的。一般的 Pico 沒有 WiFi 無法進行網路通訊。

**Q: 我可以在 Windows/Mac 上開發嗎？**  
A: Pi 端的開發建議在 Raspberry Pi OS 上進行。Pico 的開發可以在任何作業系統上使用 Thonny IDE。

更多問題請參考 [故障排除指南](resources/troubleshooting.md)

## 📄 授權

本專案採用 [MIT 授權條款](LICENSE)。

## 🤝 貢獻

歡迎貢獻！請查看 [貢獻指南](CONTRIBUTING.md) 了解如何參與專案。

## 📞 支援與回饋

- 📚 查看 [故障排除指南](resources/troubleshooting.md)
- 👨‍🏫 閱讀 [教師指引](resources/teacher_guide.md)
- 🐛 提交 [GitHub Issue](https://github.com/your-username/pi-pico-integration/issues)
- 📝 填寫 [回饋問卷](FEEDBACK.md)

---

**祝學習順利！** 🎓🚀
