#!/bin/bash
# 多裝置管理系統 - 停止腳本

echo "======================================"
echo "停止所有服務..."
echo "======================================"

# 停止訂閱器
if [ -f logs/subscriber.pid ]; then
    PID=$(cat logs/subscriber.pid)
    if ps -p $PID > /dev/null 2>&1; then
        kill $PID
        echo "✓ 已停止訂閱器 (PID: $PID)"
    fi
    rm logs/subscriber.pid
fi

# 停止監控
if [ -f logs/monitor.pid ]; then
    PID=$(cat logs/monitor.pid)
    if ps -p $PID > /dev/null 2>&1; then
        kill $PID
        echo "✓ 已停止監控 (PID: $PID)"
    fi
    rm logs/monitor.pid
fi

# 停止 API
if [ -f logs/api.pid ]; then
    PID=$(cat logs/api.pid)
    if ps -p $PID > /dev/null 2>&1; then
        kill $PID
        echo "✓ 已停止 API (PID: $PID)"
    fi
    rm logs/api.pid
fi

# 清理其他可能的進程
pkill -f "multi_device_subscriber.py" 2>/dev/null
pkill -f "device_monitor.py" 2>/dev/null
pkill -f "dashboard_api.py" 2>/dev/null

echo ""
echo "✅ 所有服務已停止"
