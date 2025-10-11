"""
MQTT 訂閱者模組
"""

import json
import threading
import paho.mqtt.client as mqtt
from typing import Callable, List

class MQTTSubscriber:
    """MQTT 訂閱者類別"""
    
    def __init__(self, broker: str, port: int, topics: List[str], on_message_callback: Callable):
        """
        初始化 MQTT 訂閱者
        
        Args:
            broker: MQTT Broker 位址
            port: MQTT Broker 埠號
            topics: 要訂閱的主題列表
            on_message_callback: 收到訊息時的回調函式
        """
        self.broker = broker
        self.port = port
        self.topics = topics
        self.on_message_callback = on_message_callback
        self.client = None
        self.is_connected = False
        self.thread = None
    
    def on_connect(self, client, userdata, flags, rc):
        """連接成功時的回調"""
        if rc == 0:
            print(f"✓ MQTT 已連接到 {self.broker}:{self.port}")
            self.is_connected = True
            
            # 訂閱所有主題
            for topic in self.topics:
                client.subscribe(topic)
                print(f"✓ 已訂閱主題: {topic}")
        else:
            print(f"✗ MQTT 連接失敗，錯誤碼: {rc}")
            self.is_connected = False
    
    def on_disconnect(self, client, userdata, rc):
        """斷線時的回調"""
        self.is_connected = False
        if rc != 0:
            print(f"✗ MQTT 意外斷線，錯誤碼: {rc}")
        else:
            print("MQTT 已斷線")
    
    def on_message(self, client, userdata, msg):
        """收到訊息時的回調"""
        try:
            # 解析 JSON 訊息
            payload = json.loads(msg.payload.decode())
            
            # 呼叫使用者定義的回調函式
            self.on_message_callback(msg.topic, payload)
            
        except json.JSONDecodeError as e:
            print(f"✗ JSON 解析失敗: {e}")
            print(f"原始訊息: {msg.payload}")
        except Exception as e:
            print(f"✗ 處理訊息時發生錯誤: {e}")
    
    def start(self):
        """啟動 MQTT 訂閱者"""
        try:
            # 建立 MQTT 客戶端
            self.client = mqtt.Client()
            self.client.on_connect = self.on_connect
            self.client.on_disconnect = self.on_disconnect
            self.client.on_message = self.on_message
            
            # 連接到 Broker
            self.client.connect(self.broker, self.port, 60)
            
            # 在背景執行緒中啟動訊息迴圈
            self.thread = threading.Thread(target=self.client.loop_forever, daemon=True)
            self.thread.start()
            
            print("MQTT 訂閱者已啟動")
            
        except Exception as e:
            print(f"✗ 啟動 MQTT 訂閱者失敗: {e}")
            raise
    
    def stop(self):
        """停止 MQTT 訂閱者"""
        if self.client:
            self.client.disconnect()
            self.client.loop_stop()
            print("MQTT 訂閱者已停止")
