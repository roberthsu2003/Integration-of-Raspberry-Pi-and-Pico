"""
感測器讀取類別
封裝感測器讀取功能，提供更好的程式結構

這個類別示範物件導向程式設計的基本概念
"""

import machine
import time

class SensorReader:
    """
    感測器讀取器類別
    
    功能：
    - 讀取溫度感測器
    - 提供資料平滑處理
    - 記錄歷史資料
    """
    
    def __init__(self):
        """初始化感測器"""
        # 初始化 ADC 4（內建溫度感測器）
        self.sensor = machine.ADC(4)
        
        # 儲存歷史讀數（用於平滑處理）
        self.history = []
        self.max_history = 5  # 保留最近 5 筆資料
    
    def read_temperature(self):
        """
        讀取當前溫度
        
        返回:
            float: 溫度值（攝氏）
        """
        # 讀取 ADC 值
        adc_value = self.sensor.read_u16()
        
        # 轉換為電壓
        voltage = adc_value * (3.3 / 65535)
        
        # 轉換為溫度
        temperature = 27 - (voltage - 0.706) / 0.001721
        
        # 加入歷史記錄
        self.history.append(temperature)
        
        # 保持歷史記錄在限制內
        if len(self.history) > self.max_history:
            self.history.pop(0)  # 移除最舊的資料
        
        return temperature
    
    def get_average_temperature(self):
        """
        取得平均溫度（使用歷史資料）
        
        返回:
            float: 平均溫度，如果沒有資料則返回 None
        """
        if not self.history:
            return None
        
        return sum(self.history) / len(self.history)
    
    def get_min_temperature(self):
        """取得歷史最低溫度"""
        if not self.history:
            return None
        return min(self.history)
    
    def get_max_temperature(self):
        """取得歷史最高溫度"""
        if not self.history:
            return None
        return max(self.history)
    
    def get_sensor_data(self):
        """
        取得完整的感測器資料
        
        返回:
            dict: 包含當前溫度、平均溫度、最小值、最大值
        """
        current = self.read_temperature()
        
        return {
            'current': current,
            'average': self.get_average_temperature(),
            'min': self.get_min_temperature(),
            'max': self.get_max_temperature(),
            'samples': len(self.history)
        }

# 示範使用
if __name__ == "__main__":
    print("感測器讀取器示範")
    print("按 Ctrl+C 停止程式")
    print()
    
    # 建立感測器讀取器物件
    reader = SensorReader()
    
    try:
        while True:
            # 取得完整資料
            data = reader.get_sensor_data()
            
            # 顯示資料
            print(f"當前溫度: {data['current']:.2f}°C")
            
            if data['average'] is not None:
                print(f"平均溫度: {data['average']:.2f}°C")
                print(f"最低溫度: {data['min']:.2f}°C")
                print(f"最高溫度: {data['max']:.2f}°C")
                print(f"樣本數量: {data['samples']}")
            
            print("-" * 40)
            
            time.sleep(2)
    
    except KeyboardInterrupt:
        print("\n程式已停止")
