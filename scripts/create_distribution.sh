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
cp PROJECT_STATUS.md ${TEMP_DIR}/
cp FINAL_SUMMARY.md ${TEMP_DIR}/
cp DISTRIBUTION.md ${TEMP_DIR}/

echo "🧹 清理不必要的檔案..."

# 移除不必要的檔案
find ${TEMP_DIR} -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null
find ${TEMP_DIR} -name "*.pyc" -delete
find ${TEMP_DIR} -name ".DS_Store" -delete
find ${TEMP_DIR} -name "*.log" -delete
find ${TEMP_DIR} -name ".git" -type d -exec rm -rf {} + 2>/dev/null

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

# 計算檔案數量
FILE_COUNT=$(find ${PACKAGE_NAME} -type f | wc -l)

echo ""
echo "📊 材料包資訊："
echo "   版本: ${VERSION}"
echo "   檔案數量: ${FILE_COUNT}"
echo "   ZIP 大小: ${ZIP_SIZE}"
echo "   TAR.GZ 大小: ${TAR_SIZE}"
echo ""
echo "🎉 材料包建立完成！"
echo ""
echo "📍 檔案位置："
echo "   ${DIST_DIR}/${PACKAGE_NAME}.zip"
echo "   ${DIST_DIR}/${PACKAGE_NAME}.tar.gz"
echo ""
echo "📝 下一步："
echo "   1. 測試壓縮檔內容"
echo "   2. 上傳到 GitHub Releases"
echo "   3. 更新下載連結"
echo "   4. 通知使用者"
