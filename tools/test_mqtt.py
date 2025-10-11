#!/usr/bin/env python3
"""
MQTT 測試工具
用於測試 MQTT Broker 連接、發布和訂閱功能
"""

import argparse
import sys
import time
import json
from datetime import datetime
import paho.mqtt.client as mqtt


class MQTTTester:
    """MQTT 測試類別"""
    
    def __init__(self, broker, port=1883, timeout=10):
        """
        初始化 MQTT 測試器
        
        Args:
            broker: MQTT Broker 位址
            port: MQTT Broker 連接埠（預設 1883）
            timeout: 連接逾時時間（秒）
        """
        self.broker = broker
        self.port = port
        self.timeout = timeout
        self.client = None
        self.connected = False
        self.messages_received = []
        
    def on_connect(self, client, userdata, flags, rc):
        """連接回調函式"""
        if rc == 0:
            self.connected = True
            print(f"✓ 成功連接到 {self.broker}:{self.port}")
        else:
            print(f"✗ 連接失敗，錯誤碼: {rc}")
            self.connected = False
    
    def on_disconnect(self, client, userdata, rc):
        """斷線回調函式"""
        self.connected = False
        if rc != 0:
            print(f"⚠️  意外斷線，錯誤碼: {rc}")
    
    def on_message(self, client, userdata, message):
        """訊息接收回調函式"""
        msg_data = {
            'topic': message.topic,
            'payload': message.payload.decode('utf-8'),
            'qos': message.qos,
            'timestamp': datetime.now().isoformat()
        }
        self.messages_received.append(msg_data)
        print(f"\n📨 收到訊息:")
        print(f"   主題: {msg_data['topic']}")
        print(f"   內容: {msg_data['payload']}")
        print(f"   QoS: {msg_data['qos']}")
    
    def on_publish(self, client, userdata, mid):
        """發布回調函式"""
        print(f"✓ 訊息已發布 (mid: {mid})")
    
    def test_connection(self):
        """測試 MQTT Broker 連接"""
        print(f"\n{'='*60}")
        print(f" 測試連接到 {self.broker}:{self.port}")
        print(f"{'='*60}")
        
        try:
            self.client = mqtt.Client()
            self.client.on_connect = self.on_connect
            self.client.on_disconnect = self.on_disconnect
            
            print(f"正在連接...")
            self.client.connect(self.broker, self.port, self.timeout)
            self.client.loop_start()
            
            # 等待連接
            wait_time = 0
            while not self.connected and wait_time < self.timeout:
                time.sleep(0.5)
                wait_time += 0.5
            
            if self.connected:
                print(f"✓ 連接測試通過")
                self.client.loop_stop()
                self.client.disconnect()
                return True
            else:
                print(f"✗ 連接逾時")
                return False
                
        except Exception as e:
            print(f"✗ 連接失敗: {e}")
            return False
    
    def test_publish(self, topic, message, qos=0):
        """
        測試發布訊息
        
        Args:
            topic: 主題
            message: 訊息內容
            qos: QoS 等級（0, 1, 2）
        """
        print(f"\n{'='*60}")
        print(f" 測試發布訊息")
        print(f"{'='*60}")
        
        try:
            self.client = mqtt.Client()
            self.client.on_connect = self.on_connect
            self.client.on_publish = self.on_publish
            
            print(f"正在連接...")
            self.client.connect(self.broker, self.port, self.timeout)
            self.client.loop_start()
            
            # 等待連接
            wait_time = 0
            while not self.connected and wait_time < self.timeout:
                time.sleep(0.5)
                wait_time += 0.5
            
            if not self.connected:
                print(f"✗ 無法連接到 Broker")
                return False
            
            print(f"\n發布訊息:")
            print(f"   主題: {topic}")
            print(f"   內容: {message}")
            print(f"   QoS: {qos}")
            
            result = self.client.publish(topic, message, qos=qos)
            
            # 等待發布完成
            result.wait_for_publish()
            
            time.sleep(1)
            self.client.loop_stop()
            self.client.disconnect()
            
            print(f"✓ 發布測試通過")
            return True
            
        except Exception as e:
            print(f"✗ 發布失敗: {e}")
            return False
    
    def test_subscribe(self, topic, duration=10):
        """
        測試訂閱訊息
        
        Args:
            topic: 訂閱主題（支援萬用字元 # 和 +）
            duration: 監聽時間（秒）
        """
        print(f"\n{'='*60}")
        print(f" 測試訂閱訊息")
        print(f"{'='*60}")
        
        try:
            self.client = mqtt.Client()
            self.client.on_connect = self.on_connect
            self.client.on_message = self.on_message
            self.messages_received = []
            
            print(f"正在連接...")
            self.client.connect(self.broker, self.port, self.timeout)
            self.client.loop_start()
            
            # 等待連接
            wait_time = 0
            while not self.connected and wait_time < self.timeout:
                time.sleep(0.5)
                wait_time += 0.5
            
            if not self.connected:
                print(f"✗ 無法連接到 Broker")
                return False
            
            print(f"\n訂閱主題: {topic}")
            self.client.subscribe(topic)
            print(f"✓ 訂閱成功")
            
            print(f"\n監聽 {duration} 秒...")
            print(f"（按 Ctrl+C 可提前結束）")
            
            try:
                time.sleep(duration)
            except KeyboardInterrupt:
                print(f"\n\n⚠️  使用者中斷")
            
            self.client.loop_stop()
            self.client.disconnect()
            
            print(f"\n{'='*60}")
            print(f" 訂閱測試結果")
            print(f"{'='*60}")
            print(f"收到 {len(self.messages_received)} 則訊息")
            
            if self.messages_received:
                print(f"\n訊息列表:")
                for i, msg in enumerate(self.messages_received, 1):
                    print(f"\n{i}. 主題: {msg['topic']}")
                    print(f"   內容: {msg['payload']}")
                    print(f"   時間: {msg['timestamp']}")
            
            return True
            
        except Exception as e:
            print(f"✗ 訂閱失敗: {e}")
            return False
    
    def test_pubsub(self, topic, message="test", duration=5):
        """
        測試發布和訂閱（完整流程）
        
        Args:
            topic: 主題
            message: 訊息內容
            duration: 等待時間（秒）
        """
        print(f"\n{'='*60}")
        print(f" 測試發布訂閱流程")
        print(f"{'='*60}")
        
        # 先啟動訂閱者
        subscriber = mqtt.Client("test_subscriber")
        subscriber.on_message = self.on_message
        self.messages_received = []
        
        try:
            print(f"1. 啟動訂閱者...")
            subscriber.connect(self.broker, self.port, self.timeout)
            subscriber.subscribe(topic)
            subscriber.loop_start()
            time.sleep(1)
            print(f"✓ 訂閱者已就緒")
            
            # 發布訊息
            print(f"\n2. 發布測試訊息...")
            publisher = mqtt.Client("test_publisher")
            publisher.connect(self.broker, self.port, self.timeout)
            publisher.loop_start()
            time.sleep(1)
            
            test_payload = {
                "message": message,
                "timestamp": datetime.now().isoformat(),
                "test": True
            }
            
            publisher.publish(topic, json.dumps(test_payload))
            print(f"✓ 訊息已發布")
            
            # 等待接收
            print(f"\n3. 等待接收訊息...")
            time.sleep(duration)
            
            # 清理
            publisher.loop_stop()
            publisher.disconnect()
            subscriber.loop_stop()
            subscriber.disconnect()
            
            # 檢查結果
            print(f"\n{'='*60}")
            print(f" 測試結果")
            print(f"{'='*60}")
            
            if self.messages_received:
                print(f"✓ 成功接收 {len(self.messages_received)} 則訊息")
                print(f"✓ 發布訂閱流程正常")
                return True
            else:
                print(f"✗ 未接收到訊息")
                print(f"⚠️  可能的原因:")
                print(f"   - Broker 未正確運行")
                print(f"   - 網路連接問題")
                print(f"   - 主題不匹配")
                return False
                
        except Exception as e:
            print(f"✗ 測試失敗: {e}")
            return False


