"""
Pico 智慧家居控制器
接收 MQTT 控制命令並執行動作（使用 LED 模擬）
"""

import network
import time
import machine
import json
from umqtt.simple import MQTTClient

# ===== 配置 =====
WIFI_SSID = "your_wifi_ssid"
WIFI_PASSWORD = "your_wifi_password"
MQTT_BROKER = "192.168.1.100"
MQTT_PORT = 1883
DEVICE_ID = "pico_001"
SENSOR_TOPIC = f"sensors/environment/temperature"
CONTROL_TOPIC = f"control/{DEVICE_ID}"
# ================

led = machine.Pin("LED", machine.Pin.OUT)

def connect_wifi():
    """連接 WiFi"""
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print(f"連接 WiFi: {WIFI_SSID}")
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)
        while not wlan.isconnected():
            time.sleep(0.5)
    print(f"WiFi 已連接: {wlan.ifconfig()[0]}")
    return True

def read_temperature():
    """讀取溫度"""
    sensor_temp = machine.ADC(4)
    reading = sensor_temp.read_u16() * (3.3 / 65535)
    temperature = 27 - (reading - 0.706) / 0.001721
    return round(temperature, 2)

def execute_action(action):
    """執行控制動作"""
    print(f"執行動作: {action}")
    
    if action == "led_on" or action == "fan_on":
        led.on()
        print("✓ LED 開啟（模擬風扇）")
    elif action == "led_off" or action == "all_off":
        led.off()
        print("✓ LED 關閉")
    elif action == "heater_on":
        # 閃爍模擬加熱器
        for _ in range(3):
            led.on()
            time.sleep(0.2)
            led.off()
            time.sleep(0.2)
        print("✓ LED 閃爍（模擬加熱器）")

def on_message(topic, msg):
    """MQTT 訊息回調"""
    try:
        data = json.loads(msg)
        action = data.get('action')
        if action:
            execute_action(action)
    except Exception as e:
        print(f"處理命令失敗: {e}")

def main():
    """主程式"""
    print("=" * 40)
    print("智慧家居控制器")
    print("=" * 40)
    
    if not connect_wifi():
        return
    
    # 建立 MQTT 客戶端
    client = MQTTClient(DEVICE_ID, MQTT_BROKER, MQTT_PORT)
    client.set_callback(on_message)
    client.connect()
    print(f"已連接到 MQTT: {MQTT_BROKER}")
    
    # 訂閱控制主題
    client.subscribe(CONTROL_TOPIC)
    print(f"已訂閱: {CONTROL_TOPIC}")
    
    last_publish = 0
    
    try:
        while True:
            # 檢查控制命令
            client.check_msg()
            
            # 每 30 秒發布感測器資料
            if time.time() - last_publish > 30:
                temp = read_temperature()
                message = json.dumps({
                    "device_id": DEVICE_ID,
                    "sensor_type": "temperature",
                    "value": temp,
                    "timestamp": time.time()
                })
                client.publish(SENSOR_TOPIC, message)
                print(f"已發布溫度: {temp}°C")
                last_publish = time.time()
            
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        print("\n程式已停止")
    finally:
        client.disconnect()
        led.off()

if __name__ == "__main__":
    main()
