"""
UART 感測器資料傳輸
透過 UART 發送感測器資料到 Pi

功能：
- 讀取溫度感測器
- 格式化為 JSON
- 透過 UART 發送
"""

import machine
import time
import json

class UARTSensor:
    """
    UART 感測器類別
    
    整合感測器讀取和 UART 傳輸
    """
    
    def __init__(self, uart_id=0, baudrate=9600, tx_pin=0, rx_pin=1):
        """
        初始化 UART 感測器
        
        參數:
            uart_id: UART ID（0 或 1）
            baudrate: 鮑率
            tx_pin: TX 腳位
            rx_pin: RX 腳位
        """
        # 初始化 UART
        self.uart = machine.UART(
            uart_id,
            baudrate=baudrate,
            tx=machine.Pin(tx_pin),
            rx=machine.Pin(rx_pin)
        )
        
        # 初始化溫度感測器
        self.sensor = machine.ADC(4)
        
        # 裝置資訊
        self.device_id = "pico_uart_001"
        
        # 統計資訊
        self.send_count = 0
    
    def read_temperature(self):
        """
        讀取溫度
        
        返回:
            float: 溫度值（攝氏）
        """
        adc_value = self.sensor.read_u16()
        voltage = adc_value * (3.3 / 65535)
        temperature = 27 - (voltage - 0.706) / 0.001721
        return temperature
    
    def format_data(self, temperature):
        """
        格式化感測器資料
        
        參數:
            temperature: 溫度值
        
        返回:
            dict: 格式化的資料
        """
        data = {
            "device_id": self.device_id,
            "sensor_type": "temperature",
            "value": round(temperature, 2),
            "unit": "celsius",
            "timestamp": time.time()
        }
        return data
    
    def send_data(self, data):
        """
        發送資料
        
        參數:
            data: 資料字典
        
        返回:
            bool: 發送是否成功
        """
        try:
            # 轉換為 JSON 字串
            json_str = json.dumps(data)
            
            # 加入換行符號（作為訊息結束標記）
            message = json_str + '\n'
            
            # 發送
            self.uart.write(message)
            
            self.send_count += 1
            return True
        
        except Exception as e:
            print(f"發送失敗: {e}")
            return False
    
    def send_sensor_data(self):
        """
        讀取並發送感測器資料
        
        返回:
            bool: 是否成功
        """
        # 讀取溫度
        temperature = self.read_temperature()
        
        # 格式化資料
        data = self.format_data(temperature)
        
        # 發送資料
        success = self.send_data(data)
        
        if success:
            print(f"[{self.send_count}] 溫度: {temperature:.2f}°C")
        
        return success
    
    def receive_command(self):
        """
        接收命令
        
        返回:
            dict: 命令字典，如果沒有則返回 None
        """
        if self.uart.any():
            try:
                data = self.uart.read()
                if data:
                    message = data.decode('utf-8').strip()
                    command = json.loads(message)
                    print(f"收到命令: {command}")
                    return command
            except Exception as e:
                print(f"接收命令失敗: {e}")
        
        return None
    
    def run(self, interval=5):
        """
        執行主迴圈
        
        參數:
            interval: 發送間隔（秒）
        """
        print("=" * 50)
        print("UART 感測器資料傳輸")
        print("=" * 50)
        print(f"裝置 ID: {self.device_id}")
        print(f"發送間隔: {interval} 秒")
        print("按 Ctrl+C 停止")
        print("=" * 50)
        print()
        
        try:
            while True:
                # 發送感測器資料
                self.send_sensor_data()
                
                # 檢查是否有命令
                command = self.receive_command()
                if command:
                    # 處理命令（可以擴展）
                    pass
                
                # 等待下次發送
                time.sleep(interval)
        
        except KeyboardInterrupt:
            print(f"\n程式已停止，總共發送 {self.send_count} 次")

# 主程式
if __name__ == "__main__":
    # 建立 UART 感測器
    sensor = UARTSensor(
        uart_id=0,
        baudrate=9600,
        tx_pin=0,
        rx_pin=1
    )
    
    # 執行
    sensor.run(interval=5)
