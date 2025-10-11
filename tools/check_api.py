#!/usr/bin/env python3
"""
API 檢查工具
用於驗證 FastAPI 服務的所有端點
"""

import argparse
import sys
import requests
import json
from datetime import datetime
from typing import Dict, List, Tuple


class APIChecker:
    """API 檢查類別"""
    
    def __init__(self, base_url, timeout=10):
        """
        初始化 API 檢查器
        
        Args:
            base_url: API 基礎 URL（例如: http://localhost:8000）
            timeout: 請求逾時時間（秒）
        """
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.results = []
        
    def check_endpoint(self, method, path, data=None, expected_status=200, description=""):
        """
        檢查單一端點
        
        Args:
            method: HTTP 方法（GET, POST, PUT, DELETE）
            path: 端點路徑
            data: 請求資料（用於 POST/PUT）
            expected_status: 預期的 HTTP 狀態碼
            description: 端點描述
        
        Returns:
            (success, message): 測試結果
        """
        url = f"{self.base_url}{path}"
        
        try:
            if method == 'GET':
                response = requests.get(url, timeout=self.timeout)
            elif method == 'POST':
                response = requests.post(url, json=data, timeout=self.timeout)
            elif method == 'PUT':
                response = requests.put(url, json=data, timeout=self.timeout)
            elif method == 'DELETE':
                response = requests.delete(url, timeout=self.timeout)
            else:
                return False, f"不支援的 HTTP 方法: {method}"
            
            success = response.status_code == expected_status
            
            result = {
                'method': method,
                'path': path,
                'description': description,
                'status_code': response.status_code,
                'expected_status': expected_status,
                'success': success,
                'response_time': response.elapsed.total_seconds(),
                'timestamp': datetime.now().isoformat()
            }
            
            if success:
                try:
                    result['response_data'] = response.json()
                except:
                    result['response_data'] = response.text
            else:
                result['error'] = f"狀態碼不符: 預期 {expected_status}, 實際 {response.status_code}"
            
            self.results.append(result)
            return success, result
            
        except requests.exceptions.ConnectionError:
            error_msg = f"無法連接到 {url}"
            self.results.append({
                'method': method,
                'path': path,
                'description': description,
                'success': False,
                'error': error_msg,
                'timestamp': datetime.now().isoformat()
            })
            return False, error_msg
            
        except requests.exceptions.Timeout:
            error_msg = f"請求逾時（{self.timeout}秒）"
            self.results.append({
                'method': method,
                'path': path,
                'description': description,
                'success': False,
                'error': error_msg,
                'timestamp': datetime.now().isoformat()
            })
            return False, error_msg
            
        except Exception as e:
            error_msg = f"請求失敗: {str(e)}"
            self.results.append({
                'method': method,
                'path': path,
                'description': description,
                'success': False,
                'error': error_msg,
                'timestamp': datetime.now().isoformat()
            })
            return False, error_msg
    
    def print_result(self, result):
        """列印單一測試結果"""
        status = "✓" if result['success'] else "✗"
        print(f"\n{status} {result['method']} {result['path']}")
        
        if result['description']:
            print(f"   描述: {result['description']}")
        
        if result['success']:
            print(f"   狀態碼: {result['status_code']}")
            print(f"   回應時間: {result['response_time']:.3f}秒")
            if 'response_data' in result and isinstance(result['response_data'], dict):
                print(f"   回應: {json.dumps(result['response_data'], ensure_ascii=False, indent=2)[:200]}")
        else:
            print(f"   錯誤: {result.get('error', '未知錯誤')}")
    
    def test_basic_endpoints(self):
        """測試基本端點"""
        print(f"\n{'='*60}")
        print(f" 測試基本端點")
        print(f"{'='*60}")
        
        # 測試健康檢查
        success, result = self.check_endpoint(
            'GET', '/api/health',
            description='健康檢查端點'
        )
        self.print_result(result)
        
        # 測試根路徑
        success, result = self.check_endpoint(
            'GET', '/',
            description='根路徑'
        )
        self.print_result(result)
        
        # 測試文件
        success, result = self.check_endpoint(
            'GET', '/docs',
            description='API 文件'
        )
        self.print_result(result)
    
    def test_data_endpoints(self):
        """測試資料端點"""
        print(f"\n{'='*60}")
        print(f" 測試資料端點")
        print(f"{'='*60}")
        
        # 測試發布資料
        test_data = {
            "device_id": "test_device",
            "device_type": "pico_w",
            "timestamp": datetime.now().isoformat(),
            "sensor_type": "temperature",
            "value": 25.5,
            "unit": "celsius",
            "location": "test_location"
        }
        
        success, result = self.check_endpoint(
            'POST', '/api/data',
            data=test_data,
            description='發布感測器資料'
        )
        self.print_result(result)
        
        # 測試查詢所有資料
        success, result = self.check_endpoint(
            'GET', '/api/data',
            description='查詢所有資料'
        )
        self.print_result(result)
        
        # 測試查詢特定裝置
        success, result = self.check_endpoint(
            'GET', '/api/data/test_device',
            description='查詢特定裝置資料'
        )
        self.print_result(result)
    
    def test_error_handling(self):
        """測試錯誤處理"""
        print(f"\n{'='*60}")
        print(f" 測試錯誤處理")
        print(f"{'='*60}")
        
        # 測試不存在的端點
        success, result = self.check_endpoint(
            'GET', '/api/nonexistent',
            expected_status=404,
            description='不存在的端點'
        )
        self.print_result(result)
        
        # 測試無效的資料格式
        invalid_data = {"invalid": "data"}
        success, result = self.check_endpoint(
            'POST', '/api/data',
            data=invalid_data,
            expected_status=422,
            description='無效的資料格式'
        )
        self.print_result(result)
    
    def generate_report(self):
        """生成測試報告"""
        print(f"\n{'='*60}")
        print(f" 測試報告")
        print(f"{'='*60}")
        
        total = len(self.results)
        passed = sum(1 for r in self.results if r['success'])
        failed = total - passed
        
        print(f"\n總測試數: {total}")
        print(f"通過: {passed}")
        print(f"失敗: {failed}")
        print(f"成功率: {(passed/total*100):.1f}%")
        
        if failed > 0:
            print(f"\n失敗的測試:")
            for result in self.results:
                if not result['success']:
                    print(f"  ✗ {result['method']} {result['path']}")
                    print(f"    {result.get('error', '未知錯誤')}")
        
        # 計算平均回應時間
        response_times = [r['response_time'] for r in self.results 
                         if 'response_time' in r]
        if response_times:
            avg_time = sum(response_times) / len(response_times)
            print(f"\n平均回應時間: {avg_time:.3f}秒")
        
        return passed == total
    
    def save_report(self, filename='api_test_report.json'):
        """儲存測試報告到檔案"""
        report = {
            'base_url': self.base_url,
            'timestamp': datetime.now().isoformat(),
            'total_tests': len(self.results),
            'passed': sum(1 for r in self.results if r['success']),
            'failed': sum(1 for r in self.results if not r['success']),
            'results': self.results
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"\n報告已儲存到: {filename}")


