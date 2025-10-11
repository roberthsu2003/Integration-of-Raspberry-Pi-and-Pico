"""
API 測試腳本
測試 FastAPI 端點的功能

使用方法：
    python test_api.py
"""

import requests
import json
from datetime import datetime

# API 基礎 URL
BASE_URL = "http://localhost:8000"

def print_section(title):
    """列印區段標題"""
    print("\n" + "=" * 60)
    print(f" {title}")
    print("=" * 60)

def test_health_check():
    """測試健康檢查端點"""
    print_section("測試健康檢查")
    
    try:
        response = requests.get(f"{BASE_URL}/api/health")
        print(f"狀態碼: {response.status_code}")
        print(f"回應: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        return response.status_code == 200
    except Exception as e:
        print(f"✗ 測試失敗: {e}")
        return False

def test_create_sensor_data():
    """測試建立感測器資料"""
    print_section("測試建立感測器資料")
    
    # 測試資料
    test_data = {
        "device_id": "pico_test_001",
        "device_type": "pico_w",
        "sensor_type": "temperature",
        "value": 25.5,
        "unit": "celsius",
        "location": "test_lab"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/data",
            json=test_data
        )
        print(f"狀態碼: {response.status_code}")
        print(f"回應: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        return response.status_code == 201
    except Exception as e:
        print(f"✗ 測試失敗: {e}")
        return False

def test_get_all_data():
    """測試查詢所有資料"""
    print_section("測試查詢所有資料")
    
    try:
        response = requests.get(f"{BASE_URL}/api/data?limit=5")
        print(f"狀態碼: {response.status_code}")
        
        data = response.json()
        print(f"狀態: {data['status']}")
        print(f"訊息: {data['message']}")
        print(f"資料筆數: {data.get('count', 0)}")
        
        if data.get('data'):
            print("\n前 5 筆資料:")
            for i, item in enumerate(data['data'][:5], 1):
                print(f"\n  {i}. 裝置: {item.get('device_id')}")
                print(f"     類型: {item.get('sensor_type')}")
                print(f"     數值: {item.get('value')} {item.get('unit')}")
                print(f"     時間: {item.get('timestamp')}")
        
        return response.status_code == 200
    except Exception as e:
        print(f"✗ 測試失敗: {e}")
        return False

def test_get_device_data():
    """測試查詢特定裝置資料"""
    print_section("測試查詢特定裝置資料")
    
    device_id = "pico_test_001"
    
    try:
        response = requests.get(f"{BASE_URL}/api/data/{device_id}?limit=3")
        print(f"狀態碼: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"狀態: {data['status']}")
            print(f"訊息: {data['message']}")
            print(f"資料筆數: {data.get('count', 0)}")
        elif response.status_code == 404:
            print(f"裝置 {device_id} 沒有資料")
        else:
            print(f"回應: {response.json()}")
        
        return response.status_code in [200, 404]
    except Exception as e:
        print(f"✗ 測試失敗: {e}")
        return False

def test_get_devices():
    """測試查詢所有裝置"""
    print_section("測試查詢所有裝置")
    
    try:
        response = requests.get(f"{BASE_URL}/api/devices")
        print(f"狀態碼: {response.status_code}")
        
        data = response.json()
        print(f"狀態: {data['status']}")
        print(f"訊息: {data['message']}")
        print(f"裝置數量: {data.get('count', 0)}")
        
        if data.get('data'):
            print("\n裝置列表:")
            for i, device in enumerate(data['data'], 1):
                print(f"\n  {i}. ID: {device.get('device_id')}")
                print(f"     名稱: {device.get('device_name')}")
                print(f"     類型: {device.get('device_type')}")
                print(f"     位置: {device.get('location')}")
                print(f"     狀態: {device.get('status')}")
        
        return response.status_code == 200
    except Exception as e:
        print(f"✗ 測試失敗: {e}")
        return False

def test_filter_data():
    """測試資料篩選"""
    print_section("測試資料篩選")
    
    try:
        # 測試按裝置 ID 篩選
        response = requests.get(
            f"{BASE_URL}/api/data",
            params={
                "device_id": "pico_001",
                "limit": 3
            }
        )
        print(f"狀態碼: {response.status_code}")
        
        data = response.json()
        print(f"篩選條件: device_id=pico_001")
        print(f"資料筆數: {data.get('count', 0)}")
        
        return response.status_code == 200
    except Exception as e:
        print(f"✗ 測試失敗: {e}")
        return False

def run_all_tests():
    """執行所有測試"""
    print("\n" + "=" * 60)
    print(" FastAPI 測試開始")
    print("=" * 60)
    print(f"\nAPI URL: {BASE_URL}")
    print(f"測試時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    tests = [
        ("健康檢查", test_health_check),
        ("建立感測器資料", test_create_sensor_data),
        ("查詢所有資料", test_get_all_data),
        ("查詢特定裝置資料", test_get_device_data),
        ("查詢所有裝置", test_get_devices),
        ("資料篩選", test_filter_data),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n✗ 測試 '{name}' 發生錯誤: {e}")
            results.append((name, False))
    
    # 顯示測試結果摘要
    print_section("測試結果摘要")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✓ 通過" if result else "✗ 失敗"
        print(f"{status} - {name}")
    
    print(f"\n總計: {passed}/{total} 測試通過")
    
    if passed == total:
        print("\n🎉 所有測試通過！")
    else:
        print(f"\n⚠️  有 {total - passed} 個測試失敗")
    
    print("=" * 60)

if __name__ == "__main__":
    try:
        run_all_tests()
    except KeyboardInterrupt:
        print("\n\n測試已中斷")
    except Exception as e:
        print(f"\n\n測試執行失敗: {e}")
