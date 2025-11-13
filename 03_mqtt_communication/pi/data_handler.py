"""
資料處理模組
處理接收到的 MQTT 訊息並儲存到資料庫

功能：
- 訊息驗證
- 資料格式化
- 資料庫儲存
- 錯誤處理
"""

import sys
import os
from datetime import datetime
from typing import Dict, Optional
import json

# 加入 FastAPI 應用程式路徑
sys.path.append(os.path.join(os.path.dirname(__file__), '../../02_pi_basics/fastapi_app'))

try:
    from database import DatabaseManager
except ImportError:
    print("警告：無法匯入 DatabaseManager，資料將不會儲存到資料庫")
    DatabaseManager = None

class DataHandler:
    """
    資料處理器類別
    
    處理 MQTT 訊息並儲存到資料庫
    """
    
    def __init__(self, db_manager: Optional[DatabaseManager] = None):
        """
        初始化資料處理器
        
        參數:
            db_manager: 資料庫管理器實例（選用）
        """
        self.db = db_manager
        
        # 統計資訊
        self.processed_count = 0
        self.saved_count = 0
        self.error_count = 0
        
        # 最近的資料（用於除錯）
        self.recent_data = []
        self.max_recent = 10
    
    def validate_sensor_data(self, data: Dict) -> bool:
        """
        驗證感測器資料格式
        
        參數:
            data: 感測器資料字典
        
        返回:
            bool: 資料是否有效
        """
        required_fields = ['device_id', 'sensor_type', 'value', 'unit']
        
        # 檢查必填欄位
        for field in required_fields:
            if field not in data:
                print(f"✗ 缺少必填欄位: {field}")
                return False
        
        # 檢查數值型別
        if not isinstance(data['value'], (int, float)):
            print(f"✗ 數值型別錯誤: {type(data['value'])}")
            return False
        
        return True
    
    def format_data(self, data: Dict) -> Dict:
        """
        格式化資料
        
        參數:
            data: 原始資料
        
        返回:
            dict: 格式化後的資料
        """
        formatted = data.copy()
        
        # 確保有時間戳記
        if 'timestamp' not in formatted:
            formatted['timestamp'] = datetime.now()
        elif isinstance(formatted['timestamp'], (int, float)):
            # 如果是 Unix 時間戳記，轉換為 datetime
            formatted['timestamp'] = datetime.fromtimestamp(formatted['timestamp'])
        
        # 確保有裝置類型
        if 'device_type' not in formatted:
            formatted['device_type'] = 'unknown'
        
        # 四捨五入數值
        if isinstance(formatted['value'], float):
            formatted['value'] = round(formatted['value'], 2)
        
        return formatted
    
    def save_to_database(self, data: Dict) -> bool:
        """
        儲存資料到資料庫
        
        參數:
            data: 感測器資料
        
        返回:
            bool: 儲存是否成功
        """
        if self.db is None:
            print("⚠ 資料庫未連接，資料未儲存")
            return False
        
        try:
            # 儲存到資料庫
            result_id = self.db.insert_sensor_data(data)
            
            if result_id:
                self.saved_count += 1
                return True
            else:
                self.error_count += 1
                return False
        
        except Exception as e:
            print(f"✗ 儲存資料失敗: {e}")
            self.error_count += 1
            return False
    
    def handle_message(self, topic: str, data: Dict) -> bool:
        """
        處理接收到的訊息
        
        參數:
            topic: MQTT 主題
            data: 訊息資料
        
        返回:
            bool: 處理是否成功
        """
        try:
            self.processed_count += 1
            
            # 如果資料是字串，嘗試解析為 JSON
            if isinstance(data, str):
                try:
                    data = json.loads(data)
                except json.JSONDecodeError:
                    print(f"✗ 無法解析 JSON: {data}")
                    self.error_count += 1
                    return False
            
            # 驗證資料
            if not self.validate_sensor_data(data):
                self.error_count += 1
                return False
            
            # 格式化資料
            formatted_data = self.format_data(data)
            
            # 儲存最近的資料
            self.recent_data.append({
                'topic': topic,
                'data': formatted_data,
                'time': datetime.now()
            })
            if len(self.recent_data) > self.max_recent:
                self.recent_data.pop(0)
            
            # 列印資料
            self.print_data(topic, formatted_data)
            
            # 儲存到資料庫
            if self.db:
                self.save_to_database(formatted_data)
            
            return True
        
        except Exception as e:
            print(f"✗ 處理訊息時發生錯誤: {e}")
            self.error_count += 1
            return False
    
    def print_data(self, topic: str, data: Dict):
        """
        列印資料（格式化輸出）
        
        參數:
            topic: MQTT 主題
            data: 資料字典
        """
        print("\n" + "-" * 50)
        print(f"📨 收到訊息 [{self.processed_count}]")
        print(f"主題: {topic}")
        print(f"裝置: {data.get('device_id')}")
        print(f"類型: {data.get('sensor_type')}")
        print(f"數值: {data.get('value')} {data.get('unit')}")
        if 'location' in data:
            print(f"位置: {data.get('location')}")
        print(f"時間: {data.get('timestamp')}")
        print("-" * 50)
    
    def get_statistics(self) -> Dict:
        """
        取得統計資訊
        
        返回:
            dict: 統計資訊
        """
        return {
            'processed': self.processed_count,
            'saved': self.saved_count,
            'errors': self.error_count,
            'success_rate': (self.saved_count / self.processed_count * 100) if self.processed_count > 0 else 0
        }
    
    def print_statistics(self):
        """列印統計資訊"""
        stats = self.get_statistics()
        print("\n" + "=" * 50)
        print("資料處理統計:")
        print(f"  處理訊息: {stats['processed']} 則")
        print(f"  成功儲存: {stats['saved']} 則")
        print(f"  發生錯誤: {stats['errors']} 次")
        print(f"  成功率: {stats['success_rate']:.1f}%")
        print("=" * 50)
    
    def get_recent_data(self, count: int = 5) -> list:
        """
        取得最近的資料
        
        參數:
            count: 返回資料筆數
        
        返回:
            list: 最近的資料列表
        """
        return self.recent_data[-count:]
    
    def print_recent_data(self, count: int = 5):
        """
        列印最近的資料
        
        參數:
            count: 顯示資料筆數
        """
        recent = self.get_recent_data(count)
        
        print("\n" + "=" * 50)
        print(f"最近 {len(recent)} 筆資料:")
        print("=" * 50)
        
        for i, item in enumerate(recent, 1):
            data = item['data']
            print(f"\n{i}. {item['time'].strftime('%H:%M:%S')}")
            print(f"   主題: {item['topic']}")
            print(f"   裝置: {data.get('device_id')}")
            print(f"   數值: {data.get('value')} {data.get('unit')}")
        
        print("=" * 50)

# ============================================================================
# 使用範例
# ============================================================================

if __name__ == "__main__":
    # 建立資料處理器（不連接資料庫）
    handler = DataHandler()
    
    # 測試資料
    test_data = {
        "device_id": "pico_001",
        "device_type": "pico_w",
        "sensor_type": "temperature",
        "value": 25.5,
        "unit": "celsius",
        "location": "classroom_a"
    }
    
    # 處理測試資料
    handler.handle_message("sensors/pico_001/temperature", test_data)
    
    # 顯示統計
    handler.print_statistics()
