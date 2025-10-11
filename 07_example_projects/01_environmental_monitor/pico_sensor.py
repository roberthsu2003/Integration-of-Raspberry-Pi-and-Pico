"""
Pico 環境監測感測器程式
讀取內建溫度感測器並透過 MQTT 發送資料
"""

import network
import time
import machine
import json
from umqtt.simple import MQTTClient

# ===== 配置區域 =====
# WiFi 設定
WIFI_SSID = "your_wifi_ssid"
WIFI_PASSWORD = "your_wifi_password"

# MQTT 設定
MQTT_BROKER = "192.168.1.100"  # 你的 Pi 的 IP 位址
MQTT_PORT = 1883
MQTT_TOPIC = "sensors/environment/temperature"
DEVICE_ID = "pico_env_001"
LOCATION = "classroom_a"

# 監測設定
PUBLISH_INTERVAL = 300  # 發布間隔（秒），預設 5 分鐘
# ==================

# 內建 LED（用於狀態指示）
led = machine.Pin("LED", machine.Pin.OUT)

def connect_wifi():
    """連接到 WiFi 網路"""
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    
    if not wlan.isconnected():
        print(f"正在連接到 WiFi: {WIFI_SSID}")
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)
        
        # 等待連接（最多 30 秒）
        timeout = 30
        while not wlan.isconnected() and timeout > 0:
            led.toggle()
            time.sleep(0.5)
            timeout -= 0.5
        
        if not wlan.isconnected():
            print("WiFi 連接失敗")
            return False
    
    print(f"WiFi 已連接")
    print(f"IP 位址: {wlan.ifconfig()[0]}")
    led.on()
    return True

def read_temperature():
    """
    讀取 Pico 內建溫度感測器
    
    Returns:
        float: 溫度值（攝氏度）
    """
    # Pico 內建溫度感測器連接到 ADC4
    sensor_temp = machine.ADC(4)
    
    # 讀取 ADC 值並轉換為溫度
    # 公式: T = 27 - (ADC_voltage - 0.706) / 0.001721
    reading = sensor_temp.read_u16() * (3.3 / 65535)
    temperature = 27 - (reading - 0.706) / 0.001721
    
    return round(temperature, 2)

def create_message(temperature):
    """
    建立 MQTT 訊息
    
    Args:
        temperature: 溫度值
        
    Returns:
        str: JSON 格式的訊息
    """
    # 取得當前時間戳記（簡化版本）
    timestamp = time.time()
    
    message = {
        "device_id": DEVICE_ID,
        "sensor_type": "temperature",
        "value": temperature,
        "unit": "celsius",
        "timestamp": timestamp,
        "location": LOCATION
    }
    
    return json.dumps(message)

def publish_data(client, temperature):
    """
    發布資料到 MQTT Broker
    
    Args:
        client: MQTT 客戶端
        temperature: 溫度值
        
    Returns:
        bool: 發布是否成功
    """
    try:
        message = create_message(temperature)
        client.publish(MQTT_TOPIC, message)
        print(f"✓ 已發布: {temperature}°C")
        
        # 閃爍 LED 表示發送成功
        led.off()
        time.sleep(0.1)
        led.on()
        
        return True
    except Exception as e:
        print(f"✗ 發布失敗: {e}")
        return False

def main():
    """主程式"""
    print("=" * 40)
    print("環境監測系統 - Pico 感測器")
    print("=" * 40)
    
    # 連接 WiFi
    if not connect_wifi():
        print("無法連接 WiFi，程式結束")
        return
    
    # 建立 MQTT 客戶端
    try:
        client = MQTTClient(
            client_id=DEVICE_ID,
            server=MQTT_BROKER,
            port=MQTT_PORT
        )
        client.connect()
        print(f"已連接到 MQTT Broker: {MQTT_BROKER}")
    except Exception as e:
        print(f"MQTT 連接失敗: {e}")
        return
    
    print(f"發布主題: {MQTT_TOPIC}")
    print(f"發布間隔: {PUBLISH_INTERVAL} 秒")
    print("-" * 40)
    
    # 主迴圈
    try:
        while True:
            # 讀取溫度
            temperature = read_temperature()
            print(f"溫度: {temperature}°C", end=" ")
            
            # 發布資料
            publish_data(client, temperature)
            
            # 等待下次發布
            time.sleep(PUBLISH_INTERVAL)
            
    except KeyboardInterrupt:
        print("\n程式已停止")
    except Exception as e:
        print(f"\n錯誤: {e}")
    finally:
        # 清理資源
        try:
            client.disconnect()
            print("已斷開 MQTT 連接")
        except:
            pass
        led.off()

# 執行主程式
if __name__ == "__main__":
    main()