def main():
    """主程式"""
    parser = argparse.ArgumentParser(
        description='MQTT 測試工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
範例:
  # 測試連接
  python test_mqtt.py --broker localhost connection
  
  # 測試發布
  python test_mqtt.py --broker localhost publish --topic test/topic --message "Hello"
  
  # 測試訂閱
  python test_mqtt.py --broker localhost subscribe --topic test/#
  
  # 完整測試
  python test_mqtt.py --broker localhost pubsub --topic test/demo
        """
    )
    
    parser.add_argument('--broker', default='localhost',
                        help='MQTT Broker 位址（預設: localhost）')
    parser.add_argument('--port', type=int, default=1883,
                        help='MQTT Broker 連接埠（預設: 1883）')
    parser.add_argument('--timeout', type=int, default=10,
                        help='連接逾時時間（秒，預設: 10）')
    
    subparsers = parser.add_subparsers(dest='command', help='測試命令')
    
    # 連接測試
    subparsers.add_parser('connection', help='測試 Broker 連接')
    
    # 發布測試
    pub_parser = subparsers.add_parser('publish', help='測試發布訊息')
    pub_parser.add_argument('--topic', required=True, help='發布主題')
    pub_parser.add_argument('--message', required=True, help='訊息內容')
    pub_parser.add_argument('--qos', type=int, default=0, choices=[0, 1, 2],
                           help='QoS 等級（預設: 0）')
    
    # 訂閱測試
    sub_parser = subparsers.add_parser('subscribe', help='測試訂閱訊息')
    sub_parser.add_argument('--topic', required=True, help='訂閱主題')
    sub_parser.add_argument('--duration', type=int, default=10,
                           help='監聽時間（秒，預設: 10）')
    
    # 發布訂閱測試
    pubsub_parser = subparsers.add_parser('pubsub', help='測試發布訂閱流程')
    pubsub_parser.add_argument('--topic', required=True, help='測試主題')
    pubsub_parser.add_argument('--message', default='test', help='測試訊息')
    pubsub_parser.add_argument('--duration', type=int, default=5,
                              help='等待時間（秒，預設: 5）')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    # 建立測試器
    tester = MQTTTester(args.broker, args.port, args.timeout)
    
    # 執行測試
    success = False
    
    if args.command == 'connection':
        success = tester.test_connection()
    
    elif args.command == 'publish':
        success = tester.test_publish(args.topic, args.message, args.qos)
    
    elif args.command == 'subscribe':
        success = tester.test_subscribe(args.topic, args.duration)
    
    elif args.command == 'pubsub':
        success = tester.test_pubsub(args.topic, args.message, args.duration)
    
    # 返回結果
    print(f"\n{'='*60}")
    if success:
        print(f"✓ 測試完成")
        return 0
    else:
        print(f"✗ 測試失敗")
        print(f"\n請參考 resources/troubleshooting.md 排除問題")
        return 1


if __name__ == "__main__":
    sys.exit(main())
