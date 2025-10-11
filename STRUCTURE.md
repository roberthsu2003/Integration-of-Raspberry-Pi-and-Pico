# 專案結構說明

本文件說明專案的目錄結構和檔案組織方式。

## 📁 根目錄結構

```
pi-pico-integration/
├── .github/                    # GitHub 相關設定
│   └── CHECKLIST.md           # 專案檢查清單
├── 01_pico_basics/            # 模組 1-2：Pico 基礎
├── 02_pi_basics/              # 模組 3：Pi 基礎
├── 03_mqtt_communication/     # 模組 4-5：MQTT 通訊
├── 04_uart_usb/               # 模組 5：UART/USB 通訊
├── 05_integration/            # 模組 6：整合應用
├── 06_multi_device/           # 模組 7：多裝置管理
├── 07_example_projects/       # 模組 8：範例專案
├── 08_final_project/          # 模組 9：綜合專題
├── resources/                 # 學習資源
├── scripts/                   # 輔助腳本
├── tools/                     # 開發工具
├── README.md                  # 專案主要說明
├── PROJECT_OVERVIEW.md        # 專案總覽
├── SETUP.md                   # 環境設定指南
├── SCHEDULE.md                # 課程時間表
├── CHANGELOG.md               # 版本更新日誌
├── CONTRIBUTING.md            # 貢獻指南
├── DISTRIBUTION.md            # 課程分發指南
├── FEEDBACK.md                # 回饋機制
├── STRUCTURE.md               # 本檔案
└── LICENSE                    # MIT 授權條款
```

## 📚 課程模組結構

每個課程模組都遵循相似的結構：

```
XX_module_name/
├── README.md                  # 模組說明和學習目標
├── EXERCISES.md               # 練習題（如適用）
├── 01_topic_name/             # 主題資料夾
│   ├── README.md             # 主題說明
│   ├── example.py            # 範例程式
│   └── ...                   # 其他相關檔案
├── 02_topic_name/             # 另一個主題
└── ...
```

## 🗂️ 詳細結構

### 01_pico_basics/ - Pico 基礎模組

```
01_pico_basics/
├── README.md                  # 模組總覽
├── EXERCISES.md               # 練習題
├── 01_led_blink/              # LED 控制
│   ├── README.md
│   ├── hello.py              # Hello World
│   ├── blink.py              # 基礎閃爍
│   ├── blink_variable.py     # 變數控制
│   └── sos.py                # SOS 訊號
├── 02_onboard_sensor/         # 內建感測器
│   ├── README.md
│   ├── temperature.py        # 溫度讀取
│   ├── data_formatter.py     # 資料格式化
│   └── sensor_class.py       # 物件導向版本
└── 03_button_input/           # 按鈕輸入
    ├── README.md
    ├── button.py             # 基礎按鈕
    ├── button_debounce.py    # 防彈跳
    ├── button_interrupt.py   # 中斷處理
    └── button_led.py         # 按鈕控制 LED
```

### 02_pi_basics/ - Pi 基礎模組

```
02_pi_basics/
├── README.md                  # 模組說明
├── docker-compose.yml         # Docker 配置
├── .env.example               # 環境變數範例
├── init-mongo.js              # MongoDB 初始化
├── test_api.py                # API 測試腳本
└── fastapi_app/               # FastAPI 應用
    ├── main.py               # 主程式
    ├── database.py           # 資料庫連接
    ├── models.py             # 資料模型
    └── requirements.txt      # Python 相依套件
```

### 03_mqtt_communication/ - MQTT 通訊模組

```
03_mqtt_communication/
├── README.md                  # 模組說明
├── mqtt_broker/               # MQTT Broker
│   ├── README.md
│   └── mosquitto.conf        # Mosquitto 配置
├── pico_publisher/            # Pico 發布者
│   ├── README.md
│   ├── config.py             # WiFi 配置
│   ├── mqtt_client.py        # MQTT 客戶端
│   └── sensor_publisher.py   # 感測器發布
├── pi_subscriber/             # Pi 訂閱者
│   ├── README.md
│   ├── mqtt_client.py        # MQTT 客戶端
│   ├── data_handler.py       # 資料處理
│   └── requirements.txt      # Python 相依套件
└── mqtt_test_tools/           # 測試工具
    ├── README.md
    ├── test_publisher.py     # 測試發布
    └── monitor.py            # 訊息監控
```

### 04_uart_usb/ - UART/USB 通訊模組

```
04_uart_usb/
├── README.md                  # 模組說明
├── pico_uart/                 # Pico UART
│   ├── README.md
│   ├── uart_sender.py        # UART 發送
│   └── uart_receiver.py      # UART 接收
└── pi_serial/                 # Pi 串列通訊
    ├── README.md
    ├── serial_reader.py      # 串列讀取
    └── requirements.txt      # Python 相依套件
```

### 05_integration/ - 整合應用模組

