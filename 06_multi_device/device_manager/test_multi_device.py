#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
多裝置管理系統測試腳本
測試裝置管理、監控和 API 功能
"""

import requests
import time
from device_manager import DeviceManager
from device_monitor import DeviceMonitor

def test_device_manager():
    """測試裝置管理功能"""
    print("\n" + "="*60)
    print("測試 1: 裝置管理功能")
    print("="*60)
    
    manager = DeviceManager()
    
    # 測試註冊裝置
    print("\n1. 註冊測試裝置...")
    test_devices = [
        ("test_pico_001", {"device_name": "測試裝置1", "location": "測試區A"}),
        ("test_pico_002", {"device_name": "測試裝置2", "location": "測試區B"}),
        ("test_pico_003", {"device_name": "測試裝置3", "location": "測試區C"})
    ]
    
    for device_id, info in test_devices:
        result = manager.register_device(device_id, info)
        assert result, f"註冊 {device_id} 失敗"
    
    print("✓ 裝置註冊成功")
    
    # 測試查詢裝置
    print("\n2. 查詢裝置列表...")
    devices = manager.get_all_devices()
    print(f"✓ 找到 {len(devices)} 個裝置")
    
    # 測試取得單一裝置
    print("\n3. 查詢單一裝置...")
    device = manager.get_device("test_pico_001")
    assert device is not None, "找不到裝置"
    print(f"✓ 裝置資訊: {device['device_name']}")
    
    # 測試更新狀態
    print("\n4. 更新裝置狀態...")
    result = manager.update_device_status("test_pico_001", "online")
    assert result, "更新狀態失敗"
    print("✓ 狀態更新成功")
    
    # 測試移除裝置
    print("\n5. 移除測試裝置...")
    for device_id, _ in test_devices:
        manager.remove_device(device_id)
    print("✓ 裝置移除成功")
    
    manager.close()
    print("\n✅ 裝置管理功能測試通過")

def test_device_monitor():
    """測試裝置監控功能"""
    print("\n" + "="*60)
    print("測試 2: 裝置監控功能")
    print("="*60)
    
    monitor = DeviceMonitor()
    
    # 測試心跳檢測
    print("\n1. 測試心跳檢測...")
    status = monitor.check_device_heartbeat("pico_001")
    print(f"✓ 裝置狀態: {status['status']}")
    
    # 測試檢查所有裝置
    print("\n2. 檢查所有裝置...")
    results = monitor.check_all_devices()
    print(f"✓ 檢查了 {len(results)} 個裝置")
    
    # 測試取得警報
    print("\n3. 取得警報記錄...")
    alerts = monitor.get_alerts(limit=5)
    print(f"✓ 找到 {len(alerts)} 筆警報")
    
    # 測試統計資訊
    print("\n4. 取得裝置統計...")
    if results:
        device_id = results[0]['device_id']
        stats = monitor.get_device_statistics(device_id, hours=24)
        print(f"✓ {device_id} 統計: {stats['total_readings']} 筆讀數")
    
    monitor.close()
    print("\n✅ 裝置監控功能測試通過")

def test_dashboard_api():
    """測試儀表板 API"""
    print("\n" + "="*60)
    print("測試 3: 儀表板 API")
    print("="*60)
    
    API_URL = "http://localhost:8001"
    
    # 測試健康檢查
    print("\n1. 測試健康檢查...")
    try:
        response = requests.get(f"{API_URL}/health", timeout=5)
        if response.status_code == 200:
            print("✓ API 服務正常")
        else:
            print("✗ API 服務異常")
            return
    except requests.exceptions.RequestException as e:
        print(f"✗ 無法連接 API: {e}")
        print("請先啟動 API 伺服器: python dashboard_api.py")
        return
    
    # 測試儀表板摘要
    print("\n2. 測試儀表板摘要...")
    response = requests.get(f"{API_URL}/api/dashboard")
    if response.status_code == 200:
        data = response.json()
        print(f"✓ 總裝置: {data['total_devices']}")
        print(f"  線上: {data['online_devices']}")
        print(f"  離線: {data['offline_devices']}")
    
    # 測試裝置列表
    print("\n3. 測試裝置列表...")
    response = requests.get(f"{API_URL}/api/devices")
    if response.status_code == 200:
        data = response.json()
        print(f"✓ 找到 {data['count']} 個裝置")
    
    # 測試裝置比較
    print("\n4. 測試裝置比較...")
    response = requests.get(
        f"{API_URL}/api/comparison",
        params={"device_ids": "pico_001,pico_002", "hours": 24}
    )
    if response.status_code == 200:
        data = response.json()
        print(f"✓ 比較了 {len(data['devices'])} 個裝置")
    
    # 測試統計資訊
    print("\n5. 測試統計資訊...")
    response = requests.get(
        f"{API_URL}/api/statistics",
        params={"hours": 24}
    )
    if response.status_code == 200:
        data = response.json()
        print(f"✓ 取得統計資訊")
    
    # 測試警報記錄
    print("\n6. 測試警報記錄...")
    response = requests.get(f"{API_URL}/api/alerts")
    if response.status_code == 200:
        data = response.json()
        print(f"✓ 找到 {data['count']} 筆警報")
    
    print("\n✅ 儀表板 API 測試通過")

def run_all_tests():
    """執行所有測試"""
    print("\n" + "="*60)
    print("多裝置管理系統 - 完整測試")
    print("="*60)
    
    try:
        # 測試 1: 裝置管理
        test_device_manager()
        
        # 測試 2: 裝置監控
        test_device_monitor()
        
        # 測試 3: 儀表板 API
        test_dashboard_api()
        
        print("\n" + "="*60)
        print("🎉 所有測試通過！")
        print("="*60)
        
    except AssertionError as e:
        print(f"\n❌ 測試失敗: {e}")
    except Exception as e:
        print(f"\n❌ 測試錯誤: {e}")

if __name__ == "__main__":
    run_all_tests()
