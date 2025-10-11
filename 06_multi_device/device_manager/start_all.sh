#!/bin/bash
# 多裝置管理系統 - 一鍵啟動腳本

echo "======================================"
echo "多裝置管理系統 - 啟動中..."
echo "======================================"

# 檢查 Python 環境
if ! command -v python3 &> /dev/null; then
    echo "❌ 找不到 Python3，請先安裝"
    exit 1
fi

# 檢查依賴
echo ""
echo "檢查依賴套件..."
pip3 list | grep -q fastapi || {
    echo "安裝依賴套件..."
    pip3 install -r requirements.txt
}

# 檢查 MongoDB
echo ""
echo "檢查 MongoDB 連接..."
python3 -c "from pymongo import MongoClient; MongoClient().admin.command('ping')" 2>/dev/null || {
    echo "❌ 無法連接 MongoDB，請確認 MongoDB 是否執行"
    echo "   啟動方式: docker-compose up -d (在 02_pi_basics 目錄)"
    exit 1
}

echo "✓ MongoDB 連接正常"

# 建立日誌目錄
mkdir -p logs

# 啟動多裝置訂閱器
echo ""
echo "啟動多裝置訂閱器..."
python3 multi_device_subscriber.py > logs/subscriber.log 2>&1 &
SUBSCRIBER_PID=$!
echo "✓ 訂閱器已啟動 (PID: $SUBSCRIBER_PID)"

# 等待訂閱器啟動
sleep 2

# 啟動裝置監控
echo ""
echo "啟動裝置監控..."
python3 device_monitor.py start > logs/monitor.log 2>&1 &
MONITOR_PID=$!
echo "✓ 監控已啟動 (PID: $MONITOR_PID)"

# 等待監控啟動
sleep 2

# 啟動儀表板 API
echo ""
echo "啟動儀表板 API..."
python3 dashboard_api.py > logs/api.log 2>&1 &
API_PID=$!
echo "✓ API 已啟動 (PID: $API_PID)"

# 等待 API 啟動
sleep 3

# 儲存 PID
echo "$SUBSCRIBER_PID" > logs/subscriber.pid
echo "$MONITOR_PID" > logs/monitor.pid
echo "$API_PID" > logs/api.pid

echo ""
echo "======================================"
echo "✅ 所有服務已啟動！"
echo "======================================"
echo ""
echo "服務資訊："
echo "  - 多裝置訂閱器: PID $SUBSCRIBER_PID"
echo "  - 裝置監控: PID $MONITOR_PID"
echo "  - 儀表板 API: PID $API_PID"
echo ""
echo "存取方式："
echo "  - API 文件: http://localhost:8001/docs"
echo "  - Web 儀表板: open dashboard.html"
echo ""
echo "查看日誌："
echo "  - tail -f logs/subscriber.log"
echo "  - tail -f logs/monitor.log"
echo "  - tail -f logs/api.log"
echo ""
echo "停止服務："
echo "  - ./stop_all.sh"
echo ""