```
05_integration/
├── README.md                  # 模組說明
├── simple_integration/        # 簡單整合
│   ├── README.md
│   ├── pico_publisher.py     # Pico 端
│   └── pi_subscriber.py      # Pi 端
└── data_collection_system/    # 資料收集系統
    ├── README.md
    ├── pico/                 # Pico 程式
    ├── pi/                   # Pi 程式
    └── test_integration.py   # 整合測試
```

### 06_multi_device/ - 多裝置管理模組

```
06_multi_device/
├── README.md                  # 模組說明
├── QUICK_START.md             # 快速開始
├── pico_setup_example.py      # Pico 設定範例
└── device_manager/            # 裝置管理系統
    ├── README.md
    ├── device_manager.py     # 裝置管理
    ├── multi_subscriber.py   # 多裝置訂閱
    └── dashboard_api.py      # 儀表板 API
```

### 07_example_projects/ - 範例專案

```
07_example_projects/
├── README.md                  # 專案總覽
├── QUICK_REFERENCE.md         # 快速參考
├── TROUBLESHOOTING.md         # 故障排除
├── 01_environmental_monitor/  # 環境監測
├── 02_data_logger/            # 資料記錄器
├── 03_alert_system/           # 警報系統
├── 04_dashboard/              # 資料視覺化
└── 05_smart_home/             # 智慧家居
```

### 08_final_project/ - 綜合專題

```
08_final_project/
├── README.md                  # 專題說明
├── QUICK_START_GUIDE.md       # 快速開始
├── EVALUATION_RUBRIC.md       # 評量標準
├── project_template/          # 專題模板
│   ├── README.md
│   ├── pico/                 # Pico 程式模板
│   └── pi/                   # Pi 程式模板
└── student_examples/          # 學生範例
    ├── smart_greenhouse/     # 智慧溫室
    └── parking_monitor/      # 停車監控
```

### resources/ - 學習資源

```
resources/
├── cheatsheets/               # 速查表
│   ├── README.md
│   ├── micropython_cheatsheet.md
│   ├── fastapi_cheatsheet.md
│   └── mqtt_cheatsheet.md
├── teacher_guide.md           # 教師指引
├── troubleshooting.md         # 故障排除
└── references.md              # 參考資源
```

### tools/ - 開發工具

```
tools/
├── README.md                  # 工具說明
├── verify_setup.py            # 環境驗證
├── test_mqtt.py               # MQTT 測試
└── check_api.py               # API 檢查
```

### scripts/ - 輔助腳本

```
scripts/
└── create_distribution.sh     # 建立分發包
```

## 📄 檔案類型說明

### README.md
每個模組和主題都有 README.md，包含：
- 學習目標
- 內容說明
- 使用方法
- 相關資源連結

### Python 程式檔案 (.py)
- Pico 端：MicroPython 程式
- Pi 端：標準 Python 程式
- 包含詳細註解和說明

### 配置檔案
- `docker-compose.yml` - Docker 服務配置
- `mosquitto.conf` - MQTT Broker 配置
- `requirements.txt` - Python 相依套件
- `.env.example` - 環境變數範例

### 文件檔案 (.md)
- 使用 Markdown 格式
- 包含程式碼範例和說明
- 提供清晰的結構和導航

## 🎯 檔案命名規則

### 目錄命名
- 使用小寫字母和底線
- 數字前綴表示順序（如 `01_`, `02_`）
- 描述性名稱（如 `led_blink`, `mqtt_broker`）

### 檔案命名
- Python 檔案：小寫字母和底線（如 `mqtt_client.py`）
- 文件檔案：大寫字母（如 `README.md`, `SETUP.md`）
- 配置檔案：小寫字母和點（如 `docker-compose.yml`）

## 📊 統計資訊

- **總目錄數：** 40+
- **總檔案數：** 65+
- **程式碼檔案：** 35+
- **文件檔案：** 30+
- **配置檔案：** 10+

## 🔍 快速查找

### 想要學習特定主題？
- LED 控制 → `01_pico_basics/01_led_blink/`
- 感測器讀取 → `01_pico_basics/02_onboard_sensor/`
- API 開發 → `02_pi_basics/fastapi_app/`
- MQTT 通訊 → `03_mqtt_communication/`
- 完整專案 → `07_example_projects/`

### 需要參考資料？
- 速查表 → `resources/cheatsheets/`
- 故障排除 → `resources/troubleshooting.md`
- 教師指引 → `resources/teacher_guide.md`

### 需要工具？
- 環境驗證 → `tools/verify_setup.py`
- MQTT 測試 → `tools/test_mqtt.py`
- API 檢查 → `tools/check_api.py`

## 📝 維護建議

### 新增內容時
1. 遵循現有的目錄結構
2. 提供完整的 README.md
3. 包含詳細的程式碼註解
4. 更新相關的索引文件

### 修改內容時
1. 保持檔案命名一致性
2. 更新相關的文件連結
3. 測試所有程式碼範例
4. 記錄在 CHANGELOG.md

---

**提示：** 如需更詳細的專案資訊，請參考 [PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md)
