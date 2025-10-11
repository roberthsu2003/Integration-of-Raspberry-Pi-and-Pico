"""
資料格式化程式
將感測器資料格式化為 JSON 格式，準備傳送到其他系統

這個程式示範如何準備資料以便後續的網路傳輸
"""

import machine
import time
import json

class DataFormatter:
    """
    資料格式化器
    
    功能：
    - 讀取感測器資料
    - 格式化為標準 JSON 格式
    - 加入時間戳記和裝置資訊
    """
    
    def __init__(self, device_id="pico_001"):
        """
        初始化格式化器
        
        參數:
            device_id: 裝置識別碼
        """
        self.device_id = device_id
        self.sensor = machine.ADC(4)
        
        # 取得 Pico 的唯一 ID
        import ubinascii
        self.unique_id = ubinascii.hexlify(machine.unique_id()).decode()
    
    def read_temperature(self):
        """讀取溫度"""
        adc_value = self.sensor.read_u16()
        voltage = adc_value * (3.3 / 65535)
        temperature = 27 - (voltage - 0.706) / 0.001721
        return temperature
    
    def get_timestamp(self):
        """
        取得時間戳記
        注意：Pico 沒有 RTC（即時時鐘），這裡使用開機後的秒數
        在實際應用中，應該從網路時間伺服器同步時間
        """
        return time.time()
    
    def format_sensor_data(self):
        """
        格式化感測器資料為標準格式
        
        返回:
            dict: 格式化的資料字典
        """
        temperature = self.read_temperature()
        
        data = {
            "device_id": self.device_id,
            "unique_id": self.unique_id,
            "device_type": "pico_w",
            "timestamp": self.get_timestamp(),
            "sensor_type": "temperature",
            "value": round(temperature, 2),
            "unit": "celsius"
        }
        
        return data
    
    def get_json_string(self):
        """
        取得 JSON 格式的字串
        
        返回:
            str: JSON 格式的資料字串
        """
        data = self.format_sensor_data()
        return json.dumps(data)
    
    def print_formatted_data(self):
        """以易讀的格式顯示資料"""
        data = self.format_sensor_data()
        
        print("=" * 50)
        print(f"裝置 ID: {data['device_id']}")
        print(f"唯一 ID: {data['unique_id']}")
        print(f"感測器類型: {data['sensor_type']}")
        print(f"溫度: {data['value']} {data['unit']}")
        print(f"時間戳記: {data['timestamp']}")
        print("=" * 50)
        
        # 也顯示 JSON 格式
        print("JSON 格式:")
        print(self.get_json_string())
        print()

# 示範使用
if __name__ == "__main__":
    print("資料格式化器示範")
    print("按 Ctrl+C 停止程式")
    print()
    
    # 建立格式化器（可以自訂裝置 ID）
    formatter = DataFormatter(device_id="pico_classroom_01")
    
    try:
        count = 0
        while True:
            count += 1
            print(f"\n第 {count} 次讀取:")
            
            # 顯示格式化的資料
            formatter.print_formatted_data()
            
            # 等待 3 秒
            time.sleep(3)
    
    except KeyboardInterrupt:
        print("\n程式已停止")
