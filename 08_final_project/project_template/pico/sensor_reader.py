"""
感測器讀取模組
根據你的專題需求修改此檔案
"""

import machine
import time

class SensorReader:
    """感測器讀取器類別"""
    
    def __init__(self):
        """初始化感測器"""
        # 初始化內建溫度感測器
        self.temp_sensor = machine.ADC(4)
        
        # 在此初始化其他感測器
        # 例如：self.light_sensor = machine.ADC(26)
    
    def read_temperature(self):
        """
        讀取 Pico 內建溫度感測器
        
        Returns:
            float: 溫度值（攝氏度）
        """
        try:
            # 讀取 ADC 值
            adc_value = self.temp_sensor.read_u16()
            
            # 轉換為電壓
            voltage = adc_value * (3.3 / 65535)
            
            # 轉換為溫度（根據 Pico 規格）
            temperature = 27 - (voltage - 0.706) / 0.001721
            
            return round(temperature, 2)
        except Exception as e:
            print(f"讀取溫度失敗: {e}")
            return None
    
    def read_custom_sensor(self):
        """
        讀取自訂感測器
        請根據你的感測器修改此方法
        
        Returns:
            dict: 感測器資料
        """
        # 範例：讀取類比感測器
        # adc = machine.ADC(26)
        # value = adc.read_u16()
        # return {"raw": value, "voltage": value * 3.3 / 65535}
        
        return {"value": 0}  # 預設值
    
    def read_all(self):
        """
        讀取所有感測器資料
        
        Returns:
            dict: 包含所有感測器資料的字典
        """
        data = {
            "temperature": self.read_temperature(),
            # 在此加入其他感測器讀取
            # "light": self.read_light(),
            # "humidity": self.read_humidity(),
        }
        
        return data

# 測試程式碼
if __name__ == "__main__":
    sensor = SensorReader()
    
    print("感測器測試程式")
    print("=" * 40)
    
    for i in range(5):
        data = sensor.read_all()
        print(f"讀取 {i+1}: {data}")
        time.sleep(2)
