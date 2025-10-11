"""
專題模板 - Pico 主程式
功能：讀取感測器資料並透過 MQTT 發送到 Pi
"""

import time
import machine
from mqtt_client import MQTTClient
from sensor_reader import SensorReader
import config

# 初始化 LED（用於狀態指示）
led = machine.Pin("LED", machine.Pin.OUT)

# 初始化感測器讀取器
sensor = SensorReader()

# 初始化 MQTT 客戶端
mqtt = MQTTClient(
    client_id=config.DEVICE_ID,
    broker=config.MQTT_BROKER,
    port=config.MQTT_PORT
)

def blink_led(times=1):
    """閃爍 LED 指示狀態"""
    for _ in range(times):
        led.on()
        time.sleep(0.1)
        led.off()
        time.sleep(0.1)

def connect_mqtt():
    """連接到 MQTT Broker"""
    print(f"正在連接到 MQTT Broker: {config.MQTT_BROKER}:{config.MQTT_PORT}")
    try:
        mqtt.connect()
        print("MQTT 連接成功")
        blink_led(3)  # 連接成功閃爍 3 次
        return True
    except Exception as e:
        print(f"MQTT 連接失敗: {e}")
        return False

def publish_sensor_data():
    """讀取感測器資料並發布到 MQTT"""
    try:
        # 讀取感測器資料
        data = sensor.read_all()
        
        # 建立 MQTT 訊息
        topic = f"{config.MQTT_TOPIC_PREFIX}/{config.DEVICE_ID}"
        message = {
            "device_id": config.DEVICE_ID,
            "timestamp": time.time(),
            "data": data
        }
        
        # 發布訊息
        mqtt.publish(topic, message)
        print(f"已發布資料: {message}")
        
        # 閃爍 LED 表示發送成功
        blink_led(1)
        
    except Exception as e:
        print(f"發布資料失敗: {e}")

def main():
    """主程式"""
    print("=" * 50)
    print(f"裝置 ID: {config.DEVICE_ID}")
    print(f"發送間隔: {config.PUBLISH_INTERVAL} 秒")
    print("=" * 50)
    
    # 連接 MQTT
    if not connect_mqtt():
        print("無法連接 MQTT，程式結束")
        return
    
    # 主迴圈
    try:
        while True:
            publish_sensor_data()
            time.sleep(config.PUBLISH_INTERVAL)
            
    except KeyboardInterrupt:
        print("\n程式被使用者中斷")
    except Exception as e:
        print(f"發生錯誤: {e}")
    finally:
        mqtt.disconnect()
        print("MQTT 已斷線")

if __name__ == "__main__":
    main()