def main():
    """主程式"""
    parser = argparse.ArgumentParser(
        description='API 檢查工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
範例:
  # 檢查本地 API
  python check_api.py --url http://localhost:8000
  
  # 完整測試並儲存報告
  python check_api.py --url http://localhost:8000 --full --save
  
  # 只測試基本端點
  python check_api.py --url http://localhost:8000 --basic
        """
    )
    
    parser.add_argument('--url', default='http://localhost:8000',
                        help='API 基礎 URL（預設: http://localhost:8000）')
    parser.add_argument('--timeout', type=int, default=10,
                        help='請求逾時時間（秒，預設: 10）')
    parser.add_argument('--basic', action='store_true',
                        help='只測試基本端點')
    parser.add_argument('--data', action='store_true',
                        help='只測試資料端點')
    parser.add_argument('--error', action='store_true',
                        help='只測試錯誤處理')
    parser.add_argument('--full', action='store_true',
                        help='執行完整測試')
    parser.add_argument('--save', action='store_true',
                        help='儲存測試報告')
    
    args = parser.parse_args()
    
    # 建立檢查器
    checker = APIChecker(args.url, args.timeout)
    
    print(f"{'='*60}")
    print(f" API 檢查工具")
    print(f"{'='*60}")
    print(f"目標 URL: {args.url}")
    print(f"逾時時間: {args.timeout}秒")
    
    # 執行測試
    if args.basic or (not args.data and not args.error and not args.full):
        checker.test_basic_endpoints()
    
    if args.data or args.full:
        checker.test_data_endpoints()
    
    if args.error or args.full:
        checker.test_error_handling()
    
    # 生成報告
    success = checker.generate_report()
    
    # 儲存報告
    if args.save:
        checker.save_report()
    
    # 返回結果
    if success:
        print(f"\n✓ 所有測試通過")
        return 0
    else:
        print(f"\n✗ 部分測試失敗")
        print(f"\n請參考 resources/troubleshooting.md 排除問題")
        return 1


if __name__ == "__main__":
    sys.exit(main())
