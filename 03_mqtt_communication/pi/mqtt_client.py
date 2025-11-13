"""
Pi MQTT 客戶端模組
處理 MQTT 訂閱和訊息接收

功能：
- MQTT 連接管理
- 訂閱主題
- 訊息處理回調
- 自動重連
"""

import paho.mqtt.client as mqtt
import json
import time
from datetime import datetime
from typing import Callable, Dict, List

class PiMQTTClient:
    """
    Pi MQTT 客戶端類別
    
    封裝 MQTT 訂閱和訊息處理功能
    """
    
    def __init__(self, client_id: str, broker: str, port: int = 1883, keepalive: int = 60):
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
        self.client = mqtt.Client(client_id=client_id)
        
        # 設定回調函式
        self.client.on_connect = self._on_connect
        self.client.on_disconnect = self._on_disconnect
        self.client.on_message = self._on_message
        
        # 連接狀態
        self.connected = False
        
        # 訂閱的主題和回調
        self.subscriptions: Dict[str, Callable] = {}
        
        # 統計資訊
        self.message_count = 0
        self.error_count = 0
    
    def _on_connect(self, client, userdata, flags, rc):
        """
        連接回調函式
        
        當連接到 Broker 時被呼叫
        """
        if rc == 0:
            print("✓ MQTT 連接成功")
            self.connected = True
            
            # 重新訂閱所有主題
            for topic in self.subscriptions.keys():
                self.client.subscribe(topic)
                print(f"  訂閱主題: {topic}")
        else:
            print(f"✗ MQTT 連接失敗，錯誤碼: {rc}")
            self.connected = False
    
    def _on_disconnect(self, client, userdata, rc):
        """
        中斷連接回調函式
        
        當與 Broker 中斷連接時被呼叫
        """
        self.connected = False
        if rc != 0:
            print(f"⚠ MQTT 連接意外中斷，錯誤碼: {rc}")
        else:
            print("MQTT 連接已中斷")
    
    def _on_message(self, client, userdata, msg):
        """
        訊息接收回調函式
        
        當收到訊息時被呼叫
        """
        try:
            self.message_count += 1
            
            # 解碼訊息
            topic = msg.topic
            payload = msg.payload.decode('utf-8')
            
            # 嘗試解析 JSON
            try:
                data = json.loads(payload)
            except json.JSONDecodeError:
                data = payload
            
            # 呼叫對應的回調函式
            for pattern, callback in self.subscriptions.items():
                if self._topic_matches(topic, pattern):
                    callback(topic, data)
                    break
        
        except Exception as e:
            print(f"✗ 處理訊息時發生錯誤: {e}")
            self.error_count += 1
    
    def _topic_matches(self, topic: str, pattern: str) -> bool:
        """
        檢查主題是否匹配模式
        
        支援 MQTT 萬用字元：
        - + : 單層萬用字元
        - # : 多層萬用字元
        """
        topic_parts = topic.split('/')
        pattern_parts = pattern.split('/')
        
        # 如果模式以 # 結尾
        if pattern_parts[-1] == '#':
            return topic.startswith('/'.join(pattern_parts[:-1]))
        
        # 檢查每一層
        if len(topic_parts) != len(pattern_parts):
            return False
        
        for t, p in zip(topic_parts, pattern_parts):
            if p != '+' and p != t:
                return False
        
        return True
    
    def connect(self) -> bool:
        """
        連接到 MQTT Broker
        
        返回:
            bool: 連接是否成功
        """
        try:
            print(f"正在連接到 MQTT Broker: {self.broker}:{self.port}")
            self.client.connect(self.broker, self.port, self.keepalive)
            
            # 啟動網路迴圈（背景執行緒）
            self.client.loop_start()
            
            # 等待連接完成
            timeout = 10
            start_time = time.time()
            while not self.connected and (time.time() - start_time) < timeout:
                time.sleep(0.1)
            
            return self.connected
        
        except Exception as e:
            print(f"✗ MQTT 連接失敗: {e}")
            return False
    
    def disconnect(self):
        """中斷 MQTT 連接"""
        try:
            self.client.loop_stop()
            self.client.disconnect()
            self.connected = False
            print("MQTT 連接已中斷")
        except Exception as e:
            print(f"中斷連接時發生錯誤: {e}")
    
    def subscribe(self, topic: str, callback: Callable, qos: int = 0):
        """
        訂閱主題
        
        參數:
            topic: MQTT 主題（支援萬用字元）
            callback: 訊息處理回調函式 callback(topic, data)
            qos: 服務品質等級（0, 1, 2）
        """
        try:
            # 儲存訂閱資訊
            self.subscriptions[topic] = callback
            
            # 如果已連接，立即訂閱
            if self.connected:
                result = self.client.subscribe(topic, qos)
                if result[0] == mqtt.MQTT_ERR_SUCCESS:
                    print(f"✓ 訂閱主題: {topic}")
                else:
                    print(f"✗ 訂閱失敗: {topic}")
        
        except Exception as e:
            print(f"✗ 訂閱主題時發生錯誤: {e}")
    
    def unsubscribe(self, topic: str):
        """
        取消訂閱主題
        
        參數:
            topic: MQTT 主題
        """
        try:
            if topic in self.subscriptions:
                del self.subscriptions[topic]
            
            if self.connected:
                self.client.unsubscribe(topic)
                print(f"✓ 取消訂閱: {topic}")
        
        except Exception as e:
            print(f"✗ 取消訂閱時發生錯誤: {e}")
    
    def publish(self, topic: str, message, qos: int = 0, retain: bool = False) -> bool:
        """
        發布訊息（Pi 也可以發布訊息）
        
        參數:
            topic: MQTT 主題
            message: 訊息內容（字串或字典）
            qos: 服務品質等級
            retain: 是否保留訊息
        
        返回:
            bool: 發布是否成功
        """
        try:
            # 如果訊息是字典，轉換為 JSON
            if isinstance(message, dict):
                message = json.dumps(message)
            
            result = self.client.publish(topic, message, qos, retain)
            
            if result.rc == mqtt.MQTT_ERR_SUCCESS:
                print(f"✓ 發布訊息到 {topic}")
                return True
            else:
                print(f"✗ 發布訊息失敗")
                return False
        
        except Exception as e:
            print(f"✗ 發布訊息時發生錯誤: {e}")
            return False
    
    def get_statistics(self) -> Dict:
        """
        取得統計資訊
        
        返回:
            dict: 統計資訊
        """
        return {
            'connected': self.connected,
            'message_count': self.message_count,
            'error_count': self.error_count,
            'subscriptions': list(self.subscriptions.keys())
        }
    
    def print_statistics(self):
        """列印統計資訊"""
        stats = self.get_statistics()
        print("\n" + "=" * 50)
        print("MQTT 客戶端統計:")
        print(f"  連接狀態: {'已連接' if stats['connected'] else '未連接'}")
        print(f"  接收訊息: {stats['message_count']} 則")
        print(f"  發生錯誤: {stats['error_count']} 次")
        print(f"  訂閱主題: {len(stats['subscriptions'])} 個")
        for topic in stats['subscriptions']:
            print(f"    - {topic}")
        print("=" * 50)

# ============================================================================
# 使用範例
# ============================================================================

if __name__ == "__main__":
    # 訊息處理回調函式
    def on_sensor_data(topic, data):
        """處理感測器資料"""
        print(f"\n收到感測器資料:")
        print(f"  主題: {topic}")
        if isinstance(data, dict):
            print(f"  裝置: {data.get('device_id')}")
            print(f"  類型: {data.get('sensor_type')}")
            print(f"  數值: {data.get('value')} {data.get('unit')}")
        else:
            print(f"  資料: {data}")
    
    # 建立 MQTT 客戶端
    client = PiMQTTClient(
        client_id="pi_subscriber",
        broker="localhost",
        port=1883
    )
    
    # 連接到 Broker
    if client.connect():
        # 訂閱所有感測器主題
        client.subscribe("sensors/#", on_sensor_data)
        
        print("\n等待訊息...")
        print("按 Ctrl+C 停止")
        
        try:
            # 保持運行
            while True:
                time.sleep(1)
        
        except KeyboardInterrupt:
            print("\n\n程式已停止")
            client.print_statistics()
            client.disconnect()
    else:
        print("無法連接到 MQTT Broker")
