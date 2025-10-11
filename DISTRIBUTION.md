# 課程材料包準備指南

本文件說明如何準備和分發課程材料。

## 📦 材料包內容

### 必要檔案
```
pi-pico-integration-course/
├── README.md                    # 課程總覽
├── SETUP.md                     # 環境設定指南
├── SCHEDULE.md                  # 課程時間表
├── LICENSE                      # 授權條款
├── CONTRIBUTING.md              # 貢獻指南
├── CHANGELOG.md                 # 更新日誌
├── 01_pico_basics/              # Day 1-2 內容
├── 02_pi_basics/                # Day 3 內容
├── 03_mqtt_communication/       # Day 4-5 內容
├── 04_uart_usb/                 # Day 5 內容
├── 05_integration/              # Day 6 內容
├── 06_multi_device/             # Day 7 內容
├── 07_example_projects/         # Day 8 內容
├── 08_final_project/            # Day 9 內容
├── tools/                       # 輔助工具
└── resources/                   # 學習資源
```

## 🎯 分發方式

### 方式 1：GitHub Repository（推薦）

**優點：**
- 版本控制
- 易於更新
- 支援協作
- 免費託管

**步驟：**
1. 建立 GitHub Repository
2. 上傳所有檔案
3. 撰寫清晰的 README
4. 設定適當的 .gitignore
5. 加入 LICENSE 檔案

**學生使用：**
```bash
# 複製專案
git clone https://github.com/your-username/pi-pico-integration.git
cd pi-pico-integration

# 更新到最新版本
git pull origin main
```

### 方式 2：壓縮檔下載

**優點：**
- 不需要 Git 知識
- 離線使用
- 完整打包

**準備步驟：**
```bash
# 建立乾淨的副本
cp -r pi-pico-integration pi-pico-integration-v1.0.0

# 移除不必要的檔案
cd pi-pico-integration-v1.0.0
rm -rf .git
rm -rf __pycache__
rm -rf *.pyc
rm -rf .DS_Store

# 建立壓縮檔
cd ..
zip -r pi-pico-integration-v1.0.0.zip pi-pico-integration-v1.0.0
# 或使用 tar
tar -czf pi-pico-integration-v1.0.0.tar.gz pi-pico-integration-v1.0.0
```

### 方式 3：USB 隨身碟

**適用場景：**
- 網路不穩定的教室
- 大量學生同時下載
- 離線教學環境

**準備步驟：**
1. 準備足夠容量的 USB（建議 4GB+）
2. 複製完整的課程資料夾
3. 加入額外資源：
   - MicroPython 韌體檔案
   - Thonny 安裝程式
   - Python 安裝程式
   - Docker Desktop 安裝程式
4. 建立 README.txt 說明使用方式

**USB 結構：**
```
USB:/
├── pi-pico-integration/         # 課程資料夾
├── software/                    # 軟體安裝程式
│   ├── thonny-windows.exe
│   ├── thonny-mac.dmg
│   ├── python-3.11-windows.exe
│   ├── docker-desktop-windows.exe
│   └── docker-desktop-mac.dmg
├── firmware/                    # 韌體檔案
│   └── rp2-pico-w-latest.uf2
└── README.txt                   # 使用說明
```

## 📋 檢查清單

### 發布前檢查

#### 檔案完整性
- [ ] 所有程式碼檔案都已包含
- [ ] 所有文件檔案都已包含
- [ ] 所有配置檔案都已包含
- [ ] README 檔案清晰完整

#### 程式碼品質
- [ ] 所有程式碼都有中文註解
- [ ] 所有程式碼都能正常執行
- [ ] 沒有硬編碼的個人資訊
- [ ] 沒有敏感資訊（密碼、金鑰）

#### 文件品質
- [ ] 所有連結都有效
- [ ] 所有圖片都能顯示
- [ ] 文字沒有錯別字
- [ ] 格式統一一致

#### 授權和版權
- [ ] LICENSE 檔案已包含
- [ ] 版權聲明正確
- [ ] 第三方資源已註明來源
- [ ] 符合開源授權要求

#### 測試驗證
- [ ] 在乾淨環境中測試
- [ ] 驗證安裝步驟
- [ ] 測試所有範例程式
- [ ] 確認文件準確性

## 🔧 自動化腳本

### 建立分發包腳本

創建 `scripts/create_distribution.sh`：

