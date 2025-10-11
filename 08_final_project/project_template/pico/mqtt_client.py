"""
MQTT 客戶端模組
處理與 MQTT Broker 的連接和訊息發布
"""

import json
from umqtt.simple import MQTTClient as UMQTTClient

class MQTTClient:
    """MQTT 客戶端類別"""
    
    def __init__(self, client_id, broker, port=1883):
        """
        初始化 MQTT 客戶端
        
        Args:
            client_id: 客戶端 ID
            broker: MQTT Broker 位址
            port: MQTT Broker 埠號
        """
        self.client_id = client_id
        self.broker = broker
        self.port = port
        self.client = None
    
    def connect(self):
        """連接到 MQTT Broker"""
        try:
            self.client = UMQTTClient(
                self.client_id,
                self.broker,
                port=self.port
            )
            self.client.connect()
            print(f"已連接到 MQTT Broker: {self.broker}:{self.port}")
            return True
        except Exception as e:
            print(f"MQTT 連接失敗: {e}")
            raise
    
    def publish(self, topic, message):
        """
        發布訊息到指定主題
        
        Args:
            topic: MQTT 主題
            message: 訊息內容（dict 會自動轉為 JSON）
        """
        try:
            # 如果訊息是字典，轉換為 JSON
            if isinstance(message, dict):
                message = json.dumps(message)
            
            # 發布訊息
            self.client.publish(topic, message)
            print(f"已發布到 {topic}: {message}")
            return True
        except Exception as e:
            print(f"發布訊息失敗: {e}")
            return False
    
    def disconnect(self):
        """斷開 MQTT 連接"""
        if self.client:
            try:
                self.client.disconnect()
                print("MQTT 已斷線")
            except Exception as e:
                print(f"斷線時發生錯誤: {e}")
