# Requirements Document

## Introduction

本專案是一個為期 9 天（54 小時）的教學課程講義，旨在教導學生如何使用 Raspberry Pi 和 Raspberry Pi Pico 進行物聯網開發。課程採用由淺入深的漸進式學習方式，從單一裝置的基礎操作開始，逐步進階到多裝置整合應用。

**技術架構：**
- Raspberry Pi：使用 FastAPI 提供 API 服務，透過 Docker 建立 MongoDB 資料庫，作為資料收集中心
- Raspberry Pi Pico：主要使用內建感測器進行資料收集
- 通訊方式：主要透過 MQTT 協定進行網路通訊，UART/USB 連線作為補充介紹
- Pi 負責收集多個 Pico 裝置的資料

**課程結構：**
- 總時數：54 小時（9 天 × 6 小時/天）
- 每日安排：上午 3 小時 + 下午 3 小時
- 學習路徑：單一裝置操作 → 整合操作 → 多裝置整合範例

## Requirements

### Requirement 1

**User Story:** 作為學生，我想要學習 Raspberry Pi Pico 的基礎操作，以便了解如何控制單一裝置

#### Acceptance Criteria

1. WHEN 學生開始課程時 THEN 講義 SHALL 提供 Pico 開發環境設定的完整步驟
2. WHEN 學生學習 Pico 時 THEN 講義 SHALL 包含 Pico 內建感測器的使用範例
3. WHEN 學生練習時 THEN 每個範例 SHALL 包含完整的程式碼和執行說明
4. WHEN 學生完成基礎練習時 THEN 學生 SHALL 能夠獨立讀取 Pico 內建感測器資料
5. WHEN 學生需要參考時 THEN 講義 SHALL 提供 MicroPython API 的常用函式說明

### Requirement 2

**User Story:** 作為學生，我想要學習 Raspberry Pi 的基礎操作，以便了解如何建立 API 服務和資料庫

#### Acceptance Criteria

1. WHEN 學生學習 Pi 時 THEN 講義 SHALL 提供 Docker 和 MongoDB 的安裝設定步驟
2. WHEN 學生建立 API 時 THEN 講義 SHALL 提供 FastAPI 的基礎範例和說明
3. WHEN 學生操作資料庫時 THEN 講義 SHALL 包含 MongoDB 的 CRUD 操作範例
4. WHEN 學生完成基礎練習時 THEN 學生 SHALL 能夠建立簡單的 REST API 端點
5. WHEN 學生測試 API 時 THEN 講義 SHALL 提供 API 測試工具的使用說明

### Requirement 3

**User Story:** 作為學生，我想要學習 MQTT 通訊協定，以便了解如何讓裝置之間進行網路通訊

#### Acceptance Criteria

1. WHEN 學生學習 MQTT 時 THEN 講義 SHALL 解釋 MQTT 的基本概念（Broker、Publisher、Subscriber）
2. WHEN 學生設定 MQTT 時 THEN 講義 SHALL 提供 MQTT Broker 的安裝和配置步驟
3. WHEN 學生實作 MQTT 時 THEN 講義 SHALL 包含 Pi 和 Pico 的 MQTT 客戶端範例
4. WHEN 學生測試通訊時 THEN 範例 SHALL 展示如何發布和訂閱訊息
5. WHEN 學生除錯時 THEN 講義 SHALL 提供 MQTT 訊息監控和除錯工具的使用方法

### Requirement 4

**User Story:** 作為學生，我想要學習 UART/USB 連線方式，以便了解不同的裝置通訊方法

#### Acceptance Criteria

1. WHEN 學生學習串列通訊時 THEN 講義 SHALL 簡介 UART/USB 的基本原理
2. WHEN 學生實作串列通訊時 THEN 講義 SHALL 提供一個簡單的 UART 通訊範例
3. WHEN 學生比較通訊方式時 THEN 講義 SHALL 說明 MQTT 和 UART/USB 的使用場景差異
4. IF 學生需要深入了解 THEN 講義 SHALL 提供額外的參考資源連結
5. WHEN 學生完成學習時 THEN 學生 SHALL 理解何時使用網路通訊或串列通訊

### Requirement 5

**User Story:** 作為學生，我想要學習整合 Pi 和 Pico，以便建立完整的物聯網應用

