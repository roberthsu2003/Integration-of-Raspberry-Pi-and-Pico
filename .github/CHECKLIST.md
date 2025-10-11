# 專案檢查清單

使用此清單確認專案的完整性和可用性。

## 📋 環境檢查

### 硬體準備
- [ ] Raspberry Pi（Pi 3 或更新版本）
- [ ] Raspberry Pi Pico W（至少 2 個）
- [ ] USB 連接線
- [ ] microSD 卡（至少 16GB）
- [ ] WiFi 路由器
- [ ] 電源供應器

### 軟體安裝
- [ ] Raspberry Pi OS 已安裝
- [ ] Python 3.9+ 已安裝
- [ ] Docker 和 Docker Compose 已安裝
- [ ] Thonny IDE 已安裝
- [ ] Git 已安裝

### 環境驗證
- [ ] 執行 `python tools/verify_setup.py` 通過
- [ ] MongoDB 容器可以啟動
- [ ] MQTT Broker 可以運行
- [ ] Pico 可以連接到電腦

## 📚 課程模組檢查

### 基礎模組
- [ ] 模組 1-2：Pico 基礎（11 個程式範例）
- [ ] 模組 3：Pi 基礎（5 個程式範例）
- [ ] 模組 4-5：MQTT 通訊（8 個程式範例）
- [ ] 模組 5：UART/USB（4 個程式範例）

### 進階模組
- [ ] 模組 6：整合應用（6 個程式範例）
- [ ] 模組 7：多裝置管理（3 個程式範例）
- [ ] 模組 8：範例專案（5 個完整專案）
- [ ] 模組 9：綜合專題（模板和範例）

## 🛠️ 工具檢查

- [ ] `tools/verify_setup.py` - 環境驗證工具
- [ ] `tools/test_mqtt.py` - MQTT 測試工具
- [ ] `tools/check_api.py` - API 檢查工具

## 📖 文件檢查

### 主要文件
- [ ] README.md - 專案說明
- [ ] SETUP.md - 環境設定指南
- [ ] SCHEDULE.md - 課程時間表
- [ ] PROJECT_OVERVIEW.md - 專案總覽

### 輔助文件
- [ ] CHANGELOG.md - 版本更新日誌
- [ ] CONTRIBUTING.md - 貢獻指南
- [ ] DISTRIBUTION.md - 課程分發指南
- [ ] FEEDBACK.md - 回饋機制
- [ ] LICENSE - MIT 授權

### 學習資源
- [ ] resources/teacher_guide.md - 教師指引
- [ ] resources/troubleshooting.md - 故障排除
- [ ] resources/references.md - 參考資源
- [ ] resources/cheatsheets/ - 速查表

## ✅ 功能測試

### Pico 測試
- [ ] LED 閃爍程式可以執行
- [ ] 溫度感測器可以讀取
- [ ] 按鈕輸入可以偵測
- [ ] WiFi 可以連接

### Pi 測試
- [ ] MongoDB 可以儲存和查詢資料
- [ ] FastAPI 服務可以啟動
- [ ] API 端點可以正常回應
- [ ] MQTT Broker 可以接收訊息

### 整合測試
- [ ] Pico 可以發布 MQTT 訊息
- [ ] Pi 可以接收 MQTT 訊息
- [ ] 資料可以儲存到資料庫
- [ ] API 可以查詢儲存的資料

## 🎯 學習目標檢查

完成課程後，學生應該能夠：

- [ ] 使用 MicroPython 控制 Pico
- [ ] 讀取和處理感測器資料
- [ ] 建立 FastAPI RESTful API
- [ ] 使用 Docker 部署服務
- [ ] 實作 MQTT 通訊
- [ ] 整合 Pi 和 Pico
- [ ] 管理多個裝置
- [ ] 設計和實作物聯網專案

## 📝 教學準備檢查

### 課前準備
- [ ] 閱讀教師指引
- [ ] 測試所有範例程式
- [ ] 準備備用硬體
- [ ] 確認網路環境

### 教學材料
- [ ] 投影片或簡報（如需要）
- [ ] 列印的速查表
- [ ] 故障排除指南
- [ ] 評量標準

### 學生準備
- [ ] 確認學生硬體清單
- [ ] 提供環境設定指南
- [ ] 說明課程目標和進度
- [ ] 建立溝通管道

## 🔧 維護檢查

### 定期檢查
- [ ] 更新相依套件
- [ ] 測試所有範例程式
- [ ] 檢查文件連結
- [ ] 收集使用者回饋

### 問題追蹤
- [ ] 記錄常見問題
- [ ] 更新故障排除指南
- [ ] 改進文件說明
- [ ] 修正程式錯誤

## ✨ 完成確認

當所有項目都勾選完成時，專案即可開始使用！

**檢查日期：** ___________  
**檢查者：** ___________  
**狀態：** [ ] 通過 [ ] 需要改進

---

**提示：** 如有任何問題，請參考 [故障排除指南](../resources/troubleshooting.md) 或提交 [GitHub Issue](https://github.com/your-username/pi-pico-integration/issues)。
