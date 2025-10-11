#!/bin/bash
# API 測試腳本

echo "======================================"
echo "IoT 資料查詢 API 測試"
echo "======================================"
echo ""

API_URL="http://localhost:8000"

# 測試 1: 健康檢查
echo "測試 1: 健康檢查"
echo "GET $API_URL/health"
curl -s "$API_URL/health" | python3 -m json.tool
echo ""
echo "--------------------------------------"
echo ""

# 測試 2: 取得所有裝置
echo "測試 2: 取得所有裝置"
echo "GET $API_URL/api/devices"
curl -s "$API_URL/api/devices" | python3 -m json.tool
echo ""
echo "--------------------------------------"
echo ""

# 測試 3: 取得所有資料（限制 5 筆）
echo "測試 3: 取得所有資料（限制 5 筆）"
echo "GET $API_URL/api/data?limit=5"
curl -s "$API_URL/api/data?limit=5" | python3 -m json.tool
echo ""
echo "--------------------------------------"
echo ""

# 測試 4: 取得特定裝置資料
echo "測試 4: 取得特定裝置資料"
echo "GET $API_URL/api/data/pico_001?limit=3"
curl -s "$API_URL/api/data/pico_001?limit=3" | python3 -m json.tool
echo ""
echo "--------------------------------------"
echo ""

# 測試 5: 取得最近 1 小時的資料
echo "測試 5: 取得最近 1 小時的資料"
echo "GET $API_URL/api/data/range?hours=1&limit=5"
curl -s "$API_URL/api/data/range?hours=1&limit=5" | python3 -m json.tool
echo ""
echo "--------------------------------------"
echo ""

# 測試 6: 取得裝置統計資訊
echo "測試 6: 取得裝置統計資訊"
echo "GET $API_URL/api/stats/pico_001"
curl -s "$API_URL/api/stats/pico_001" | python3 -m json.tool
echo ""
echo "--------------------------------------"
echo ""

echo "測試完成！"