#### Acceptance Criteria

1. WHEN 學生進入整合階段時 THEN 講義 SHALL 提供 Pi 收集 Pico 資料的完整範例
2. WHEN 學生實作整合時 THEN 範例 SHALL 展示 Pico 透過 MQTT 發送感測器資料到 Pi
3. WHEN Pi 接收資料時 THEN 範例 SHALL 展示如何將資料儲存到 MongoDB
4. WHEN 學生查詢資料時 THEN 範例 SHALL 提供透過 FastAPI 查詢資料庫的 API 端點
5. WHEN 學生完成整合時 THEN 學生 SHALL 能夠建立端到端的資料收集和查詢系統

### Requirement 6

**User Story:** 作為學生，我想要學習多裝置整合，以便了解如何管理多個 Pico 裝置

#### Acceptance Criteria

1. WHEN 學生學習多裝置管理時 THEN 講義 SHALL 提供至少 3 個不同的整合範例
2. WHEN 多個 Pico 連接時 THEN 範例 SHALL 展示如何識別和管理不同的裝置
3. WHEN Pi 收集資料時 THEN 範例 SHALL 展示如何同時處理多個 Pico 的資料流
4. WHEN 學生實作時 THEN 每個範例 SHALL 逐步增加複雜度和功能
5. WHEN 學生完成課程時 THEN 學生 SHALL 能夠設計和實作自己的多裝置物聯網專案

### Requirement 7

**User Story:** 作為學生，我想要有清晰的課程進度安排，以便在 9 天內有效學習所有內容

#### Acceptance Criteria

1. WHEN 學生查看課程時 THEN 講義 SHALL 提供 9 天的詳細課程大綱
2. WHEN 每天開始時 THEN 講義 SHALL 明確標示當天的學習目標和預期成果
3. WHEN 學生學習時 THEN 每個主題 SHALL 分配適當的時間（考慮 3 小時的上下午時段）
4. WHEN 學生完成每日課程時 THEN 講義 SHALL 提供練習題或小專題驗證學習成果
5. WHEN 學生需要複習時 THEN 講義 SHALL 提供每日重點摘要和參考資料

### Requirement 8

**User Story:** 作為學生，我想要有實用的範例專案，以便將所學知識應用到實際場景

#### Acceptance Criteria

1. WHEN 學生查看範例時 THEN 講義 SHALL 提供至少 5 個完整的專案範例
2. WHEN 範例展示時 THEN 每個專案 SHALL 包含完整的程式碼、電路圖和說明文件
3. WHEN 學生實作範例時 THEN 專案 SHALL 涵蓋不同的應用場景（如環境監測、自動控制等）
4. WHEN 學生遇到問題時 THEN 每個範例 SHALL 包含常見問題和解決方案
5. WHEN 學生完成範例時 THEN 講義 SHALL 提供延伸挑戰題鼓勵創新應用

### Requirement 9

**User Story:** 作為講師，我想要有完整的教學資源，以便有效地教授這門課程

#### Acceptance Criteria

1. WHEN 講師準備課程時 THEN 講義 SHALL 提供每日的教學指引和時間分配建議
2. WHEN 講師教學時 THEN 講義 SHALL 包含重點概念的說明和常見學生問題的解答
3. WHEN 講師評估學習成果時 THEN 講義 SHALL 提供評量標準和檢核表
4. WHEN 講師需要調整進度時 THEN 講義 SHALL 標示哪些內容是核心必學、哪些是選修延伸
5. WHEN 課程結束時 THEN 講義 SHALL 提供學生能力檢核表和後續學習建議

### Requirement 10

**User Story:** 作為學生，我想要有良好的程式碼結構和註解，以便理解和修改範例程式

#### Acceptance Criteria

1. WHEN 學生閱讀程式碼時 THEN 所有範例 SHALL 包含清晰的中文註解說明
2. WHEN 學生學習時 THEN 程式碼 SHALL 遵循一致的命名規範和格式
3. WHEN 學生修改程式時 THEN 程式碼 SHALL 採用模組化設計便於擴展
4. WHEN 學生除錯時 THEN 程式碼 SHALL 包含適當的錯誤處理和日誌輸出
5. WHEN 學生參考時 THEN 每個函式和類別 SHALL 有清楚的功能說明和參數描述
