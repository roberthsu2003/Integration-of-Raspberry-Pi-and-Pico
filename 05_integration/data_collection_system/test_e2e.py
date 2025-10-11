#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
端到端測試腳本
測試完整的資料流程：MQTT 發布 → 資料庫儲存 → API 查詢
"""

import paho.mqtt.client as mqtt
import requests
import json
import time
from datetime import datetime
from pymongo import MongoClient

# ============ 配置參數 ============
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
API_URL = "http://localhost:8000"
MONGO_URI = "mongodb://localhost:27017/"
MONGO_DB = "iot_data"
MONGO_COLLECTION = "sensor_readings"

TEST_DEVICE_ID = "test_pico_e2e"
TEST_TOPIC = f"sensors/{TEST_DEVICE_ID}/temperature"

# ============ 測試結果追蹤 ============
test_results = {
    "total": 0,
    "passed": 0,
    "failed": 0,
    "tests": []
}

def log_test(test_name, passed, message=""):
    """記錄測試結果"""
    test_results["total"] += 1
    if passed:
        test_results["passed"] += 1
        status = "✓ PASS"
    else:
        test_results["failed"] += 1
        status = "✗ FAIL"
    
    test_results["tests"].append({
        "name": test_name,
        "passed": passed,
        "message": message
    })
    
    print(f"{status} - {test_name}")
    if message:
        print(f"      {message}")

# ============ 測試函式 ============

def test_mqtt_connection():
    """測試 1: MQTT Broker 連接"""
    try:
        client = mqtt.Client(client_id="test_client")
        client.connect(MQTT_BROKER, MQTT_PORT, keepalive=10)
        client.disconnect()
        log_test("MQTT Broker 連接", True)
        return True
    except Exception as e:
        log_test("MQTT Broker 連接", False, str(e))
        return False

def test_mongodb_connection():
    """測試 2: MongoDB 連接"""
    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        client.admin.command('ping')
        client.close()
        log_test("MongoDB 連接", True)
        return True
    except Exception as e:
        log_test("MongoDB 連接", False, str(e))
        return False

def test_api_health():
    """測試 3: API 健康檢查"""
    try:
        response = requests.get(f"{API_URL}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "healthy":
                log_test("API 健康檢查", True)
                return True
            else:
                log_test("API 健康檢查", False, f"狀態: {data.get('status')}")
                return False
        else:
            log_test("API 健康檢查", False, f"HTTP {response.status_code}")
            return False
    except Exception as e:
        log_test("API 健康檢查", False, str(e))
        return False

def test_publish_data():
    """測試 4: 發布測試資料"""
    try:
        client = mqtt.Client(client_id="test_publisher")
        client.connect(MQTT_BROKER, MQTT_PORT, keepalive=10)
        
        # 建立測試資料
        test_data = {
            "device_id": TEST_DEVICE_ID,
            "device_type": "test_device",
            "sensor_type": "temperature",
            "value": 25.5,
            "unit": "celsius",
            "timestamp": time.time()
        }
        
        payload = json.dumps(test_data)
        result = client.publish(TEST_TOPIC, payload, qos=1)
        result.wait_for_publish()
        
        client.disconnect()
        
        if result.is_published():
            log_test("發布測試資料", True)
            return True
        else:
            log_test("發布測試資料", False, "發布失敗")
            return False
    except Exception as e:
        log_test("發布測試資料", False, str(e))
        return False

def test_data_in_database():
    """測試 5: 驗證資料已儲存到資料庫"""
    try:
        # 等待資料處理
        time.sleep(2)
        
        client = MongoClient(MONGO_URI)
        db = client[MONGO_DB]
        collection = db[MONGO_COLLECTION]
        
        # 查詢測試資料
        doc = collection.find_one({"device_id": TEST_DEVICE_ID})
        client.close()
        
        if doc:
            log_test("資料儲存到資料庫", True, f"找到文件 ID: {doc['_id']}")
            return True
        else:
            log_test("資料儲存到資料庫", False, "找不到測試資料")
            return False
    except Exception as e:
        log_test("資料儲存到資料庫", False, str(e))
        return False

def test_api_query_all():
    """測試 6: API 查詢所有資料"""
    try:
        response = requests.get(f"{API_URL}/api/data?limit=10", timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "success" and data.get("count") > 0:
                log_test("API 查詢所有資料", True, f"取得 {data['count']} 筆資料")
                return True
            else:
                log_test("API 查詢所有資料", False, "沒有資料")
                return False
        else:
            log_test("API 查詢所有資料", False, f"HTTP {response.status_code}")
            return False
    except Exception as e:
        log_test("API 查詢所有資料", False, str(e))
        return False

def test_api_query_device():
    """測試 7: API 查詢特定裝置"""
    try:
        response = requests.get(f"{API_URL}/api/data/{TEST_DEVICE_ID}", timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "success" and data.get("count") > 0:
                # 驗證資料內容
                first_record = data['data'][0]
                if first_record.get('device_id') == TEST_DEVICE_ID:
                    log_test("API 查詢特定裝置", True, f"取得 {data['count']} 筆資料")
                    return True
                else:
                    log_test("API 查詢特定裝置", False, "裝置 ID 不符")
                    return False
            else:
                log_test("API 查詢特定裝置", False, "沒有資料")
                return False
        else:
            log_test("API 查詢特定裝置", False, f"HTTP {response.status_code}")
            return False
    except Exception as e:
        log_test("API 查詢特定裝置", False, str(e))
        return False

def test_api_query_time_range():
    """測試 8: API 時間範圍查詢"""
    try:
        response = requests.get(f"{API_URL}/api/data/range?hours=1&limit=10", timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "success":
                log_test("API 時間範圍查詢", True, f"取得 {data['count']} 筆資料")
                return True
            else:
                log_test("API 時間範圍查詢", False, "查詢失敗")
                return False
        else:
            log_test("API 時間範圍查詢", False, f"HTTP {response.status_code}")
            return False
    except Exception as e:
        log_test("API 時間範圍查詢", False, str(e))
        return False

def test_api_statistics():
    """測試 9: API 統計資訊"""
    try:
        response = requests.get(f"{API_URL}/api/stats/{TEST_DEVICE_ID}", timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "success":
                stats_msg = f"總計: {data['total_records']} 筆, 平均: {data.get('avg_value')}"
                log_test("API 統計資訊", True, stats_msg)
                return True
            else:
                log_test("API 統計資訊", False, "查詢失敗")
                return False
        else:
            log_test("API 統計資訊", False, f"HTTP {response.status_code}")
            return False
    except Exception as e:
        log_test("API 統計資訊", False, str(e))
        return False

def test_api_devices_list():
    """測試 10: API 裝置列表"""
    try:
        response = requests.get(f"{API_URL}/api/devices", timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "success":
                # 檢查測試裝置是否在列表中
                device_ids = [d['device_id'] for d in data['devices']]
                if TEST_DEVICE_ID in device_ids:
                    log_test("API 裝置列表", True, f"找到 {data['count']} 個裝置")
                    return True
                else:
                    log_test("API 裝置列表", False, "測試裝置不在列表中")
                    return False
            else:
                log_test("API 裝置列表", False, "查詢失敗")
                return False
        else:
            log_test("API 裝置列表", False, f"HTTP {response.status_code}")
            return False
    except Exception as e:
        log_test("API 裝置列表", False, str(e))
        return False

def test_data_integrity():
    """測試 11: 資料完整性驗證"""
    try:
        # 從 API 取得資料
        response = requests.get(f"{API_URL}/api/data/{TEST_DEVICE_ID}?limit=1", timeout=5)
        if response.status_code != 200:
            log_test("資料完整性驗證", False, "無法取得資料")
            return False
        
        api_data = response.json()['data'][0]
        
        # 從資料庫直接取得資料
        client = MongoClient(MONGO_URI)
        db = client[MONGO_DB]
        collection = db[MONGO_COLLECTION]
        db_data = collection.find_one({"device_id": TEST_DEVICE_ID})
        client.close()
        
        # 比對關鍵欄位
        if (api_data['device_id'] == db_data['device_id'] and
            api_data['value'] == db_data['value'] and
            api_data['sensor_type'] == db_data['sensor_type']):
            log_test("資料完整性驗證", True, "API 和資料庫資料一致")
            return True
        else:
            log_test("資料完整性驗證", False, "資料不一致")
            return False
    except Exception as e:
        log_test("資料完整性驗證", False, str(e))
        return False

def cleanup_test_data():
    """清理測試資料"""
    try:
        client = MongoClient(MONGO_URI)
        db = client[MONGO_DB]
        collection = db[MONGO_COLLECTION]
        result = collection.delete_many({"device_id": TEST_DEVICE_ID})
        client.close()
        print(f"\n清理測試資料: 刪除 {result.deleted_count} 筆")
    except Exception as e:
        print(f"\n清理測試資料失敗: {e}")

# ============ 主程式 ============
def main():
    """執行所有測試"""
    print("=" * 60)
    print("端到端測試 - IoT 資料收集系統")
    print("=" * 60)
    print()
    print("測試項目：")
    print("  1. MQTT Broker 連接")
    print("  2. MongoDB 連接")
    print("  3. API 健康檢查")
    print("  4. 發布測試資料")
    print("  5. 驗證資料已儲存")
    print("  6. API 查詢所有資料")
    print("  7. API 查詢特定裝置")
    print("  8. API 時間範圍查詢")
    print("  9. API 統計資訊")
    print("  10. API 裝置列表")
    print("  11. 資料完整性驗證")
    print()
    print("開始測試...")
    print("-" * 60)
    
    # 執行測試
    test_mqtt_connection()
    test_mongodb_connection()
    test_api_health()
    test_publish_data()
    test_data_in_database()
    test_api_query_all()
    test_api_query_device()
    test_api_query_time_range()
    test_api_statistics()
    test_api_devices_list()
    test_data_integrity()
    
    # 顯示測試結果
    print("-" * 60)
    print()
    print("測試結果摘要：")
    print(f"  總測試數: {test_results['total']}")
    print(f"  通過: {test_results['passed']} ✓")
    print(f"  失敗: {test_results['failed']} ✗")
    
    if test_results['failed'] > 0:
        print()
        print("失敗的測試：")
        for test in test_results['tests']:
            if not test['passed']:
                print(f"  - {test['name']}")
                if test['message']:
                    print(f"    {test['message']}")
    
    # 清理測試資料
    cleanup_test_data()
    
    print()
    print("=" * 60)
    
    # 回傳結果
    return test_results['failed'] == 0

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
