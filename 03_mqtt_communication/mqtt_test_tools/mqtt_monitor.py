"""
MQTT 訊息監控工具
即時監控和顯示 MQTT 訊息

功能：
- 訂閱多個主題
- 即時顯示訊息
- 訊息統計
- 訊息過濾
"""

import paho.mqtt.client as mqtt
import json
import time
from datetime import datetime
import argparse

class MQTTMonitor:
    """
    MQTT 監控器類別
    """
    
    def __init__(self, broker: str, port: int = 1883, topics: list = None):
        """
        初始化監控器
        
        參數:
            broker: MQTT Broker 位址
            port: MQTT 連接埠
            topics: 要監控的主題列表
        """
        self.broker = broker
        self.port = port
        self.topics = topics or ["#"]
        
        # 建立客戶端
        self.client = mqtt.Client(client_id="mqtt_monitor")
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message
        
        # 統計資訊
        self.message_count = 0
        self.topic_stats = {}
        self.start_time = None
    
    def _on_connect(self, client, userdata, flags, rc):
        """連接回調"""
        if rc == 0:
            print("=" * 70)
            print("✓ 已連接到 MQTT Broker")
            print("=" * 70)
            
            # 訂閱主題
            for topic in self.topics:
                client.subscribe(topic)
                print(f"📡 訂閱主題: {topic}")
            
            print("=" * 70)
            print("開始監控訊息...")
            print("按 Ctrl+C 停止")
            print("=" * 70)
            print()
        else:
            print(f"✗ 連接失敗，錯誤碼: {rc}")
    
    def _on_message(self, client, userdata, msg):
        """訊息接收回調"""
        self.message_count += 1
        
        # 更新主題統計
        topic = msg.topic
        if topic not in self.topic_stats:
            self.topic_stats[topic] = 0
        self.topic_stats[topic] += 1
        
        # 解碼訊息
        try:
            payload = msg.payload.decode('utf-8')
            
            # 嘗試解析 JSON
            try:
                data = json.loads(payload)
                payload_str = json.dumps(data, indent=2, ensure_ascii=False)
            except json.JSONDecodeError:
                payload_str = payload
        except Exception as e:
            payload_str = f"<無法解碼: {e}>"
        
        # 顯示訊息
        self._print_message(topic, payload_str)
    
    def _print_message(self, topic: str, payload: str):
        """
        格式化顯示訊息
        
        參數:
            topic: 主題
            payload: 訊息內容
        """
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        print(f"┌─ [{self.message_count}] {timestamp} " + "─" * 40)
        print(f"│ 主題: {topic}")
        print(f"│ 內容:")
        
        # 縮排顯示內容
        for line in payload.split('\n'):
            print(f"│   {line}")
        
        print("└" + "─" * 68)
        print()
    
    def run(self):
        """執行監控器"""
        try:
            self.start_time = time.time()
            
            # 連接到 Broker
            self.client.connect(self.broker, self.port, 60)
            
            # 啟動迴圈
            self.client.loop_forever()
        
        except KeyboardInterrupt:
            print("\n\n監控已停止")
            self._print_statistics()
        
        except Exception as e:
            print(f"\n錯誤: {e}")
        
        finally:
            self.client.disconnect()
    
    def _print_statistics(self):
        """列印統計資訊"""
        duration = time.time() - self.start_time if self.start_time else 0
        
        print("\n" + "=" * 70)
        print("統計資訊")
        print("=" * 70)
        print(f"運行時間: {duration:.1f} 秒")
        print(f"總訊息數: {self.message_count}")
        
        if duration > 0:
            rate = self.message_count / duration
            print(f"訊息速率: {rate:.2f} 則/秒")
        
        print(f"\n各主題訊息數:")
        for topic, count in sorted(self.topic_stats.items(), key=lambda x: x[1], reverse=True):
            print(f"  {topic}: {count}")
        
        print("=" * 70)

def main():
    """主程式"""
    parser = argparse.ArgumentParser(description='MQTT 訊息監控工具')
    parser.add_argument('--broker', default='localhost', help='MQTT Broker 位址')
    parser.add_argument('--port', type=int, default=1883, help='MQTT 連接埠')
    parser.add_argument('--topics', nargs='+', default=['#'], help='要監控的主題')
    
    args = parser.parse_args()
    
    print("\n" + "=" * 70)
    print("MQTT 訊息監控工具")
    print("=" * 70)
    print(f"Broker: {args.broker}:{args.port}")
    print(f"主題: {', '.join(args.topics)}")
    print("=" * 70)
    print()
    
    monitor = MQTTMonitor(args.broker, args.port, args.topics)
    monitor.run()

if __name__ == "__main__":
    main()
