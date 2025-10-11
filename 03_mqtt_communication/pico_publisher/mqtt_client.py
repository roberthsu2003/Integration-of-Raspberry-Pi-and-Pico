"""
Pico MQTT 客戶端模組
處理 MQTT 連接和訊息發布

功能：
- MQTT 連接管理
- 訊息發布
- 自動重連
- 錯誤處理
"""

from umqtt.simple import MQTTClient
import time
import json
import machine

class PicoMQTTClient:
    """
    Pico MQTT 客戶端類別
    
    封裝 MQTT 連接和發布功能
    """
    
    def __init__(self, client_id, broker, port=1883, keepalive=60):
        """
        初始化 MQTT 客戶端
        
        參數:
            client_id: 客戶端唯一識別碼
            broker: MQTT Broker 位址
            port: MQTT 連接埠（預設 1883）
            keepalive: 保持連接時間（秒）
        """
        self.client_id = client_id
        self.broker = broker
        self.port = port
        self.keepalive = keepalive
        
        # 建立 MQTT 客戶端
        self.client = MQTTClient(
            client_id=client_id,
            server=broker,
            port=port,
            keepalive=keepalive
        )
        
        # 連接狀態
        self.connected = False
        
        # LED 指示
        self.led = machine.Pin("LED", machine.Pin.OUT)
    
    def connect(self, clean_session=True):
        """
        連接到 MQTT Broker
        
        參數:
            clean_session: 是否清除會話
        
        返回:
            bool: 連接是否成功
        """
        try:
            print(f"正在連接到 MQTT Broker: {self.broker}:{self.port}")
            
            # 連接到 Broker
            self.client.connect(clean_session=clean_session)
            
            self.connected = True
            print("MQTT 連接成功！")
            
            # LED 快閃表示連接成功
            for _ in range(3):
                self.led.on()
                time.sleep(0.1)
                self.led.off()
                time.sleep(0.1)
            
            return True
        
        except Exception as e:
            print(f"MQTT 連接失敗: {e}")
            self.connected = False
            return False
    
    def disconnect(self):
        """中斷 MQTT 連接"""
        try:
            if self.connected:
                self.client.disconnect()
                self.connected = False
                print("MQTT 連接已中斷")
        except Exception as e:
            print(f"中斷連接時發生錯誤: {e}")
    
    def publish(self, topic, message, qos=0, retain=False):
        """
        發布訊息到指定主題
        
        參數:
            topic: MQTT 主題
            message: 訊息內容（字串或字典）
            qos: 服務品質等級（0, 1, 2）
            retain: 是否保留訊息
        
        返回:
            bool: 發布是否成功
        """
        try:
            # 如果訊息是字典，轉換為 JSON 字串
            if isinstance(message, dict):
                message = json.dumps(message)
            
            # 確保訊息是字串
            if not isinstance(message, str):
                message = str(message)
            
            # 發布訊息
            self.client.publish(
                topic=topic,
                msg=message.encode(),
                qos=qos,
                retain=retain
            )
            
            print(f"✓ 發布訊息到 {topic}")
            
            # LED 閃爍表示發布成功
            self.led.on()
            time.sleep(0.05)
            self.led.off()
            
            return True
        
        except Exception as e:
            print(f"✗ 發布訊息失敗: {e}")
            return False
    
    def publish_sensor_data(self, device_id, sensor_type, value, unit, location=None):
        """
        發布感測器資料（便利方法）
        
        參數:
            device_id: 裝置 ID
            sensor_type: 感測器類型
            value: 數值
            unit: 單位
            location: 位置（選用）
        
        返回:
            bool: 發布是否成功
        """
        # 建立資料字典
        data = {
            "device_id": device_id,
            "device_type": "pico_w",
            "sensor_type": sensor_type,
            "value": round(value, 2),
            "unit": unit,
            "timestamp": time.time()
        }
        
        if location:
            data["location"] = location
        
        # 建立主題：sensors/{device_id}/{sensor_type}
        topic = f"sensors/{device_id}/{sensor_type}"
        
        # 發布資料
        return self.publish(topic, data)
    
    def reconnect_if_needed(self):
        """
        如果連接中斷，自動重新連接
        
        返回:
            bool: 是否已連接
        """
        if not self.connected:
            print("偵測到 MQTT 連接中斷，嘗試重新連接...")
            return self.connect()
        return True
    
    def ping(self):
        """
        發送 ping 保持連接
        
        返回:
            bool: ping 是否成功
        """
        try:
            self.client.ping()
            return True
        except Exception as e:
            print(f"Ping 失敗: {e}")
            self.connected = False
            return False
    
    def check_msg(self):
        """
        檢查是否有新訊息（用於訂閱）
        
        注意：此方法用於訂閱者，發布者通常不需要使用
        """
        try:
            self.client.check_msg()
        except Exception as e:
            print(f"檢查訊息時發生錯誤: {e}")

# ============================================================================
# 使用範例
# ============================================================================

if __name__ == "__main__":
    # 匯入配置
    from wifi_config import MQTT_BROKER, MQTT_PORT, MQTT_CLIENT_ID, DEVICE_ID
    from wifi_manager import WiFiManager
    from wifi_config import WIFI_SSID, WIFI_PASSWORD
    
    # 1. 連接 WiFi
    print("步驟 1: 連接 WiFi")
    wifi = WiFiManager(WIFI_SSID, WIFI_PASSWORD)
    
    if not wifi.wait_for_connection():
        print("無法連接到 WiFi，程式結束")
        import sys
        sys.exit(1)
    
    # 2. 建立 MQTT 客戶端
    print("\n步驟 2: 建立 MQTT 客戶端")
    mqtt = PicoMQTTClient(
        client_id=MQTT_CLIENT_ID,
        broker=MQTT_BROKER,
        port=MQTT_PORT
    )
    
    # 3. 連接到 MQTT Broker
    print("\n步驟 3: 連接到 MQTT Broker")
    if not mqtt.connect():
        print("無法連接到 MQTT Broker，程式結束")
        import sys
        sys.exit(1)
    
    # 4. 發布測試訊息
    print("\n步驟 4: 發布測試訊息")
    
    try:
        count = 0
        while True:
            count += 1
            
            # 檢查連接狀態
            wifi.reconnect_if_needed()
            mqtt.reconnect_if_needed()
            
            # 發布測試訊息
            test_data = {
                "device_id": DEVICE_ID,
                "message": f"Test message {count}",
                "timestamp": time.time()
            }
            
            mqtt.publish("test/topic", test_data)
            
            print(f"已發布第 {count} 則訊息")
            
            # 等待 5 秒
            time.sleep(5)
    
    except KeyboardInterrupt:
        print("\n程式已停止")
        mqtt.disconnect()
        wifi.disconnect()
