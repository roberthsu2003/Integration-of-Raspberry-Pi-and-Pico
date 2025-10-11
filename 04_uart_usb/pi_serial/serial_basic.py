"""
基本串列通訊範例
Pi 端的串列通訊程式

功能：
- 接收 Pico 發送的訊息
- 發送回應訊息
"""

import serial
import time

class SerialCommunication:
    """
    串列通訊類別
    """
    
    def __init__(self, port='/dev/ttyACM0', baudrate=9600, timeout=1):
        """
        初始化串列通訊
        
        參數:
            port: 串列埠
            baudrate: 鮑率
            timeout: 讀取逾時（秒）
        """
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.ser = None
    
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
                timeout=self.timeout
            )
            print(f"✓ 已開啟串列埠: {self.port}")
            print(f"  鮑率: {self.baudrate}")
            return True
        except Exception as e:
            print(f"✗ 開啟串列埠失敗: {e}")
            return False
    
    def close_port(self):
        """關閉串列埠"""
        if self.ser and self.ser.is_open:
            self.ser.close()
            print("串列埠已關閉")
    
    def send_data(self, data):
        """
        發送資料
        
        參數:
            data: 要發送的資料（字串）
        
        返回:
            bool: 是否成功
        """
        try:
            if isinstance(data, str):
                data = data.encode('utf-8')
            
            self.ser.write(data + b'\n')
            print(f"發送: {data.decode('utf-8')}")
            return True
        except Exception as e:
            print(f"✗ 發送失敗: {e}")
            return False
    
    def receive_data(self):
        """
        接收資料
        
        返回:
            str: 接收到的資料，如果沒有則返回 None
        """
        try:
            if self.ser.in_waiting > 0:
                data = self.ser.readline()
                message = data.decode('utf-8').strip()
                return message
        except Exception as e:
            print(f"✗ 接收失敗: {e}")
        
        return None
    
    def run(self):
        """執行通訊迴圈"""
        if not self.open_port():
            return
        
        print("\n開始通訊...")
        print("按 Ctrl+C 停止")
        print("-" * 50)
        print()
        
        try:
            while True:
                # 接收訊息
                message = self.receive_data()
                if message:
                    print(f"接收: {message}")
                    
                    # 發送回應
                    response = f"Echo: {message}"
                    self.send_data(response)
                
                time.sleep(0.1)
        
        except KeyboardInterrupt:
            print("\n\n程式已停止")
        
        finally:
            self.close_port()

# 主程式
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='串列通訊程式')
    parser.add_argument('--port', default='/dev/ttyACM0', help='串列埠')
    parser.add_argument('--baudrate', type=int, default=9600, help='鮑率')
    
    args = parser.parse_args()
    
    print("=" * 50)
    print("串列通訊程式")
    print("=" * 50)
    
    comm = SerialCommunication(args.port, args.baudrate)
    comm.run()
