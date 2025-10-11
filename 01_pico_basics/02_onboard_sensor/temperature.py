"""
讀取 Pico 內建溫度感測器
Pico 內建一個溫度感測器，可以測量晶片溫度

硬體：Raspberry Pi Pico / Pico W
功能：讀取並顯示晶片溫度
"""

import machine
import time

# 初始化 ADC（類比數位轉換器）
# ADC 4 連接到內建溫度感測器
sensor_temp = machine.ADC(4)

def read_temperature():
    """
    讀取溫度感測器並轉換為攝氏溫度
    
    返回:
        float: 溫度值（攝氏）
    """
    # 讀取 ADC 原始值（0-65535）
    adc_value = sensor_temp.read_u16()
    
    # 轉換為電壓（0-3.3V）
    voltage = adc_value * (3.3 / 65535)
    
    # 根據 Pico 資料手冊的公式轉換為溫度
    # T = 27 - (ADC_voltage - 0.706) / 0.001721
    temperature = 27 - (voltage - 0.706) / 0.001721
    
    return temperature

# 主程式
print("Pico 溫度感測器讀取程式")
print("按 Ctrl+C 停止程式")
print()

try:
    while True:
        # 讀取溫度
        temp = read_temperature()
        
        # 顯示溫度（保留 2 位小數）
        print(f"晶片溫度: {temp:.2f}°C")
        
        # 每 2 秒讀取一次
        time.sleep(2)

except KeyboardInterrupt:
    print("\n程式已停止")
