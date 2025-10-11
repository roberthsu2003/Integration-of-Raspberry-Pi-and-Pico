"""
MQTT 測試發布工具
用於測試 MQTT 訊息發布

功能：
- 發布測試訊息
- 批次發布
- 模擬感測器資料
- 壓力測試
"""

import paho.mqtt.client as mqtt
import json
import time
import random
import argparse
from datetime import datetime

class MQTTPublisher:
    """
    MQTT 發布器類別
    """
    
    def __init__(self, broker: str, port: int = 1883):
        """
        初始化發布器
        
        參數:
            broker: MQTT Broker 位址
            port: MQTT 連接埠
        """
        self.broker = broker
        self.port = port
        
        # 建立客戶端
        self.client = mqtt.Client(client_id="mqtt_publisher")
        
        # 統計資訊
        self.publish_count = 0
        self.error_count = 0
    
    def connect(self) -> bool:
        """
        連接到 MQTT Broker
        
        返回:
            bool: 連接是否成功
        """
        try:
            self.client.connect(self.broker, self.port, 60)
            print(f"✓ 已連接到 {self.broker}:{self.port}")
            return True
        except Exception as e:
            print(f"✗ 連接失敗: {e}")
            return False
    
    def disconnect(self):
        """中斷連接"""
        self.client.disconnect()
        print("已中斷連接")
    
    def publish(self, topic: str, message, qos: int = 0) -> bool:
        """
        發布訊息
        
        參數:
            topic: 主題
            message: 訊息（字串或字典）
            qos: 服務品質等級
        
        返回:
            bool: 發布是否成功
        """
        try:
            # 如果是字典，轉換為 JSON
            if isinstance(message, dict):
                message = json.dumps(message)
            
            result = self.client.publish(topic, message, qos)
            
            if result.rc == mqtt.MQTT_ERR_SUCCESS:
                self.publish_count += 1
                return True
            else:
                self.error_count += 1
                return False
        
        except Exception as e:
            print(f"✗ 發布失敗: {e}")
            self.error_count += 1
            return False
    
    def publish_sensor_data(
        self,
        device_id: str,
        sensor_type: str,
        value: float,
        unit: str,
        location: str = None
    ) -> bool:
        """
        發布感測器資料
        
        參數:
            device_id: 裝置 ID
            sensor_type: 感測器類型
            value: 數值
            unit: 單位
            location: 位置
        
        返回:
            bool: 發布是否成功
        """
        data = {
            "device_id": device_id,
            "device_type": "test",
            "sensor_type": sensor_type,
            "value": round(value, 2),
            "unit": unit,
            "timestamp": time.time()
        }
        
        if location:
            data["location"] = location
        
        topic = f"sensors/{device_id}/{sensor_type}"
        return self.publish(topic, data)
    
    def simulate_temperature(
        self,
        device_id: str,
        count: int = 10,
        interval: float = 1.0,
        base_temp: float = 25.0,
        variation: float = 5.0
    ):
        """
        模擬溫度感測器資料
        
        參數:
            device_id: 裝置 ID
            count: 發布次數
            interval: 發布間隔（秒）
            base_temp: 基礎溫度
            variation: 溫度變化範圍
        """
        print(f"\n模擬溫度感測器: {device_id}")
        print(f"發布 {count} 次，間隔 {interval} 秒")
        print("-" * 50)
        
        for i in range(count):
            # 生成隨機溫度
            temp = base_temp + random.uniform(-variation, variation)
            
            # 發布資料
            success = self.publish_sensor_data(
                device_id=device_id,
                sensor_type="temperature",
                value=temp,
                unit="celsius"
            )
            
            status = "✓" if success else "✗"
            print(f"{status} [{i+1}/{count}] 溫度: {temp:.2f}°C")
            
            if i < count - 1:
                time.sleep(interval)
        
        print("-" * 50)
        print(f"完成！成功: {self.publish_count}, 失敗: {self.error_count}")
    
    def stress_test(
        self,
        topic: str,
        count: int = 100,
        delay: float = 0.01
    ):
        """
        壓力測試
        
        參數:
            topic: 主題
            count: 發布次數
            delay: 發布間隔（秒）
        """
        print(f"\n壓力測試")
        print(f"主題: {topic}")
        print(f"訊息數: {count}")
        print(f"間隔: {delay} 秒")
        print("-" * 50)
        
        start_time = time.time()
        
        for i in range(count):
            message = {
                "index": i,
                "timestamp": time.time(),
                "data": f"test_message_{i}"
            }
            
            self.publish(topic, message)
            
            if (i + 1) % 10 == 0:
                print(f"已發布 {i + 1}/{count} 則訊息")
            
            time.sleep(delay)
        
        duration = time.time() - start_time
        rate = count / duration
        
        print("-" * 50)
        print(f"完成！")
        print(f"總時間: {duration:.2f} 秒")
        print(f"速率: {rate:.2f} 則/秒")
        print(f"成功: {self.publish_count}, 失敗: {self.error_count}")

def main():
    """主程式"""
    parser = argparse.ArgumentParser(description='MQTT 測試發布工具')
    parser.add_argument('--broker', default='localhost', help='MQTT Broker 位址')
    parser.add_argument('--port', type=int, default=1883, help='MQTT 連接埠')
    
    subparsers = parser.add_subparsers(dest='command', help='命令')
    
    # 單次發布
    publish_parser = subparsers.add_parser('publish', help='發布單則訊息')
    publish_parser.add_argument('topic', help='主題')
    publish_parser.add_argument('message', help='訊息內容')
    
    # 模擬感測器
    simulate_parser = subparsers.add_parser('simulate', help='模擬感測器資料')
    simulate_parser.add_argument('--device-id', default='test_device', help='裝置 ID')
    simulate_parser.add_argument('--count', type=int, default=10, help='發布次數')
    simulate_parser.add_argument('--interval', type=float, default=1.0, help='發布間隔（秒）')
    
    # 壓力測試
    stress_parser = subparsers.add_parser('stress', help='壓力測試')
    stress_parser.add_argument('--topic', default='test/stress', help='主題')
    stress_parser.add_argument('--count', type=int, default=100, help='訊息數量')
    stress_parser.add_argument('--delay', type=float, default=0.01, help='發布間隔（秒）')
    
    args = parser.parse_args()
    
    # 建立發布器
    publisher = MQTTPublisher(args.broker, args.port)
    
    if not publisher.connect():
        return
    
    try:
        if args.command == 'publish':
            # 單次發布
            success = publisher.publish(args.topic, args.message)
            if success:
                print(f"✓ 已發布訊息到 {args.topic}")
            else:
                print(f"✗ 發布失敗")
        
        elif args.command == 'simulate':
            # 模擬感測器
            publisher.simulate_temperature(
                device_id=args.device_id,
                count=args.count,
                interval=args.interval
            )
        
        elif args.command == 'stress':
            # 壓力測試
            publisher.stress_test(
                topic=args.topic,
                count=args.count,
                delay=args.delay
            )
        
        else:
            parser.print_help()
    
    finally:
        publisher.disconnect()

if __name__ == "__main__":
    main()
