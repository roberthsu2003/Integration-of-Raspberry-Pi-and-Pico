"""
串列資料接收器
接收 Pico 發送的感測器資料並儲存到資料庫

功能：
- 接收 JSON 格式的感測器資料
- 驗證資料格式
- 儲存到資料庫（選用）
- 統計資訊
"""

import serial
import json
import time
from datetime import datetime
import sys
import os

# 加入資料庫模組路徑
sys.path.append(os.path.join(os.path.dirname(__file__), '../../02_pi_basics/fastapi_app'))

try:
    from database import DatabaseManager
    DB_AVAILABLE = True
except ImportError:
    print("警告：無法匯入 DatabaseManager")
    DB_AVAILABLE = False

class SerialReceiver:
    """
    串列資料接收器類別
    """
    
    def __init__(
        self,
        port='/dev/ttyACM0',
        baudrate=9600,
        use_database=True
    ):
        """
        初始化接收器
        
        參數:
            port: 串列埠
            baudrate: 鮑率
            use_database: 是否使用資料庫
        """
        self.port = port
        self.baudrate = baudrate
        self.ser = None
        
        # 初始化資料庫
        self.db = None
        if use_database and DB_AVAILABLE:
            try:
                self.db = DatabaseManager()
                print("✓ 資料庫連接成功")
            except Exception as e:
                print(f"✗ 資料庫連接失敗: {e}")
        
        # 統計資訊
        self.receive_count = 0
        self.save_count = 0
        self.error_count = 0
    
    def open_port(self):
        """
        開啟串列埠
        
        返回:
            bool: 是否成功
        """
        try:
            self.ser = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                timeout=1
            )
            print(f"✓ 已開啟串列埠: {self.port}")
            return True
        except Exception as e:
            print(f"✗ 開啟串列埠失敗: {e}")
            return False
    
    def close_port(self):
        """關閉串列埠"""
        if self.ser and self.ser.is_open:
            self.ser.close()
            print("串列埠已關閉")
    
    def validate_data(self, data):
        """
        驗證資料格式
        
        參數:
            data: 資料字典
        
        返回:
            bool: 資料是否有效
        """
        required_fields = ['device_id', 'sensor_type', 'value', 'unit']
        
        for field in required_fields:
            if field not in data:
                print(f"✗ 缺少必填欄位: {field}")
                return False
        
        return True
    
    def save_to_database(self, data):
        """
        儲存資料到資料庫
        
        參數:
            data: 感測器資料
        
        返回:
            bool: 是否成功
        """
        if self.db is None:
            return False
        
        try:
            # 確保有時間戳記
            if 'timestamp' not in data:
                data['timestamp'] = datetime.now()
            elif isinstance(data['timestamp'], (int, float)):
                data['timestamp'] = datetime.fromtimestamp(data['timestamp'])
            
            # 儲存到資料庫
            result_id = self.db.insert_sensor_data(data)
            
            if result_id:
                self.save_count += 1
                return True
            else:
                self.error_count += 1
                return False
        
        except Exception as e:
            print(f"✗ 儲存失敗: {e}")
            self.error_count += 1
            return False
    
    def process_message(self, message):
        """
        處理接收到的訊息
        
        參數:
            message: 訊息字串
        
        返回:
            bool: 處理是否成功
        """
        try:
            self.receive_count += 1
            
            # 解析 JSON
            data = json.loads(message)
            
            # 驗證資料
            if not self.validate_data(data):
                self.error_count += 1
                return False
            
            # 顯示資料
            self.print_data(data)
            
            # 儲存到資料庫
            if self.db:
                self.save_to_database(data)
            
            return True
        
        except json.JSONDecodeError as e:
            print(f"✗ JSON 解析失敗: {e}")
            self.error_count += 1
            return False
        
        except Exception as e:
            print(f"✗ 處理訊息失敗: {e}")
            self.error_count += 1
            return False
    
    def print_data(self, data):
        """
        顯示資料
        
        參數:
            data: 資料字典
        """
        print("\n" + "-" * 50)
        print(f"📨 收到資料 [{self.receive_count}]")
        print(f"裝置: {data.get('device_id')}")
        print(f"類型: {data.get('sensor_type')}")
        print(f"數值: {data.get('value')} {data.get('unit')}")
        if 'timestamp' in data:
            print(f"時間: {data.get('timestamp')}")
        print("-" * 50)
    
    def print_statistics(self):
        """列印統計資訊"""
        print("\n" + "=" * 50)
        print("統計資訊")
        print("=" * 50)
        print(f"接收訊息: {self.receive_count} 則")
        print(f"成功儲存: {self.save_count} 則")
        print(f"發生錯誤: {self.error_count} 次")
        
        if self.receive_count > 0:
            success_rate = (self.save_count / self.receive_count) * 100
            print(f"成功率: {success_rate:.1f}%")
        
        print("=" * 50)
    
    def run(self):
        """執行接收器"""
        print("=" * 50)
        print("串列資料接收器")
        print("=" * 50)
        print(f"串列埠: {self.port}")
        print(f"鮑率: {self.baudrate}")
        print(f"資料庫: {'啟用' if self.db else '停用'}")
        print("=" * 50)
        print()
        
        if not self.open_port():
            return
        
        print("開始接收資料...")
        print("按 Ctrl+C 停止")
        print()
        
        try:
            while True:
                if self.ser.in_waiting > 0:
                    # 讀取一行
                    line = self.ser.readline()
                    message = line.decode('utf-8').strip()
                    
                    if message:
                        self.process_message(message)
                
                time.sleep(0.01)
        
        except KeyboardInterrupt:
            print("\n\n程式已停止")
            self.print_statistics()
        
        finally:
            self.close_port()
            if self.db:
                self.db.close()

# 主程式
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='串列資料接收器')
    parser.add_argument('--port', default='/dev/ttyACM0', help='串列埠')
    parser.add_argument('--baudrate', type=int, default=9600, help='鮑率')
    parser.add_argument('--no-db', action='store_true', help='不使用資料庫')
    
    args = parser.parse_args()
    
    receiver = SerialReceiver(
        port=args.port,
        baudrate=args.baudrate,
        use_database=not args.no_db
    )
    
    receiver.run()
