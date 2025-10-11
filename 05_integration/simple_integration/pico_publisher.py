# Pico 簡單整合範例 - MQTT 發布者
# 這個範例展示如何從 Pico 讀取感測器資料並透過 MQTT 發布到 Pi

import network
import time
from umqtt.simple import MQTTClient
import machine
import json

# ============ 配置參數 ============
WIFI_SSID = "your_wifi_ssid"        # 請修改為你的 WiFi 名稱
WIFI_PASSWORD = "your_wifi_password"  # 請修改為你的 WiFi 密碼
MQTT_BROKER = "192.168.1.100"       # 請修改為你的 Pi IP 位址
MQTT_PORT = 1883
DEVICE_ID = "pico_001"
PUBLISH_INTERVAL = 5  # 發布間隔（秒）

# ============ WiFi 連接函式 ============
def connect_wifi():
    """連接到 WiFi 網路"""
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    
    if not wlan.isconnected():
        print(f"正在連接到 WiFi: {WIFI_SSID}...")
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)
        
        # 等待連接，最多 10 秒
        timeout = 10
        while not wlan.isconnected() and timeout > 0:
            time.sleep(1)
            timeout -= 1
            print(".", end="")
        
        print()
    
    if wlan.isconnected():
        print(f"WiFi 連接成功！IP: {wlan.ifconfig()[0]}")
        return True
    else:
        print("WiFi 連接失敗！")
        return False

# ============ 感測器讀取函式 ============
def read_temperature():
    """讀取 Pico 內建溫度感測器"""
    sensor = machine.ADC(4)  # ADC4 是內建溫度感測器
    reading = sensor.read_u16()
    
    # 轉換為溫度（攝氏）
    voltage = reading * 3.3 / 65535
    temperature = 27 - (voltage - 0.706) / 0.001721
    
    return round(temperature, 2)

# ============ MQTT 發布函式 ============
def publish_sensor_data(client):
    """讀取感測器並發布資料"""
    try:
        # 讀取溫度
        temperature = read_temperature()
        
        # 建立資料 payload
        data = {
            "device_id": DEVICE_ID,
            "device_type": "pico_w",
            "sensor_type": "temperature",
            "value": temperature,
            "unit": "celsius",
            "timestamp": time.time()
        }
        
        # 轉換為 JSON 字串
        payload = json.dumps(data)
        
        # 發布到 MQTT
        topic = f"sensors/{DEVICE_ID}/temperature"
        client.publish(topic, payload)
        
        print(f"[{time.time()}] 已發布: {temperature}°C")
        return True
        
    except Exception as e:
        print(f"發布資料時發生錯誤: {e}")
        return False

# ============ 主程式 ============
def main():
    """主程式流程"""
    print("=" * 50)
    print("Pico 簡單整合範例 - MQTT 發布者")
    print("=" * 50)
    
    # 1. 連接 WiFi
    if not connect_wifi():
        print("無法連接 WiFi，程式結束")
        return
    
    # 2. 連接 MQTT Broker
    print(f"\n正在連接到 MQTT Broker: {MQTT_BROKER}:{MQTT_PORT}...")
    try:
        client = MQTTClient(
            client_id=DEVICE_ID,
            server=MQTT_BROKER,
            port=MQTT_PORT,
            keepalive=60
        )
        client.connect()
        print("MQTT 連接成功！")
    except Exception as e:
        print(f"MQTT 連接失敗: {e}")
        return
    
    # 3. 開始發布資料
    print(f"\n開始發布感測器資料（每 {PUBLISH_INTERVAL} 秒）...")
    print("按 Ctrl+C 停止\n")
    
    try:
        while True:
            # 發布資料
            publish_sensor_data(client)
            
            # 等待下次發布
            time.sleep(PUBLISH_INTERVAL)
            
    except KeyboardInterrupt:
        print("\n\n程式已停止")
    finally:
        # 斷開連接
        try:
            client.disconnect()
            print("MQTT 連接已關閉")
        except:
            pass

# ============ 執行主程式 ============
if __name__ == "__main__":
    main()