```bash
#!/bin/bash

# 課程材料包建立腳本
VERSION="1.0.0"
PROJECT_NAME="pi-pico-integration"
DIST_DIR="dist"
PACKAGE_NAME="${PROJECT_NAME}-v${VERSION}"

echo "🚀 建立課程材料包 v${VERSION}"

# 建立分發目錄
mkdir -p ${DIST_DIR}

# 建立臨時目錄
TEMP_DIR="${DIST_DIR}/${PACKAGE_NAME}"
mkdir -p ${TEMP_DIR}

echo "📦 複製檔案..."

# 複製主要內容
cp -r 01_pico_basics ${TEMP_DIR}/
cp -r 02_pi_basics ${TEMP_DIR}/
cp -r 03_mqtt_communication ${TEMP_DIR}/
cp -r 04_uart_usb ${TEMP_DIR}/
cp -r 05_integration ${TEMP_DIR}/
cp -r 06_multi_device ${TEMP_DIR}/
cp -r 07_example_projects ${TEMP_DIR}/
cp -r 08_final_project ${TEMP_DIR}/
cp -r tools ${TEMP_DIR}/
cp -r resources ${TEMP_DIR}/

# 複製文件
cp README.md ${TEMP_DIR}/
cp SETUP.md ${TEMP_DIR}/
cp SCHEDULE.md ${TEMP_DIR}/
cp LICENSE ${TEMP_DIR}/
cp CONTRIBUTING.md ${TEMP_DIR}/
cp CHANGELOG.md ${TEMP_DIR}/
cp COMPLETION_GUIDE.md ${TEMP_DIR}/

echo "🧹 清理不必要的檔案..."

# 移除不必要的檔案
find ${TEMP_DIR} -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null
find ${TEMP_DIR} -name "*.pyc" -delete
find ${TEMP_DIR} -name ".DS_Store" -delete
find ${TEMP_DIR} -name "*.log" -delete

echo "📦 建立壓縮檔..."

# 建立 ZIP 檔案
cd ${DIST_DIR}
zip -r ${PACKAGE_NAME}.zip ${PACKAGE_NAME} -q
echo "✅ 已建立: ${DIST_DIR}/${PACKAGE_NAME}.zip"

# 建立 TAR.GZ 檔案
tar -czf ${PACKAGE_NAME}.tar.gz ${PACKAGE_NAME}
echo "✅ 已建立: ${DIST_DIR}/${PACKAGE_NAME}.tar.gz"

# 計算檔案大小
ZIP_SIZE=$(du -h ${PACKAGE_NAME}.zip | cut -f1)
TAR_SIZE=$(du -h ${PACKAGE_NAME}.tar.gz | cut -f1)

echo ""
echo "📊 材料包資訊："
echo "   版本: ${VERSION}"
echo "   ZIP 大小: ${ZIP_SIZE}"
echo "   TAR.GZ 大小: ${TAR_SIZE}"
echo ""
echo "🎉 材料包建立完成！"
echo ""
echo "📍 檔案位置："
echo "   ${DIST_DIR}/${PACKAGE_NAME}.zip"
echo "   ${DIST_DIR}/${PACKAGE_NAME}.tar.gz"
```

### 使用方式

```bash
# 賦予執行權限
chmod +x scripts/create_distribution.sh

# 執行腳本
./scripts/create_distribution.sh
```

## 📤 上傳和分享

### GitHub Releases

1. 在 GitHub 上建立新的 Release
2. 標記版本號（如 v1.0.0）
3. 撰寫 Release Notes
4. 上傳壓縮檔作為附件
5. 發布 Release

### 雲端儲存

**Google Drive：**
- 上傳壓縮檔
- 設定分享權限為「知道連結的人」
- 複製分享連結

**Dropbox：**
- 上傳壓縮檔
- 建立分享連結
- 設定下載權限

**OneDrive：**
- 上傳壓縮檔
- 建立分享連結
- 設定檢視/下載權限

## 📝 分發說明範本

### 給學生的說明

```markdown
# 課程材料下載說明

## 下載方式

### 方式 1：GitHub（推薦）
```bash
git clone https://github.com/your-username/pi-pico-integration.git
```

### 方式 2：直接下載
1. 前往 [Releases 頁面](https://github.com/your-username/pi-pico-integration/releases)
2. 下載最新版本的 ZIP 檔案
3. 解壓縮到你的工作目錄

### 方式 3：雲端下載
- [Google Drive 連結](https://drive.google.com/...)
- [Dropbox 連結](https://www.dropbox.com/...)

## 安裝步驟

1. 下載並解壓縮課程材料
2. 閱讀 `README.md` 了解課程概覽
3. 按照 `SETUP.md` 設定開發環境
4. 參考 `SCHEDULE.md` 了解課程安排

## 需要協助？

- 查看 `resources/troubleshooting.md`
- 聯絡講師
- 提交 GitHub Issue
```

## 🔄 更新流程

### 發布更新版本

1. **更新程式碼和文件**
2. **更新 CHANGELOG.md**
3. **更新版本號**
4. **建立新的分發包**
5. **測試新版本**
6. **發布到 GitHub Releases**
7. **通知使用者**

### 版本號規則

- **1.0.0** → 首次發布
- **1.0.1** → 錯誤修正
- **1.1.0** → 新增功能
- **2.0.0** → 重大變更

## 📊 使用統計

### 追蹤下載量

**GitHub：**
- 查看 Releases 頁面的下載統計
- 使用 GitHub Insights

**Google Analytics：**
- 在文件中加入追蹤碼
- 分析使用者行為

## 🎓 教師專用

### 內部分發

如果是學校內部使用：

1. **建立內部 Git Server**
   - GitLab
   - Gitea
   - 學校的 Git 服務

2. **使用學校的檔案伺服器**
   - 網路磁碟機
   - 學校雲端空間

3. **課堂直接分發**
   - USB 隨身碟
   - 區域網路共享

### 客製化版本

為不同班級建立客製化版本：

```bash
# 建立分支
git checkout -b class-2025-spring

# 進行客製化修改
# ...

# 建立該班級的材料包
./scripts/create_distribution.sh
```

## 📞 支援

如有問題：
- 查看 [CONTRIBUTING.md](CONTRIBUTING.md)
- 提交 GitHub Issue
- 聯絡專案維護者

---

**最後更新：** 2025-10-11
**版本：** 1.0.0
