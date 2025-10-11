"""
智慧教室監控系統 - Pico 端
功能：監測溫度並控制空調（LED 模擬）
"""

import time
import machine
import json
from umqtt.simple import MQTTClient
import config

# 初始化硬體
led = machine.Pin("LED", machine.Pin.OUT)
ac_led = machine.Pin(15, machine.Pin.OUT)  # GPIO 15 模擬空調
temp_sensor = machine.ADC(4)

# 溫度濾波器
class TempFilter:
    def __init__(self, size=5):
        self.readings = []
        self.size = size
    
    def add(self, value):
        self.readings.append(value)
        if len(self.readings) > self.size:
            self.readings.pop(0)
        return sum(self.readings) / len(self.readings)

temp_filter = TempFilter()

def read_temperature():
    """讀取並濾波溫度"""
    adc = temp_sensor.read_u16()
    voltage = adc * 3.3 / 65535
    temp = 27 - (voltage - 0.706) / 0.001721
    return temp_filter.add(temp)

def control_ac(temp):
    """根據溫度控制空調"""
    if temp > config.TEMP_THRESHOLD:
        ac_led.on()
        return "on"
    else:
        ac_led.off()
        return "off"

# 連接 MQTT
client = MQTTClient(config.DEVICE_ID, config.MQTT_BROKER, config.MQTT_PORT)
client.connect()
print("MQTT 已連接")
led.on()
time.sleep(0.5)
led.off()

# 主迴圈
while True:
    try:
        temp = read_temperature()
        ac_status = control_ac(temp)
        
        data = {
            "device_id": config.DEVICE_ID,
            "timestamp": time.time(),
            "temperature": round(temp, 2),
            "ac_status": ac_status
        }
        
        client.publish(config.MQTT_TOPIC, json.dumps(data))
        print(f"溫度: {temp:.1f}°C, 空調: {ac_status}")
        
        time.sleep(config.INTERVAL)
    except Exception as e:
        print(f"錯誤: {e}")
        time.sleep(5)
